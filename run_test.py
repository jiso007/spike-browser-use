import asyncio
import logging
import sys
import os
import json

# Get the directory where this script (run_test.py) is located.
# This should be your project root: C:\...\browser-use
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add this script's directory to Python's path if it's not already there.
# This ensures Python looks for modules starting from your project root.
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Now print sys.path for debugging immediately before the try-except block
print("--- Current sys.path for Python interpreter: ---")
for p in sys.path:
    print(p)
print("-------------------------------------------------")

# Attempt to import project modules. 
# This assumes the script is run from the project root or that PYTHONPATH is set up correctly.
try:
    from browser_use_ext.extension_interface.service import ExtensionInterface
    from browser_use_ext.browser.context import BrowserContext, BrowserContextConfig
    from browser_use_ext.browser.views import BrowserState # For type hinting
except ImportError as e:
    print(f"ImportError: {e}. Please ensure this script is run from the project root directory,")
    print("or that your PYTHONPATH is configured to find the 'browser_use_ext' module.")
    print("Example: If 'browser_use_ext' is in '/path/to/project/browser_use_ext', run from '/path/to/project/'.")
    print(f"Script directory added to path was: {script_dir}") # Debugging print
    exit(1)

ORIGINAL_PORT = 8765 # CHANGED: Define the original port

