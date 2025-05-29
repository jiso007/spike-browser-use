from __future__ import annotations

import asyncio
import logging
import time
import json
from typing import Any, List, Optional, Dict, TYPE_CHECKING

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from pydantic import ValidationError

if TYPE_CHECKING:
    from browser_use_ext.extension_interface.service import ExtensionInterface

from browser_use_ext.exceptions import LLMException, InvalidActionError, ActionFailedException
from browser_use_ext.browser.views import BrowserState
from browser_use_ext.agent.prompts import SystemPrompt, DEFAULT_SYSTEM_PROMPT
from browser_use_ext.agent.views import (
    AgentSettings,
    AgentState,
    AgentHistory,
    AgentHistoryList,
    AgentLLMOutput,
    ActionCommand,
    ActionResult,
    StepMetadata,
    AgentError,
    AgentBrain
)
from browser_use_ext.agent.message_manager.service import MessageManager, MessageManagerSettings
from browser_use_ext.agent.message_manager.utils import save_conversation

logger = logging.getLogger(__name__)

DEFAULT_MAX_STEPS = 10
DEFAULT_MAX_FAILURES = 3

class Agent:
    def __init__(
        self,
        task: str,
        llm: BaseChatModel,
        extension_interface: ExtensionInterface,
        settings: Optional[AgentSettings] = None,
        initial_state: Optional[AgentState] = None,
    ):
        self.task = task
        self.llm = llm
        self.extension_interface = extension_interface
        self.settings = settings if settings is not None else AgentSettings()
        
        self.state = initial_state if initial_state is not None else AgentState()
        # self.state.agent_id is generated if not provided in initial_state

        self.message_manager = MessageManager(
            initial_task=self.task,
            agent_id=self.state.agent_id, # Pass agent_id
            settings=MessageManagerSettings(
                max_total_tokens=self.settings.max_input_tokens,
                additional_task_context=self.settings.message_context,
                include_json_output_example=True,
                max_actions_per_step=self.settings.max_actions_per_step,
            ),
            initial_state=None, 
        )
        
        self.state.message_manager_state = self.message_manager.get_current_state()
        
        logger.info(f"Agent initialized for task: '{self.task}'. Agent ID: {self.state.agent_id}")
        logger.info(f"Using LLM: {self.llm.__class__.__name__}")
        if hasattr(self.llm, 'model_name'):
            logger.info(f"LLM Model Name: {getattr(self.llm, 'model_name', 'N/A')}")

    async def _call_llm(self, messages: List[BaseMessage]) -> str:
        """Directly calls the LLM with the provided messages."""
        logger.debug(f"Calling LLM with {len(messages)} messages.")
        # Ensure messages are in the correct format if necessary (e.g. some models expect dicts)
        # For now, assuming the self.llm (MockLLM or other) handles BaseMessage objects directly.

        # Example check (adapt if your LLM needs a different format):
        # if not messages or not isinstance(messages[0], SystemMessage):
        #     logger.warning("LLM call missing or malformed system message. This might lead to unexpected behavior.")
        
        # Correct way to check message type from Langchain BaseMessage objects
        if messages and messages[0].type == "system": # Check .type attribute
            logger.debug(f"First message is System: {messages[0].content[:100]}...")
        elif messages:
            logger.warning(f"First message is not System, it is {messages[0].type}. This might be unexpected.")

        try:
            # self.llm.agenerate is expected to return an LLMResult (ChatResult is a subclass)
            # LLMResult.generations is List[List[Generation]].
            # Since we send one list of messages, we expect one list of generations back.
            # Each inner list can have multiple generations if n > 1 for the LLM call (e.g. multiple choices).
            # We typically care about the first generation of the first (and only) prompt.
            response = await self.llm.agenerate(messages)
            
            # Correctly extract content from LLMResult/ChatResult
            if (
                response.generations and 
                response.generations[0] and 
                isinstance(response.generations[0], list) and # Ensure it's a list of generations
                response.generations[0][0] and 
                hasattr(response.generations[0][0], 'message') and # For ChatGeneration
                response.generations[0][0].message
            ):
                response_content = str(response.generations[0][0].message.content)
            elif (
                response.generations and 
                response.generations[0] and 
                isinstance(response.generations[0], list) and # Ensure it's a list of generations
                response.generations[0][0] and 
                hasattr(response.generations[0][0], 'text') # For base Generation
            ):
                response_content = str(response.generations[0][0].text) # Fallback for base Generation if message isn't there
            else:
                logger.error("LLM response did not contain expected generation structure (generations[0][0].message.content or generations[0][0].text).")
                response_content = "" # Or raise an error

            logger.debug(f"LLM raw response content: {response_content}")
            if not response_content:
                logger.warning("LLM returned empty content.")
            return response_content
        except Exception as e:
            logger.error(f"LLM API call failed: {e}", exc_info=True)
            status_code = getattr(e, 'status_code', 500)
            raise LLMException(status_code=status_code, message=f"LLM call failed: {str(e)}") from e

    def _parse_llm_response(self, response_str: str) -> AgentLLMOutput | None:
        """
        Parses the LLM's JSON string response into an AgentLLMOutput.
        """
        logger.debug(f"Attempting to parse LLM response string (first 300 chars): {response_str[:300]}")
        try:
            output = AgentLLMOutput.model_validate_json(response_str)
            logger.info("Successfully parsed and validated LLM response into AgentLLMOutput.")
            if len(output.action) > self.settings.max_actions_per_step:
                logger.warning(f"LLM proposed {len(output.action)} actions, but max_actions_per_step is {self.settings.max_actions_per_step}. Truncating actions.")
                output.action = output.action[:self.settings.max_actions_per_step]
            elif not output.action:
                logger.warning("LLM did not propose any actions.")
            return output
        except InvalidActionError as e:
            # InvalidActionError from the validator should be treated as a validation error
            logger.error(f"LLM response validation failed for AgentLLMOutput: {e}")
            raise InvalidActionError(f"Malformed LLM response or failed validation for AgentLLMOutput: {e}") from e
        except ValidationError as e:
            logger.error(f"LLM response validation failed for AgentLLMOutput: {e.errors(include_url=False)}")
            raise InvalidActionError(f"Malformed LLM response or failed validation for AgentLLMOutput: {e}") from e
        except Exception as e:
            logger.error(f"Failed to parse LLM response string. Error: {e}", exc_info=True)
            raise InvalidActionError(f"Could not parse LLM response: {e}") from e

    async def _get_next_llm_output(self, task: str, history: AgentHistoryList, current_browser_state: BrowserState, last_action_results: Optional[List[ActionResult]], settings: AgentSettings) -> AgentLLMOutput | None:
        """
        Formats the prompt using MessageManager, calls the LLM, and parses the response.
        """
        logger.info(f"Agent ({self.state.agent_id}): Entering _get_next_llm_output for step {self.state.n_steps}.")
        logger.debug(f"Agent: Browser state for LLM input - URL: {current_browser_state.url if current_browser_state else 'N/A'}")
        # Potentially log more details from current_browser_state if needed, e.g., number of actionable elements
        if current_browser_state and hasattr(current_browser_state, 'actionable_elements'):
             logger.debug(f"Agent: Browser state actionable elements count: {len(current_browser_state.actionable_elements)}")
        
        if last_action_results:
            self.message_manager.add_action_results_to_context(last_action_results)
            logger.debug(f"Agent: Added {len(last_action_results)} last action results to message manager.")

        # Convert BrowserState to a string (e.g., JSON) and add as a user message
        browser_state_content = current_browser_state.model_dump_json(indent=2) if current_browser_state else "No browser state available."
        self.message_manager.add_user_message(browser_state_content, message_type="browser_state")
        logger.debug(f"Agent: Added browser state to message manager (length: {len(browser_state_content)} chars).")

        messages_for_llm = self.message_manager.get_messages_for_llm()
        logger.info(f"Agent: Prepared {len(messages_for_llm)} messages for LLM. About to call LLM.")
        # For verbose debugging, you could log the full messages_for_llm if needed, but be mindful of large outputs
        # for msg_idx, msg in enumerate(messages_for_llm):
        #    logger.debug(f"  LLM Message {msg_idx} Type: {msg.type}, Content (first 100 chars): {str(msg.content)[:100]}")
        
        llm_response_str = ""
        try:
            llm_response_str = await self._call_llm(messages_for_llm)
            logger.info(f"Agent: LLM call successful. Raw response string (first 300 chars): {llm_response_str[:300]}")
        except LLMException as e:
            logger.error(f"Agent: LLMException in _get_next_llm_output: {e}")
            raise # Re-raise to be handled by the main run loop
        if not llm_response_str:
            logger.warning("Agent: LLM returned an empty string. Cannot parse.")
            return None
            
        try:
            parsed_output = self._parse_llm_response(llm_response_str)
            if parsed_output:
                logger.info(f"Agent: Successfully parsed LLM response. Actions proposed: {len(parsed_output.action)}")
            else:
                logger.warning("Agent: Parsing LLM response resulted in None.")
            return parsed_output
        except InvalidActionError as e:
            logger.error(f"Agent: InvalidActionError parsing LLM response in _get_next_llm_output: {e}")
            raise
        except Exception as e:
            logger.error(f"Error parsing LLM response in _get_next_llm_output: {e}", exc_info=True)
            raise InvalidActionError(f"Unexpected error parsing LLM response: {e}") from e

    async def _execute_actions(self, actions: List[ActionCommand]) -> List[ActionResult]:
        """
        Executes a list of actions using the ExtensionInterface.
        """
        results: List[ActionResult] = []
        if not actions:
            logger.warning("No actions to execute.")
            results.append(ActionResult(
                action_name="internal_decision",
                params={},
                success=False, 
                error="No actions provided by LLM.",
                include_in_memory=True
            ))
            return results

        for i, command in enumerate(actions):
            logger.info(f"Executing action {i+1}/{len(actions)}: {command.action} with params: {command.params}")
            action_start_time = time.time()
            action_result_data = {}
            error_message = None
            success = False

            try:
                api_response = await self.extension_interface.execute_action(
                    action_name=command.action,
                    params=command.params,
                )
                
                if isinstance(api_response, dict):
                    success = api_response.get("success", False)
                    if success:
                        action_result_data = api_response.get("data", {})
                        logger.info(f"Action '{command.action}' executed successfully. Data: {action_result_data}")
                    else:
                        error_message = api_response.get("error", "Unknown error from extension action execution.")
                        logger.error(f"Action '{command.action}' failed. Error: {error_message}")
                else:
                    success = False
                    error_message = f"Unexpected response type from extension: {type(api_response)}. Expected dict."
                    logger.error(f"Action '{command.action}' failed due to unexpected response: {api_response}")

            except Exception as e:
                logger.error(f"Exception during execution of action '{command.action}': {e}", exc_info=True)
                error_message = f"Python-side error executing action '{command.action}': {str(e)}"
                success = False
            
            action_duration = time.time() - action_start_time
            
            is_done_action_flag = command.action.lower() == "done"
            
            extracted_content_from_action = None # This variable is not used further, consider removing if not needed for ActionResult
            if is_done_action_flag:
                # For 'done' action, 'text' or 'reason' in params can be the final message.
                # 'success' in params indicates overall task success from LLM's perspective.
                final_message_from_params = command.params.get("text", command.params.get("reason"))
                if final_message_from_params:
                     action_result_data = {"message": final_message_from_params} # Store as part of returned_data
                if "success" in command.params and isinstance(command.params["success"], bool):
                    success = command.params["success"]
                # If not specified by LLM, a 'done' action implies the action itself was successful if no exception occurred.
                # The task success is separate.

            result = ActionResult(
                action_name=command.action,
                params=command.params,
                success=success,
                error=error_message,
                returned_data=action_result_data, 
                include_in_memory=command.action.lower() != "done"
            )
            results.append(result)

            if not result.success or result.is_done_action: # Correctly use result.is_done_action
                if not result.success:
                    logger.warning(f"Stopping further actions in this step due to failure of action: {command.action}")
                break 
        
        return results

    async def _handle_step_error(self, error: Exception, current_step: int) -> List[ActionResult]:
        """Handles errors occurring during a step's execution."""
        logger.error(f"Error during step {current_step}: {error}", exc_info=True)
        self.state.consecutive_failures += 1
        
        error_message = AgentError.format_error(error, include_trace=logger.isEnabledFor(logging.DEBUG))
        
        if isinstance(error, LLMException):
            error_message = f"LLM Error (Code {error.status_code}): {error.message}"
        elif isinstance(error, InvalidActionError):
            error_message = f"Invalid Action Error: {str(error)}"
        
        # Provide default values for required fields in ActionResult
        return [ActionResult(
            action_name="error_handler", 
            params={"error_details": str(error)}, 
            success=False, 
            error=error_message, 
            include_in_memory=True
        )]

    def _make_history_item(self, llm_output: Optional[AgentLLMOutput], executed_results: List[ActionResult], browser_url: Optional[str], metadata: StepMetadata) -> None:
        """Creates and appends an item to the agent's history."""
        if llm_output is None:
            try:
                placeholder_brain = AgentBrain(
                    page_summary="LLM output was not generated or parsed.",
                    evaluation_previous_goal="N/A",
                    memory="N/A",
                    next_goal="Attempt to recover or retry."
                )
                llm_output = AgentLLMOutput(current_state=placeholder_brain, action=[])
            except Exception as e:
                logger.error(f"Could not create placeholder AgentLLMOutput: {e}")
                llm_output = AgentLLMOutput(current_state=None, action=[])

        history_item = AgentHistory(
            step_metadata=metadata,
            llm_output=llm_output,
            action_results=executed_results,
            browser_url=browser_url,
        )
        self.state.history.history.append(history_item)
        logger.info(f"Step {metadata.step_number} history recorded. URL: {browser_url}. Actions: {len(executed_results)}")

    async def run(self, max_steps: int = DEFAULT_MAX_STEPS) -> AgentHistoryList:
        """
        Runs the agent for a maximum number of steps or until a 'done' action is received.
        """
        logger.info(f"Agent ({self.state.agent_id}): Starting run for task: '{self.task}'. Max steps: {max_steps}, Max failures: {self.settings.max_failures}")
        self._log_agent_run_start(max_steps) # Log start of run

        self.state.history = AgentHistoryList(history=[]) # Reset history for this run
        self.state.consecutive_failures = 0 # Reset failure count
        self.state.n_steps = 0 # Reset step count
        self.state.last_action_result = [] # Reset last action results
        # Note: self.state.browser_state is NOT reset here, it reflects the browser state at the start of the run

        # Main agent loop
        # The loop condition checks max steps at the BEGINNING of each iteration
        while self.state.n_steps < max_steps:
            current_step_num = self.state.n_steps + 1 # 1-based step number
            step_start_time = time.time() # Timer for the entire step
            logger.info(f"\nAgent ({self.state.agent_id}): --- Starting Step {current_step_num} ---")

            # Check for max consecutive failures before attempting the step
            if self.state.consecutive_failures >= self.settings.max_failures:
                logger.warning(f"Agent: Step {current_step_num}: Reached max consecutive failures ({self.state.consecutive_failures}/{self.settings.max_failures}). Terminating run.")
                break # Exit loop due to max failures

            # --- Step Execution Flow ---
            # This flag tracks if the core logic for the step (state fetch, LLM call, action execution) completed successfully
            step_core_logic_successful = False
            step_failure_reason = None

            # 1. Fetch the current browser state for THIS step's LLM call
            logger.info(f"Agent: Step {current_step_num}: Getting current browser state...")
            step_state_fetch_start_time = time.time() # Timer for state fetch within the loop
            current_browser_state = None # Initialize state for this step

            try:
                active_tab_id = await self.extension_interface.get_active_tab_id()
                if active_tab_id is None:
                    step_failure_reason = f"Step {current_step_num}: No active tab ID found. Cannot fetch state."
                    logger.warning(step_failure_reason)
                    # Error handled below after the try/except blocks

                else:
                    current_browser_state = await self.extension_interface.get_state(
                        for_vision=self.settings.use_vision,
                        tab_id=active_tab_id
                    )

                if not current_browser_state:
                    step_failure_reason = f"Agent: Step {current_step_num}: Failed to get browser state from extension."
                    logger.error(step_failure_reason)
                    # Error handled below after the try/except blocks
                else:
                    logger.info(f"Agent: Step {current_step_num}: Successfully retrieved browser state. URL: {current_browser_state.url}")
                    # 2. Update the agent's internal state with the newly fetched browser state
                    self.state.update_browser_state(current_browser_state) # Update self.state.browser_state
                    # State fetch was successful, can proceed to LLM

            except Exception as e: # Catch any exception during state fetch within the loop
                step_failure_reason = f"Agent: Step {current_step_num}: Critical error during state fetch: {e}"
                logger.error(step_failure_reason, exc_info=True)
                # Error handled below after the try/except blocks

            # Check if state fetch failed before proceeding to LLM
            if step_failure_reason is not None:
                # Log the state fetch failure and continue to next step (failure count incremented below)
                error_action_result = ActionResult(action_name="state_fetch_failure", params={}, success=False, error_message=step_failure_reason, include_in_memory=True)
                self._make_history_item(None, [error_action_result], self.state.browser_state.url if self.state.browser_state else None, StepMetadata(step_number=current_step_num, step_start_time=step_state_fetch_start_time, step_end_time=time.time(), input_tokens=0)) # Log against state fetch duration
                self.state.consecutive_failures += 1 # Count state fetch failure as a step failure
                logger.warning(f"Agent: Step {current_step_num}: Consecutive failures count: {self.state.consecutive_failures}/{self.settings.max_failures}.")
                self.state.n_steps += 1 # Increment step count even on failure to prevent infinite loops if state fetch always fails
                continue # Continue loop to check max failures or terminate the run

            # --- State fetch successful, proceed to LLM Call ---
            llm_output_obj = None

            # 3. Get next LLM output based on FRESH state and history
            logger.info(f"Agent: Step {current_step_num}: Calling LLM with fresh browser state.")
            llm_call_start_time = time.time() # Timer for LLM call
            input_tokens_for_step = 0 # Initialize token count for this step

            try:
                llm_output_obj = await self._get_next_llm_output(
                    task=self.task,
                    history=self.state.history, # MessageManager uses history
                    current_browser_state=self.state.browser_state, # Uses the state updated moments ago
                    last_action_results=self.state.last_action_result, # Use last action results from previous step
                    settings=self.settings,
                )
                logger.info(f"Agent: Step {current_step_num}: LLM call completed in {time.time() - llm_call_start_time:.2f}s.")
                # Get token count after LLM call
                input_tokens_for_step = self.message_manager.get_last_prompt_token_count() if self.message_manager else 0

                if not llm_output_obj or not llm_output_obj.action:
                    step_failure_reason = f"Agent: Step {current_step_num}: LLM provided no valid output or actions after parsing."
                    logger.warning(step_failure_reason)
                    # Error handled below after the try/except blocks
                # else: LLM call successful and provided actions, can proceed to action execution

            except Exception as e: # Catch any exception during LLM call or parsing
                step_failure_reason = f"Agent: Step {current_step_num}: Error during LLM call or parsing: {e}"
                logger.error(step_failure_reason, exc_info=True)
                # Error handled below after the try/except blocks

            # Check if LLM call failed before proceeding to action execution
            if step_failure_reason is not None:
                # Log the LLM failure and continue to next step (failure count incremented below)
                error_action_results_list = await self._handle_step_error(Exception(step_failure_reason), current_step_num) # Use _handle_step_error for formatting
                self._make_history_item(llm_output_obj, error_action_results_list, self.state.browser_state.url if self.state.browser_state else None, StepMetadata(step_number=current_step_num, step_start_time=llm_call_start_time, step_end_time=time.time(), input_tokens=input_tokens_for_step)) # Log against LLM call duration
                self.state.consecutive_failures +=1 # Count LLM/parsing failure as a step failure
                logger.warning(f"Agent: Step {current_step_num}: Consecutive failures count: {self.state.consecutive_failures}/{self.settings.max_failures}.")
                self.state.n_steps += 1 # Increment step count even on failure
                continue # Continue loop to check max failures or terminate the run

            # --- LLM Call Successful and provided actions, proceed to Action Execution ---

            # 4. Execute actions
            logger.info(f"Agent: Step {current_step_num}: Executing {len(llm_output_obj.action)} actions...")
            action_execution_start_time = time.time() # Timer for action execution
            executed_action_results: List[ActionResult] = [] # Initialize results for this step's actions

            try:
                executed_action_results = await self._execute_actions(llm_output_obj.action)
                logger.info(f"Agent: Step {current_step_num}: Action execution completed in {time.time() - action_execution_start_time:.2f}s. Results count: {len(executed_action_results)}")
                # Log detailed results
                for i, res in enumerate(executed_action_results):
                    logger.debug(f"  Action Result {i+1}: Name={res.action_name}, Success={res.success}, Error={res.error_message}, Returned Data={res.returned_data}")

                # After action execution, check if any action failed
                if any(not ar.success for ar in executed_action_results):
                    step_failure_reason = f"Agent: Step {current_step_num}: One or more actions failed during execution."
                    logger.warning(step_failure_reason)
                    # Error handled below after the try/except blocks
            except Exception as e: # Catch unexpected errors during _execute_actions
                step_failure_reason = f"Agent: Step {current_step_num}: Critical error during action execution: {e}"
                logger.error(step_failure_reason, exc_info=True)
                # Error handled below after the try/except blocks
            else:
                step_core_logic_successful = True # All core steps (state, LLM, Actions) were successful

            # 5. Process action results and check for task completion/failures AFTER execution
            step_end_time = time.time()
            # Use the input_tokens calculated after the LLM call

            step_metadata = StepMetadata(
                step_number=current_step_num,
                step_start_time=step_start_time,
                step_end_time=step_end_time,
                input_tokens=input_tokens_for_step,
            )
            logger.debug(f"Step {current_step_num} metadata: {step_metadata}")
            # Use the input_tokens calculated after the LLM call

            self._make_history_item(llm_output_obj, executed_action_results, self.state.browser_state.url if self.state.browser_state else None, step_metadata) # Pass current_browser_state url

            # Update agent state based on action results
            self.state.last_action_result = executed_action_results # Store results for next LLM call's context
            logger.debug(f"Agent: Step {current_step_num}: self.state.last_action_result updated for next step: {self.state.last_action_result}")

            # Check for task completion (done action) - use the results from THIS step
            is_task_done = any(ar.is_done_action and ar.success for ar in executed_action_results)
            if is_task_done:
                logger.info(f"Agent: Step {current_step_num}: Task reported as done by action result.")
                # Task is complete, log final status and break
                self._log_agent_run_end()
                logger.info("Agent run finished due to successful 'done' action.")
                return self.state.history # Exit on successful completion

            # Handle step failure after actions are processed if it occurred
            if step_failure_reason is not None:
                # Log the action execution failure and continue to next step (failure count incremented below)
                # The error is already added to history by _make_history_item if it was a critical exception in action execution
                # If it was a non-critical action failure (success=False), it's logged in _execute_actions.
                # We just need to increment failure count if any part of the core step logic failed and wasn't a task completion.
                pass # Failure count handled below


            # --- Manage consecutive failures based on step outcome ---
            # Check if the step failed but wasn't a task completion (which resets failures)
            if not step_core_logic_successful and not is_task_done:
                logger.warning(f"Agent: Step {current_step_num} not fully successful and not task done. Incrementing consecutive failures.")
                self.state.consecutive_failures += 1
            elif is_task_done:
                 # Task is done, reset failures even if some previous action failed in this step
                 logger.info(f"Agent: Step {current_step_num} task done. Resetting consecutive failures.")
                 self.state.consecutive_failures = 0
            else:
                 # Step was fully successful and not a done step
                 logger.info(f"Agent: Step {current_step_num} fully successful and not task done. Resetting consecutive failures.")
                 self.state.consecutive_failures = 0

            logger.warning(f"Agent: Step {current_step_num}: Final Consecutive failures count: {self.state.consecutive_failures}/{self.settings.max_failures}.")

            # Increment step count at the end of a completed step
            self.state.n_steps += 1

            # Add a delay between steps if configured, UNLESS task is done or max failures reached (which break the loop at the START of the next iteration)
            # Check conditions again BEFORE delaying
            if not is_task_done and self.state.consecutive_failures < self.settings.max_failures and self.state.n_steps < max_steps:
                 if self.settings.delay_between_steps_ms > 0:
                    logger.info(f"Agent: Delaying for {self.settings.delay_between_steps_ms}ms before next step.")
                    await asyncio.sleep(self.settings.delay_between_steps_ms / 1000.0)


        # After loop: Determine why the loop terminated and log/handle final status
        logger.info("Agent run loop terminated.")
        self._log_agent_run_end() # Log end of run

        final_step_count = self.state.n_steps
        terminated_due_to_max_steps = final_step_count >= max_steps
        terminated_due_to_max_failures = self.state.consecutive_failures >= self.settings.max_failures
        # Check for done action by reviewing the complete history after the loop
        terminated_due_to_done_action = any(ar.is_done_action and ar.success for step in self.state.history.history for ar in step.action_results)

        logger.info(f"Agent run termination analysis: Max Steps Reached={terminated_due_to_max_steps}, Max Failures Reached={terminated_due_to_max_failures}, Successful Done Action={terminated_due_to_done_action}")

        if terminated_due_to_done_action:
             logger.info("Agent run finished successfully because a successful 'done' action was recorded in history.")
             # Return history on successful completion (already done inside the loop break, but ensuring here too)
             pass # The return self.state.history happens inside the loop for done action

        elif terminated_due_to_max_failures:
             logger.warning(f"Agent run terminated after {final_step_count} steps due to reaching max consecutive failures ({self.state.consecutive_failures}).")
             # Add final error to history if not already added by break block
             # Check if the last history item's actions include a termination error to avoid duplicates
             last_history_actions = self.state.history.history[-1].action_results if self.state.history.history else []
             if not any(ar.action_name in ["run_termination_error", "run_termination_unexpected", "state_fetch_failure", "no_action_from_llm"] for ar in last_history_actions): 
                  final_error_message = f"Agent run terminated after {final_step_count} steps due to reaching max consecutive failures ({self.state.consecutive_failures})."
                  error_result = ActionResult(action_name="run_termination_error", params={}, success=False, error_message=final_error_message, include_in_memory=False)
                  # Use the end time of the last step recorded if history exists, otherwise current time
                  # The step number for this final event should be the total steps taken + 1
                  step_num_for_final_event = final_step_count + 1
                  last_step_end_time_for_meta = self.state.history.history[-1].step_metadata.step_end_time if self.state.history.history else time.time()
                  self._make_history_item(None, [error_result], self.state.browser_state.url if self.state.browser_state else None, StepMetadata(step_number=step_num_for_final_event, step_start_time=last_step_end_time_for_meta, step_end_time=time.time(), input_tokens=0)) # Log against step number AFTER final step

        elif terminated_due_to_max_steps:
             logger.warning(f"Agent run terminated after reaching max steps ({max_steps}) without successful completion.")
             # Add final info/warning to history unless the last step already added a meaningful error
             last_history_actions = self.state.history.history[-1].action_results if self.state.history.history else []
             if not any(ar.action_name in ["run_termination_error", "run_termination_unexpected", "state_fetch_failure", "no_action_from_llm"] for ar in last_history_actions): 
                  final_message = f"Agent run terminated after reaching max steps ({max_steps}) without task completion."
                  info_result = ActionResult(action_name="run_terminated_max_steps", params={}, success=True, error_message=final_message, include_in_memory=False) # Use success=True for informational message, not a failure
                  step_num_for_final_event = final_step_count + 1
                  last_step_end_time_for_meta = self.state.history.history[-1].step_metadata.step_end_time if self.state.history.history else time.time()
                  self._make_history_item(None, [info_result], self.state.browser_state.url if self.state.browser_state else None, StepMetadata(step_number=step_num_for_final_event, step_start_time=last_step_end_time_for_meta, step_end_time=time.time(), input_tokens=0)) # Log against step number AFTER final step

        else:
             logger.warning("Agent run terminated unexpectedly without a clear reason (not done, max steps, or max failures).")
             final_message = "Agent run terminated unexpectedly."
             error_result = ActionResult(action_name="run_termination_unexpected", params={}, success=False, error_message=final_message, include_in_memory=False)
             step_num_for_final_event = final_step_count + 1
             last_step_end_time_for_meta = self.state.history.history[-1].step_metadata.step_end_time if self.state.history.history else time.time()
             self._make_history_item(None, [error_result], self.state.browser_state.url if self.state.browser_state else None, StepMetadata(step_number=step_num_for_final_event, step_start_time=last_step_end_time_for_meta, step_end_time=time.time(), input_tokens=0)) # Log against step number AFTER final step

        # Return the complete history regardless of termination reason
        return self.state.history

    def _log_agent_run_start(self, max_steps_for_run: int):
        logger.info(f"\n{'='*50}\nAgent Run Started\nTask: {self.task}\nMax Steps: {max_steps_for_run}\n{'='*50}")

    def _log_agent_run_end(self):
        logger.info(f"\n{'='*50}\nAgent Run Finished\nTotal Steps: {len(self.state.history.history)}\nTotal Failures: {self.state.consecutive_failures}\n{'='*50}")

    async def close(self):
        """Cleans up resources, like stopping the interface server."""
        logger.info("Agent: Closing resources...")
        if self.extension_interface:
            await self.extension_interface.close()
            logger.info("Agent: ExtensionInterface closed.")

        # Example: if self.extension_interface needs explicit closing:
        # if hasattr(self.extension_interface, 'close') and asyncio.iscoroutinefunction(self.extension_interface.close):
        #     await self.extension_interface.close()
        pass 