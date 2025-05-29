from __future__ import annotations

import json
import logging
from typing import Dict, List, Optional, Union, Any, Tuple

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from pydantic import BaseModel, Field

from browser_use_ext.agent.message_manager.views import (
    MessageManagerState,
    MessageMetadata,
)
from browser_use_ext.browser.views import BrowserState
from browser_use_ext.agent.prompts import DEFAULT_SYSTEM_PROMPT 
from browser_use_ext.agent.views import AgentBrain, ActionCommand, AgentLLMOutput

from .utils import (
    _merge_successive_messages, 
    _convert_messages_for_non_function_calling_models,
    is_model_without_tool_support
)

logger = logging.getLogger(__name__)

ESTIMATED_CHARS_PER_TOKEN = 3
DEFAULT_IMAGE_TOKENS = 800

class MessageManagerSettings(BaseModel):
    max_total_tokens: int = Field(default=120000)
    min_tokens_for_model_output: int = Field(default=2000)
    additional_task_context: Optional[str] = None
    target_llm_model_name: Optional[str] = None
    include_json_output_example: bool = True
    max_actions_per_step: int = 7

class MessageManager:
    def __init__(
        self,
        initial_task: str,
        agent_id: str,
        system_prompt_content: Optional[str] = None,
        settings: Optional[MessageManagerSettings] = None,
        initial_state: Optional[MessageManagerState] = None,
    ):
        self.task = initial_task
        self.agent_id = agent_id
        self.settings = settings if settings is not None else MessageManagerSettings()
        self.state = initial_state if initial_state is not None else MessageManagerState()

        self._last_prompt_token_count: Optional[int] = None

        if not self.state.history.messages:
            self._initialize_messages(system_prompt_content)
        
        self.model_name = self.settings.target_llm_model_name
        logger.info(f"MessageManager initialized for task: '{self.task}'. Agent ID: {self.agent_id}")

    def _initialize_messages(self, system_prompt_content: Optional[str]) -> None:
        if system_prompt_content:
            formatted_sys_prompt = system_prompt_content
        else:
            try:
                formatted_sys_prompt = DEFAULT_SYSTEM_PROMPT.format_prompt(
                    task=self.task, 
                    agent_id=self.agent_id, 
                    max_actions=self.settings.max_actions_per_step if hasattr(self.settings, 'max_actions_per_step') else 7
                )
            except Exception as e:
                logger.error(f"Unexpected error formatting system prompt: {e}. Using template directly as fallback.", exc_info=True)
                formatted_sys_prompt = DEFAULT_SYSTEM_PROMPT.template
        
        self._add_message_to_history(SystemMessage(content=formatted_sys_prompt), message_type='init_system')

        task_message_content = (
            f"Your primary goal is to accomplish the following task: '''{self.task}'''. "
            f"Review the browser content and decide on the best next action(s). "
            f"If you believe the task is complete, use the 'done' action."
        )
        self._add_message_to_history(HumanMessage(content=task_message_content), message_type='init_task')

        if self.settings.additional_task_context:
            context_msg = HumanMessage(content=f"Additional Context: {self.settings.additional_task_context}")
            self._add_message_to_history(context_msg, message_type='init_context')

        if self.settings.include_json_output_example:
            example_brain = AgentBrain(
                evaluation_previous_goal="Success - The previous action was successful.",
                memory="I have loaded the page and identified key elements.",
                next_goal="Click the login button to proceed."
            )
            example_action = ActionCommand(action="click", params={"element_id": "login_button_id"}, thought="The login button is clearly visible and is the next logical step.")
            example_llm_output = AgentLLMOutput(current_state=example_brain, action=[example_action])
            
            example_message_content = (
                "IMPORTANT: You MUST respond in the following JSON format. Ensure your response is a single, valid JSON object.\n"
                f"Example JSON Output:\n```json\n{example_llm_output.model_dump_json(indent=2)}\n```"
            )
            # Changed flow: Human confirms understanding, AI provides the example output directly.
            self._add_message_to_history(HumanMessage(content="Understood. I will respond in the specified JSON format."), message_type='init_confirmation')
            self._add_message_to_history(AIMessage(content=example_llm_output.model_dump_json(indent=2)), message_type='init_example_output')

        logger.info(f"MessageManager initialized with {len(self.state.history.messages)} messages. Total tokens: {self.state.history.current_tokens}")

    def _add_message_to_history(self, message: BaseMessage, message_type: Optional[str] = None, position: Optional[int] = None) -> None:
        tokens = self._count_tokens(message)
        metadata = MessageMetadata(tokens=tokens, message_type=message_type)
        self.state.history.add_message(message, metadata, position=position)
        logger.debug(f"Added {type(message).__name__} (type: {message_type}, tokens: {tokens}). History now {len(self.state.history.messages)} msgs, ~{self.state.history.current_tokens} tokens.")
        # self._ensure_token_limits() # Call this after major additions, or selectively

    def _count_tokens(self, message: BaseMessage) -> int:
        count = 0
        if isinstance(message.content, str):
            count = len(message.content) // ESTIMATED_CHARS_PER_TOKEN
        elif isinstance(message.content, list):
            for item in message.content:
                if isinstance(item, dict):
                    if item.get('type') == 'text':
                        count += len(item.get('text', '')) // ESTIMATED_CHARS_PER_TOKEN
                    elif item.get('type') == 'image_url':
                        count += DEFAULT_IMAGE_TOKENS
        count += 5 
        return count

    def add_user_message(self, content: Union[str, List[Dict[str, Any]]], message_type: str = "user_turn") -> None:
        """Adds a standard user message (browser state, task follow-up, etc.) to history."""
        # content can be a string or a list for multimodal messages (text + image_url)
        if isinstance(content, str) and not content:
            logger.warning("Attempted to add message with empty content")
        self._add_message_to_history(HumanMessage(content=content), message_type=message_type)

    def add_ai_response(self, agent_llm_output: AgentLLMOutput, message_type: str = "ai_response") -> None:
        """Adds the AI's structured response (AgentLLMOutput) to history as an AIMessage."""
        # The content of the AIMessage will be the JSON string of AgentLLMOutput
        json_content = agent_llm_output.model_dump_json()
        self._add_message_to_history(AIMessage(content=json_content), message_type=message_type)

    def add_action_results_to_context(self, results: List[ActionResult], message_type: str = "action_results") -> None:
        """Adds results from executed actions to the message history as HumanMessages, if they should be in memory."""
        for result in results:
            if result.include_in_memory:
                if result.success and result.returned_data:
                    # Simplified representation of returned_data for now
                    data_str = str(result.returned_data)
                    if len(data_str) > 300: # Truncate very long results
                        data_str = data_str[:300] + "... (truncated)"
                    content = f"Action '{result.action_name}' was successful. Returned data: {data_str}"
                    self._add_message_to_history(HumanMessage(content=content), message_type=message_type)
                elif not result.success and result.error_message:
                    content = f"Action '{result.action_name}' failed. Error: {result.error_message}"
                    self._add_message_to_history(HumanMessage(content=content), message_type=message_type)
                elif result.is_done_action:
                     self._add_message_to_history(HumanMessage(content="Action 'done' was executed."), message_type=message_type)


    def get_messages_for_llm(self) -> List[BaseMessage]:
        """Prepares and returns the list of messages for the LLM, ensuring token limits and applying model-specific conversions."""
        self._ensure_token_limits()
        
        raw_messages = self.state.history.get_messages()
        
        # Apply conversions if a specific LLM model name is set in settings
        if self.settings.target_llm_model_name:
            logger.debug(f"Converting messages for model: {self.settings.target_llm_model_name}")
            # converted_messages = convert_input_messages(raw_messages, self.settings.target_llm_model_name)
            # The convert_input_messages from utils.py might need to be used carefully,
            # as it might flatten tool calls that are not used in our current main flow.
            # For now, let's assume the primary LLM supports the direct JSON in AIMessage content.
            # If specific models need flattening, that logic would be invoked here.
            # For example, if a model cannot take AIMessage(content=JSON_STRING) and needs it as a tool_call.
            # For now, we pass raw_messages, assuming the target LLM handles the sequence correctly.
            processed_messages = raw_messages 
            
            # Example of using _merge_successive_messages if needed for a model:
            # processed_messages = _merge_successive_messages(processed_messages, HumanMessage)
            # processed_messages = _merge_successive_messages(processed_messages, AIMessage)
        else:
            processed_messages = raw_messages

        # Log token counts before returning
        final_tokens = sum(self._count_tokens(m) for m in processed_messages)
        logger.info(f"Returning {len(processed_messages)} messages for LLM. Estimated total tokens: {final_tokens}")
        self._last_prompt_token_count = final_tokens
        return processed_messages

    def get_last_prompt_token_count(self) -> int:
        """Returns the token count of the last set of messages prepared for the LLM."""
        return self._last_prompt_token_count if self._last_prompt_token_count is not None else 0

    def _ensure_token_limits(self) -> None:
        """Ensures the message history does not exceed max_total_tokens, removing old messages if necessary."""
        # Calculate available tokens for model output
        target_max_history_tokens = self.settings.max_total_tokens - self.settings.min_tokens_for_model_output
        
        while self.state.history.current_tokens > target_max_history_tokens:
            removed_message = self.state.history.remove_oldest_message_if_needed()
            if removed_message:
                logger.warning(
                    f"Token limit exceeded. Removed oldest message (type: {removed_message.metadata.message_type}, tokens: {removed_message.metadata.tokens}) "
                    f"to free up space. Current tokens: {self.state.history.current_tokens}"
                )
            else:
                # This case should ideally not be reached if there are non-system messages
                logger.error("Token limit exceeded, but no non-system messages to remove. History might be too long with only system messages.")
                break 
        # After pruning, log final state
        # logger.debug(f"Token limit check done. Current history tokens: {self.state.history.current_tokens} (Target max for history: {target_max_history_tokens})")

    def get_current_state(self) -> MessageManagerState:
        """Returns the current internal state of the MessageManager for persistence."""
        return self.state

    def load_state(self, state: MessageManagerState) -> None:
        """Loads a previously saved state into the MessageManager."""
        self.state = state
        logger.info(f"MessageManager state loaded. History has {len(self.state.history.messages)} messages, ~{self.state.history.current_tokens} tokens.")

# Example Usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # Initialize with a system prompt
    manager = MessageManager(system_prompt_content="You are a helpful AI assistant.")
    manager.add_user_message("Hello, assistant!")
    manager.add_ai_response(AgentLLMOutput(current_state=AgentBrain(evaluation_previous_goal="Success - The previous action was successful.", memory="I have loaded the page and identified key elements.", next_goal="Click the login button to proceed."), action=[ActionCommand(action="click", params={"element_id": "login_button_id"}, thought="The login button is clearly visible and is the next logical step.")]))

    history = manager.get_messages_for_llm()
    for msg in history:
        logger.info(f"[{msg.timestamp.isoformat()}] {msg.role.upper()}: {msg.content}")

    manager.clear_history()
    logger.info(f"History count after clear: {len(manager.get_messages_for_llm())}") 