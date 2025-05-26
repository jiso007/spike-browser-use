# CURRENT_PROJECT_STATE.md

This document outlines the current state of the `/browser_use_ext` project, comparing it against the goals defined in `CURRENT_PROJECT_GOAL.md`. It identifies action items required for full integration and functionality.

## Overall Project Status Summary

*   **Overall Completeness:** The project is in its early to mid-stages of development. Foundational components for backend-extension communication (WebSocket server, basic message handling in `ExtensionInterface`, `background.js`) are present. **The core `Agent` class (`browser_use_ext/agent/agent_core.py`) has been implemented, providing the foundational logic for task processing, including state fetching, prompt formatting, (mocked) LLM interaction, and action command parsing. This significantly advances the agent's intelligence capabilities.** Critical data/interface alignment between the agent and the extension, specifically regarding state representation and element identification in `content.js`, has also been significantly advanced. However, a functional user task input mechanism in the extension UI and the full iterative decision loop for the agent are still pending.
*   **Major Roadblocks / Critical Gaps:**
    1.  **Agent Core Logic Implementation:** **This gap has been significantly reduced.** The central `Agent` class (`browser_use_ext/agent/agent_core.py`) now exists and implements key functionalities:
        *   Fetching browser state via `ExtensionInterface.get_state()` (consuming the new `actionable_elements` format).
        *   Formatting prompts using `SystemPrompt` from `browser_use_ext/agent/prompts.py`.
        *   Making (currently mocked) LLM calls.
        *   Parsing LLM responses into a structured `ActionCommand` (Pydantic model in `agent_core.py`), which is designed to be compatible with the `content.js` string-based `element_id` system.
        *   **Remaining:** The full iterative task execution loop (Phase 6) and integration with a real LLM are still needed.
    2.  **State Representation & Element ID Strategy Alignment:** This was a major roadblock. **The refactoring of `content.js` as per `PROJECT_DOCS/PERPLEXITY_OUTPUT.md` has largely addressed this gap.** `content.js` now generates an `actionable_elements` list with stable string IDs and can execute actions based on these string IDs. **The backend `Agent` in `agent_core.py` is now implemented to consume this new state format (`BrowserState` from `browser_use_ext/browser/views.py`) and is designed to produce `ActionCommand`s compatible with this `element_id` system.**
    3.  **User Task Input Pathway:** The Chrome extension's `popup.html` is currently a placeholder and lacks functionality for users to input tasks. The complete pathway from user task submission in the extension UI, through `popup.js` and `background.js`, to the backend as a `"user_task_submission"` message is not yet built (blocking Phase 2).
    4.  **Action Result State Update:** The action result sent from the extension back to the agent currently does not include the updated browser state after an action is performed. `PROJECT_DOCS/PERPLEXITY_OUTPUT.md` refactored state *generation* but did not explicitly add the new state to the *action result response*. This is crucial for the agent's iterative loop (Phase 5).
*   **Top 3-4 Critical Next Steps (to achieve core functionality):**
    1.  **Implement Core Agent Service (Phase 3, Action Items 1 & 2; leads into Phase 6):**
        *   **The `Agent` class has been developed in `browser_use_ext/agent/agent_core.py`.**
        *   **It implements the main `process_task` method to: fetch state (via `ExtensionInterface`, receiving the new `actionable_elements` format from `BrowserState`), format prompts (using `agent/prompts.py`), make (initially mock) LLM calls, and parse the LLM response to get an `ActionCommand` (using the new Pydantic model in `agent_core.py` expecting actions with string `element_id`).**
        *   **Next:** Implement the integration for dispatching this action command via `ExtensionInterface` to the extension (Phase 3, Action Item 2).
        *   **Next:** Implement the basic iterative loop for the agent (Phase 6, Action Item 1) and integrate a real LLM.
    2.  **Align Content Script State & Actioning with Goals (Phase 4, Action Items 1 & 2):**
        *   **This has been significantly progressed by the `content.js` refactoring based on `PROJECT_DOCS/PERPLEXITY_OUTPUT.md`.** `content.js` now generates `actionable_elements` with stable string `id`s and handles actions using these `element_id`s.
        *   Remaining work includes ensuring `background.js` correctly forwards the new action formats and verifying end-to-end communication with the updated `content.js`.
    3.  **Build User Task Input & Forwarding (Phase 2, Action Items 1, 2, & 3):**
        *   Develop the `popup.html` UI with a task input field and submit button.
        *   Implement `popup.js` to send task and context to `background.js`.
        *   Implement `background.js` to forward this as a `"user_task_submission"` to `ExtensionInterface`.
        *   Implement the handler in `ExtensionInterface` to receive this message and pass it to the (newly developed) `Agent` service.
    4.  **Ensure Action Results Include Updated State (Phase 5, Action Items 1 & 2):**
        *   Modify `content.js` (`handleExecuteAction`) to re-gather and include the new browser state (using the aligned format from step 2 above) in the result it sends back after an action.
        *   Ensure `background.js` forwards this complete result (including new state) to the backend.

Addressing these areas will unblock the main functional flow of the application from user input to agent-driven browser interaction and iteration.

### Phase 1: Initialization & Setup

