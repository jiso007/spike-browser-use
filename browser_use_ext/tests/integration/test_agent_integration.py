"""
Test script for agent integration with extension interface.
This demonstrates the complete flow from user task submission to agent execution.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from browser_use_ext.extension_interface.service import ExtensionInterface
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def test_agent_integration():
    """Test the agent integration with a simple task."""
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: No LLM API keys found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file")
        return
    
    print("Starting agent integration test...")
    print("Please ensure:")
    print("1. Chrome browser is open")
    print("2. Extension is loaded from browser_use_ext/extension")
    print("3. You're on a test page (e.g., example.com)")
    print()
    
    # Create extension interface
    interface = ExtensionInterface(
        host="localhost",
        port=8765,
        llm_model="gpt-4o",  # or "claude-3-opus-20240229" for Anthropic
        llm_temperature=0.0
    )
    
    try:
        # Start the WebSocket server
        print("Starting WebSocket server on ws://localhost:8765...")
        await interface.start_server()
        
        print("WebSocket server started. Please:")
        print("1. Open the extension popup")
        print("2. Verify it shows 'Connected'")
        print("3. Enter a task like 'Click the More information link' or 'Type hello in the search box'")
        print("4. Click 'Execute Task'")
        print()
        print("The agent will process your task automatically...")
        print("Press Ctrl+C to stop the server")
        
        # Keep the server running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await interface.close()
        print("Server closed.")


async def test_programmatic_task():
    """Test submitting a task programmatically (simulating what the extension does)."""
    interface = ExtensionInterface()
    
    try:
        await interface.start_server()
        
        print("Waiting for extension to connect...")
        # Wait a bit for extension to connect
        await asyncio.sleep(3)
        
        if interface.has_active_connection:
            print("Extension connected! Simulating task submission...")
            
            # Simulate what happens when user submits a task
            # This would normally come from the extension popup
            await interface.process_user_task(
                task="Click on the 'More information' link",
                context={
                    "url": "https://example.com",
                    "title": "Example Domain"
                },
                tab_id=1  # This would be the actual tab ID from extension
            )
            
            # Let the agent work
            await asyncio.sleep(10)
        else:
            print("No extension connected. Please load the extension and refresh the page.")
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await interface.close()


if __name__ == "__main__":
    print("Agent Integration Test")
    print("=" * 50)
    
    # Run the interactive test
    asyncio.run(test_agent_integration())
    
    # Uncomment to test programmatic submission
    # asyncio.run(test_programmatic_task())