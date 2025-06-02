#!/usr/bin/env python3
"""
Simple test script to verify user input functionality in the extension.
This script starts the WebSocket server and waits for extension connection.
"""

import asyncio
import logging
import sys
import signal
from browser_use_ext.extension_interface.service import ExtensionInterface

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestExtensionInterface:
    def __init__(self):
        self.interface = ExtensionInterface(host="localhost", port=8765)
        self.running = True
        
    async def start_test_server(self):
        """Start the WebSocket server and wait for messages."""
        logger.info("Starting test WebSocket server on port 8765...")
        
        try:
            await self.interface.start_server()
            logger.info("✅ WebSocket server started successfully!")
            logger.info("📱 Open your Chrome extension popup and submit a task to test the functionality")
            logger.info("🔄 Server will log any received messages...")
            
            # Keep the server running
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("💤 Received shutdown signal...")
        except Exception as e:
            logger.error(f"❌ Server error: {e}", exc_info=True)
        finally:
            logger.info("🔧 Cleaning up...")
            await self.interface.close()
            logger.info("✅ Server shutdown complete")

    def stop(self):
        """Stop the server gracefully."""
        self.running = False

async def main():
    """Main test function."""
    test_server = TestExtensionInterface()
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        test_server.stop()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    await test_server.start_test_server()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Test server terminated by user")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)