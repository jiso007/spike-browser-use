# Standard library imports
import logging
from typing import List, Optional, Dict, Any, Type, Union, Callable, get_type_hints, Literal
from typing import List, Optional, Dict, Any, Type, Union
import json

# Third-party imports
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

# Local application/library specific imports
from .actions import (
    ClickParams,
    InputTextParams,
    ScrollParams,
    NavigateParams,
    GetStateParams,
    DoneParams,
    ExtractContentParams
)
from .views import ActionCommand

# Initialize logger for this module
logger = logging.getLogger(__name__)

# --- Helper function to get type string for prompt --- 
def _get_type_str(field_info: FieldInfo) -> str:
    """Gets a string representation of a field's type for prompts."""
    # This is a simplified version. Pydantic's internal type representation can be complex.
    # For basic types, this should suffice.
    if hasattr(field_info.annotation, '__name__'):
        return field_info.annotation.__name__
    elif hasattr(field_info.annotation, '__origin__'): # For Optional, List, Literal etc.
        origin = field_info.annotation.__origin__.__name__
        args = getattr(field_info.annotation, '__args__', [])
        # Filter out NoneType for Optionals to show the actual type
        type_args_str = ", ".join([arg.__name__ for arg in args if arg is not type(None)])
        if origin == 'Union': # Typically for Optional[X]
             return f"Optional[{type_args_str}]"
        if origin == 'Literal':
            literal_values = [repr(val) for val in args]
            return f"Literal[{', '.join(literal_values)}]"
        return f"{origin}[{type_args_str}]"
    return str(field_info.annotation)

# --- Action Schema/Description Generation Utilities ---

# Dictionary mapping action names (as used in ActionCommand.action Literal)
# to their corresponding Pydantic parameter models.
ACTION_PARAM_MODELS: Dict[str, Type[BaseModel]] = {
    "click": ClickParams,
    "input_text": InputTextParams,
    "scroll": ScrollParams,
    "navigate": NavigateParams,
    "get_state": GetStateParams,
    "done": DoneParams,
    "extract_content": ExtractContentParams,
}

def get_action_model_map() -> Dict[str, Type[BaseModel]]:
    """Helper to get a map of action names to their Pydantic parameter models."""
    # This relies on ActionCommand literals and the imported action parameter models
    # Ensure ActionCommand.action literals match keys and models are imported.
    return {
        "click": ClickParams,
        "input_text": InputTextParams,
        "scroll": ScrollParams,
        "navigate": NavigateParams,
        "get_state": GetStateParams,
        "done": DoneParams,
        "extract_content": ExtractContentParams,
    }

def generate_actions_text_description(**kwargs: Any) -> str:
    """Generates a textual description of available actions and their parameters."""
    descriptions = []
    model_map = get_action_model_map()

    for action_name, action_model in model_map.items():
        action_desc = f"- {action_name}:\n"
        param_descs = []
        if action_model.model_fields:
            for name, field_info in action_model.model_fields.items():
                param_info = f"    - {name} (type: {get_type_hints(action_model).get(name, Any).__name__}): {field_info.description or 'No description'}"
                required = field_info.is_required()
                
                # Corrected check for default value in Pydantic V2
                has_default_value = field_info.default is not PydanticUndefined
                default_val = None
                if has_default_value:
                    default_val = field_info.default
                elif field_info.default_factory is not None:
                    try:
                        default_val = field_info.default_factory()
                    except TypeError:
                        default_val = "(computed)"

                if not required:
                    param_info += f" (optional, default: {default_val if default_val is not None else 'Not specified'})"
                else:
                    param_info += " (required)"
                param_descs.append(param_info)
        else:
            param_descs.append("    (No parameters)")
        
        descriptions.append(action_desc + "\n".join(param_descs))
    
    return "\n".join(descriptions)

def get_agent_llm_output_json_schema(indent: Optional[int] = 2) -> str:
    """
    Generates the JSON schema for the AgentLLMOutput model.
    This schema defines the expected structure of the LLM's JSON response.
    """
    from .views import AgentLLMOutput
    schema = AgentLLMOutput.model_json_schema(by_alias=True) # by_alias=True if using Field(alias=...)
    return json.dumps(schema, indent=indent)


# --- PromptVariable and SystemPrompt Classes (largely unchanged but might use new utils) ---

