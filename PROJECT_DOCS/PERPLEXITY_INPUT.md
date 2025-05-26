## Project Goal

The primary goal for the `/browser_use_ext` project, as outlined in `PROJECT_DOCS/CURRENT_PROJECT_TASK.md`, is to implement the core `Agent` service. This involves creating or enhancing an `Agent` class (e.g., in `browser_use_ext/agent/agent_core.py`).

This `Agent` class will be responsible for:
1.  Receiving a user task and its context.
2.  Fetching the current browser state via `ExtensionInterface.get_state()`. This state will utilize the new format with `actionable_elements` identified by stable, string-based `id`s.
3.  Formatting the task and browser state into an LLM-ready prompt, potentially using helpers from `browser_use_ext/agent/prompts.py`.
4.  Making a (initially mockable) call to an LLM.
5.  Parsing the LLM's response to extract a structured action command (e.g., `{"action": "click", "params": {"element_id": "some-stable-id"}}`), ensuring compatibility with the refactored `content.js` and its use of string `element_id`s.
6.  Returning this structured action command.

It is understood that Perplexity AI will provide refined, best-practice adjustments and detailed implementation steps for this goal.

## Codebase Analysis

The task focuses on creating a new Python module, `agent_core.py` (or similar), within the `browser_use_ext/agent/` directory. This new module will house the main `Agent` class.

**Key Interactions and Dependencies:**

1.  **`Agent` and `ExtensionInterface`:**
    *   The `Agent` class will depend on `browser_use_ext/extension_interface/service.py` (specifically, the `ExtensionInterface` class and its `get_state()` method) to fetch the current browser state from the Chrome extension.
    *   The `get_state()` method in `ExtensionInterface` communicates with the Chrome extension (`background.js` and `content.js`) over WebSockets to retrieve this state. The state format, particularly `actionable_elements`, has recently been refactored in `content.js` to use stable string IDs, which the new `Agent` must correctly consume.

2.  **`Agent` and Prompting Logic:**
    *   The `Agent` will utilize `browser_use_ext/agent/prompts.py` to format the user task and the browser state into a coherent prompt for the LLM. This involves using Pydantic models like `SystemPrompt` and helper functions within `prompts.py`.

3.  **`Agent` and Action/View Structures:**
    *   The `Agent` will use or align with Pydantic models defined in `browser_use_ext/agent/views.py` (e.g., `AgentThought`, though this might need adjustment or new models for representing the extracted action command that is sent back to `ExtensionInterface` for dispatch). The key is that the action command structure must be compatible with what `content.js` now expects (i.e., action type and parameters including `element_id`).

4.  **Module Exposure:**
    *   The new `Agent` class will need to be exposed via `browser_use_ext/agent/__init__.py` to make it easily importable by other parts of the system, such as the `ExtensionInterface` service if it's responsible for instantiating or calling the agent upon receiving a user task.

**Implicit Dependencies/Considerations:**

*   **LLM Interaction:** While initially mocked, the design should account for future integration with an actual LLM client library (e.g., OpenAI, Anthropic). This includes API key management and structuring API calls.
*   **Error Handling:** The `Agent` will need robust error handling for scenarios like failed state retrieval, LLM API errors (once live), or inability to parse a valid action from the LLM response.
*   **State Transformation:** The `Agent` might need internal logic to transform or summarize the detailed `BrowserState` (received from `ExtensionInterface` and originating from `content.js`) into a more concise format suitable for the LLM prompt, while ensuring all critical information (like `actionable_elements`) is preserved.

## Tech Stack Context

*   **Backend:** Python (likely 3.9+ based on `asyncio` usage and type hinting style).
    *   **Core Libraries/Frameworks:**
        *   `asyncio` for asynchronous operations (evident in `ExtensionInterface`).
        *   `websockets` library for WebSocket communication between the backend and the Chrome extension.
        *   `Pydantic` for data validation and settings management (used extensively in `agent/views.py`, `agent/prompts.py`, `extension_interface/models.py`).
    *   **LLM Interaction (Planned):** Will involve an LLM client library (e.g., `openai`, `anthropic`).
*   **Chrome Extension:** JavaScript.
    *   `manifest.json` (Version 3).
    *   `background.js` (service worker) for WebSocket connection management and message routing.
    *   `content.js` for DOM interaction, state gathering, and action execution.
    *   `popup.html` and `popup.js` for user interface (though not directly part of this task, the agent's output will eventually drive what the user experiences).
*   **Development Environment:**
    *   Uses `requirements.txt` for Python dependencies.
    *   Logging is configured, likely using Python's built-in `logging` module.

## Affected Files

Based on the project goal, the following files are likely to be created or modified:

*   **To be Created/Significantly Enhanced:**
    *   `browser_use_ext/agent/agent_core.py` (New file to house the primary `Agent` class logic).
*   **To be Modified:**
    *   `browser_use_ext/agent/__init__.py` (To import and expose the new `Agent` class from `agent_core.py`).
    *   `browser_use_ext/agent/views.py` (Potentially to refine or add Pydantic models for action commands or agent thoughts, ensuring compatibility with `element_id` based actions).
*   **To be Utilized (but not necessarily modified for this specific task's core logic):**
    *   `browser_use_ext/extension_interface/service.py` (The `Agent` will call `ExtensionInterface.get_state()`).
    *   `browser_use_ext/extension_interface/models.py` (The `Agent` will consume `BrowserState` or similar models returned by `get_state()`).
    *   `browser_use_ext/agent/prompts.py` (For formatting LLM prompts).
    *   `browser_use_ext/extension/content.js` (The structure of actions generated by the `Agent` must align with what the refactored `content.js` expects, specifically string `element_id`s).

## Folder Structure
/
└── browser_use_ext/
    ├── README.md
    ├── __init__.py
    ├── __pycache__/
    │   ├── __init__.cpython-311.pyc
    │   └── logging_config.cpython-311.pyc
    ├── agent/
    │   ├── __init__.py
    │   ├── __pycache__/
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── prompts.cpython-311.pyc
    │   │   └── views.cpython-311.pyc
    │   ├── message_manager/
    │   ├── memory/
    │   ├── prompts.py
    │   └── views.py
    ├── browser/
    │   ├── __init__.py
    │   ├── __pycache__/
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── browser.cpython-311.pyc
    │   │   ├── context.cpython-311.pyc
    │   │   └── views.cpython-311.pyc
    │   ├── browser.py
    │   ├── context.py
    │   └── views.py
    ├── controller/
    ├── dom/
    ├── extension/
    │   ├── background.js
    │   ├── content.js
    │   ├── images/
    │   │   ├── icon128.png
    │   │   ├── icon16.png
    │   │   └── icon48.png
    │   ├── manifest.json
    │   ├── popup.html
    │   └── popup.js
    ├── extension_interface/
    │   ├── __init__.py
    │   ├── __pycache__/
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── models.cpython-311.pyc
    │   │   └── service.cpython-311.pyc
    │   ├── models.py
    │   └── service.py
    ├── requirements.txt
    └── tests/
        ├── __init__.py
        ├── __pycache__/
        │   └── __init__.cpython-311.pyc
        ├── conftest.py
        ├── javascript/
        ├── python/
        ├── test_action_execution.js
        ├── test_actionable_elements.js
        ├── test_agent_prompts.py
        └── test_extension_interface.py 