*   **Goal for this Phase (from `PROJECT_DOCS/CURRENT_PROJECT_GOAL.md`):** The main application/backend initializes, primarily setting up the intelligent agent (LLM interface) and a communication channel (e.g., WebSocket server) to listen for connections from the Chrome extension. The Chrome extension, upon browser startup or being enabled, establishes a connection with the main application/backend. It registers itself and signals its readiness to receive commands and send browser state updates. No direct browser instance is launched by the backend.
*   **Current State Analysis:**
    *   **What is currently happening (that misses the goal):**
        *   The `content.js` script (`browser_use_ext/extension/content.js`) is missing the explicit `chrome.runtime.sendMessage({ type: "content_script_ready" })` call to `background.js`. This call is a critical part of the two-way "Ready" handshake mechanism (detailed in the `chrome_extension_content_readiness` rule) to ensure `background.js` doesn't message `content.js` prematurely.
    *   **What is currently happening (that moves towards/accomplishes the goal):**
        *   **Backend (`browser_use_ext/extension_interface/service.py`):**
            *   A WebSocket server is implemented within the `ExtensionInterface` class (`start_server` method).
            *   New client connections are handled (`_handle_connection`), assigning a unique `client_id` and storing `ConnectionInfo` (including the WebSocket connection object and a handler task).
            *   The backend is prepared to receive a `"content_script_ready_ack"` event from `background.js` (logged in `_process_message`), indicating its awareness of the readiness handshake.
            *   It also processes a `page_fully_loaded_and_ready` event sent by the extension.
        *   **Chrome Extension (`browser_use_ext/extension/background.js`):**
            *   Successfully establishes a WebSocket connection to the backend (`ws://localhost:8765`) via `connectWebSocket()`, with reconnection logic.
            *   Implements the client-side of the content script readiness check: maintains a `contentScriptsReady` Set and uses an `async function waitForContentScriptReady(tabId, timeoutMs)` before attempting to send messages to `content.js` (e.g., for `get_state` requests). This aligns with the `chrome_extension_content_readiness` rule.
            *   Sends a `page_fully_loaded_and_ready` event to the backend when tabs are updated or activated, providing initial context.
    *   **What needs to happen (that will move towards/accomplish the goal):**
        1.  **Implement `content_script_ready` Ping in `content.js`:**
            *   **Affected Components:** `browser_use_ext/extension/content.js`.
            *   **Details:** Add the `chrome.runtime.sendMessage({ type: "content_script_ready" }, response => { ... });` call. This should be placed after its `chrome.runtime.onMessage.addListener` is set up and any other critical initializations in `content.js` are complete.
            *   **Data Structures/Interfaces:**
                *   Message sent from `content.js` to `background.js`: `{ type: "content_script_ready" }`.
                *   Response received by `content.js` from `background.js` (optional to log, but good for debugging): `{ status: "acknowledged_content_script_ready", tabId: number }`.
            *   **Define "Done":**
                *   `content.js` successfully sends the `content_script_ready` message upon its initialization for a given tab.
                *   `background.js` receives this message, adds the `sender.tab.id` to its `contentScriptsReady` Set, and sends an acknowledgment back to `content.js`.
                *   Subsequent calls to `waitForContentScriptReady(tabId)` in `background.js` for that tab resolve successfully (return `true`) without timing out.
            *   **Prioritize:** High - This is fundamental for reliable messaging between `background.js` and `content.js` and is a core requirement of the `chrome_extension_content_readiness` rule.
            *   **Relevant Rules/Guidelines:** `chrome_extension_content_readiness`.

### Phase 2: Task Reception