async def trigger_get_state_from_extension():
    """
    Initializes the ExtensionInterface, starts its server, waits for an extension connection,
    then calls get_state() via a BrowserContext and prints the result.
    """
    # Configure basic logging to see output from this Python script
    logging.basicConfig(
        level=logging.DEBUG, 
        format="%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
        handlers=[logging.StreamHandler()] # Ensure logs go to console
    )
    logger = logging.getLogger(__name__)

    # 1. Create an instance of your ExtensionInterface
    ext_interface = ExtensionInterface(host="localhost", port=ORIGINAL_PORT) # CHANGED: Use ORIGINAL_PORT

    try:
        # 2. Start the WebSocket server that the extension connects to
        logger.info(f"Starting Python WebSocket server on port {ORIGINAL_PORT}...") # CHANGED: Log ORIGINAL_PORT
        await ext_interface.start_server()
        logger.info(f"Python WebSocket server started on ws://{ext_interface.host}:{ext_interface.port}")
        logger.info("Ensure your Chrome extension (browser-use-ext) is loaded, enabled, and can connect.")

        # 3. Wait a few seconds for the extension to connect
        #    In a real app, you might loop and check ext_interface.has_active_connection
        wait_time = 5 // seconds
        logger.info(f"Waiting {wait_time} seconds for the Chrome extension to connect...")
        
        # More robust connection wait loop
        connection_attempts = 0
        max_connection_attempts = wait_time * 2 # Try for 10s if sleep is 0.5s
        while not ext_interface.has_active_connection and connection_attempts < max_connection_attempts:
            await asyncio.sleep(0.5)
            connection_attempts += 1
            if connection_attempts % 4 == 0: # Log every 2 seconds
                 logger.info(f"Still waiting for extension connection... ({connection_attempts / 2}s / {max_connection_attempts / 2}s)")


        if not ext_interface.has_active_connection:
            logger.warning("No active connection from the Chrome extension after waiting.")
            logger.warning("Please check the following:")
            logger.warning("  1. Is the 'browser-use-ext' extension loaded and enabled in Chrome?")
            logger.warning("  2. Are there any errors in the extension's Service Worker console?")
            logger.warning(f"  3. Does the extension's WS_URL (in background.js) match ws://{ext_interface.host}:{ORIGINAL_PORT}?") 
            logger.warning(f"  4. Is another process already using port {ORIGINAL_PORT}?") # CHANGED
            return # Exit if no connection

        logger.info("Chrome extension appears to be connected! Proceeding to call get_state.")

        # 4. Create a BrowserContext instance and call get_state
        # Ensure BrowserContextConfig also uses the original port
        context_config = BrowserContextConfig(extension_port=ORIGINAL_PORT) # CHANGED: Pass ORIGINAL_PORT to context config
        
        browser_context = BrowserContext(config=context_config, extension_interface=ext_interface)

        # The async with block for BrowserContext might also handle server start/stop
        # or other setup/teardown if implemented in its __aenter__/__aexit__.
        # For this test, primary server control is outside.
        async with browser_context:
            logger.info("CALLING THIS TEST SCRIPT REQUIRES MANUAL SETUP IN YOUR BROWSER:")
            logger.info("1. Please open a NEW TAB in Chrome.")
            logger.info("2. Navigate to: https://www.example.com")
            logger.info("3. Make sure this tab is the ACTIVE TAB.")
            logger.info("Waiting 10 seconds for you to do this...")
            await asyncio.sleep(10) # Give user time to set up the page
            
            logger.info("Attempting to call browser_context.get_state(include_screenshot=False)...")
            current_browser_state: BrowserState = await browser_context.get_state(include_screenshot=False)
            
            logger.info("--- Successfully Received BrowserState from Extension ---")
            output_filename = "browser_state_integration_test.json" # Changed filename
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(current_browser_state.model_dump_json(indent=2))
            logger.info(f"BrowserState successfully saved to {output_filename}")

            if current_browser_state and current_browser_state.actionable_elements:
                logger.info(f"Found {len(current_browser_state.actionable_elements)} actionable elements on the page.")
                
                # Attempt to find a link to click (example.com should have one)
                target_link_element = None
                for elem in current_browser_state.actionable_elements:
                    if elem.type == "link" and elem.text_content and "more information" in elem.text_content.lower():
                        target_link_element = elem
                        break
                
                if target_link_element:
                    logger.info(f"Identified target link: ID \'{target_link_element.element_id}\', Text: \'{target_link_element.text_content}\'")
                    logger.info(f"Attempting to click this link using element_id: {target_link_element.element_id}")
                    try:
                        click_result = await browser_context.execute_action(
                            action_name="click_element", 
                            action_params={"element_id": target_link_element.element_id}
                        )
                        logger.info(f"\'click_element\' action result: {click_result}")
                        logger.info("Please visually confirm if the link on example.com was clicked (e.g., navigated to a new page or new content loaded).")
                    except Exception as e_click:
                        logger.error(f"Error during \'click_element\' action: {e_click}", exc_info=True)
                else:
                    logger.warning("Could not find the target \'More information...\' link on example.com to test click action.")
                    logger.info("Available actionable elements:")
                    for i, elem in enumerate(current_browser_state.actionable_elements[:5]): # Log first 5
                        logger.info(f"  {i+1}. ID: {elem.element_id}, Type: {elem.type}, Text: \'{elem.text_content[:50]}\'")

            else:
                logger.warning("No actionable elements found in the browser state. Cannot test click action.")


    except ConnectionRefusedError:
        logger.error(f"Connection refused when trying to start server on port {ext_interface.port}.") # This will now show ORIGINAL_PORT
        logger.error("Is another process (perhaps another instance of this script or your main app) already using this port?")
    except RuntimeError as e:
        logger.error(f"RuntimeError encountered: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        logger.info("Test script attempting to clean up...")
        # Ensure server is stopped if it was started
        # Check if _server attribute exists and is not None, indicating it might have been started
        if hasattr(ext_interface, '_server') and ext_interface._server is not None:
            logger.info("Shutting down WebSocket server...")
            await ext_interface.close() # Use the close method which handles server and connections
        else:
            logger.info("WebSocket server was not started or already cleaned up.")
        logger.info("Test script finished.")

if __name__ == "__main__":
    # This setup allows the script to be run directly.
    # Python's asyncio event loop will manage the async operations.
    asyncio.run(trigger_get_state_from_extension()) 