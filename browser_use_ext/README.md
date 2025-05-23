# browser-use-ext: Python Backend for Chrome Extension Browser Automation

This project implements a Python backend designed to replace Playwright for browser automation tasks. It works in conjunction with a custom Chrome Extension (not included in this Python-only part of the repository, but located in `extension/` if part of the same overarching project structure).

The Python backend provides:
- A WebSocket server (`ExtensionInterface`) to communicate with the Chrome extension.
- Pydantic models for structured data exchange (DOM elements, browser state, actions).
- A `Browser` and `BrowserContext` layer to manage interactions, mimicking some Playwright concepts but powered by the extension.
- A `Controller` to dispatch actions to the browser via the extension.
- An `Agent` scaffolding (though not fully implemented in this phase) for more complex automation logic.

## Project Structure (`browser-use-ext` directory)

```
browser-use-ext/
├── agent/                  # Components for higher-level agent logic
│   ├── memory/
│   ├── message_manager/
│   ├── __init__.py
│   ├── prompts.py
│   └── views.py
├── browser/                # Core browser interaction logic (mimicking Playwright)
│   ├── __init__.py
│   ├── browser.py
│   ├── context.py
│   └── views.py
├── controller/             # Service for dispatching actions
│   ├── registry/
│   │   ├── __init__.py
│   │   └── views.py
│   ├── __init__.py
│   └── service.py
├── dom/                    # DOM element representations
│   ├── __init__.py
│   └── views.py
├── extension_interface/    # WebSocket server for extension communication
│   ├── __init__.py
│   └── service.py
├── tests/                  # Pytest unit tests for the Python backend
│   ├── __init__.py
│   ├── test_agent_memory.py
│   ├── test_agent_prompts.py
│   ├── test_browser.py
│   ├── test_browser_context.py
│   ├── test_controller_service.py
│   ├── test_extension_interface.py
│   └── test_message_manager.py
├── __init__.py             # Makes browser-use-ext a package (if needed for parent imports)
└── requirements.txt        # Python dependencies

# Note: The Chrome Extension itself (manifest.json, background.js, content.js)
# would typically reside in a separate `extension/` directory, ideally at the same
# level as the `browser-use-ext/` directory if they are part of one larger project.
```

## Setup and Installation

1.  **Clone the repository** (if applicable, or ensure you have the `browser-use-ext` directory).

2.  **Navigate to the project directory**:
    ```bash
    cd path/to/your/project/browser-use-ext
    ```

3.  **Create a Python virtual environment** (recommended):
    ```bash
    python -m venv .venv
    ```
    (Note: `python3` might be needed instead of `python` depending on your system setup.)

4.  **Activate the virtual environment**:
    -   On Windows (PowerShell/CMD):
        ```powershell
        .\.venv\Scripts\Activate.ps1 
        ```
        or
        ```cmd
        .venv\Scripts\activate.bat
        ```
    -   On macOS/Linux (bash/zsh):
        ```bash
        source .venv/bin/activate
        ```

5.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running Tests

The project uses `pytest` for unit testing. The necessary `pytest.ini` is located in the parent directory (one level above `browser-use-ext/`) to ensure correct path resolution for imports.

1.  **Ensure your virtual environment is activated** and dependencies are installed.

2.  **Navigate to the workspace root** (the directory containing `pytest.ini` and the `browser-use-ext` folder).
    For example, if your structure is `.../05_Browser_Use/browser-use-ext/` and `.../05_Browser_Use/pytest.ini`, you should be in `.../05_Browser_Use/`.
    ```bash
    cd /path/to/your/workspace_root 
    ```

3.  **Run pytest**:
    ```bash
    pytest
    ```
    Pytest will automatically discover and run tests from the `browser-use-ext/tests` directory based on the `pytest.ini` configuration.

    You should see output indicating the number of tests passed, failed, or skipped.

## Starting the Python WebSocket Server (Standalone)

To run the Python WebSocket server so the Chrome extension can connect to it:

1.  **Ensure your virtual environment is activated** and dependencies are installed.

2.  **Navigate to the workspace root** (the directory that *contains* the `browser-use-ext` package, e.g., `path/to/your/project/browser-use`).

3.  **Run the following command**:
    ```bash
    python -m browser_use_ext.extension_interface.service
    ```
    This will start the WebSocket server, typically listening on `ws://localhost:8765` (or `ws://127.0.0.1:8765`). The console will show log messages, including the listening address.

    **Note on Automatic State Logging:** Once the server is running and the corresponding Chrome Extension (see below) is loaded and connected, this system will automatically log the browser's state upon each full page load. See the "Automatic Browser State Logging on Page Load" section for more details.

## Chrome Extension Interaction

-   The Python backend (`ExtensionInterface` in `browser_use_ext/extension_interface/service.py`) starts a WebSocket server (default: `ws://localhost:8765`).
-   The accompanying Chrome Extension (assumed to be in `../extension/` relative to `browser-use-ext/` or a similar known location) is responsible for connecting to this WebSocket server.
-   Once connected, the extension can receive commands from the Python backend (e.g., to get browser state, click elements, input text) and send back responses or state information.
-   The tests for `ExtensionInterface` in `tests/test_extension_interface.py` mock a client connection but also attempt to start a real WebSocket server on a test port (8766) for some of its tests.

### Automatic Browser State Logging on Page Load

A key feature of this system when the Python server and the Chrome extension are running together is the automatic logging of the browser's state every time a page fully loads.

**Interaction Flow:**

1.  When a webpage loads, the extension's content script (`content.js`) initializes and sends a `content_script_ready` message to its background script (`background.js`).
2.  The background script also detects when the page is fully loaded (`tab.status === 'complete'`) and sends a `page_fully_loaded_and_ready` event to the Python WebSocket server.
3.  Upon receiving this event, the Python server requests the full browser state (`get_state`) from the extension's background script.
4.  The background script, before forwarding this request to the content script, verifies that the content script for the target tab has signaled its readiness (from step 1). It will wait for a brief timeout for this signal if it hasn't received it yet.
5.  If the content script is ready, the background script relays the `get_state` request to it.
6.  The content script collects detailed page information (DOM structure, URL, title, scroll positions, etc.) and sends it back up the chain to the Python server.

**Output Details:**

-   **Content:** The complete `BrowserState` (including the DOM tree, current URL, page title, list of all open tabs, etc.) is captured.
-   **Format:** The state is saved as a JSON file.
-   **Location:** These JSON files are automatically saved into a directory named `browser_states_json_logs/`. This directory will be created at your **workspace root** (i.e., the directory from which you launched the `python -m browser_use_ext.extension_interface.service` command, typically the parent of `browser-use-ext/`).
-   **Filename Convention:** Files are named dynamically to ensure uniqueness and provide context, following a pattern like: `browser_state_tab<TAB_ID>_<SANITIZED_URL>_<TIMESTAMP>.json`.
    For example: `browser_state_tab123_google_com_search_q_example_20231105_153000_123.json`.

**Purpose of State Logs:**

These detailed JSON logs are invaluable for:
*   Debugging issues related to browser interaction and control flow between Python and the extension.
*   Understanding the precise structure and content of the data being extracted from web pages.
*   Developing and testing new browser automation features and Pydantic models.
*   Analyzing how different web pages are structured and perceived by the system.

## Further Development

-   Implement the Chrome Extension (`