from __future__ import annotations
# Standard library imports
from typing import Optional, Dict, Any, List, Union, Literal
import logging

# Third-party imports
from pydantic import BaseModel, Field, field_validator, model_validator, RootModel, create_model, validator, ValidationError
from typing_extensions import Annotated
from langchain_core.messages import BaseMessage

# Local application/library specific imports
from browser_use_ext.browser.views import BrowserState

# Import action parameter models
from .actions import (
    ClickParams,
    InputTextParams,
    ScrollParams,
    NavigateParams,
    GetStateParams,
    DoneParams,
    ExtractContentParams,
)

logger = logging.getLogger(__name__)

import uuid
from dataclasses import dataclass
import traceback

from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel, Field

# Assuming MessageManagerState will be ported or defined elsewhere in browser_use_ext
# from browser_use_ext.agent.message_manager.views import MessageManagerState

# Forward declare for AgentState to use AgentHistoryList
class AgentHistoryList(BaseModel):
    history: List[AgentHistory] = Field(default_factory=list)

    # Methods to manage and query history (can be expanded from browser_use/agent/views.py if needed)
    def add_history_item(self, item: 'AgentHistory'):
        self.history.append(item)

    def get_last_action_results(self) -> Optional[List['ActionResult']]:
        if not self.history: return None
        last_item = self.history[-1]
        return last_item.action_results if last_item else None
    
    def add_error_to_last_step(self, error_message: str):
        if not self.history: 
            # Create a dummy step if history is empty
            dummy_metadata = StepMetadata(step_number=0, step_start_time=0, step_end_time=0)
            dummy_history = AgentHistory(step_metadata=dummy_metadata, action_results=[ActionResult(action_name="error_step", params={}, success=False, error_message=error_message)])
            self.history.append(dummy_history)
            return
        last_item = self.history[-1]
        if not last_item.action_results:
            last_item.action_results = []
        last_item.action_results.append(ActionResult(action_name="error_step", params={}, success=False, error_message=error_message))

    def is_task_marked_done(self) -> bool:
        if not self.history: return False
        last_item = self.history[-1]
        if last_item.action_results:
            for res in reversed(last_item.action_results):
                if res.is_done_action:
                    return True
        return False

    def is_task_successful(self) -> bool:
        if not self.history: return False
        last_item = self.history[-1]
        if last_item.action_results:
            for res in reversed(last_item.action_results):
                if res.is_done_action:
                    return res.success # Success of the 'done' action determines task success
        return False # Not marked done or done action was not successful

    @property
    def final_message(self) -> Optional[str]:
        if not self.history: return None
        last_item = self.history[-1]
        if last_item.action_results:
            for res in reversed(last_item.action_results):
                if res.is_done_action and isinstance(res.returned_data, str):
                    return res.returned_data
                elif res.is_done_action and res.params and isinstance(res.params.get('message'), str):
                    return res.params.get('message')
        return None

    def get_total_steps(self) -> int:
        return len(self.history)

    def total_input_tokens(self) -> int:
        return sum(item.step_metadata.input_tokens for item in self.history if item.step_metadata and item.step_metadata.input_tokens is not None)
    
    def total_duration_seconds(self) -> float:
        return sum(item.step_metadata.duration_seconds for item in self.history if item.step_metadata)


ToolCallingMethod = Literal['function_calling', 'json_mode', 'raw', 'auto']
REQUIRED_LLM_API_ENV_VARS = {
    'ChatOpenAI': ['OPENAI_API_KEY'],
    'AzureChatOpenAI': ['AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_KEY'],
    'ChatBedrockConverse': ['ANTHROPIC_API_KEY'], # Note: Often AWS credentials are used, API key is for specific Anthropic direct access
    'ChatAnthropic': ['ANTHROPIC_API_KEY'],
    'ChatGoogleGenerativeAI': ['GEMINI_API_KEY'], # Often GOOGLE_API_KEY
    'ChatDeepSeek': ['DEEPSEEK_API_KEY'],
    'ChatOllama': [],
    'ChatGrok': ['GROK_API_KEY'],
}


