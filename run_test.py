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
        wait_time = 5
        logger.info(f"Waiting {wait_time} seconds for the Chrome extension to connect...")
        await asyncio.sleep(wait_time) 

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
            logger.info("Calling browser_context.get_state(include_screenshot=False)...")
            # Type hint for clarity
            current_browser_state: BrowserState = await browser_context.get_state(include_screenshot=False)
            
            logger.info("--- Successfully Received BrowserState from Extension ---")
            # .model_dump_json(indent=2) is a Pydantic method for nice JSON output
            # This will print the structured data to your Python console.
            # MODIFIED: Comment out the line that prints the full BrowserState to console
            # logger.info(current_browser_state.model_dump_json(indent=2)) 
            logger.info("--- End of BrowserState (Full content NOT printed to console) ---") # MODIFIED log message
            logger.info("Now, check the Chrome extension's Service Worker console for its detailed logs regarding this get_state operation.")

            # MODIFIED: Save the output to a JSON file
            output_filename = "browser_state_output.json"
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(current_browser_state.model_dump_json(indent=2))
            logger.info(f"BrowserState successfully saved to {output_filename}")

    except ConnectionRefusedError:
        logger.error(f"Connection refused when trying to start server on port {ext_interface.port}.") # This will now show ORIGINAL_PORT
        logger.error("Is another process (perhaps another instance of this script or your main app) already using this port?")
    except RuntimeError as e:
        logger.error(f"RuntimeError encountered: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        if ext_interface.is_server_running:
            logger.info("Stopping Python WebSocket server...")
            await ext_interface.stop_server()
            logger.info("Python WebSocket server stopped.")
        else:
            logger.info("Python WebSocket server was not running at the end or failed to start.")

if __name__ == "__main__":
    # This setup allows the script to be run directly.
    # Python's asyncio event loop will manage the async operations.
    asyncio.run(trigger_get_state_from_extension()) 