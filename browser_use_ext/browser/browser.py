from __future__ import annotations

# Standard library imports
import asyncio
import logging
from typing import Optional, Any

# Third-party imports
from pydantic import BaseModel, Field

# Local application/library specific imports
from .context import BrowserContext, BrowserContextConfig

# Initialize logger for this module
logger = logging.getLogger(__name__)

class BrowserConfig(BaseModel):
    """
    Configuration for the main Browser class.
    This can include settings for the extension interface and default context configurations.
    """
    # Host for the WebSocket server that the extension connects to.
    extension_host: str = Field(default="localhost", description="Hostname for the extension WebSocket server.")
    # Port for the WebSocket server.
    extension_port: int = Field(default=8765, description="Port for the extension WebSocket server.")
    # Default browser context configuration, can be overridden when creating a new context.
    default_context_config: BrowserContextConfig = Field(
        default_factory=BrowserContextConfig,
        description="Default configuration for new browser contexts."
    )
    # Add other browser-level configurations here if needed in the future
    # For example: path to Chrome user data directory if managing browser launch (not current scope)
    # chrome_user_data_dir: Optional[str] = Field(None, description="Path to Chrome user data directory.")

class Browser:
    """
    Manages the browser instance and communication with the Chrome extension.
    
    This class is responsible for initializing the WebSocket server (via ExtensionInterface)
    that the Chrome extension connects to. It then provides methods to create and manage
    BrowserContext instances, which represent individual pages or sessions controlled
    through the extension.
    """

    def __init__(self, config: BrowserConfig = BrowserConfig()):
        """
        Initializes the Browser instance.

        Args:
            config: Configuration for the browser and extension interface.
        """
        # Import ExtensionInterface here to break circular dependency
        from ..extension_interface.service import ExtensionInterface

        self.config = config
        # Initialize the ExtensionInterface which manages the WebSocket server and communication.
        # This interface will be shared across all browser contexts created by this Browser instance.
        self._extension_interface = ExtensionInterface(
            host=self.config.extension_host,
            port=self.config.extension_port
        )
        # Internal state to track if the browser (specifically the extension server) is active.
        self._is_active = False
        logger.info(f"Browser instance initialized. Extension server configured for ws://{self.config.extension_host}:{self.config.extension_port}")

    async def launch(self) -> "Browser":
        """
        "Launches" the browser by starting the ExtensionInterface WebSocket server.
        
        In this extension-based model, "launching" primarily means ensuring the backend
        WebSocket server is ready to accept connections from the Chrome extension.
        The actual Chrome browser is assumed to be launched manually by the user with the
        extension installed.
        """
        if self._is_active and self._extension_interface.is_server_running:
            logger.warning("Browser (ExtensionInterface server) is already active and running.")
            return self

        logger.info("Starting ExtensionInterface WebSocket server...")
        try:
            await self._extension_interface.start_server()
            self._is_active = True
            logger.info("ExtensionInterface WebSocket server started. Browser is now 'active'.")
            # At this point, the Python backend is ready. The user needs to ensure Chrome is running
            # with the extension, and the extension is configured to connect to the server.
            return self
        except Exception as e:
            logger.error(f"Failed to start ExtensionInterface server: {e}", exc_info=True)
            self._is_active = False # Ensure state reflects failure
            raise # Re-raise the exception to indicate launch failure

    async def new_context(self, context_config: Optional[BrowserContextConfig] = None) -> BrowserContext:
        """
        Creates a new browser context for interacting with a page via the extension.

        Args:
            context_config: Specific configuration for this context. If None, uses
                            the default context config from the Browser instance.

        Returns:
            A BrowserContext instance.

        Raises:
            RuntimeError: If the browser (ExtensionInterface server) is not active/launched.
        """
        if not self._is_active or not self._extension_interface.is_server_running:
            logger.error("Cannot create new context: Browser (ExtensionInterface server) is not active or not running.")
            raise RuntimeError("Browser must be launched and ExtensionInterface server running before creating a context.")

        config_to_use = context_config or self.config.default_context_config
        logger.info(f"Creating new BrowserContext with config: {config_to_use.model_dump_json(indent=2)}")
        
        # The BrowserContext will use the shared ExtensionInterface instance.
        return BrowserContext(config=config_to_use, extension_interface=self._extension_interface)

    async def close(self) -> None:
        """
        Closes the browser by stopping the ExtensionInterface WebSocket server.
        This will disconnect any connected Chrome extensions.
        """
        if not self._is_active:
            logger.warning("Browser (ExtensionInterface server) is not active, nothing to close.")
            return

        logger.info("Closing browser: stopping ExtensionInterface WebSocket server...")
        try:
            await self._extension_interface.stop_server()
            logger.info("ExtensionInterface WebSocket server stopped.")
        except Exception as e:
            logger.error(f"Error stopping ExtensionInterface server: {e}", exc_info=True)
            # Continue with setting _is_active to False even if server stop had issues.
        finally:
            self._is_active = False
            logger.info("Browser is now 'inactive'.")

    @property
    def is_connected(self) -> bool:
        """
        Checks if the ExtensionInterface has at least one active connection from an extension.
        
        Returns:
            True if at least one extension is connected, False otherwise.
        """
        return self._extension_interface.has_active_connection

    @property
    def is_launched(self) -> bool:
        """
        Indicates whether the browser (specifically the ExtensionInterface server)
        has been successfully launched and is currently active.
        """
        return self._is_active

    # Asynchronous context manager support
    async def __aenter__(self) -> "Browser":
        """
        Allows the Browser instance to be used as an asynchronous context manager.
        Ensures the browser (ExtensionInterface server) is launched upon entering the context.
        """
        await self.launch()
        return self

    async def __aexit__(self, exc_type: Optional[type[BaseException]], 
                        exc_val: Optional[BaseException], 
                        exc_tb: Optional[Any]) -> None:
        """
        Cleans up by closing the browser (stopping the ExtensionInterface server)
        when exiting the asynchronous context.
        """
        await self.close()

