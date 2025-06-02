# Agent Integration for Browser Use Extension

This document describes the agent integration that connects user tasks from the Chrome extension to the AI-powered browser automation agent.

## Overview

The integration creates a complete automation loop:
1. User enters task in Chrome extension popup
2. Task is sent to Python WebSocket server  
3. Agent (powered by GPT-4 or Claude) processes the task
4. Agent analyzes current browser state
5. Agent generates and executes browser actions
6. Task completes automatically

## Setup

### 1. Install Dependencies

```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install langchain-openai langchain-anthropic python-dotenv
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```bash
# For OpenAI (GPT-4)
OPENAI_API_KEY=your-openai-api-key-here

# For Anthropic (Claude)  
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### 3. Load the Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `browser_use_ext/extension/` directory

### 4. Run the Server

```bash
# Simple demo script
python examples/extension_agent_demo.py

# Or run the test
python browser_use_ext/tests/integration/test_agent_integration.py
```

## Usage

1. Start the Python server (see above)
2. Open any website in Chrome
3. Click the extension icon in the toolbar
4. Verify status shows "Connected"
5. Enter a task, for example:
   - "Click the search button"
   - "Fill in the email field with test@example.com"
   - "Find information about Python"
   - "Navigate to the contact page"
6. Click "Execute Task"
7. Watch as the AI agent completes your task!

## How It Works

### Server Side (Python)

The `ExtensionInterface` class now includes:

```python
class ExtensionInterface:
    def __init__(self, host="localhost", port=8765, llm_model="gpt-4o", llm_temperature=0.0):
        # ... existing code ...
        self._llm = self._initialize_llm()  # Initialize GPT-4 or Claude
        self._active_agents = {}  # Track active agent sessions
    
    async def process_user_task(self, task: str, context: dict, tab_id: int):
        """Process user task through the agent"""
        agent = Agent(
            task=task,
            llm=self._llm,
            extension_interface=self,
            settings=AgentSettings(max_steps=15)
        )
        history = await agent.run()  # Execute the task
```

### Extension Side (JavaScript)

When user submits a task:

```javascript
// popup.js sends task to background.js
chrome.runtime.sendMessage({
    type: "SUBMIT_TASK",
    task: task,
    context: { url: tab.url, title: tab.title, tabId: tab.id }
});

// background.js forwards to Python server
websocket.send(JSON.stringify({
    type: "extension_event",
    data: {
        event_name: "user_task_submitted",
        task: task,
        context: context,
        tabId: tabId
    }
}));
```

### Agent Processing

1. Agent receives the task and current browser state
2. Uses LLM to understand the task and plan actions
3. Generates specific browser commands (click, type, scroll, etc.)
4. Executes actions through the extension
5. Monitors results and adjusts strategy
6. Continues until task is complete

## Configuration Options

### LLM Model Selection

In `ExtensionInterface.__init__()`:

```python
# For GPT-4 (default)
interface = ExtensionInterface(llm_model="gpt-4o")

# For GPT-3.5 (faster, less capable)
interface = ExtensionInterface(llm_model="gpt-3.5-turbo")

# For Claude
interface = ExtensionInterface(llm_model="claude-3-opus-20240229")
```

### Agent Settings

Customize agent behavior:

```python
settings = AgentSettings(
    max_steps=15,          # Maximum actions to take
    stop_on_error=False,   # Continue on minor errors
    display_progress=True   # Show progress in logs
)
```

## Troubleshooting

### "No LLM configured" Error
- Ensure `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` is set in `.env`
- Check the key is valid and has credits

### Extension Shows "Disconnected"
- Ensure Python server is running (`python examples/extension_agent_demo.py`)
- Check WebSocket port 8765 is not in use
- Refresh the extension or reload the page

### Agent Not Executing Actions
- Check browser console for errors
- Ensure content script is loaded (refresh page after loading extension)
- Verify the website allows extensions (some sites block them)

### Task Fails or Times Out
- Try simpler tasks first (e.g., "Click the first link")
- Ensure the target elements are visible on the page
- Check agent logs for specific errors

## Examples

### Simple Click Task
```
Task: "Click the login button"
Result: Agent finds and clicks the login button
```

### Form Filling
```
Task: "Fill in the contact form with name John Doe and email john@example.com"
Result: Agent locates form fields and enters the information
```

### Navigation
```
Task: "Go to the about page and find the company address"
Result: Agent navigates to about page and extracts address information
```

### Multi-Step Task
```
Task: "Search for Python tutorials and open the first result"
Result: Agent performs search, waits for results, clicks first link
```

## Development

### Adding Custom Actions

Extend the agent's capabilities in `browser_use_ext/agent/service.py`.

### Improving Task Understanding

Modify the system prompt in `browser_use_ext/agent/system_prompt.md`.

### Debugging

Enable debug logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

View agent decision making:
```python
settings = AgentSettings(display_progress=True)
```

## Security Notes

- The agent can only interact with pages where the extension is active
- Actions are limited to what the extension can do (no system access)
- API keys should be kept secure and not committed to version control
- The agent respects same-origin policies and browser security

## Future Enhancements

- [ ] Send task progress updates to extension popup
- [ ] Support for multiple concurrent tasks
- [ ] Task history and replay functionality
- [ ] Custom task templates and shortcuts
- [ ] Integration with more LLM providers
- [ ] Visual feedback in extension for running tasks