"""
Debug test to understand content script injection issues.
"""

import asyncio
import logging
import pytest
from browser_use_ext.extension_interface.service import ExtensionInterface

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_debug_content_script_injection(extension_interface: ExtensionInterface, playwright_browser):
    """Debug test to check content script injection step by step."""
    logger.info("=== DEBUG: Content Script Injection Test ===")
    
    # Get the first page
    if not playwright_browser.pages:
        await playwright_browser.new_page()
    page = playwright_browser.pages[0]
    
    # Start with a simple page
    logger.info("1. Navigating to example.com...")
    await page.goto("https://example.com", wait_until="networkidle")
    await asyncio.sleep(2.0)
    
    # Check if content script injected
    marker = await page.evaluate("() => window.__browserUseContentScriptReady || false")
    logger.info(f"2. Content script marker on example.com: {marker}")
    
    # Check console logs
    console_logs = []
    page.on('console', lambda msg: console_logs.append(f"{msg.type()}: {msg.text()}"))
    
    # Navigate to Wikipedia
    logger.info("3. Navigating to Wikipedia...")
    await page.goto("https://en.wikipedia.org/wiki/Main_Page", wait_until="networkidle")
    await asyncio.sleep(3.0)
    
    # Check if content script injected on Wikipedia
    marker = await page.evaluate("() => window.__browserUseContentScriptReady || false")
    logger.info(f"4. Content script marker on Wikipedia: {marker}")
    
    # Print console logs
    if console_logs:
        logger.info("Console logs from page:")
        for log in console_logs[-10:]:  # Last 10 logs
            logger.info(f"  {log}")
    
    # Try to manually check for content script elements
    has_listener = await page.evaluate("""
        () => {
            // Try to see if our message listener is there
            try {
                // Check if chrome.runtime exists
                return typeof chrome !== 'undefined' && 
                       typeof chrome.runtime !== 'undefined';
            } catch (e) {
                return false;
            }
        }
    """)
    logger.info(f"5. Chrome runtime available: {has_listener}")
    
    # Get the active tab ID from extension
    await extension_interface.wait_for_active_tab(timeout_seconds=5.0)
    active_tab_id = extension_interface._active_tab_id
    logger.info(f"6. Active tab ID from extension: {active_tab_id}")
    
    # Try a different approach - inject our own test script
    test_result = await page.evaluate("""
        () => {
            const testResults = {
                hasChrome: typeof chrome !== 'undefined',
                hasRuntime: typeof chrome !== 'undefined' && typeof chrome.runtime !== 'undefined',
                hasSendMessage: typeof chrome !== 'undefined' && 
                               typeof chrome.runtime !== 'undefined' && 
                               typeof chrome.runtime.sendMessage === 'function',
                documentState: document.readyState,
                url: window.location.href,
                isSecure: window.location.protocol === 'https:',
                hasContentScriptMarker: window.__browserUseContentScriptReady || false
            };
            return testResults;
        }
    """)
    logger.info(f"7. Page state check: {test_result}")
    
    # Wait a bit more and check again
    logger.info("8. Waiting 5 more seconds...")
    await asyncio.sleep(5.0)
    
    final_marker = await page.evaluate("() => window.__browserUseContentScriptReady || false")
    logger.info(f"9. Final content script marker: {final_marker}")
    
    # Check if we can get browser state despite the issues
    logger.info("10. Attempting to get browser state anyway...")
    try:
        state = await extension_interface.get_state(for_vision=False)
        logger.info(f"✅ Got state! URL: {state.url}, Title: {state.title}")
    except Exception as e:
        logger.error(f"❌ Failed to get state: {e}")
        
        # Check what tabs the extension knows about
        logger.info("11. Checking extension's view of tabs...")
        # This is a debug hack - normally we wouldn't access internals
        if hasattr(extension_interface, '_connections'):
            logger.info(f"Active connections: {len(extension_interface._connections)}")