# This is conftest.py for the tests directory.
# It can be used for test-specific fixtures and plugins.
# Keeping it minimal for now to resolve import errors.

# Minimal conftest.py for the tests directory
# This file is intentionally kept simple to avoid import errors. 

import pytest
import pytest_asyncio
import asyncio
import logging
import os
from pathlib import Path
from typing import AsyncGenerator, Generator
from playwright.async_api import async_playwright, Browser, BrowserContext, Page # type: ignore

from browser_use_ext.extension_interface.service import ExtensionInterface

logger = logging.getLogger(__name__)

TEST_SERVER_PORT = 8766  # Use a different port than the default to avoid conflicts

def get_extension_path() -> str:
    """Get the absolute path to the Chrome extension directory."""
    # Navigate from tests/conftest.py to extension directory
    current_file = Path(__file__)
    # Assuming conftest.py is in browser_use_ext/tests/
    # So, current_file.parent is browser_use_ext/tests/
    # current_file.parent.parent is browser_use_ext/
    # current_file.parent.parent / "extension" is browser_use_ext/extension/
    extension_path = current_file.parent.parent / "extension"
    
    if not extension_path.exists() or not extension_path.is_dir():
        # Fallback for potentially different execution context (e.g. running from project root)
        alt_extension_path = Path(os.getcwd()) / "browser_use_ext" / "extension"
        if alt_extension_path.exists() and alt_extension_path.is_dir():
            extension_path = alt_extension_path
        else:
            raise FileNotFoundError(
                f"Extension directory not found at {str(extension_path.absolute())} " 
                f"or {str(alt_extension_path.absolute())}"
            )
    
    abs_path = str(extension_path.resolve()) # Use resolve() for absolute path
    logger.info(f"Determined extension path: {abs_path}")
    return abs_path

@pytest_asyncio.fixture(scope="function")
async def playwright_browser() -> AsyncGenerator[BrowserContext, None]: # Changed Browser to BrowserContext
    """
    Pytest fixture to launch and manage a Playwright browser with the Chrome extension loaded.
    Yields a BrowserContext, not the entire Browser object, for more focused interaction.
    """
    logger.info("Playwright fixture: Starting browser with extension...")
    
    playwright = None
    context = None
    
    try:
        playwright = await async_playwright().start()
        
        # Get extension path
        extension_path = get_extension_path()
        logger.info(f"Loading extension from: {extension_path}")
        
        # Launch browser with extension
        # Using launch_persistent_context is often more reliable for extensions
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir="",  # Use a temporary user data directory (empty string means Playwright manages it)
            headless=False,  # Must be False for extensions to load and background scripts to run properly.
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
                "--no-first-run",
                "--no-default-browser-check",
                # "--disable-web-security", # Generally not recommended unless strictly necessary
                # Consider "--disable-features=VizDisplayCompositor" if rendering issues occur
            ]
        )
        
        # Check if we already have a tab from launch_persistent_context
        logger.info(f"Playwright fixture: Current pages count: {len(context.pages)}")
        
        # Use the existing tab if there is one, otherwise create one
        if context.pages:
            logger.info("Playwright fixture: Using existing tab")
            page = context.pages[0]
        else:
            logger.info("Playwright fixture: No existing tab, creating one...")
            page = await context.new_page()
        
        logger.info(f"Playwright fixture: Total pages: {len(context.pages)}")
        logger.info("Playwright fixture: NOT navigating with Playwright - extension will handle navigation via DOM injection")
        
        # It is important to wait for the extension to load and its background script to run.
        # A fixed sleep is not ideal, but often necessary for extensions.
        # A more robust solution would be for the extension to signal readiness.
        logger.info("Playwright fixture: Browser launched, waiting for extension to initialize...")
        await asyncio.sleep(5.0) # Increased sleep duration for reliability to allow extension to detect active tab
        
        logger.info(f"Playwright fixture: Browser context ready. Pages: {len(context.pages)}")
        yield context # Yield the context
        
    except Exception as e:
        logger.error(f"Playwright fixture: Error during browser setup: {e}", exc_info=True)
        raise
    finally:
        logger.info("Playwright fixture: Cleaning up browser context...")
        if context:
            await context.close()
            logger.info("Playwright fixture: Browser context closed.")
        if playwright:
            await playwright.stop()
            logger.info("Playwright fixture: Playwright stopped.")

@pytest_asyncio.fixture(scope="function")
async def extension_interface(playwright_browser: BrowserContext) -> AsyncGenerator[ExtensionInterface, None]: # Added playwright_browser dep
    """
    Pytest fixture to start and stop the ExtensionInterface server for each test function.
    Depends on playwright_browser to ensure browser is up before server starts.
    """
    logger.info("ExtensionInterface fixture: Starting server...")
    # Note: playwright_browser fixture ensures the browser with extension is running
    # before this fixture proceeds.
    interface = ExtensionInterface(host="localhost", port=TEST_SERVER_PORT)
    try:
        await interface.start_server()
        logger.info(f"ExtensionInterface fixture: Server started on port {TEST_SERVER_PORT}.")
        
        # Wait for the extension to connect to this server instance
        connection_established = await wait_for_extension_connection(interface, timeout_seconds=15.0)
        if not connection_established:
            # Log pages if connection fails, to help debug if extension loaded
            if playwright_browser and playwright_browser.pages:
                for i, page_in_ctx in enumerate(playwright_browser.pages):
                    logger.error(f"Page {i} URL at connection failure: {page_in_ctx.url}")
            else:
                logger.error("No pages found in browser context at connection failure.")
            raise RuntimeError(f"Extension failed to connect to WebSocket server at port {TEST_SERVER_PORT} within timeout.")
        
        logger.info("ExtensionInterface fixture: Extension connected.")
        yield interface
        
    except Exception as e:
        logger.error(f"ExtensionInterface fixture: Error during server setup or test: {e}", exc_info=True)
        raise # Re-raise the exception to fail the test
    finally:
        logger.info("ExtensionInterface fixture: Stopping server...")
        if interface:
            await interface.close()
            logger.info("ExtensionInterface fixture: Server stopped.")

async def wait_for_extension_connection(
    interface: ExtensionInterface, 
    timeout_seconds: float = 10.0
) -> bool:
    """
    Wait for the Chrome extension to establish a WebSocket connection.
    
    Args:
        interface: The ExtensionInterface instance to monitor.
        timeout_seconds: Maximum time to wait for connection.
        
    Returns:
        True if connection established, False if timeout.
    """
    logger.info(f"Waiting for extension WebSocket connection (timeout: {timeout_seconds}s)...")
    
    start_time = asyncio.get_event_loop().time()
    while not interface.has_active_connection:
        if (asyncio.get_event_loop().time() - start_time) >= timeout_seconds:
            logger.error("Timeout waiting for extension WebSocket connection.")
            return False
        await asyncio.sleep(0.25) # Check frequently
    
    logger.info(f"Extension WebSocket connected: Client ID {interface.active_connection_object.client_id if interface.active_connection_object else 'N/A'}")
    return True

# Minimal conftest.py for the tests directory
# This file is intentionally kept simple to avoid import errors. 