class PromptVariable(BaseModel):
    """Describes a variable that can be injected into a prompt template."""
    name: str = Field(description="Name of the variable (e.g., 'user_query') - DO NOT include {{}} here.")
    description: str = Field(description="Description of what the variable represents")
    example_value: Optional[Any] = Field(default=None, description="An example value for the variable")

class SystemPrompt:
    """Manages the system prompt for the agent, with dynamic action descriptions."""
    def __init__(self, template: str):
        self.template = template

    def format_prompt(self, task: str, agent_id: str, **kwargs: Any) -> str:
        action_descriptions = generate_actions_text_description(**kwargs)
        # logger.debug(f"Generated action descriptions for prompt: {action_descriptions}")
        try:
            return self.template.format(
                task=task,
                agent_id=agent_id,
                action_descriptions=action_descriptions,
                **kwargs
            )
        except KeyError as e:
            logger.error(f"KeyError formatting system prompt: {e}. Available kwargs: {kwargs.keys()}")
            logger.error(f"Template: {self.template}")
            # Fallback if a specific key in kwargs is missing but template expects it, though action_descriptions covers the main dynamic part.
            return self.template # Or a more robust fallback


# Example of a default system prompt
# The original system_prompt.md content:
ORIGINAL_SYSTEM_PROMPT_MD_CONTENT = """
You are an AI agent designed to automate browser tasks using a provided set of tools (actions).
Your goal is to accomplish the user's ultimate task by planning and executing these actions sequentially.

# Input Format (Provided by the system at each step):
- User Task: The overall objective.
- Previous Step Summary: A brief of what happened in the last step (actions taken, outcomes).
- Current URL: The URL of the active browser tab.
- Open Tabs: A list of currently open tabs with their IDs and titles.
- Actionable Elements: A simplified list of interactive elements on the current page, each with an `id`, `type`, and `text_content`.
  Example:
  `[element_123]<button>Submit Form</button>`

# Response Rules & Format:

1.  **JSON Output**: You MUST ALWAYS respond with a valid JSON object matching this schema:
    ```json
    {{llm_output_json_schema}}
    ```
    Specifically, your JSON output must contain:
    -   `current_state`: An object with your analysis:
        -   `evaluation_previous_goal` (string): Evaluate if the previous action(s) succeeded or failed and why.
        -   `memory` (string): Summarize key learnings, progress, and what to remember for next steps. Count repetitive tasks (e.g., "2 of 5 items processed").
        -   `next_goal` (string): Clearly state the immediate sub-goal for the *next* set of actions.
    -   `action`: A list of one or more action commands to execute. Each command is an object with `action` (the action name) and `params` (action-specific parameters).

2.  **Actions Execution**:
    -   The `action` list can contain multiple commands.
    -   Actions are executed sequentially. If an action significantly changes the page state (e.g., navigation, form submission that reloads), subsequent actions in the list for *that turn* might not execute as expected. Plan accordingly.
    -   You can specify up to `{{max_actions}}` actions per turn.
    -   Only use actions listed in the "Available Actions" section below.

3.  **Available Actions**:
    {{available_actions_description}}

4.  **Interaction Strategy**:
    -   Use the `element_id` from the "Actionable Elements" list for actions that target specific elements.
    -   If needed elements aren't visible, use `scroll` action. If an element cannot be found, do not hallucinate an ID; try a different approach (e.g., navigate, search, or use `extract_content` if the goal is information gathering).
    -   Handle popups or cookie banners by trying to click accept/close buttons if they appear as actionable elements.

5.  **Task Completion**:
    -   Use the `done` action as the VERY LAST action once the user's ultimate task is fully completed. Include a summary message and set `success: true`.
    -   If you reach the maximum allowed steps and the task is not complete, use `done` with `success: false` and summarize progress.
    -   For tasks involving repetition (e.g., "for each item..."), keep track in your `memory` field and ensure all repetitions are completed before using `done`.

6.  **Error Handling & Robustness**:
    -   If an action fails, the system will inform you. Analyze the error and your `current_state.evaluation_previous_goal` to decide on a recovery strategy (e.g., retry, try a different element, navigate away).
    -   If the page content is unexpected or you're stuck, consider using `get_state` again (if you need a new screenshot/element list) or `navigate` to a known good URL or a search engine.

Focus on the user's task, be methodical, and use the provided actions and information to achieve the goal.
"""

DEFAULT_SYSTEM_PROMPT_TEMPLATE = ORIGINAL_SYSTEM_PROMPT_MD_CONTENT
DEFAULT_SYSTEM_PROMPT = SystemPrompt(template=DEFAULT_SYSTEM_PROMPT_TEMPLATE)

