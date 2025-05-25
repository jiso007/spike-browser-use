# Standard library imports
import logging
from typing import Dict, Any, Optional, Callable, Awaitable, Union, List

# Third-party imports
from pydantic import BaseModel, Field # For potential future use with action definitions

# Local application/library specific imports
from ..browser.context import BrowserContext
from ..dom.views import DOMElementNode
from .registry.views import get_action_definition, list_available_actions, ActionDefinition

# Initialize logger for this module
logger = logging.getLogger(__name__)

# ActionFunctionType = Callable[[BrowserContext, Dict[str, Any]], Awaitable[Dict[str, Any]]]

class Controller:
    """
    The Controller class is responsible for executing actions within a given browser context.
    It acts as an abstraction layer over the BrowserContext's direct interaction methods,
    allowing for a more structured way to define and dispatch browser operations.
    
    In this extension-based setup, most actions are directly translated into commands
    sent to the Chrome extension via the BrowserContext and its underlying ExtensionInterface.
    """

    def __init__(self, browser_context: BrowserContext):
        """
        Initializes the Controller with a specific browser context.

        Args:
            browser_context: The BrowserContext instance through which actions will be performed.
        """
        if not isinstance(browser_context, BrowserContext):
            raise TypeError("Controller must be initialized with a valid BrowserContext instance.")
        self.browser_context = browser_context
        # self.action_registry: Dict[str, ActionFunctionType] = self._register_default_actions()
        logger.info(f"Controller initialized with BrowserContext for URL (if known): {browser_context._cached_state.url if browser_context._cached_state else 'Unknown'}")

    # def _register_default_actions(self) -> Dict[str, ActionFunctionType]:
    #     """ Placeholder for registering known actions. """
    #     # In a more complex system, actions could be dynamically registered.
    #     # For now, actions are mostly directly passed to the extension.
    #     return {
    #         "click_element_by_index": self.click_element_by_index,
    #         "input_text": self.input_text,
    #         "go_to_url": self.go_to_url,
    #         # ... other actions
    #     }

    async def execute_action(self, action_name: str, params: Optional[Dict[str, Any]] = None, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """
        Directly executes an action by name via the BrowserContext's ExtensionInterface.
        This is the primary method for sending commands to the Chrome extension.

        Args:
            action_name: The exact name of the action recognized by the Chrome extension's content script.
                         (e.g., "click_element_by_index", "input_text", "go_to_url").
            params: A dictionary of parameters specific to the action.
            timeout: Timeout in seconds for the action to complete.

        Returns:
            A dictionary containing the result from the extension, or None if an error occurs.
        """
        logger.info(f"Controller executing action: '{action_name}' with params: {params}")
        
        # Optionally, validate action_name and params against a registry
        # action_def: Optional[ActionDefinition] = get_action_definition(action_name)
        # if not action_def:
        #     logger.error(f"Action '{action_name}' is not defined in the registry.")
        #     return {"error": f"Action '{action_name}' not defined."}
        # try:
        #     # If action_def.parameters describes Pydantic models for params, validate here.
        #     # For now, assuming params are directly passed.
        #     pass 
        # except Exception as e:
        #     logger.error(f"Parameter validation failed for action '{action_name}': {e}")
        #     return {"error": f"Parameter validation failed: {e}"}

        # Delegate to the BrowserContext's underlying ExtensionInterface
        # The execute_action method in ExtensionInterface is designed to take the raw action_name and params
        # that the *extension* understands.
        try:
            # The BrowserContext itself doesn't have execute_action, it's on the ExtensionInterface
            result = await self.browser_context.extension.execute_action(
                action_name=action_name, 
                params=params or {},
                timeout=timeout
            )
            logger.info(f"Action '{action_name}' execution result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error during Controller.execute_action for '{action_name}': {e}", exc_info=True)
            return {"error": str(e)}

    # --- Wrapper methods for common actions --- 
    # These provide a more Pythonic interface and can encapsulate parameter structuring.

    async def go_to_url(self, url: str, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Navigates the active tab to the specified URL."""
        return await self.execute_action(action_name="go_to_url", params={"url": url}, timeout=timeout)

    async def click_element_by_index(self, index: int, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Clicks an element identified by its highlight_index in the active tab."""
        return await self.execute_action(action_name="click_element_by_index", params={"highlight_index": index}, timeout=timeout)

    async def input_text(self, index: int, text: str, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Inputs text into an element (identified by highlight_index) in the active tab."""
        return await self.execute_action(action_name="input_text", params={"highlight_index": index, "text": text}, timeout=timeout)

    async def scroll_page(self, direction: str, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Scrolls the page 'up' or 'down'."""
        if direction not in ["up", "down"]:
            logger.error(f"Invalid scroll direction: {direction}. Must be 'up' or 'down'.")
            return {"error": "Invalid scroll direction"}
        return await self.execute_action(action_name="scroll_page", params={"direction": direction}, timeout=timeout)

    async def go_back(self, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Navigates the active tab back in its history."""
        return await self.execute_action(action_name="go_back", params={}, timeout=timeout)

    async def extract_content(self, index: Optional[int] = None, content_type: str = "text", timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """
        Extracts content from an element (by index) or the whole page.
        Args:
            index: Highlight index of the element. If None, extracts from the whole page (extension specific).
            content_type: 'text' or 'html'.
            timeout: Timeout for the action.
        Returns:
            Dictionary with extracted content or error.
        """
        params = {"content_type": content_type}
        if index is not None:
            params["highlight_index"] = index
        # Assuming extension has an "extract_content" action that handles these params
        return await self.execute_action(action_name="extract_content", params=params, timeout=timeout)

    async def send_keys(self, keys: str, index: Optional[int] = None, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """
        Simulates sending key presses to an element (by index) or the active element on the page.
        Args:
            keys: The keys to send (e.g., "Enter", "Hello World").
            index: Highlight index of the target element. If None, keys sent to active element.
            timeout: Timeout for the action.
        """
        params = {"keys": keys}
        if index is not None:
            params["highlight_index"] = index
        return await self.execute_action(action_name="send_keys", params=params, timeout=timeout)

    # --- Tab Management Wrappers (delegating to BrowserContext which calls ExtensionInterface) ---

    async def open_tab(self, url: Optional[str] = None, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Opens a new tab, optionally navigating to a URL."""
        # This will call BrowserContext.create_new_tab(), which then calls execute_action
        # For a more direct call consistent with other controller methods:
        action_params = {"url": url if url else "about:blank"}
        response = await self.browser_context.extension.execute_action(
            action_name="open_tab", params=action_params, timeout=timeout
        )
        if response and response.get("success"):
            await self.browser_context.get_state(force_refresh=True) # Update context state
        return response

    async def switch_tab(self, tab_id: Union[int, str], timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Switches to the specified tab using its ID (Chrome tab ID or index from get_state)."""
        # This will call BrowserContext.switch_to_tab(), which then calls execute_action
        # Direct call style:
        response = await self.browser_context.extension.execute_action(
            action_name="switch_tab", params={"tab_id": tab_id}, timeout=timeout
        )
        if response and response.get("success"):
            await self.browser_context.get_state(force_refresh=True) # Update context state
        return response

    async def close_tab(self, tab_id: Optional[Union[int, str]] = None, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """
        Closes the specified tab. If tab_id is None, attempts to close the active tab.
        The tab_id should be the actual Chrome tab ID.
        """
        # This will call BrowserContext.close_tab(), which determines target and calls execute_action
        # Direct call style (if tab_id is known and is the Chrome Tab ID):
        if tab_id is None:
            # Determine active tab from context to close it
            active_pg = await self.browser_context.active_page()
            if active_pg and active_pg.page_id is not None:
                target_tab_id = active_pg.page_id
            else:
                logger.error("Close tab: No specific tab_id provided and no active page found.")
                return {"error": "No active tab to close and no tab_id specified."}
        else:
            target_tab_id = tab_id
            
        response = await self.browser_context.extension.execute_action(
            action_name="close_tab", params={"tab_id": target_tab_id}, timeout=timeout
        )
        if response and response.get("success"):
            await self.browser_context.get_state(force_refresh=True) # Update context state
        return response

    # --- Utility --- 
    async def list_actions(self) -> List[ActionDefinition]:
        """Returns a list of known action definitions from the local registry."""
        return list_available_actions()

    async def get_current_browser_state(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Retrieves and returns the full browser state as a dictionary."""
        state_obj = await self.browser_context.get_state(force_refresh=force_refresh)
        if state_obj:
            return state_obj.model_dump() # Convert Pydantic model to dict
        return None

# Example Usage (requires a running BrowserContext setup):
async def example_controller_usage():
    from browser.browser import Browser, BrowserConfig # For setup
    
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting controller example...")

    browser_config = BrowserConfig()
    browser = Browser(config=browser_config)

    async with browser: # Manages launch and close of browser (ExtensionInterface server)
        if not browser.is_connected:
            logger.warning("Extension not connected after browser launch. Waiting a bit...")
            await asyncio.sleep(5) # Wait for potential connection
            if not browser.is_connected:
                logger.error("Extension still not connected. Aborting controller example.")
            return
        
        logger.info("Browser launched and extension connected.")
        b_context = await browser.new_context()
        controller = Controller(browser_context=b_context)

        try:
            # List available actions (from local registry)
            actions = await controller.list_actions()
            logger.info(f"Available actions: {[action.name for action in actions]}")

            # Get current state
            # current_state = await controller.get_current_browser_state()
            # if current_state:
            #     logger.info(f"Current URL: {current_state.get('tabs',[{}])[0].get('url', 'N/A')}")

            # Navigate
            nav_result = await controller.go_to_url("https://www.example.com")
            logger.info(f"Navigation to example.com result: {nav_result}")
            await asyncio.sleep(2) # Allow page to load

            # Refresh state and log new URL
            # refreshed_state_data = await controller.get_current_browser_state(force_refresh=True)
            # if refreshed_state_data and refreshed_state_data.get('tabs'):
            #     active_tab_url = next((tab.get('url') for tab in refreshed_state_data['tabs'] if tab.get('active')), "N/A")
            #     logger.info(f"After navigation, active tab URL: {active_tab_url}")

            # Example: Click (assuming a clickable element with index 0 exists after nav)
            # This requires knowing a valid highlight_index from the current page state.
            # For a robust test, one would first get_state, identify an index, then click.
            # click_result = await controller.click_element_by_index(index=0) # This is a guess for index 0
            # logger.info(f"Click element 0 result: {click_result}")

            # Example: Input text (similarly, requires a valid index for an input field)
            # input_result = await controller.input_text(index=1, text="Hello from controller") # Guess for index 1
            # logger.info(f"Input text result: {input_result}")

        except Exception as e:
            logger.error(f"Error during controller example: {e}", exc_info=True)
        finally:
            logger.info("Closing browser context in controller example...")
            await b_context.close_context() # Context is managed by the `async with browser` block too
    
    logger.info("Controller example finished.")

if __name__ == "__main__":
    asyncio.run(example_controller_usage()) 