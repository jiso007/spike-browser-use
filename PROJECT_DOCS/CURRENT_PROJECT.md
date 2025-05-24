# CURRENT_PROJECT.md: System Modernization Plan (Based on `old-existing-folder`)

This document outlines the key operational phases of the system currently residing in the `/browser_use` directory. Understanding these phases is crucial for planning system modernization while preserving core logic.

---

### Phase 1: Initialization and Configuration

*   **Action that Occurs:**
    *   The system initializes its core components, including the AI Agent, Browser controller, and connections to external services like Large Language Models (LLMs). This phase sets up the operational parameters and loads necessary configurations.
    *   Key objects such as the `Agent` (from `browser_use/agent/service.py`), `Browser` (from `browser_use/browser/browser.py`), `BrowserContext` (from `browser_use/browser/context.py`), and `Controller` (from `browser_use/controller/service.py`) are instantiated.
    *   Configurations are loaded, potentially using `.env` files (as suggested by `dotenv` import in `browser_use/agent/service.py`) and `BrowserContextConfig` (defined in `browser_use/browser/context.py`). These configs define parameters like LLM model details, browser window size, timeouts, and paths for saving data (e.g., `save_conversation_path`, `trace_path`).
    *   The `Agent` constructor in `browser_use/agent/service.py` takes numerous parameters for task definition, LLM instance, browser instance, controller, and various settings related to vision, memory, planner, max failures, retry delays, etc.
    *   The `BrowserContext` in `browser_use/browser/context.py` is initialized with configurations for cookies, security settings, viewport size, user agent, and paths for recordings or downloads. It also sets up an `init_script` for the browser pages.
    *   Logging is configured via `browser_use/logging_config.py` as seen in `browser_use/__init__.py`.
*   **Specific Folder/File Structure:**
    *   `browser_use/__init__.py`: Initializes logging and exposes core classes.
    *   `browser_use/agent/service.py`: Contains the `Agent` class initialization.
    *   `browser_use/agent/views.py`: Defines `AgentSettings` and other Pydantic models for configuration.
    *   `browser_use/browser/browser.py`: Contains the `Browser` class initialization.
    *   `browser_use/browser/context.py`: Contains `BrowserContext` and `BrowserContextConfig` initialization.
    *   `browser_use/controller/service.py`: Contains the `Controller` class initialization.
    *   `browser_use/logging_config.py`: Handles setup of logging.
*   **Hardcoded Values, External Dependencies, Config Files:**
    *   **External Dependencies:** Playwright (Patchright), Large Language Models (interfaces like `BaseChatModel` from Langchain), `python-dotenv`.
    *   **Config Files:** Likely uses `.env` files for API keys (e.g., `REQUIRED_LLM_API_ENV_VARS` in `browser_use/agent/views.py`). Explicit config objects like `AgentSettings` and `BrowserContextConfig` centralize other settings.
    *   **Hardcoded Values:** Default values for `BrowserContextConfig` (e.g., `minimum_wait_page_load_time`, `user_agent`), `BROWSER_NAVBAR_HEIGHT` in `browser_use/browser/context.py`. Default model names or tool calling methods might be implicitly set if not overridden.
*   _Consideration(s):_
    *   Modernizing this phase involves ensuring flexible and secure configuration management, potentially using a centralized configuration service or more robust environment variable handling.
    *   Dependency versions (Playwright, LLM SDKs) need careful management for stability.

---

### Phase 2: Task Ingestion and Planning

*   **Action that Occurs:**
    *   The Agent receives a primary task (a string description of what needs to be achieved). Initial actions or sensitive data can also be provided.
    *   If a planner is configured (`planner_llm` and `planner_interval` in `AgentSettings`), the Agent may invoke a planning step. This involves querying an LLM (potentially with vision capabilities if `use_vision_for_planner` is true) to break down the main task into sub-goals or a sequence of steps.
    *   The `Agent` in `browser_use/agent/service.py` takes a `task` string in its constructor. The `_run_planner()` method handles interaction with the planner LLM, using `PlannerPrompt`.
    *   The `MessageManager` (`browser_use/agent/message_manager/service.py`) is initialized and manages the conversation history, including system prompts and task definitions.