*   **Goal for this Phase (from `PROJECT_DOCS/CURRENT_PROJECT_GOAL.md`):** The user inputs a high-level task or goal directly into a UI element within the Chrome extension. The Chrome extension sends this user-provided task, potentially bundled with relevant contextual information from the active tab, to the main application/backend. The main application/backend receives the task and routes it to the intelligent agent.
*   **Current State Analysis:**
    *   **What is currently happening (that misses the goal):**
        *   **Extension UI for Task Input:** The current `browser_use_ext/extension/popup.html` is a basic status display and lacks any input fields (e.g., textarea, input button) for users to submit tasks. `browser_use_ext/extension/popup.js` only handles status updates and does not capture or forward user tasks.
        *   **Task Forwarding from Extension to Backend:** `browser_use_ext/extension/background.js` currently does not have specific logic to listen for a user task submitted from `popup.js`, bundle it with contextual information (URL, title), and send it to the backend with a distinct message type like `"user_task_submission"`.
        *   **Backend Task Reception & Routing:** The `ExtensionInterface` in `browser_use_ext/extension_interface/service.py` (`_process_message` method) only handles message types `"response"` and `"extension_event"`. It lacks a dedicated handler for `"user_task_submission"` messages and does not yet have a mechanism to route such tasks to an agent component.
        *   **Agent Integration Point:** While an `browser_use_ext/agent/` directory exists, its `__init__.py` is minimal. There isn't a clearly defined and exposed `Agent` class or service within this package that `ExtensionInterface` can readily use to pass on a user task.
    *   **What is currently happening (that moves towards/accomplishes the goal):**
        *   The fundamental WebSocket communication channel between the extension and the backend is established (as per Phase 1 progress).
        *   `background.js` includes a generic `sendDataToServer` function that could be adapted for sending user tasks.
        *   `ExtensionInterface._process_message` in `service.py` can be extended to recognize and handle new message types.
        *   The presence of the `browser_use_ext/agent/` directory and its submodules (`prompts.py`, `views.py`, `message_manager/`, `memory/`) indicates foundational work for agent capabilities.
    *   **What needs to happen (that will move towards/accomplish the goal):**
        1.  **Develop Extension Popup UI for Task Input:**
            *   **Affected Components:** `browser_use_ext/extension/popup.html`, `browser_use_ext/extension/popup.js`.
            *   **Details:**
                *   Enhance `popup.html` to include an input field (e.g., `<textarea id="taskInput">`) and a submit button (e.g., `<button id="submitTask">`).
                *   Update `popup.js` to add an event listener to the submit button. On click, it should retrieve the task string from the input field, gather basic context (current tab URL and title via `chrome.tabs.query({active: true, currentWindow: true}, ...)`), and then send a message to `background.js` containing this data.
            *   **Data Structures/Interfaces (popup.js to background.js):** Message: `{ type: "submit_user_task", task: "user_task_string", context: { url: "current_tab_url", title: "current_tab_title" } }`.
            *   **Define "Done":** A user can type a task into the extension popup, click submit, and `popup.js` successfully dispatches a message with the task and context to `background.js` (verifiable via `console.log` in `background.js`).
            *   **Prioritize:** High - Essential for enabling user interaction as per the project goals.
        2.  **Implement Task Forwarding in `background.js` to Backend:**
            *   **Affected Components:** `browser_use_ext/extension/background.js`.
            *   **Details:** Add a handler within `chrome.runtime.onMessage.addListener` for messages of `type: "submit_user_task"` (from `popup.js`). This handler should construct a new message payload according to the format specified in `CURRENT_PROJECT_GOAL.md` (Section 3: User Input Contextual Information, e.g., including `user_prompt`, `timestamp`, `context` with `url`, `page_title`, `active_tab_id`) and send it to the backend WebSocket server using the existing `sendDataToServer` function.
            *   **Data Structures/Interfaces (background.js to backend):** WebSocket Message (JSON): `{ type: "user_task_submission", user_prompt: "...", timestamp: "ISO_string_timestamp", context: { url: "...", page_title: "...", active_tab_id: tabId_number } }`.
            *   **Define "Done":** `background.js` successfully receives the task data from `popup.js`, formats it into the specified JSON structure, and sends it to the backend. The backend logs receipt of this message type.
            *   **Prioritize:** High - Critical link between user input in the extension and the backend processing.
        3.  **Implement Backend Reception & Agent Routing for User Tasks:**
            *   **Affected Components:** `browser_use_ext/extension_interface/service.py`; a new or existing agent controller/service module within `browser_use_ext/agent/` (e.g., a new `browser_use_ext/agent/service.py` or `browser_use_ext/agent/coordinator.py`).
            *   **Details:**
                *   In `ExtensionInterface._process_message` (in `service.py`), add a condition to handle messages where `base_msg.type == "user_task_submission"`.
                *   This new handler block should validate and parse the `user_prompt` and `context` from `base_msg.data` (potentially using a Pydantic model for `UserTaskSubmissionMessage`).
                *   An `Agent` class or a dedicated agent service function needs to be defined/exposed by the `browser_use_ext/agent/` package. `ExtensionInterface` should hold a reference to or be able to instantiate/call this agent component.
                *   The handler will then invoke a method on this agent component (e.g., `agent_instance.handle_incoming_task(prompt, context)`).
            *   **Data Structures/Interfaces:**
                *   Pydantic model (e.g., `UserTaskSubmissionData`) for the `data` field of the `"user_task_submission"` message.
                *   Clear interface for the agent's task intake method (e.g., `def handle_incoming_task(self, prompt: str, context: dict) -> None:`).
            *   **Define "Done":** The `ExtensionInterface` successfully receives a `"user_task_submission"` message, validates its payload, and calls the designated method on an `Agent` component, passing the user's prompt and the contextual information. The agent component logs that it has received the task for processing.
            *   **Prioritize:** High - Connects the user-initiated task to the backend agent logic.
        4.  **Define and Expose a Core Agent Service/Class:**
            *   **Affected Components:** `browser_use_ext/agent/__init__.py`; potentially a new `browser_use_ext/agent/agent_core.py` (or `service.py`) to house the main `Agent` class.
            *   **Details:** Design and implement a main `Agent` class (or a central callable function) within the `browser_use_ext/agent/` package. This class will be responsible for receiving tasks, and (in later phases) managing state, interacting with an LLM, and generating actions. Update `browser_use_ext/agent/__init__.py` to make this `Agent` class easily importable by `ExtensionInterface`.
            *   **Data Structures/Interfaces:** Initial definition of the `Agent` class structure, its constructor (if any dependencies like API keys are needed later), and its primary method for task intake (e.g., `handle_incoming_task`).
            *   **Define "Done":** The `Agent` class/service is defined, and `ExtensionInterface` can successfully import and instantiate it (or call its main function) to pass task data.
            *   **Prioritize:** Medium - This is a structural prerequisite for step 3 to function correctly. The full agent logic will be developed in subsequent phases.

### Phase 3: Action Generation (by the Agent/LLM)