class AgentSettings(BaseModel):
    """Options for the agent"""

    use_vision: bool = True
    use_vision_for_planner: bool = False
    save_conversation_path: Optional[str] = None
    save_conversation_path_encoding: Optional[str] = 'utf-8'
    max_failures: int = Field(default=3, description="Maximum total consecutive failures before the agent run stops.")
    retry_delay: int = 10
    max_input_tokens: int = 128000 # Max tokens for the input to the LLM
    validate_llm_output: bool = False # Whether to validate LLM output against a schema (distinct from action validation)
    message_context: Optional[str] = None # General context to prepend to messages
    
    # GIF generation might be re-implemented if screenshots from extension are available
    # generate_gif: bool | str = False 
    
    available_file_paths: Optional[list[str]] = None # For actions that might interact with local files
    override_system_message: Optional[str] = None
    extend_system_message: Optional[str] = None
    
    # Attributes to include if we parse detailed elements from the extension
    # For now, the extension sends simplified actionable_elements
    # include_attributes: list[str] = [ 
    #     'title', 'type', 'name', 'role', 'tabindex', 
    #     'aria-label', 'placeholder', 'value', 'alt', 'aria-expanded',
    # ]
    max_actions_per_step: int = 7 # Max actions the LLM can propose in one turn

    tool_calling_method: Optional[ToolCallingMethod] = 'auto'
    # These LLMs would be used by the orchestrator/higher-level agent
    page_extraction_llm: Optional[BaseChatModel] = None 
    planner_llm: Optional[BaseChatModel] = None
    
    planner_interval: int = 1  # Run planner every N steps if planner_llm is set
    is_planner_reasoning: bool = False
    extend_planner_system_message: Optional[str] = None
    delay_between_steps_ms: int = Field(default=1000, description="Delay in milliseconds between agent steps.")
    max_steps_per_run: int = Field(default=10, description="Maximum number of steps the agent will take in a single run.")
    
    # arbitrary_types_allowed for Pydantic V2 is model_config
    model_config = {"arbitrary_types_allowed": True}


class AgentState(BaseModel):
    """Holds all state information for a multi-step Agent"""

    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    n_steps: int = 0 # Start at 0, first step becomes 1
    consecutive_failures: int = 0
    last_action_result: Optional[List['ActionResult']] = None # Result from the last executed action(s)
    
    # Placeholder for MessageManagerState if MessageManager is ported
    # message_manager_state: MessageManagerState = Field(default_factory=MessageManagerState)
    message_manager_state: Dict[str, Any] = Field(default_factory=dict) # Temp placeholder

    history: AgentHistoryList = Field(default_factory=AgentHistoryList)
    
    last_plan: Optional[str] = None # If a planner is used
    paused: bool = False
    stopped: bool = False
    
    # ADDED: Field to store the current browser state
    browser_state: Optional[BrowserState] = Field(None, description="The current state of the browser, including URL, elements, etc.")

    # arbitrary_types_allowed for Pydantic V2
    model_config = {"arbitrary_types_allowed": True}

    # ADDED: Method to update the browser state
    def update_browser_state(self, new_browser_state: BrowserState):
        """Updates the browser state within the AgentState."""
        self.browser_state = new_browser_state


@dataclass
class AgentStepInfo:
    step_number: int
    max_steps: int

    def is_last_step(self) -> bool:
        """Check if this is the last step"""
        return self.step_number >= self.max_steps # If max_steps is 10, last step is 10.


class ActionResult(BaseModel):
    """Result of executing an action by the browser extension"""

    action_name: str # Name of the action executed (e.g., "click", "type")
    params: Dict[str, Any] # Parameters used for the action
    
    is_done_action: Optional[bool] = False # Specifically if the 'done' action was called
    success: bool # True if the action execution was successful (not necessarily task completion)
    
    # Content extracted or message returned by the extension/action.
    # For 'get_state', this might be complex. For 'click', a simple confirmation.
    returned_data: Optional[Any] = None 
    
    error_message: Optional[str] = None # If the action failed to execute
    
    # Whether this action's outcome (especially returned_data or error) should be part of memory/prompt for next step
    include_in_memory: bool = True 
    duration: Optional[float] = None # Duration of the action execution in seconds


class StepMetadata(BaseModel):
    """Metadata for a single step including timing and token information"""

    step_number: int
    step_start_time: float
    step_end_time: float
    input_tokens: Optional[int] = None # Approximate tokens for LLM input this step
    output_tokens: Optional[int] = None # Approximate tokens for LLM output this step

    @property
    def duration_seconds(self) -> float:
        """Calculate step duration in seconds"""
        return self.step_end_time - self.step_start_time


