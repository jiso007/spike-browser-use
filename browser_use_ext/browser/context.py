from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING, cast

from pydantic import BaseModel, Field, ValidationError

# Local application/library specific imports
from .views import BrowserState, TabInfo
from ..dom.views import DOMElementNode, DOMDocumentNode
from ..extension_interface.models import ResponseData

if TYPE_CHECKING:
    from ..extension_interface.service import ExtensionInterface

# Initialize logger for this module
logger = logging.getLogger(__name__)

class BrowserContextConfig(BaseModel):
    """
    Configuration for the browser context.

    This model holds settings that affect how the browser context interacts
    with the browser, such as viewport size and whether to highlight elements.
    """
    # Optional viewport height for the browser page.
    view_port_height: Optional[int] = Field(default=None, description="Viewport height for the browser.")
    # Optional viewport width for the browser page.
    view_port_width: Optional[int] = Field(default=None, description="Viewport width for the browser.")
    # Flag to determine if interactive elements should be highlighted by the extension.
    highlight_elements: bool = Field(default=True, description="Whether to highlight interactive elements.")
    # Placeholder for stealth mode, not implemented with extension but kept for API compatibility.
    use_stealth: bool = Field(default=False, description="Placeholder for stealth mode usage (not used by extension).")
    extension_host: str = Field(default="localhost", description="Host for the extension WebSocket server")
    extension_port: int = Field(default=8765, description="Port for the extension WebSocket server")
    