*   **Goal for this Phase (from `PROJECT_DOCS/CURRENT_PROJECT_GOAL.md`):** The intelligent agent in the main application/backend receives the task (from the extension) and the latest "simplified state representation" of the relevant browser tab (also from the extension). The agent, guided by its system prompt and LLM, analyzes the task and current browser state to decide on the next appropriate action. It formulates this decision as an action command (e.g., a JSON object specifying action type and parameters) tailored for the Chrome extension's capabilities.
*   **Current State Analysis:**
    *   **What is currently happening (that misses the goal):**
        *   **Core Agent Logic Orchestration:** **This is now significantly addressed.** The `Agent` class in `browser_use_ext/agent/agent_core.py` provides the core orchestration. It:
            *   Actively fetches the current browser state using `ExtensionInterface.get_state()` when a task is processed. The state received is the `BrowserState` model (from `browser.views.py`) which includes the `actionable_elements` format.
            *   Formats this live browser state along with the user task into a complete prompt using `SystemPrompt` from `browser_use_ext/agent/prompts.py`.
            *   Makes a (currently mocked) call to an LLM via its `_call_llm` method.
            *   Parses the LLM's response to determine a specific action and its parameters, populating the `ActionCommand` Pydantic model (defined in `agent_core.py`). This `ActionCommand` is designed for string `element_id`s.
            *   **Remaining:** Integration with a real LLM service and the logic to initiate sending this formulated action command back to the Chrome extension via the `ExtensionInterface` (covered in Action Item 2 of this phase).
        *   The `tool_input` equivalent is handled by the `ActionCommand.params` field, which is structured for `element_id` where appropriate.
    *   **What is currently happening (that moves towards/accomplishes the goal):**
        *   **`Agent` Class Implementation:** **COMPLETE.** The `Agent` class is implemented in `browser_use_ext/agent/agent_core.py`. It includes:
            *   `__init__(self, extension_interface)`
            *   `async process_task(self, user_task: str, task_context: dict | None = None)`: Orchestrates state fetching, prompt formatting, LLM call (mocked), and response parsing.
            *   `_format_prompt(self, task: str, state: BrowserState)`: Uses `SystemPrompt` and `actionable_elements` from `BrowserState`.
            *   `async _call_llm(self, prompt: str)`: Currently mocked.
            *   `_parse_response(self, response_str: str)`: Parses JSON into `ActionCommand`, handles `ValidationError`, and raises `InvalidActionError`.
        *   **`ActionCommand` Model:** **COMPLETE.** Defined in `agent_core.py` with validation for `action` type and `params`.
        *   **Unit Tests for Parsing:** **COMPLETE.** Pytest unit tests for `_parse_response` are in `browser_use_ext/tests/python/test_agent_core.py`.
        *   **`agent/__init__.py` Exports:** **COMPLETE.** Updated to export `Agent`, `ActionCommand`, and `InvalidActionError`.
        *   **Browser State Acquisition Path:** The backend (`ExtensionInterface`) provides `get_state()`. The `Agent` class now calls this, and the `BrowserState` model from `browser.views.py` (which includes `actionable_elements`) is used.
        *   **Prompting Structures:** `browser_use_ext/agent/prompts.py` (with `SystemPrompt`) is used by `Agent._format_prompt`.
        *   **Action Representation Structures:** The `ActionCommand` model in `agent_core.py` serves this purpose.
        *   **Mechanism for Sending Actions to Extension:** The `ExtensionInterface._send_request()` method is suitable for sending commands. `background.js` is set up to receive `execute_action`. **This integration is the next step (Action Item 2).**
    *   **What needs to happen (that will move towards/accomplish the goal):**
        1.  **Implement Core Agent Service (`Agent` class for LLM Interaction and Decision Making):**
            *   **This action item is now LARGELY COMPLETE.** The `Agent` class is created in `browser_use_ext/agent/agent_core.py`. Its constructor accepts `ExtensionInterface`. The `process_task` method:
                *   Calls `await self.extension_interface.get_state(...)` and uses `BrowserState` (with `actionable_elements`).
                *   Uses `SystemPrompt.load("default").format(...)` via `_format_prompt`.
                *   Includes a mocked `_call_llm` method.
                *   Parses the LLM response into `ActionCommand` using `_parse_response`, designed for `element_id`.
            *   **Remaining Sub-tasks:**
                *   Integrate a real LLM client library (e.g., `openai`, `anthropic`), add to `requirements.txt`, and implement the actual API call in `_call_llm`. Handle API key management.
                *   Refine `_format_prompt` to ensure it optimally uses the `SystemPrompt` template variables with `state.actionable_elements` and other `BrowserState` fields.
            *   **Data Structures/Interfaces:**
                *   Inputs to `process_task`: `user_task: str`, `task_context: dict`.
                *   Internal data: `BrowserState` (from `browser_use_ext.browser.views`), LLM API request/response structures (once real LLM is integrated).
                *   Output of `process_task`: An `ActionCommand` instance or `None`.
            *   **Define "Done" (for remaining sub-tasks):** The `Agent` class can make a real call to an LLM service, and the prompt formatting is robust.
            *   **Prioritize:** High (for LLM integration).
            *   **Relevant Rules/Guidelines:** `pydantic_model_guidelines`. Environment variables for API keys.
        2.  **Integrate Agent's Action Command with `ExtensionInterface` for Dispatch:**
            *   **Affected Components:** `browser_use_ext/extension_interface/service.py` (specifically the logic handling `"user_task_submission"` developed in Phase 2), and the `Agent` class.
            *   **Details:** Modify the `ExtensionInterface` logic that handles `"user_task_submission"`. After this logic calls the agent's `process_task(user_prompt, context)` method and receives the `ActionCommand` object, it must then use its own `_send_request` method to dispatch this action to the Chrome extension. The call would be like: `response_from_action = await self._send_request(action="execute_action", data=action_command.model_dump())`. (Note: `action_command.model_dump()` to get a dict).
            *   **Data Structures/Interfaces:** The dictionary from `agent.process_task()` (now using `element_id`) is used as the `data` argument for `_send_request` where the `action` argument is `"execute_action"`.
            *   **Define "Done":** When `ExtensionInterface` processes a `"user_task_submission"`, it successfully calls the agent, gets back an action command dictionary (with `element_id`), and then sends a WebSocket message to the connected extension with `type: "execute_action"` and a `data` payload containing the agent's chosen action and parameters. The extension (`background.js`) should log receipt of this message.
            *   **Prioritize:** High - Completes the loop from agent decision to dispatching the command.