class AgentBrain(BaseModel):
    """Structure for the 'current_state' field the LLM should produce, as per system prompt."""
    evaluation_previous_goal: str = Field(description="Evaluation of the previous goal: Success, Failed, or Unknown, with a short explanation.")
    memory: str = Field(description="Description of what has been done and what to remember. Be specific. Include counts for repetitive tasks.")
    next_goal: str = Field(description="What needs to be done with the next immediate action(s).")


class AgentError:
    """Container for common agent error messages and formatting"""

    VALIDATION_ERROR = 'Invalid LLM output format. Please follow the correct schema.'
    RATE_LIMIT_ERROR = 'LLM rate limit reached. Waiting before retry.'
    ACTION_EXECUTION_ERROR = 'Failed to execute action in the browser.'
    NO_VALID_ACTION_PARSED = 'LLM response did not contain a valid action to execute.'
    BROWSER_CONNECTION_ERROR = 'Could not connect to or communicate with the browser extension.'

    @staticmethod
    def format_error(error: Exception, include_trace: bool = False) -> str:
        """Formats an exception into a string for logging or LLM context."""
        error_type = type(error).__name__
        base_message = f"{error_type}: {str(error)}"
        if include_trace:
            # Limit traceback length to avoid overly long messages
            tb_lines = traceback.format_exception(type(error), error, error.__traceback__, limit=5)
            trace_info = "\nTraceback (most recent call last):\n" + "".join(tb_lines)
            return f"{base_message}{trace_info}"
        return base_message


class AgentThought(BaseModel):
    """
    Represents a single thought or reasoning step of the agent.
    Useful for logging, debugging, and understanding the agent's decision process.
    """
    thought_process: str = Field(description="Textual description of the agent's reasoning.")
    tool_to_use: Optional[str] = Field(default=None, description="The name of the tool or action the agent decided to use.")
    tool_input: Optional[Dict[str, Any]] = Field(default_factory=dict, description="The parameters for the tool/action.")
    confidence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Agent's confidence in its decision (0.0 to 1.0).")
    raw_llm_response: Optional[str] = Field(default=None, description="Raw response from the LLM if applicable.")

    class Config:
        from_attributes = True

class AgentOutput(BaseModel):
    """
    Represents the final output or result of an agent's run or a significant step.
    """
    status: Literal["success", "failure", "max_iterations_reached"] = Field(description="Final status of the agent's execution.")
    output_message: str = Field(description="A summary message describing the outcome.")
    final_answer: Optional[Any] = Field(default=None, description="The final answer or result produced by the agent, if any.")
    iterations_taken: int = Field(description="Number of iterations the agent performed.")
    full_history_json: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Full conversation history as JSON if available.")
    thoughts_history: Optional[List[AgentThought]] = Field(default_factory=list, description="History of agent's thoughts and actions.")
    final_browser_state: Optional[BrowserState] = Field(None, description="Browser state at the end of operation.")
    error: Optional[str] = Field(None, description="Error message if the agent run failed.")

    class Config:
        from_attributes = True
        json_encoders = {
            BaseMessage: lambda v: v.model_dump(exclude_none=True)
        }

# More Pydantic models can be added here as the agent's capabilities grow,
# for example, for specific task inputs, structured observations, etc. 

# Example:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    settings = AgentSettings(name="DemoAgent", max_iterations=5, verbose=True)
    logger.info(f"Agent Settings: {settings.model_dump_json(indent=2)}")

    thought = AgentThought(
        thought_process="The user wants to know the weather. I should use the get_weather tool.",
        tool_to_use="get_weather",
        tool_input={"city": "London"},
        confidence_score=0.9
    )
    logger.info(f"Agent Thought: {thought.model_dump_json(indent=2)}")

    output_success = AgentOutput(
        status="success",
        output_message="Successfully retrieved weather for London.",
        final_answer={"temperature": "15C", "condition": "Cloudy"},
        iterations_taken=3,
        thoughts_history=[thought]
    )
    logger.info(f"Agent Output (Success): {output_success.model_dump_json(indent=2)}")

    output_failure = AgentOutput(
        status="failure",
        output_message="Could not retrieve weather information after multiple attempts.",
        iterations_taken=5
    )
    logger.info(f"Agent Output (Failure): {output_failure.model_dump_json(indent=2)}")

# --- Define ActionCommand here ---

# --- Discriminated Union for Action Parameters ---
ActionParamsUnion = Annotated[
    Union[
        ClickParams,
        InputTextParams,
        ScrollParams,
        NavigateParams,
        GetStateParams,
        DoneParams,
        ExtractContentParams,
    ],
    Field(discriminator="action_type_hint") # A common field to help Pydantic, actual discrimination is by ActionCommand.action
]

