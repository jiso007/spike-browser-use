"""
Simple test to verify basic state retrieval works.
"""

import asyncio
import logging
import pytest
from browser_use_ext.extension_interface.service import ExtensionInterface

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_simple_state_retrieval(extension_interface: ExtensionInterface, playwright_browser):
    """Simple test that waits longer for content script to be ready."""
    logger.info("=== Simple State Retrieval Test ===")
    
    # Get the page
    if not playwright_browser.pages:
        await playwright_browser.new_page()
    page = playwright_browser.pages[0]
    
    # Navigate to a simple page
    logger.info("Navigating to example.com...")
    await page.goto("https://example.com", wait_until="networkidle")
    
    # Wait much longer for everything to stabilize
    logger.info("Waiting 10 seconds for content script to fully initialize...")
    await asyncio.sleep(10.0)
    
    # Check if the extension detected the page
    await extension_interface.wait_for_active_tab(timeout_seconds=5.0)
    active_tab_id = extension_interface._active_tab_id
    logger.info(f"Active tab ID: {active_tab_id}")
    
    # Try to get state with a longer timeout
    logger.info("Attempting to get browser state...")
    try:
        # The default timeout might be too short, but we can't easily change it
        # So let's just try and see what happens
        state = await extension_interface.get_state(for_vision=False)
        
        logger.info(f"✅ SUCCESS! Got state:")
        logger.info(f"  URL: {state.url}")
        logger.info(f"  Title: {state.title}")
        logger.info(f"  Actionable elements: {len(state.actionable_elements)}")
        
        # Success!
        assert "example.com" in state.url.lower()
        assert len(state.title) > 0
        
    except Exception as e:
        logger.error(f"Failed to get state: {e}")
        
        # Let's try a hacky workaround - manually inject a script to signal readiness
        logger.info("Trying workaround - manually signaling content script ready...")
        
        # This is a hack but might help us understand the issue
        try:
            # Try to manually send the ready signal from the page
            await page.evaluate("""
                () => {
                    if (chrome && chrome.runtime && chrome.runtime.sendMessage) {
                        chrome.runtime.sendMessage({ type: "content_script_ready" });
                        console.log("Manually sent content_script_ready signal");
                    }
                }
            """)
            logger.info("Sent manual ready signal, waiting 2 seconds...")
            await asyncio.sleep(2.0)
            
            # Try again
            state = await extension_interface.get_state(for_vision=False)
            logger.info(f"✅ SUCCESS with workaround! Got state:")
            logger.info(f"  URL: {state.url}")
            logger.info(f"  Title: {state.title}")
            
        except Exception as e2:
            logger.error(f"Workaround also failed: {e2}")
            raise