### Phase 4: Action Execution

*   **Goal for this Phase (from `PROJECT_DOCS/CURRENT_PROJECT_GOAL.md`):** The Chrome extension's `background.js` or `content.js` receives the action command from the main application/backend. `content.js`, injected into the target web page, executes the command using vanilla JavaScript DOM manipulation and browser APIs.
*   **Current State Analysis:**
    *   **What is currently happening (that misses the goal):**
        *   **Element Identification Mismatch for Actions:** `browser_use_ext/extension/content.js` (`handleExecuteAction` function) currently expects to identify elements for interaction (e.g., click, input) using a `params.highlight_index`. This index refers to an internal numeric key in its `selectorMap` (which maps the index to an XPath and a direct element reference). This contrasts with the strategy outlined in `CURRENT_PROJECT_GOAL.md`, which states the extension should report elements with a unique, stable string `id` (e.g., `"product-title-h1"`, `"add-to-cart-btn-001"`) in its state representation, and the agent should subsequently use this `element_id` in its action commands. Action names like `"click_element_by_index"` in `content.js` reflect this current index-based approach.
        *   **State Representation for Agent:** The structure of the state information generated by `content.js` (specifically how actionable elements are represented and identified with `highlight_index` and XPath in `pageState.selector_map`) does not align with the `actionable_elements: [{ id: string, type: string, ... }]` list format specified in `CURRENT_PROJECT_GOAL.md` (Section 1). This format is what the agent is expected to consume to make decisions and select elements by their string `id`.
    *   **What is currently happening (that moves towards/accomplishes the goal):**
        *   **`content.js` Refactoring Complete:** The implementation steps from `PROJECT_DOCS/PERPLEXITY_OUTPUT.md` have been applied. This means:
            *   `content.js` now has an enhanced element identification system (`generateStableElementId`, `detectActionableElements`).
            *   State generation (`handleGetState`) now produces an `actionable_elements` list with stable string IDs, including comprehensive metadata for each element (type, tag, text, attributes, visibility, available operations).
            *   Action execution (`handleExecuteAction`) has been modernized to use string-based `element_id`s for targeting, and action names have been generalized (e.g., `click` instead of `click_element_by_index`).
            *   Element resolution from string ID to DOM element (`resolveElementById`) is implemented.
            *   Robust error handling and fallback mechanisms for element resolution are in place within `content.js`.
        *   **Action Command Forwarding:** `browser_use_ext/extension/background.js` (`handleServerMessage` function) correctly receives `"execute_action"` messages from the backend. It extracts the `subActionName` (e.g., `"click_element_by_index"`) and `subActionParams` from the `data` payload and successfully forwards these to the `activeTabId`'s `content.js` using `chrome.tabs.sendMessage`. **This part needs to be updated to reflect the new action names and `element_id` parameter.**
        *   **`content.js` Action Handling Logic:** `browser_use_ext/extension/content.js` (`handleExecuteAction` function) contains a `switch` statement that routes to specific JavaScript functions for various `actionName`s it receives (e.g., `click_element_by_index`, `input_text`, `go_to_url`, `scroll_page`, `extract_content`). **This has been updated with generalized action names and `element_id` based logic.**
        *   **Basic DOM Interaction Implemented:** For the implemented actions, `content.js` uses vanilla JavaScript DOM manipulation methods (e.g., `element.click()`, `element.value = params.text`, `window.location.href = params.url`). **These have been updated to work with the new element resolution system.**
    *   **What needs to happen (that will move towards/accomplish the goal):**
        1.  **Align `content.js` State Generation with `CURRENT_PROJECT_GOAL.md` Specifications:**
            *   **This action item is now largely COMPLETE** due to the refactoring outlined in `PROJECT_DOCS/PERPLEXITY_OUTPUT.md`.
            *   **Affected Components:** `browser_use_ext/extension/content.js` (primarily the `detectActionableElements` function (formerly `buildDomTreeWithMappings`) and the `handleGetState` function).
            *   **Details:**
                *   The refactored `detectActionableElements` function now generates a list of `actionable_elements` adhering to the structure defined in `CURRENT_PROJECT_GOAL.md` (Section 1: State Representation).
                *   The `handleGetState` function in `content.js` has been updated to include this `actionable_elements` list in the `pageState` object it constructs (as per `PROJECT_DOCS/PERPLEXITY_OUTPUT.md` snippets for `handleGetState`).
            *   **Data Structures/Interfaces:** The `pageState.data` object sent from `content.js` to `background.js` now includes `actionable_elements: [{id: string, type: string, tag: string, text_content: string, attributes: object, is_visible: boolean, available_operations: string[]}, ...]`, as well as other state details like `url`, `title`, `viewport`, `scroll_position`, and `page_metrics`.
            *   **Define "Done":** COMPLETE. `content.js`, when handling a `get_state` request, generates and returns a state object that includes the `actionable_elements` list in the specified detailed format. Each element in this list has a unique string `id` that the extension can later use to re-identify the element.
            *   **Prioritize:** COMPLETE.
        2.  **Modify `content.js` Action Execution to Use `element_id` (String-Based Identifier):**
            *   **This action item is now largely COMPLETE** due to the refactoring outlined in `PROJECT_DOCS/PERPLEXITY_OUTPUT.md`.
            *   **Affected Components:** `browser_use_ext/extension/content.js` (specifically the `handleExecuteAction` function and its internal action handlers like `executeClick`, `executeInputText` etc.).
            *   **Details:**
                *   The `handleExecuteAction` function now expects `params.element_id` (a string) for all actions that target a specific DOM element.
                *   The logic within `handleExecuteAction` and its helper functions (`resolveElementById`, `executeClick`, etc.) now finds the target DOM element based on the received string `element_id`.
                *   Action types have been generalized (e.g., `"click"` instead of `"click_element_by_index"`).
            *   **Data Structures/Interfaces:** Action parameters received by `content.js` from `background.js` are now structured like `payload: { element_id: "some-unique-string-id", ...other_params }`.
            *   **Define "Done":** COMPLETE. `content.js` can successfully receive an action command (e.g., `actionName: "click"`) that includes a string `element_id` in its parameters, correctly find the corresponding DOM element using this `element_id`, and execute the intended interaction.
            *   **Prioritize:** COMPLETE.
        3.  **Update `background.js` Action Forwarding for Consistency (Minor Task):**
            *   **Affected Components:** `browser_use_ext/extension/background.js` (`handleServerMessage` function).
            *   **Details:** Ensure that the `subActionName` it forwards to `content.js` matches the new, generalized actions (e.g., `"click"` instead of `"click_element_by_index"`). The `subActionParams` payload it constructs must correctly include the `element_id` (string) as expected by the updated `content.js`. This is primarily about ensuring consistency with the changes made in `content.js` and the action commands generated by the agent.
            *   **Data Structures/Interfaces:** The message structure passed to `chrome.tabs.sendMessage(activeTabId, { type: subActionName, payload: subActionParams, ...})` must align with `content.js`'s updated expectations for `subActionName` and `subActionParams` (i.e., using `element_id` and generalized action names like `"click"`, `"input_text"`).
            *   **Define "Done":** `background.js` correctly forwards action commands with string `element_id`s and updated action names to `content.js` without issues. The agent needs to send these new action names.
            *   **Prioritize:** Medium - Dependent on the more significant changes in `content.js` and agent action generation. **This is a remaining task.**

