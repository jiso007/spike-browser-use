#!/usr/bin/env python3
"""
Demo script showing user input functionality with Chrome extension.

This demonstrates:
1. Starting the WebSocket server
2. Waiting for Chrome extension connection
3. Receiving user tasks from the popup
4. Processing tasks with the agent system
"""

import asyncio
import logging
from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.browser.context import BrowserContext, BrowserContextConfig
from browser_use_ext.controller.service import Controller

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UserInputDemo:
    def __init__(self):
        self.interface = ExtensionInterface(host="localhost", port=8765)
        self.browser_context = None
        self.controller = None
        self.running = True
        
    async def setup(self):
        """Initialize the browser context and controller."""
        config = BrowserContextConfig()
        self.browser_context = BrowserContext(
            config=config,
            extension_interface=self.interface
        )
        self.controller = Controller(browser_context=self.browser_context)
        
    async def handle_user_task(self, task: str, context: dict):
        """Process a user task received from the extension popup."""
        logger.info(f"🎯 Processing user task: '{task}'")
        logger.info(f"📍 Context: {context}")
        
        # Simple task parsing and execution
        task_lower = task.lower()
        
        try:
            if "go to" in task_lower or "navigate to" in task_lower:
                # Extract URL from task
                if "google" in task_lower:
                    url = "https://www.google.com"
                elif "amazon" in task_lower:
                    url = "https://www.amazon.com"
                elif "github" in task_lower:
                    url = "https://www.github.com"
                else:
                    # Try to extract URL pattern
                    words = task.split()
                    for word in words:
                        if word.startswith("http"):
                            url = word
                            break
                    else:
                        url = "https://www.google.com/search?q=" + task.replace(" ", "+")
                
                logger.info(f"🌐 Navigating to: {url}")
                result = await self.controller.go_to_url(url)
                logger.info(f"✅ Navigation result: {result}")
                
            elif "search" in task_lower:
                # Handle search tasks
                search_query = task.replace("search for", "").replace("search", "").strip()
                
                # Navigate to Google if not already there
                current_state = await self.browser_context.get_state()
                if current_state and "google.com" not in current_state.url:
                    await self.controller.go_to_url("https://www.google.com")
                    await asyncio.sleep(2)  # Wait for page load
                
                # Find and click search box
                state = await self.browser_context.get_state()
                search_box = None
                for element in state.actionable_elements:
                    if element.attributes.get("name") == "q" or element.attributes.get("title") == "Search":
                        search_box = element
                        break
                
                if search_box:
                    await self.controller.click_element_by_index(search_box.highlight_index)
                    await self.controller.input_text(search_box.highlight_index, search_query)
                    # Press Enter to search
                    await self.controller.send_keys("Return")
                    logger.info(f"✅ Searched for: {search_query}")
                else:
                    logger.warning("❌ Could not find search box")
                    
            elif "click" in task_lower:
                # Handle click tasks
                state = await self.browser_context.get_state()
                logger.info(f"📋 Found {len(state.actionable_elements)} clickable elements")
                
                # Simple heuristic: click the first link or button mentioned
                for element in state.actionable_elements:
                    element_text = (element.text or "").lower()
                    if any(word in task_lower for word in element_text.split()):
                        await self.controller.click_element_by_index(element.highlight_index)
                        logger.info(f"✅ Clicked element: {element.text}")
                        break
                else:
                    logger.warning("❌ Could not find element to click")
                    
            else:
                logger.info(f"ℹ️ Task not understood, would normally use LLM here: {task}")
                
        except Exception as e:
            logger.error(f"❌ Error processing task: {e}", exc_info=True)
    
    async def monitor_tasks(self):
        """Monitor for incoming user tasks."""
        logger.info("👀 Monitoring for user tasks...")
        
        # In a real implementation, this would be event-driven
        # For now, we'll just log when tasks are received
        while self.running:
            await asyncio.sleep(1)
            
            # Check if we have an active tab
            if self.interface._active_tab_id:
                # In production, this would be triggered by actual events
                pass
    
    async def run(self):
        """Run the demo."""
        logger.info("🚀 Starting User Input Demo")
        logger.info("=" * 50)
        
        try:
            # Start WebSocket server
            logger.info("📡 Starting WebSocket server on port 8765...")
            await self.interface.start_server()
            
            # Wait for extension connection
            logger.info("⏳ Waiting for Chrome extension to connect...")
            logger.info("👉 Please load the extension in Chrome and open the popup")
            
            timeout = 30  # seconds
            start_time = asyncio.get_event_loop().time()
            
            while not self.interface.has_active_connection:
                if asyncio.get_event_loop().time() - start_time > timeout:
                    logger.error("❌ Timeout waiting for extension connection")
                    return
                await asyncio.sleep(0.5)
            
            logger.info("✅ Extension connected!")
            
            # Setup browser context
            await self.setup()
            
            # Instructions
            logger.info("\n" + "=" * 50)
            logger.info("📝 INSTRUCTIONS:")
            logger.info("1. Click the extension icon in Chrome")
            logger.info("2. Enter a task in the popup, such as:")
            logger.info("   - 'Go to Google'")
            logger.info("   - 'Search for Python tutorials'")
            logger.info("   - 'Navigate to GitHub'")
            logger.info("3. Click 'Execute Task'")
            logger.info("4. Watch the browser and this console")
            logger.info("=" * 50 + "\n")
            
            # Monitor for tasks
            await self.monitor_tasks()
            
        except KeyboardInterrupt:
            logger.info("\n🛑 Demo interrupted by user")
        except Exception as e:
            logger.error(f"❌ Demo error: {e}", exc_info=True)
        finally:
            logger.info("🧹 Cleaning up...")
            await self.interface.close()
            logger.info("✅ Demo complete")


async def main():
    """Main entry point."""
    demo = UserInputDemo()
    
    # Monkey patch to intercept task events
    original_process_message = demo.interface._process_message
    
    async def process_message_with_handler(client_id, message_json):
        # Call original handler
        await original_process_message(client_id, message_json)
        
        # Check if it was a user task
        try:
            import json
            message = json.loads(message_json)
            if (message.get("type") == "extension_event" and 
                message.get("data", {}).get("event_name") == "user_task_submitted"):
                
                task = message["data"].get("task")
                context = message["data"].get("context", {})
                
                # Handle the task
                await demo.handle_user_task(task, context)
                
        except Exception as e:
            logger.error(f"Error in task handler: {e}")
    
    demo.interface._process_message = process_message_with_handler
    
    # Run the demo
    await demo.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Demo terminated by user")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)