*   **Specific Folder/File Structure:**
    *   `browser_use/agent/service.py`: `Agent.__init__` (receives task), `_run_planner()` method.
    *   `browser_use/agent/prompts.py`: Contains `PlannerPrompt` and `SystemPrompt` which are crucial inputs for the LLMs.
    *   `browser_use/agent/views.py`: Defines `AgentSettings` which includes planner configurations.
    *   `browser_use/agent/message_manager/service.py`: Manages messages including the initial task.
*   **Hardcoded Values, External Dependencies, Config Files:**
    *   **External Dependencies:** LLM for planning.
    *   **Config Files:** Planner configuration (model, interval, vision usage) is part of `AgentSettings`.
    *   **Hardcoded Values:** Default planner interval (`planner_interval: int = 1`). Prompt templates in `browser_use/agent/prompts.py` structure the input to the planner LLM.
*   _Consideration(s):_
    *   The effectiveness of the planning phase heavily depends on the quality of the planner LLM and the prompt engineering in `PlannerPrompt`.
    *   Improving this phase could involve more sophisticated planning algorithms or allowing for dynamic adjustment of plans based on execution feedback.

---

### Phase 3: Browser State Perception

*   **Action that Occurs:**
    *   The Agent, through the `BrowserContext`, gathers the current state of the active web page. This is a critical input for the LLM to decide the next action.
    *   State information includes the page URL, title, open tabs, a screenshot of the page (if `use_vision` is enabled), and a structured representation of the DOM. The DOM representation often includes visible elements, interactive elements, and their attributes.
    *   The `BrowserContext.get_state()` method in `browser_use/browser/context.py` is central to this phase. It orchestrates fetching various pieces of information.
    *   `DomService` (from `browser_use/dom/service.py`) and its associated JavaScript (`buildDomTree.js` in `browser_use/dom/`) are likely used to build the structured DOM representation and identify interactive elements (e.g. using `ClickableElementProcessor`).
    *   The `MessageManager` adds this state information (textual and potentially visual) to the message history for the LLM.
*   **Specific Folder/File Structure:**
    *   `browser_use/browser/context.py`: `get_state()`, `take_screenshot()`, `get_tabs_info()`, `_get_page_structure()` (likely calls `DomService`).
    *   `browser_use/dom/service.py`: `DomService` likely processes the raw HTML into a more structured format.
    *   `browser_use/dom/buildDomTree.js`: JavaScript executed in the browser to extract DOM information.
    *   `browser_use/dom/views.py`: Defines DOM structure models like `DOMElementNode`, `SelectorMap`.
    *   `browser_use/dom/clickable_element_processor/service.py`: Likely processes DOM elements to identify clickable ones.
    *   `browser_use/agent/message_manager/service.py`: `add_state_message()` method.
*   **Hardcoded Values, External Dependencies, Config Files:**
    *   **External Dependencies:** Browser (via Playwright).
    *   **Config Files:** `AgentSettings.use_vision` controls screenshot capture. `BrowserContextConfig.include_attributes` controls which HTML attributes are included in the DOM representation. `BrowserContextConfig.viewport_expansion` affects which elements are considered visible.
    *   **Hardcoded Values:** JavaScript code in `buildDomTree.js`. Default attributes to include if not specified.
*   _Consideration(s):_
    *   The quality and conciseness of the state representation are vital for LLM performance and token efficiency.
    *   Modifying this phase could involve optimizing DOM processing, experimenting with different state representations (e.g., simplified DOM, accessibility tree), or improving vision capabilities. Ensuring accurate identification of interactive elements is crucial.

---

### Phase 4: Action Generation (LLM Interaction)