class BrowserContext:
    """
    Manages interaction with a browser page through the Chrome extension.

    This class replaces Playwright-based interactions by communicating with a
    custom Chrome extension via WebSockets. It provides methods to get browser
    state, and execute actions on the page.
    """
    
    def __init__(
        self,
        extension_interface: ExtensionInterface,
        config: BrowserContextConfig = BrowserContextConfig(),
    ):
        """
        Initializes the BrowserContext.

        Args:
            extension_interface: An instance of ExtensionInterface for communication.
            config: Configuration settings for the browser context.
        """
        self.config = config
        if extension_interface is None:
            raise ValueError("ExtensionInterface instance must be provided to BrowserContext.")
        self._extension = extension_interface
        # Caching the highlight_elements config for quick access
        self._highlight_elements = config.highlight_elements
        # Cache for the last retrieved browser state
        self._cached_browser_state: Optional[BrowserState] = None
        # Cache for the selector map from the last state
        self._cached_selector_map: Dict[int, Any] = {}
        # Manages multiple page proxies if the application handles multiple tabs simultaneously
        self._pages: Dict[Union[str, int], ExtensionPageProxy] = {}
        self._active_page_proxy: Optional[ExtensionPageProxy] = None
    
    async def __aenter__(self):
        """
        Asynchronous context manager entry.

        Ensures the WebSocket server for the extension interface is started
        if it\'s not already running.
        """
        # Start the extension server if it\'s not already running
        if not self._extension.is_server_running:
            logger.info("ExtensionInterface server not running, starting it now.")
            await self._extension.start_server()
        # Wait briefly to ensure connection can be established if extension just started
        # This is a pragmatic delay; a more robust solution might involve checking connection status.
        if not self._extension.has_active_connection:
            logger.info("Waiting briefly for potential extension connection...")
            await asyncio.sleep(2.0) # Allow time for extension to connect
            if not self._extension.has_active_connection:
                logger.warning("No active extension connection after waiting. Proceeding, but get_state might fail.")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Asynchronous context manager exit.

        Currently, this does not stop the server, as the server might be shared
        or managed externally. Consider adding server stop logic if BrowserContext
        is meant to exclusively manage the server lifecycle.
        """
        # The server is not stopped here to allow for shared or externally managed instances.
        # If BrowserContext should own the server lifecycle, uncomment the next lines:
        # if self._extension and self._extension.is_server_running:
        #     logger.info("Stopping ExtensionInterface server in BrowserContext aexit.")
        #     await self._extension.stop_server()
        pass # Current implementation does not stop the server on exit.
    
    async def get_state(self, include_screenshot: bool = False, tab_id: Optional[int] = None) -> BrowserState:
        """
        Asynchronously retrieves the current state of the browser, including all tabs,
        the active tab's content (DOM, screenshot if requested), and other relevant metadata.

        Args:
            include_screenshot: Whether to include a screenshot of the active page.
                                Defaults to False.
            tab_id: Optional specific tab ID to target for page-specific data.
                    If None, the extension will likely use the currently active tab.

        Returns:
            A BrowserState Pydantic model instance representing the current browser state.
        """
        logger.info(f"Requesting browser state (screenshot: {include_screenshot}, target_tab_id: {tab_id}).")
        
        try:
            # self._extension.get_state() now directly returns a BrowserState object on success
            # or raises an error (e.g., RuntimeError) on failure.
            browser_state: BrowserState = await self._extension.get_state(
                for_vision=include_screenshot,
                # tab_id is handled by ExtensionInterface._active_tab_id internally
            )
            
            # Update caches
            self._cached_browser_state = browser_state
            self._cached_selector_map = browser_state.selector_map if browser_state.selector_map is not None else {}
            return browser_state
            
        except RuntimeError as e: # Catch specific errors from ExtensionInterface.get_state
            error_message = f"Failed to get browser state from ExtensionInterface: {e}"
            logger.error(error_message, exc_info=True)
            return BrowserState(
                url="", title="", tabs=[],
                tree=DOMDocumentNode(children=[]),
                selector_map={},
                screenshot=None,
                pixels_above=0, pixels_below=0,
                error_message=error_message
            )
        except ValidationError as e: # Should ideally not happen here if ExtensionInterface.get_state returns valid BrowserState
            error_message = f"Pydantic validation error for BrowserState (unexpected): {e}"
            logger.error(error_message, exc_info=True)
            return BrowserState(
                url="", title="", tabs=[],
                tree=DOMDocumentNode(children=[]),
                selector_map={},
                screenshot=None,
                pixels_above=0, pixels_below=0,
                error_message=error_message
            )
        except Exception as e: # Catch any other unexpected errors
            error_message = f"Unexpected error in BrowserContext.get_state: {e}"
            logger.error(error_message, exc_info=True)
            return BrowserState(
                url="", title="", tabs=[],
                tree=DOMDocumentNode(children=[]),
                selector_map={},
                screenshot=None,
                pixels_above=0, pixels_below=0,
                error_message=error_message
            )
    
    async def get_current_page(self) -> "ExtensionPageProxy":
        """
        Returns a proxy object that mimics a Playwright Page.

        This provides a compatibility layer for parts of the system
        that might expect a Page-like interface for common operations.
        """
        logger.debug("Returning ExtensionPageProxy.")
        # The proxy uses the same extension interface instance
        return ExtensionPageProxy(self._extension, self)
    
    async def get_session(self) -> "BrowserContext":
        """
        Returns the current BrowserContext instance.

        Used for compatibility or when an explicit reference to the context is needed.
        """
        return self # Returns self, as this class is the session/context.
    
    async def get_selector_map(self) -> Dict[int, Dict[str, str]]:
        """
        Retrieves the cached selector map from the last call to get_state.

        If the cache is empty, it will trigger a new get_state call.

        Returns:
            A dictionary mapping highlight indices to element information.
        """
        if not self._cached_selector_map:
            logger.info("Selector map cache is empty, refreshing browser state.")
            # Refresh state to populate the selector map
            await self.get_state(include_screenshot=False) 
        return self._cached_selector_map
    
    async def get_dom_element_by_index(self, index: int) -> DOMElementNode:
        """
        Retrieves a specific DOMElementNode using its highlight_index.
        
        This method relies on the `selector_map` from the `BrowserState`, which
        is populated by the extension. The `selector_map` usually contains
        direct references or XPaths to elements. This Python-side function
        is more of a conceptual getter, as the actual element reference
        is within the extension's context.

        Args:
            index: The highlight_index of the desired element.

        Returns:
            A DOMElementNode representing the element (may be a simplified representation).

        Raises:
            ValueError: If the element with the given index is not found in the selector map.
            RuntimeError: If the state or element tree hasn't been fetched yet.
        """
        # Ensure the state is fresh enough or update it
        # _ = await self.get_state() # get_state updates caches, but might be too broad here if only tree needed
        # For now, assume _cached_browser_state is populated by a prior get_state() call in the test setup or real flow.

        if not self._cached_browser_state or not self._cached_browser_state.tree: # MODIFIED: element_tree -> tree
            logger.error("Attempted to get DOM element by index, but browser state or DOM tree is not cached.")
            raise RuntimeError("Browser state or DOM tree not available. Call get_state() first.")

        # This is a conceptual placeholder. In reality, the selector_map from the extension
        # gives us info, and the actual DOMElementNode might be constructed or found based on that.
        # The current BrowserState.tree *is* the parsed DOM tree (DOMDocumentNode).
        # We need to find the element within this tree that corresponds to the highlight_index.
        # The DOMElementNode itself now contains highlight_index.

        # Helper function to search the tree
        def find_node_by_highlight_index(node: Union[DOMElementNode, DOMDocumentNode], target_index: int) -> Optional[DOMElementNode]:
            if isinstance(node, DOMElementNode) and node.highlight_index == target_index:
                return node
            if node.children:
                for child in node.children:
                    found = find_node_by_highlight_index(child, target_index)
                    if found:
                        return found
            return None

        found_node = find_node_by_highlight_index(self._cached_browser_state.tree, index)

        if not found_node:
            logger.error(f"Element with highlight_index {index} not found in the cached DOM tree.")
            raise ValueError(f"No DOM element found for highlight index {index} in the cached DOM tree.") # MODIFIED ERROR MESSAGE
        
        return found_node

    async def _click_element_node(self, element_node: DOMElementNode) -> Optional[str]:
        """
        Sends a command to the extension to click an element.

        Args:
            element_node: The DOMElementNode to be clicked. Its highlight_index is used.

        Returns:
            Optional[str]: Path to a downloaded file if the click resulted in a download
                           (currently not supported by extension, returns None).

        Raises:
            ValueError: If the element_node does not have a highlight_index.
        """
        if element_node.highlight_index is None:
            logger.error("Cannot click element: highlight_index is missing.")
            raise ValueError("Element must have a highlight_index to be clicked via extension.")
        
        logger.info(f"Requesting click on element with index: {element_node.highlight_index}")
        await self._extension.execute_action("click_element_by_index", {
            "index": element_node.highlight_index
        })
        # Download handling is not implemented in this extension-based approach.
        return None
    
    async def _input_text_element_node(self, element_node: DOMElementNode, text: str) -> None:
        """
        Sends a command to the extension to input text into an element.

        Args:
            element_node: The DOMElementNode to input text into. Its highlight_index is used.
            text: The text to input.

        Raises:
            ValueError: If the element_node does not have a highlight_index.
        """
        if element_node.highlight_index is None:
            logger.error("Cannot input text: highlight_index is missing from element_node.")
            raise ValueError("Element must have a highlight_index for text input via extension.")
        
        logger.info(f"Requesting text input \'{text}\' into element with index: {element_node.highlight_index}")
        await self._extension.execute_action("input_text", {
            "index": element_node.highlight_index,
            "text": text
        })
    
    async def is_file_uploader(self, element_node: DOMElementNode) -> bool:
        """
        Checks if a given DOMElementNode represents a file input element.

        Args:
            element_node: The DOMElementNode to check.

        Returns:
            True if the element is an <input type="file">, False otherwise.
        """
        # This check is based on common HTML attributes for file inputs.
        is_uploader = (
            element_node.tag_name.lower() == "input" and
            element_node.attributes.get("type", "").lower() == "file"
        )
        logger.debug(f"Element (index {element_node.highlight_index}) is_file_uploader: {is_uploader}")
        return is_uploader
    
    async def take_screenshot(self, full_page: bool = False) -> Optional[str]:
        """
        Requests a screenshot of the current page from the extension.

        Args:
            full_page: This parameter is for Playwright compatibility. The extension currently
                       captures the visible tab. Full page screenshots are not directly supported
                       by `chrome.tabs.captureVisibleTab` in the same way.

        Returns:
            A base64 encoded string of the screenshot PNG, or None if failed.
        """
        if full_page:
            logger.warning("Full page screenshot requested, but extension captures visible tab. Proceeding with visible tab capture.")
        
        # Request state with screenshot included
        state = await self.get_state(include_screenshot=True)
        if state.screenshot:
            logger.info("Screenshot taken successfully.")
        else:
            logger.warning("Screenshot attempt made, but no screenshot data received.")
        return state.screenshot # This will be base64 data or None
    
    async def remove_highlights(self) -> None:
        """
        Placeholder for removing highlights from elements on the page.
        
        This functionality would need to be implemented in the content script
        of the Chrome extension.
        """
        # This functionality would be an action sent to the content script.
        # For example: await self._extension.execute_action("remove_highlights", {})
        logger.info("remove_highlights called (placeholder - requires extension implementation).")
        pass # No-op for now, requires extension-side implementation.
    
    async def create_new_tab(self, url: Optional[str] = None) -> None:
        """
        Requests the extension to open a new browser tab.

        Args:
            url: The URL to open in the new tab. If None, "about:blank" is typically used.
        """
        target_url = url or "about:blank" # Default to blank page if no URL specified
        logger.info(f"Requesting to open new tab with URL: {target_url}")
        await self._extension.execute_action("open_tab", {"url": target_url})
        # Active tab should be updated by the background script logic and subsequent get_state calls.
    
    async def switch_to_tab(self, page_id: int) -> None:
        """
        Requests the extension to switch to a different browser tab.

        Args:
            page_id: The page_id (index from the tabs list) of the tab to switch to.
        """
        logger.info(f"Requesting to switch to tab with page_id: {page_id}")
        await self._extension.execute_action("switch_tab", {"page_id": page_id})
        # Active tab status should be reflected in subsequent get_state calls.

    async def go_back(self) -> None:
        """
        Requests the extension to navigate back in the current tab\'s history.
        """
        logger.info("Requesting to navigate back.")
        await self._extension.execute_action("go_back", {})
        # Page state will change, new get_state() will reflect it.
    
    async def close_tab(self, page_id: Optional[int] = None) -> None:
        """
        Requests the extension to close a browser tab.

        Args:
            page_id: The page_id (index from the tabs list) of the tab to close.
                     If None, it attempts to close the current active tab.
        """
        current_page_id_to_close = page_id

        if current_page_id_to_close is None:
            # If no page_id is provided, try to determine the current active tab's page_id
            if self._cached_browser_state and self._cached_browser_state.tabs:
                # Find the current tab based on URL and Title (less reliable) or assume first active
                # A more robust way is if background.js returns active_tab_chrome_id and we map it.
                # For now, let's assume if no page_id, the action should target what the extension considers active.
                # The background script's close_tab should ideally handle "current active" if no id provided.
                # However, our current background script expects a page_id.
                # Let's try to find the active one from our cached state.
                active_tab_info = next((tab for tab in self._cached_browser_state.tabs if self._cached_browser_state.url == tab.url), None) # Simple match
                if active_tab_info:
                    current_page_id_to_close = active_tab_info.page_id
                    logger.info(f"No page_id provided for close_tab, attempting to close current tab (page_id: {current_page_id_to_close}).")
                else:
                    logger.error("Cannot determine current tab to close: no page_id provided and no matching active tab in cache.")
                    raise ValueError("Cannot determine current tab to close without page_id or cached active tab info.")
            else:
                # If no cached state, we must have a page_id
                logger.error("Cannot close tab: no page_id specified and no cached browser state to determine active tab.")
                raise ValueError("page_id must be specified to close a tab if browser state is not cached.")

        logger.info(f"Requesting to close tab with page_id: {current_page_id_to_close}")
        await self._extension.execute_action("close_tab", {"page_id": current_page_id_to_close})
        # State should be updated on next get_state call.


class ExtensionPageProxy:
    """
    A proxy class that provides a simplified, Playwright-Page-like interface.

    This class delegates actions to the ExtensionInterface, allowing other parts
    of the application to interact with the browser via the extension using
    a familiar API (subset of Playwright Page API).
    """
    
    def __init__(self, extension: ExtensionInterface, browser_context: BrowserContext):
        """
        Initializes the ExtensionPageProxy.

        Args:
            extension: The ExtensionInterface instance for communication.
            browser_context: The parent BrowserContext, used to refresh state.
        """
        self._extension = extension
        self._browser_context = browser_context
        self.url: Optional[str] = None
        self.title_val: Optional[str] = None
        self.frames: list = []

    async def goto(self, url: str, **kwargs: Any) -> None:
        """
        Navigates the current active tab to the specified URL via the extension.

        Args:
            url: The URL to navigate to.
            **kwargs: Ignored, for Playwright compatibility.
        """
        logger.info(f"ExtensionPageProxy: Navigating to URL: {url}")
        await self._extension.execute_action("go_to_url", {"url": url})
        # After navigation, update local URL and title by fetching new state
        # Note: Navigation can take time. A robust solution might wait for load.
        await asyncio.sleep(1.5) # Simple delay, replace with load state check if possible
        try:
            state = await self._browser_context.get_state()
            self.url = state.url
            self.title_val = state.title
            logger.info(f"ExtensionPageProxy: Navigation complete. New URL: {self.url}")
        except Exception as e:
            logger.warning(f"ExtensionPageProxy: Could not refresh state after goto: {e}")
            self.url = url # Tentatively set
            self.title_val = "Unknown"


    async def wait_for_load_state(self, state: str = "networkidle", **kwargs: Any) -> None:
        """
        Simulates waiting for a page load state.

        In a Playwright context, this waits for network activity to cease.
        With the extension, this is simplified. A more complex implementation
        could involve messages from the content script about load status.

        Args:
            state: The desired load state (e.g., "load", "domcontentloaded", "networkidle"). Ignored.
            **kwargs: Ignored, for Playwright compatibility.
        """
        # This is a simplified version. True load state waiting is complex with extensions.
        # Content script could send 'load_complete' event, or we poll for document.readyState.
        logger.info(f"ExtensionPageProxy: Simulating wait_for_load_state ('{state}'). Adding small delay.")
        await asyncio.sleep(1.5) # Arbitrary delay to simulate load time.
        # Refresh state after "waiting"
        try:
            new_state = await self._browser_context.get_state()
            self.url = new_state.url
            self.title_val = new_state.title
        except Exception as e:
            logger.warning(f"ExtensionPageProxy: Could not refresh state after wait_for_load_state: {e}")

    async def content(self) -> str:
        """
        Retrieves the "content" of the page (currently simplified to title and URL).

        A full implementation would require the extension to send the full HTML source.
        For now, it returns a string combining title and URL.

        Returns:
            A string representing basic page information.
        """
        logger.debug("ExtensionPageProxy: content() called.")
        # To get full HTML, an "extract_html" action would be needed in the extension.
        # For now, refresh state and return some info.
        state = await self._browser_context.get_state()
        self.url = state.url
        self.title_val = state.title
        # Placeholder for actual HTML content
        return f"<html><head><title>{self.title_val or 'Page'}</title></head><body>Content of {self.url or 'current page'}. (Full HTML not retrieved)</body></html>"

    async def title(self) -> str:
        """
        Retrieves the title of the current page via the extension.

        Returns:
            The title of the page, or an empty string if not available.
        """
        logger.debug("ExtensionPageProxy: title() called.")
        state = await self._browser_context.get_state()
        self.url = state.url # Keep URL fresh
        self.title_val = state.title
        return self.title_val or "" 