# Example Usage (can be run for basic testing if this file is executed directly)
async def main_example():
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting Browser example...")

    browser_config = BrowserConfig() # Default config
    browser = Browser(config=browser_config)

    async with browser: # Uses __aenter__ and __aexit__ for launch and close
        logger.info("Browser launched via context manager.")
        
        # Wait for an extension to connect (manual step by user)
        logger.info(f"Please ensure Chrome extension is running and connected to ws://{browser.config.extension_host}:{browser.config.extension_port}")
        for _ in range(15): # Wait up to 15 seconds for connection
            if browser.is_connected:
                logger.info("Extension connected!")
                break
            await asyncio.sleep(1)
        else:
            logger.warning("No extension connected after 15 seconds. Example might not work fully.")
            # Depending on strictness, could raise error or proceed cautiously.

        if browser.is_connected:
            try:
                # Create a new browser context
                context = await browser.new_context()
                logger.info("BrowserContext created.")

                async with context: # Manages context resources (server start is by Browser obj)
                    logger.info("Entered BrowserContext.")
                    # Use the context to interact with the browser page
                    # 1. Navigate to a page (using the proxy)
                    page_proxy = await context.get_current_page()
                    target_url = "https://www.google.com"
                    logger.info(f"Attempting to navigate to: {target_url}")
                    await page_proxy.goto(target_url)
                    logger.info(f"Navigation to {target_url} initiated.")

                    # 2. Get browser state
                    logger.info("Attempting to get browser state...")
                    state = await context.get_state(include_screenshot=False) # Set to True for screenshot
                    logger.info(f"Current page URL: {state.url}")
                    logger.info(f"Current page Title: {state.title}")
                    if state.tabs:
                        logger.info(f"Open tabs ({len(state.tabs)}): {[(t.page_id, t.title, t.url) for t in state.tabs]}")
                    if state.screenshot:
                        logger.info("Screenshot was captured (first few chars): " + state.screenshot[:50] + "...")
                    
                    # Example: Find an interactive element (e.g., search bar on Google)
                    # This requires the DOM to be parsed and selector_map to be populated.
                    if state.selector_map:
                        logger.info(f"Selector map has {len(state.selector_map)} interactive elements.")
                        # Try to find an input field (heuristic)
                        input_element_index = None
                        for idx, details in state.selector_map.items():
                            # `details` in our current setup is just the xpath from extension's `cachedSelectorMap`
                            # To get tag_name, we need to look up `idx` in `state.element_tree`
                            # For simplicity, we'll assume the first one or a known one for example.
                            # Let's assume index 0 is an input field for this example if map not empty
                            if state.element_tree:
                                node_candidate = await context.get_dom_element_by_index(idx) # type: ignore
                                if node_candidate and node_candidate.tag_name == 'input' and node_candidate.attributes.get('type') == 'text':
                                    input_element_index = idx
                                    logger.info(f"Found potential input field with index {idx}")
                                    break
                        if input_element_index is not None:
                            logger.info(f"Attempting to type into element with index {input_element_index}")
                            search_term = "Browser-Use Automation"
                            await context._input_text_element_node(
                                await context.get_dom_element_by_index(input_element_index), 
                                search_term
                            )
                            logger.info(f"Typed '{search_term}' into element {input_element_index}.")
                            # Potentially click a search button here if one is found
                        else:
                            logger.info("No suitable input field found in selector_map for typing example.")
                    else:
                        logger.info("Selector map is empty. Cannot demonstrate typing.")

                    # 3. Example: Create and switch tab (if extension supports it)
                    # await context.create_new_tab("https://www.bing.com")
                    # logger.info("New tab requested for bing.com")
                    # await asyncio.sleep(2) # Give time for tab to open
                    # updated_state = await context.get_state()
                    # logger.info(f"Tabs after opening new one: {[(t.page_id, t.title) for t in updated_state.tabs]}")
                    # Find the new tab's page_id and switch
                    # ... (logic to find and switch) ...

            except RuntimeError as e:
                logger.error(f"Runtime error during browser interaction: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred during example interaction: {e}", exc_info=True)
        else:
            logger.error("Cannot run example interactions: Chrome extension is not connected.")

    logger.info("Browser example finished.")

if __name__ == "__main__":
    asyncio.run(main_example()) 