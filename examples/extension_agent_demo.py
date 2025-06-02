#!/usr/bin/env python3
"""
Demo script showing the complete browser automation flow with Chrome extension.

Prerequisites:
1. Install dependencies: pip install -r requirements.txt
2. Set environment variable: export OPENAI_API_KEY="your-key-here"
3. Load the Chrome extension from browser_use_ext/extension/
4. Navigate to a website (e.g., https://example.com)
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from browser_use_ext.extension_interface.service import ExtensionInterface
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Reduce noise from some loggers
logging.getLogger('websockets').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


async def main():
    """Run the extension agent demo."""
    print("\n🤖 Browser Automation Extension Demo")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ ERROR: OPENAI_API_KEY not found!")
        print("Please set it in your .env file or export it:")
        print("  export OPENAI_API_KEY='your-key-here'")
        return
    
    print("\n✅ Prerequisites:")
    print("  - OpenAI API key found")
    print("  - Starting WebSocket server...")
    
    # Create extension interface with agent support
    interface = ExtensionInterface(
        host="localhost",
        port=8765,
        llm_model="gpt-4o",
        llm_temperature=0.0
    )
    
    try:
        # Start the server
        await interface.start_server()
        
        print("\n🚀 Server started on ws://localhost:8765")
        print("\n📋 Instructions:")
        print("  1. Open Chrome and load the extension from 'browser_use_ext/extension/'")
        print("  2. Navigate to any website (e.g., https://example.com)")
        print("  3. Click the extension icon in toolbar")
        print("  4. Check that status shows 'Connected'")
        print("  5. Enter a task like:")
        print("     - 'Click the More information link'")
        print("     - 'Search for Python tutorials'") 
        print("     - 'Fill in the email field with test@example.com'")
        print("  6. Click 'Execute Task'")
        print("\n👀 Watch the browser as the AI agent completes your task!")
        print("\n Press Ctrl+C to stop the server")
        
        # Keep running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down server...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        await interface.close()
        print("✅ Server stopped. Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Exiting...")