import logging
from pydantic import BaseModel, Field, ValidationError

# Attempt to import BrowserState, if not found, it implies a structural issue or that
# the model is defined elsewhere or needs to be created based on project docs.
# For now, we'll assume it's available as per Perplexity's plan.
# from browser_use_ext.extension_interface.models import BrowserState
from browser_use_ext.browser.views import BrowserState
from browser_use_ext.agent.prompts import SystemPrompt

class InvalidActionError(Exception):
    """Custom exception for invalid actions parsed from LLM response."""
    pass

class ActionCommand(BaseModel):
    """Validated action structure for browser operations"""
    action: str = Field(..., pattern="^(click|type|input_text|scroll|navigate|get_state|done)$") # Expanded pattern based on common needs
    params: dict = Field(
        default_factory=dict,
        examples=[
            {"element_id": "menu-123"}, 
            {"text": "Hello World", "element_id": "input-field-456"},
            {"direction": "down"},
            {"url": "https://example.com"}
        ]
    )
    # Added thought field based on common agent designs, can be adjusted.
    thought: str | None = Field(default=None, description="The thought process behind selecting this action.")


class Agent:
    def __init__(self, extension_interface):
        """
        Initializes the Agent.

        Args:
            extension_interface: An instance of ExtensionInterface for interacting with the browser.
        """
        self.extension_interface = extension_interface
        self.logger = logging.getLogger(__name__)
        # Ensure basic logging is configured if not done globally
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(level=logging.INFO)

    async def process_task(self, user_task: str, task_context: dict | None = None) -> ActionCommand | None:
        """
        Main workflow to process a user task.
        Fetches browser state, formats a prompt, calls an LLM (mocked initially),
        and parses the response into an action command.

        Args:
            user_task: The task string provided by the user.
            task_context: Optional dictionary containing context like active_tab_id.

        Returns:
            An ActionCommand if successful, None otherwise.
        """
        self.logger.info(f"Processing task: '{user_task}' with context: {task_context}")
        if task_context is None:
            task_context = {}
        
        active_tab_id = task_context.get("active_tab_id")
        
        try:
            self.logger.debug(f"Fetching browser state for tab_id: {active_tab_id}...")
            # Call to ExtensionInterface to get the current browser state.
            # The BrowserState object is expected to be Pydantic model defined in extension_interface.models
            state: BrowserState | None = await self.extension_interface.get_state(tab_id=active_tab_id)
            if not state:
                self.logger.error("Failed to fetch browser state. Aborting task processing.")
                return None
            self.logger.info(f"Successfully fetched browser state. URL: {state.url}")
            self.logger.debug(f"State details: {state.model_dump_json(indent=2, exclude_none=True)[:500]}...") # Log snippet of state

        except Exception as e:
            self.logger.error(f"Error fetching browser state: {e}", exc_info=True)
            return None
        
        # Format the prompt for the LLM
        try:
            self.logger.debug("Formatting prompt for LLM...")
            prompt = self._format_prompt(user_task, state)
            self.logger.info("Successfully formatted prompt for LLM.")
            self.logger.debug(f"Formatted prompt (first 200 chars): {prompt[:200]}...")
        except Exception as e:
            self.logger.error(f"Error formatting prompt: {e}", exc_info=True)
            return None

        # Call the LLM (mocked for now)
        try:
            self.logger.debug("Calling LLM...")
            llm_response_str = await self._call_llm(prompt)
            self.logger.info("Successfully received response from LLM.")
            self.logger.debug(f"LLM raw response: {llm_response_str}")
        except Exception as e:
            self.logger.error(f"Error calling LLM: {e}", exc_info=True)
            return None

        # Parse the LLM response into an ActionCommand
        try:
            self.logger.debug("Parsing LLM response...")
            action_command = self._parse_response(llm_response_str)
            if not action_command:
                # _parse_response already logs specific parsing/validation errors
                self.logger.error("Failed to parse LLM response into a valid ActionCommand.")
                return None
            self.logger.info(f"Successfully parsed LLM response into ActionCommand: {action_command.action}")
            return action_command
        except InvalidActionError:
            # Error already logged by _parse_response, just return None
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error parsing LLM response: {e}", exc_info=True)
            return None

    def _format_prompt(self, task: str, state: BrowserState) -> str:
        """
        Formats the prompt for the LLM using the user task and browser state.

        Args:
            task: The user's task.
            state: The current browser state, expected to have an `actionable_elements` attribute.

        Returns:
            A formatted prompt string.
        """
        self.logger.debug(f"Formatting prompt with task: '{task}' and state from URL: {state.url}")
        
        # Extract actionable elements for the prompt. 
        # Ensure actionable_elements exists and is a list.
        # Perplexity's example uses state.actionable_elements directly.
        # We should ensure this attribute exists on the BrowserState model.
        actionable_elements_summary = []
        if hasattr(state, 'actionable_elements') and isinstance(state.actionable_elements, list):
            for element in state.actionable_elements:
                # Assuming element is a Pydantic model or dict with 'id', 'type', and 'text_content'
                if isinstance(element, dict):
                    element_id = element.get('id', 'unknown_id')
                    element_type = element.get('type', 'UNKNOWN_TYPE')
                    text_content = element.get('text_content', '')[:100] # Limit text length
                    actionable_elements_summary.append(
                        f"ID: {element_id}, Type: {element_type}, Text: '{text_content}'"
                    )
                elif hasattr(element, 'id') and hasattr(element, 'type'): # Pydantic model check
                    text_content = getattr(element, 'text_content', '')[:100]
                    actionable_elements_summary.append(
                        f"ID: {element.id}, Type: {element.type}, Text: '{text_content}'"
                    )
        else:
            self.logger.warning("'actionable_elements' not found or not a list in BrowserState. Sending empty list to prompt.")

        # Prepare a simplified list of strings for the prompt context for elements
        # This is a simplified representation for the prompt to keep it concise.
        elements_context_for_prompt = "\n".join(actionable_elements_summary) if actionable_elements_summary else "No actionable elements detected."

        # Load the default system prompt. Ensure 'default_system_prompt.txt' or equivalent is available.
        # Perplexity used SystemPrompt.load("default").format(...)
        # Assuming SystemPrompt can take these named arguments.
        # The actual available variables in SystemPrompt.format() depend on its template string.
        # We will construct a dictionary of variables to pass.
        prompt_variables = {
            "user_query": task,
            "current_url": state.url,
            "page_title": state.title,
            "actionable_elements_list_str": elements_context_for_prompt,
            # Add other state variables as needed by the prompt template
        }
        
        # This assumes SystemPrompt.format() can handle these variables.
        # The Perplexity example showed `elements=state.actionable_elements`.
        # Let's stick to the SystemPrompt.load("default").format(**vars) pattern
        # for flexibility if the prompt template changes.
        try:
            # TODO: Confirm actual variables available in SystemPrompt template
            # For now, using a simplified set of variables based on common needs.
            # The example showed `elements=state.actionable_elements`
            # which implies the prompt template string might iterate over a complex list.
            # For now, providing `actionable_elements_list_str` as a string.
            # If `SystemPrompt.template_string` uses `{{ elements }}`, it expects `elements` keyword.
            formatted_prompt = SystemPrompt.load("default").format(
                user_query=task, 
                elements=state.actionable_elements # Pass the raw list as per Perplexity example
            )
            # formatted_prompt = SystemPrompt.load("default").format(**prompt_variables) 
        except KeyError as e:
            self.logger.error(f"Missing variable in prompt template: {e}. Using basic format.")
            # Fallback to a simpler format if specific keys are missing
            formatted_prompt = f"User Query: {task}\nURL: {state.url}\nTitle: {state.title}\nActionable Elements:\n{elements_context_for_prompt}"
        except Exception as e:
            self.logger.error(f"Error loading or formatting system prompt: {e}", exc_info=True)
            # Fallback to a simpler format on any other error
            formatted_prompt = f"User Query: {task}\nURL: {state.url}\nTitle: {state.title}\nActionable Elements:\n{elements_context_for_prompt}"

        self.logger.debug(f"Formatted prompt created: {formatted_prompt[:500]}...")
        return formatted_prompt

    async def _call_llm(self, prompt: str) -> str:
        """
        Calls the LLM with the given prompt. (Mocked for now)

        Args:
            prompt: The prompt string to send to the LLM.

        Returns:
            The LLM's response as a string.
        """
        # Mocked LLM call
        self.logger.info(f"Mock LLM call with prompt: {prompt[:200]}...") # Log snippet of prompt
        # Simulate an LLM response that might be parsed into an ActionCommand
        mock_response = '''
        {
            "thought": "The user wants to click a button. I should find a button and click it.",
            "action": "click",
            "params": {"element_id": "example-button-id-123"}
        }
        '''
        self.logger.debug(f"Mock LLM response: {mock_response}")
        return mock_response

    def _parse_response(self, response_str: str) -> ActionCommand | None:
        """
        Parses the LLM's JSON string response into an ActionCommand.
        Raises InvalidActionError if validation fails.

        Args:
            response_str: The JSON string response from the LLM.

        Returns:
            An ActionCommand instance if parsing is successful.
        
        Raises:
            InvalidActionError: If the response cannot be parsed or validated.
        """
        self.logger.debug(f"Attempting to parse LLM response string: {response_str}")
        try:
            # Validate and parse the JSON string into the ActionCommand Pydantic model.
            # This uses model_validate_json which is the Pydantic v2+ way.
            # If using Pydantic v1, it would be ActionCommand.parse_raw(response_str).
            action = ActionCommand.model_validate_json(response_str)
            self.logger.info(f"Successfully parsed and validated LLM response into ActionCommand: {action.action}")
            return action
        except ValidationError as e:
            # Log the detailed validation error from Pydantic.
            self.logger.error(f"LLM response validation failed: {e.errors(include_url=False)}")
            # Raise a custom error to be handled by the caller, indicating a parsing/validation problem.
            raise InvalidActionError(f"Malformed LLM response or failed validation: {e}") from e
        except Exception as e:
            # Catch any other unexpected errors during parsing (e.g., not valid JSON at all).
            self.logger.error(f"Failed to parse LLM response string. Error: {e}", exc_info=True)
            raise InvalidActionError(f"Could not parse LLM response: {e}") from e

# Example usage (for testing purposes, not part of the class)
async def example_run():
    class MockExtensionInterface:
        async def get_state(self, tab_id=None):
            print(f"MockExtensionInterface: get_state called for tab_id {tab_id}")
            # Simulate a BrowserState object based on expected structure
            # This structure needs to align with the actual BrowserState model
            # from browser_use_ext.extension_interface.models
            mock_actionable_elements = [
                {"id": "btn-login", "type": "BUTTON", "text_content": "Login"},
                {"id": "search-input", "type": "INPUT_FIELD", "current_value": ""}
            ]
            return BrowserState(
                url="https://example.com",
                title="Example Page",
                actionable_elements=mock_actionable_elements,
                # Assuming other fields for BrowserState might be optional or have defaults
                # tree={}, tabs=[], screenshot=None, dom_tree=None,
            )

    agent = Agent(extension_interface=MockExtensionInterface())
    user_task_example = "Click the login button"
    # action = await agent.process_task(user_task_example) # This will run through placeholders
    # print(f"Agent decided action: {action}")

if __name__ == "__main__":
    # To run the example:
    # import asyncio
    # asyncio.run(example_run())
    pass 