### Phase 5: Result Processing & State Update

*   **Goal for this Phase (from `PROJECT_DOCS/CURRENT_PROJECT_GOAL.md`):** After executing an action, the Chrome extension's `content.js` observes the outcome. It then gathers the updated browser state. The extension sends an action result message back to the main application/backend. This message includes success/failure status, any extracted data, error information, and *potentially the new simplified state representation*. The backend updates its understanding of the browser state based on this message.
*   **Current State Analysis:**
    *   **What is currently happening (that misses the goal):**
        *   **Missing New State in Action Result Sent to Backend:** When `browser_use_ext/extension/background.js` forwards the result of an executed action from `content.js` to the backend server, the `data` payload of this message (`type: "response"`) includes `success` status, `error` information (if any), and action-specific data (e.g., `extracted_text` from `extract_content` action). However, it **critically omits the new/updated simplified state representation of the browser tab** (e.g., updated `actionable_elements`, URL, title) which is required by `CURRENT_PROJECT_GOAL.md` for the agent to make its next decision based on fresh information. The refactoring in `PROJECT_DOCS/PERPLEXITY_OUTPUT.md` updated `handleGetState` but did not integrate its call into the action response path of `handleExecuteAction`.
        *   The `ExtensionInterface._process_message` in `browser_use_ext/extension_interface/service.py` parses the incoming response into a `ResponseData` Pydantic model. While this `ResponseData` model (`browser_use_ext/extension_interface/models.py`) *is* designed with fields capable of holding browser state information (e.g., `url`, `title`, `actionable_elements` if it were added there, currently it has `tree`, `tabs`), it only materializes what `background.js` actually sends. Consequently, the agent (which would receive this `ResponseData` via an `asyncio.Future`) does not get the updated browser state directly with the action result.
    *   **What is currently happening (that moves towards/accomplishes the goal):**
        *   **Action Result Propagation Path Exists:**
            *   `content.js` (`handleExecuteAction` function, now refactored) correctly returns a structured response (`{ request_id, type: "response", status, data, error }`) to `background.js` upon completing an action.
            *   `background.js` (`handleServerMessage` function, specifically the block for `serverActionType === "execute_action"`) receives this response from `content.js`. It then forwards a message of `type: "response"` to the backend server, including the `success` status, `error` message (if any), and any specific `data` returned by `content.js`.
            *   The backend (`ExtensionInterface._process_message` in `service.py`) correctly receives this `"response"` message from the extension, correlates it to the original request using the message `id`, and resolves the corresponding `asyncio.Future` with the `ResponseData`.
        *   The `ResponseData` Pydantic model in `extension_interface/models.py` is flexible (`Config.extra = "allow"`) and already contains many state-related fields, making it capable of holding the new state if sent by the extension.
        *   **Details:** After an action is successfully performed within `handleExecuteAction` (and before constructing the return object), `content.js` must re-evaluate the current page state. This involves calling its state generation logic (i.e., the refactored `handleGetState` function from Phase 4 and `PROJECT_DOCS/PERPLEXITY_OUTPUT.md`, which produces the `actionable_elements` list and other relevant state fields like URL, title, scroll position, viewport dimensions). This newly gathered state object (the entire result of `handleGetState()`) should be included within the `resultData` object that `handleExecuteAction` returns to `background.js`.
        *   **Data Structures/Interfaces:** The `resultData` object in the response from `handleExecuteAction` should be augmented. For example: `resultData: { /* other action-specific data like extracted_text */ new_browser_state: { url: "...", title: "...", actionable_elements: [...], scroll_position: {...}, viewport: {...}, page_metrics: {...}, timestamp: "..." /* etc., i.e., the full state object from handleGetState() */ } }`.
        *   **Define "Done":** After `content.js` executes an action, the response object it sends to `background.js` includes a `new_browser_state` field. This field contains a comprehensive snapshot of the current page state, structured according to the agreed-upon format (the output of the refactored `handleGetState` function).
        *   **Prioritize:** High - This is essential for providing the agent with immediate feedback and fresh context after each action, enabling a reactive decision loop.
        2.  **Ensure `background.js` Forwards the New State in Action Result to Backend:**
            *   **Affected Components:** `browser_use_ext/extension/background.js` (the `handleServerMessage` function, specifically the `execute_action` response handling block).
            *   **Details:** When `background.js` receives the response from `content.js` (which now includes `new_browser_state` within `response.data`), it must ensure this entire `new_browser_state` object is correctly included in the `data` payload it sends to the backend server. The current forwarding logic `data: { success: response.status === "success", ..., ...(response.data || {})}` should capture this if `content.js` correctly nests `new_browser_state` inside `response.data`.
            *   **Data Structures/Interfaces:** The `data` field in the `sendDataToServer` call (when sending the action response to the backend) should look like: `data: { success: boolean, error: string|null, extracted_text: "...", /* other action data */ new_browser_state: { url: "...", ... } }`.
            *   **Define "Done":** The backend (`ExtensionInterface`) receives the action response message from `background.js`. When this message is parsed into a `ResponseData` object, the `ResponseData` instance now correctly contains the `new_browser_state` information sent from `content.js`.
            *   **Prioritize:** High - Ensures the complete action result, including fresh state, reaches the backend and the agent.
        3.  **Agent Utilizes Updated State from Action Result for Next Iteration:**
            *   **Affected Components:** The new `Agent` class/service (developed in Phase 3).
            *   **Details:** When the agent's call to `await self.extension_interface._send_request(action="execute_action", data=agent_action_command_dict)` returns, the resolved `Future` will provide the `ResponseData` (as a dictionary). This dictionary will now contain the `new_browser_state` (e.g., accessible via `response_data_dict['data']['new_browser_state']` if `ResponseData` model is updated or uses `extra='allow'` and `background.js` correctly passes the nested structure). The agent, in its main iterative loop, must extract and use this `new_browser_state` as the basis for its next decision-making cycle, rather than making a separate, potentially redundant, call to `get_state()` unless specifically required for a full refresh or error recovery.
            *   **Data Structures/Interfaces:** The agent's internal logic must be updated to look for and use the `new_browser_state` field from the `data` attribute of the `ResponseData` dictionary received after an action executes.
            *   **Define "Done":** The agent's decision-making loop correctly extracts the `new_browser_state` from the result of an executed action and uses this state to inform its subsequent analysis and action generation. Logging within the agent should confirm this flow.
            *   **Prioritize:** High - Makes the agent's operation efficient and reactive to the latest browser state.