*   **Action that Occurs:**
    *   The Agent constructs a prompt for the LLM, including the original task, conversation history, the latest browser state (textual and/or visual), available actions, and any plan generated.
    *   This prompt is sent to the configured LLM. The LLM's response is expected to be a structured output (e.g., JSON) specifying the next action(s) to take.
    *   `Agent.get_next_action()` in `browser_use/agent/service.py` manages this LLM call. It uses `MessageManager` to assemble `input_messages`.
    *   The system handles different tool calling methods (`function_calling`, `raw`, or `None`) based on LLM capabilities and configuration (`AgentSettings.tool_calling_method`).
    *   The response from the LLM is parsed into `AgentOutput`, which includes the proposed `action` (a list of `ActionModel` instances) and other fields like `evaluation_previous_goal`, `memory`, and `next_goal`.
    *   Error handling and retries are implemented if the LLM returns an empty or invalid action.
*   **Specific Folder/File Structure:**
    *   `browser_use/agent/service.py`: `get_next_action()`, `_verify_llm_connection()`.
    *   `browser_use/agent/message_manager/service.py`: `get_messages()`, `add_model_output()`.
    *   `browser_use/agent/prompts.py`: `SystemPrompt`, `AgentMessagePrompt` contribute to the LLM prompt.
    *   `browser_use/agent/views.py`: Defines `AgentOutput` and the dynamic `ActionModel` (based on `controller.registry`).
    *   `browser_use/controller/registry/views.py`: `ActionModel` is dynamically created here based on registered actions.
*   **Hardcoded Values, External Dependencies, Config Files:**
    *   **External Dependencies:** The primary LLM.
    *   **Config Files:** `AgentSettings` (LLM model details, `max_input_tokens`, `tool_calling_method`, `override_system_message`, `extend_system_message`).
    *   **Hardcoded Values:** Prompt templates in `prompts.py`. Retry logic for empty actions. Regular expressions for parsing (e.g., `THINK_TAGS`).
*   _Consideration(s):_
    *   Prompt engineering is critical. Changes here directly impact the agent's ability to choose correct actions.
    *   Managing context window limits (`max_input_tokens`) is essential. The `MessageManager` handles this by cutting messages or summarizing.
    *   The reliability of LLM output parsing and action validation (`validate_output`) is key.

---

### Phase 5: Action Execution

*   **Action that Occurs:**
    *   The `Agent` takes the list of `ActionModel` instances from the `AgentOutput` and executes them sequentially using the `Controller`.
    *   The `Controller` (from `browser_use/controller/service.py`) dispatches these actions to the appropriate handlers. These handlers interact with the `BrowserContext` to perform browser operations.
    *   Supported actions might include: navigating to a URL, clicking elements, inputting text, scrolling, managing tabs, using a "done" action to signify task completion, etc.
    *   The `Agent.multi_act()` method in `browser_use/agent/service.py` iterates through the actions and calls `controller.execute_action()`.
    *   `BrowserContext` methods like `navigate_to()`, `_click_element_node()`, `_input_text_element_node()`, `refresh_page()`, `go_back()`, `close_current_tab()`, etc. (in `browser_use/browser/context.py`) are invoked by action handlers within the controller.
    *   Element locating strategies (CSS selectors, XPath, text) are used by `BrowserContext` (e.g., `get_locate_element_by_css_selector`).
*   **Specific Folder/File Structure:**
    *   `browser_use/agent/service.py`: `multi_act()`.
    *   `browser_use/controller/service.py`: `Controller.execute_action()` and its registered action handlers.
    *   `browser_use/controller/registry/`: Likely contains the registration logic for different actions.
    *   `browser_use/browser/context.py`: Contains methods for actual browser interactions.
    *   `browser_use/dom/views.py`: `DOMElementNode` is used to reference elements for actions.