# Planner Prompt
# Content from browser_use/agent/prompts.py -> PlannerPrompt class
PLANNER_PROMPT_TEMPLATE = """
You are a planning agent that helps break down tasks into smaller steps and reason about the current state.
Your role is to:
1. Analyze the current state and history
2. Evaluate progress towards the ultimate goal
3. Identify potential challenges or roadblocks
4. Suggest the next high-level steps to take

Inside your messages, there will be AI messages from different agents with different formats.

Your output format should be always a JSON object with the following fields:
{{
    "state_analysis": "Brief analysis of the current state and what has been done so far",
    "progress_evaluation": "Evaluation of progress towards the ultimate goal (as percentage and description)",
    "challenges": "List any potential challenges or roadblocks",
    "next_steps": "List 2-3 concrete next steps to take",
    "reasoning": "Explain your reasoning for the suggested next steps"
}}

Ignore the other AI messages output structures.

Keep your responses concise and focused on actionable insights.
"""

DEFAULT_PLANNER_PROMPT_TEMPLATE = PLANNER_PROMPT_TEMPLATE
DEFAULT_PLANNER_PROMPT = SystemPrompt(template=DEFAULT_PLANNER_PROMPT_TEMPLATE)

# More specific prompts can be defined here, e.g., for data extraction, form filling, etc.
# class DataExtractionPrompt(SystemPrompt):
#     task_description: str = Field(description="Specific instructions for what data to extract.")
#     output_format: str = Field(default="JSON", description="Desired format for the extracted data.")

#     def get_full_content(self) -> str:
#         return f"{self.content}\n\nTask: {self.task_description}\nOutput Format: {self.output_format}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    logger.info(f"Default Prompt Name: {DEFAULT_SYSTEM_PROMPT.name}")
    logger.info(f"Default Prompt Template Variables: {[v.name for v in DEFAULT_SYSTEM_PROMPT.variables]}")
    # logger.info(f"Default Prompt Template:\n{DEFAULT_SYSTEM_PROMPT.template}") # Avoid printing very long string

    try:
        formatted = DEFAULT_SYSTEM_PROMPT.format_prompt(
            max_actions="7" # Example value for max_actions
        )
        logger.info(f"\nFormatted Main System Prompt (first 100 chars):\n{formatted[:100]}...")
    except Exception as e:
        logger.error(f"Error formatting default prompt in example: {e}")

    logger.info(f"\nPlanner Prompt Name: {DEFAULT_PLANNER_PROMPT.name}")
    # logger.info(f"Planner Prompt Template:\n{DEFAULT_PLANNER_PROMPT.template}") # Avoid printing very long string
    try:
        formatted_planner_prompt = DEFAULT_PLANNER_PROMPT.format_prompt() # No variables to pass
        logger.info(f"\nFormatted Planner Prompt (first 100 chars):\n{formatted_planner_prompt[:100]}...")
    except Exception as e:
        logger.error(f"Error formatting planner prompt: {e}")

    # Example of a prompt that might be used for a different purpose
    SUMMARIZE_PAGE_PROMPT_TEMPLATE = (
        "Please summarize the key information from the following web page content.\n\n"
        "Page Title: {{page_title}}\n"
        "Page URL: {{page_url}}\n\n"
        "Visible Text Content Snippet:\n{{visible_text_snippet}}\n\n"
        "Your Summary:"
    )
    SUMMARIZE_PAGE_PROMPT = SystemPrompt(
        name="SummarizeWebPagePrompt",
        template=SUMMARIZE_PAGE_PROMPT_TEMPLATE,
        variables=[
            PromptVariable(name="page_title", description="Title of the web page."),
            PromptVariable(name="page_url", description="URL of the web page."),
            PromptVariable(name="visible_text_snippet", description="A snippet of the visible text from the page.")
        ],
        description="A prompt to guide an LLM to summarize a web page."
    )

    try:
        formatted_summary_prompt = SUMMARIZE_PAGE_PROMPT.format_prompt(
            page_title="Awesome AI Innovations",
            page_url="https://example.com/ai-news/awesome-innovations",
            visible_text_snippet="Researchers today announced a breakthrough in AI that allows... (rest of content)"
        )
        logger.info(f"\nFormatted Summarize Prompt:\n{formatted_summary_prompt}")
    except Exception as e:
        logger.error(f"Error formatting summary prompt: {e}") 