### Phase 6: Iterative Loop or Termination

*   **Goal for this Phase (from `PROJECT_DOCS/CURRENT_PROJECT_GOAL.md`):** The main application/backend's agent receives the action result from the Chrome extension. If the result indicates the overall task is complete and the action was successful, the process may terminate or await a new task. If the task is not done, or if an error occurred, the agent uses the result and the latest browser state (provided by the extension) to decide on the next action command. The cycle (from Phase 3: Action Generation) repeats.
*   **Current State Analysis:**
    *   **What is currently happening (that misses the goal):**
        *   **No Agent Iterative Processing Loop:** The central `Agent` class/service, which would manage the iterative cycle of decision-making, action dispatch, result processing, and state updating (now with refactored state from `content.js`), is not yet implemented. This core logic (intended for `browser_use_ext/agent/agent_core.py` or similar, as per Phase 3 planning) is currently absent.
        *   **Task Completion Logic Undefined:** There are no defined mechanisms or criteria within the planned agent logic to determine when a multi-step user task is fully accomplished. This requires the agent (likely guided by the LLM) to assess progress and recognize completion, using the newly structured state information.
        *   **Agent-Level Error Handling Strategy Missing:** While the extension can report errors for individual actions, the agent's overarching strategy for handling these errors (e.g., when to retry, when to attempt alternative actions, when to give up and report failure to the user) is not yet designed or implemented.
    *   **What is currently happening (that moves towards/accomplishes the goal):**
        *   **Foundation for Loop Control:** The `AgentSettings` Pydantic model (`browser_use_ext/agent/views.py`) includes a `max_iterations` field. This provides a basic but important safety net to prevent runaway loops in the future agent implementation.
        *   **Structured Output for Loop Termination:** The `AgentOutput` model (`browser_use_ext/agent/views.py`) is designed to capture the final status of an agent's execution (e.g., `"success"`, `"failure"`, `"max_iterations_reached"`), along with `iterations_taken`, `full_history` of messages, and `thoughts_history`. This is well-suited for summarizing the outcome of an iterative process.
        *   **Prerequisite for State Updates in Loop:** The planned work in Phase 5 (ensuring that action results from the extension include the `new_browser_state`) is a critical prerequisite. Once implemented, it will provide the agent with the necessary fresh state information for each iteration of its decision loop without needing extra `get_state` calls.
    *   **What needs to happen (that will move towards/accomplish the goal):**
        1.  **Implement Agent's Main Iterative Processing Loop:**
            *   **Affected Components:** The `Agent` class to be developed (e.g., in `browser_use_ext/agent/agent_core.py`).
            *   **Details:** This is the primary execution logic within the `Agent`. It will involve:
                *   Initializing a loop that continues until task completion, max iterations are met (from `AgentSettings`), or an unrecoverable error occurs.
                *   **Inside each loop iteration:**
                    1.  Call its internal `async def decide_next_action(self, user_task: str, current_browser_state: dict, conversation_history: list) -> Optional[dict]:` method. This method encapsulates LLM interaction (using current state - now the `actionable_elements` format, task, and history to get the next action command or a completion signal). The action command will use string `element_id`s.
                    2.  If `decide_next_action` indicates task completion or no further action, the loop should terminate appropriately.
                    3.  If an action command is returned, send it to the extension via `await self.extension_interface._send_request("execute_action", data=action_command)`. Store the original `action_command` in `thoughts_history`.
                    4.  Await the `ResponseData` (as a dictionary) from the extension.
                    5.  Process `ResponseData`:
                        *   Log the result (e.g., add to `thoughts_history` or `conversation_history`).
                        *   If `ResponseData['success']` is `False` or `ResponseData['error']` is present, invoke error handling logic (see Action Item 3 below).
                        *   Extract the `new_browser_state` from `ResponseData['data']` (assuming Phase 5 work is complete) to be used as `current_browser_state` for the next iteration.
                        *   Update `conversation_history` with the latest turn.
                *   Upon loop termination, construct and return/log an `AgentOutput` object summarizing the entire process.
            *   **Data Structures/Interfaces:** The agent will manage `current_browser_state` (dictionary), a `conversation_history` (list of messages/turns), and use `AgentSettings` for control parameters. `AgentThought` will be used to log each step.
            *   **Define "Done":** The agent can execute a mock task involving a sequence of at least two mock actions: (a) it calls `decide_next_action` (mocked LLM), gets a mock action (with string `element_id`), (b) sends it via `ExtensionInterface` (mocked to return a successful `ResponseData` with a new mock state in `actionable_elements` format), (c) then uses this new mock state to call `decide_next_action` again. The loop should correctly terminate based on a mock "task complete" signal from `decide_next_action` or after reaching `max_iterations`. An `AgentOutput` object is generated and logged.
            *   **Prioritize:** High - This ties together all previous phases into a functioning agent process.
        2.  **Define and Implement Task Completion Logic within the Agent:**
            *   **Affected Components:** The `Agent` class (specifically its `decide_next_action` method and the LLM prompt engineering part).
            *   **Details:**
                *   The LLM prompts used by `decide_next_action` must instruct the LLM to explicitly signal when it believes the user's high-level task is fully accomplished or if it determines it cannot proceed further (and why).
                *   The agent's logic for parsing the LLM's response (within `decide_next_action`) must be able to reliably identify this "task_complete: true/false" signal (or a similar indicator like "final_answer_provided: true").
                *   The main iterative loop will use this signal to decide whether to continue or terminate execution and report success.
            *   **Data Structures/Interfaces:** May involve standardizing a part of the LLM's JSON output to include a field like `is_task_complete: bool` or `status: "continue"|"complete"|"cannot_proceed"`.
            *   **Define "Done":** The agent correctly identifies from a (mocked) LLM response that a task is complete. Consequently, its main iterative loop terminates, and it reports overall success in the final `AgentOutput`.
            *   **Prioritize:** Medium - Crucial for enabling purposeful and finite agent operations.
        3.  **Implement Agent-Level Error Handling and Basic Retry Strategy:**
            *   **Affected Components:** The `Agent` class (its main iterative loop and potentially `decide_next_action`).
            *   **Details:**
                *   When `ResponseData['success']` is `False` or `ResponseData['error']` is present after an action is attempted by the extension, the agent must log this error clearly.
                *   Implement a simple retry policy (e.g., allow one retry for the same action if a potentially transient error occurs). The agent might re-send the same action or ask the LLM for an alternative if the first attempt fails.
                *   If an error is persistent, deemed critical, or retries are exhausted, the agent should terminate its loop and report overall failure in the `AgentOutput`, including details of the error.
                *   Optionally, the LLM could be prompted with the error context to suggest a recovery step, which would then become the next action.
            *   **Data Structures/Interfaces:** The agent may need to track retry attempts for the current step/action. `AgentOutput.error` field should be populated on failure.
            *   **Define "Done":** If an action execution returns an error (via `ResponseData`), the agent logs it. Based on a simple policy (e.g., one retry for specific error types), it either attempts the action again or terminates, correctly populating `AgentOutput` to reflect the failure and the error encountered.
            *   **Prioritize:** Medium - Improves the robustness and resilience of the agent.
--- 