*   **Hardcoded Values, External Dependencies, Config Files:**
    *   **External Dependencies:** Playwright for browser manipulation.
    *   **Config Files:** `BrowserContextConfig.wait_between_actions` introduces delays.
    *   **Hardcoded Values:** Specific action names (e.g., "done", "click", "type_text" - though these are usually defined dynamically via the controller's registry). Timeout values within Playwright calls might be hardcoded or configurable.
*   _Consideration(s):_
    *   Robust error handling for action execution (e.g., element not found, navigation failed) is critical.
    *   Ensuring actions are idempotent or that their effects are correctly tracked is important for retries and reliability.
    *   The mapping from LLM-generated action parameters to concrete browser operations needs to be precise.

---

### Phase 6: Result Evaluation, State Update, and History Logging

*   **Action that Occurs:**
    *   After each action or set of actions in a step, the system captures the `ActionResult`. This includes any output from the action, errors, or extracted content.
    *   The Agent updates its internal state (`AgentState`), including the step count (`n_steps`), consecutive failures, and the last result.
    *   A history item (`AgentHistory`) is created, logging the model output (planned actions), the browser state before the actions, the actual results of the actions, and metadata like execution time and token usage.
    *   If enabled, memory (contextual or procedural) is updated by the `Memory` service (`browser_use/agent/memory/service.py`).
    *   If enabled, a GIF of the browser interaction for the step might be generated (`browser_use/agent/gif.py`).
    *   The `Agent` checks if the last action was `done` and if it indicated success or failure.
*   **Specific Folder/File Structure:**
    *   `browser_use/agent/service.py`: `step()` method orchestrates this; `_make_history_item()`, `_handle_step_error()`.
    *   `browser_use/agent/views.py`: Defines `ActionResult`, `AgentHistory`, `AgentState`, `StepMetadata`.
    *   `browser_use/agent/memory/service.py`: `Memory` class for updating/creating memories.
    *   `browser_use/telemetry/service.py`: `ProductTelemetry` captures events like `AgentStepTelemetryEvent`.
    *   `browser_use/agent/gif.py`: `create_history_gif()`.
*   **Hardcoded Values, External Dependencies, Config Files:**
    *   **Config Files:** `AgentSettings.save_conversation_path` for logging full conversation history. `AgentSettings.generate_gif`. Memory configuration via `memory_config`.
    *   **External Dependencies:** File system for saving history, GIFs, or telemetry.
*   _Consideration(s):_
    *   Comprehensive history logging is vital for debugging and improving the agent's performance.
    *   The criteria for evaluating "success" or "failure" of a step or the overall task can be complex and may need refinement.
    *   Memory mechanisms can significantly impact long-term task performance but also add complexity.

---

### Phase 7: Looping or Termination

*   **Action that Occurs:**
    *   The Agent checks for termination conditions:
        *   Has the "done" action been called with success?
        *   Has the maximum number of steps (`max_steps` in `Agent.run()`) been reached?
        *   Has the maximum number of consecutive failures (`AgentSettings.max_failures`) been reached?
        *   Has an explicit stop/pause signal been received?
    *   If no termination condition is met, the Agent increments its step count and loops back to Phase 3 (Browser State Perception) to continue processing the task.
    *   If a termination condition is met, the Agent run concludes. Callbacks like `register_done_callback` may be invoked. The browser context might be closed if it wasn't injected.
*   **Specific Folder/File Structure:**
    *   `browser_use/agent/service.py`: The main `run()` loop logic, `take_step()` method, checks for `is_done` in `ActionResult`, `max_steps` handling, `max_failures` check in `_handle_step_error()`, `pause()`, `stop()` methods.
    *   `browser_use/browser/context.py`: `close()` method to clean up browser resources.
*   **Hardcoded Values, External Dependencies, Config Files:**
    *   **Config Files:** `AgentSettings.max_failures`, `AgentSettings.retry_delay`. `max_steps` is a parameter to the `run` method.
*   _Consideration(s):_
    *   The logic for looping and termination determines the agent's persistence and resilience.
    *   Graceful shutdown and resource cleanup (e.g., closing browser contexts) are important.
    *   Clear reporting of why an agent terminated (success, failure, max steps) is needed.

--- 