class ActionCommand(BaseModel):
    """Validated action structure for browser operations."""
    action: Literal[
        "click", 
        "input_text", 
        "scroll", 
        "navigate", 
        "get_state", 
        "done", 
        "extract_content"
    ] = Field(description="The type of action to perform.")
    
    # This field will hold the specific parameters for the action_type
    # We use a discriminated union approach manually here via a validator for now
    # as Pydantic v1 support for discriminated unions on a `dict` field is tricky.
    # For Pydantic v2, `params: ActionParamsUnion` would be more direct if ActionParamsUnion is defined with proper discriminators.
    params: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters for the action. Structure depends on the 'action' type."
    )
    thought: Optional[str] = Field(default=None, description="The thought process behind selecting this action.")

    @model_validator(mode='before')
    @classmethod
    def validate_params_based_on_action(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data # Or raise error, depends on how LLM output is structured before this point
        
        action_type = data.get('action')
        params_data = data.get('params')

        if action_type is None or params_data is None:
            # Let standard validation catch missing 'action' or 'params' if they are required by schema
            return data

        model_map = {
            "click": ClickParams,
            "input_text": InputTextParams,
            "scroll": ScrollParams,
            "navigate": NavigateParams,
            "get_state": GetStateParams,
            "done": DoneParams,
            "extract_content": ExtractContentParams,
        }

        param_model = model_map.get(action_type)
        if param_model:
            try:
                # Validate and replace the generic dict with the specific model instance
                # This doesn't directly modify `data['params']` to be an instance in the output model easily with before validator
                # Pydantic v2 with Annotated unions is better for this.
                # For now, we just validate. The type of `params` remains Dict[str, Any] in ActionCommand itself.
                # The agent or interface using ActionCommand would re-parse `params` using the correct model if needed.
                param_model(**params_data)
            except ValidationError as e:
                # Raise ValueError which Pydantic will convert to ValidationError
                raise ValueError(
                    f"Invalid parameters for action '{action_type}': {e.errors()}"
                ) from e
        else:
            # This case should ideally be caught by the Literal type on `action` field itself.
            raise ValueError(f"Unknown action type: {action_type}")
        return data

# AgentLLMOutput now uses the locally defined ActionCommand
class AgentLLMOutput(BaseModel):
    """Defines the expected JSON structure from the LLM based on the system prompt."""
    current_state: AgentBrain = Field(description="The agent's analysis of the current situation and memory.")
    action: List[ActionCommand] = Field(description="List of actions the agent has decided to take.", min_length=0) # Allow empty action list
    model_config = {"arbitrary_types_allowed": True}

class AgentHistory(BaseModel):
    step_metadata: Optional[StepMetadata] = None # Made optional as it might not exist for initial state or errors before step completion
    llm_output: Optional[AgentLLMOutput] = None
    action_results: List[ActionResult] = Field(default_factory=list) # Renamed from executed_actions_results
    browser_url: Optional[str] = None # Renamed from browser_url_at_step
    # browser_state_screenshot: Optional[str] = None # Add if screenshots are part of history
    # browser_actionable_elements_summary: Optional[str] = None # Add if element summaries are stored
    model_config = {"arbitrary_types_allowed": True}

# Update AgentHistoryList to use the correctly defined AgentHistory
# This was previously a forward reference (List[Any])
# No, AgentHistoryList is defined above AgentHistory for the forward reference to work, then updated later.
# This is okay. Or define all models then update fields with `update_forward_refs()` if needed.
# AgentHistoryList.model_fields['history'].annotation = List[AgentHistory] # Pydantic v2 way
# For Pydantic V1, the forward ref should resolve if defined in same file before use.
# If AgentHistoryList is before AgentHistory, it needs `update_forward_refs` or type to be `List["AgentHistory"]` initially.
# Let's ensure AgentHistoryList is defined AFTER AgentHistory or uses string literal for forward ref.
# Corrected: AgentHistoryList is defined above, its `history` field used List[Any].
# It should ideally be List["AgentHistory"] or updated after AgentHistory is defined.
# Since it's already List[AgentHistory] now, it should be fine if defined after.
# Let's move AgentHistoryList definition after AgentHistory to be certain or use update_forward_refs.

# For simplicity if issues arise, ensure AgentHistoryList is defined after AgentHistory
# Or use: AgentHistoryList.update_forward_refs() at the end of the file. 