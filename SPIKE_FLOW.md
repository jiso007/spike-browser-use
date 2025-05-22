# Execution Flow for `examples/simple.py`

This document outlines the sequence of class, method, and function calls when executing the `examples/simple.py` script using the `browser-use` library.

## 1. Initialization (`examples/simple.py` - Module Level)

1.  **Imports:** Standard Python imports (`os`, `sys`, `asyncio`) and project/library imports (`dotenv`, `langchain_openai.ChatOpenAI`, `browser_use.Agent`).
2.  **Environment Variables:** `dotenv.load_dotenv()` loads API keys and other configurations from a `.env` file.
3.  **LLM Instantiation:** `langchain_openai.ChatOpenAI(...)` creates the language model instance (`llm`) specified (e.g., 'gpt-4o').
4.  **Agent Instantiation:** `browser_use.agent.service.Agent(task=..., llm=...)` creates the main agent object. This triggers the `Agent.__init__` method.

## 2. Agent Initialization (`browser_use.agent.service.Agent.__init__`)

This method sets up the core components of the agent:

1.  **Basic Attributes:** Stores `task`, `llm`.
2.  **Settings:** Instantiates `browser_use.agent.views.AgentSettings`.
3.  **State:** Instantiates `browser_use.agent.views.AgentState`.
4.  **Action Models Setup (`_setup_action_models`):**
    *   Dynamically creates Pydantic models for browser actions using `browser_use.controller.service.Controller.registry.create_action_model()`.
    *   Creates specialized `AgentOutput` types using `browser_use.agent.views.AgentOutput.type_with_custom_actions()`.
5.  **Metadata Setup:**
    *   `_set_browser_use_version_and_source()`: Determines package version/source.
    *   `_set_model_names()`: Extracts model name(s).
    *   `_set_tool_calling_method()`: Determines how the LLM calls actions (e.g., function calling).
6.  **LLM Verification (`_verify_llm_connection`):** Performs a test call to the LLM API.
7.  **Message Context (`_set_message_context`):** Sets up initial context for LLM messages.
8.  **Message Manager:** Instantiates `browser_use.agent.message_manager.service.MessageManager` to handle conversation history and system prompts.
9.  **Memory (Optional):** If `enable_memory` is true, instantiates `browser_use.agent.memory.service.Memory`.
10. **Browser Setup:**
    *   Instantiates `browser_use.browser.browser.Browser` (via `Browser.__init__`).
    *   Instantiates `browser_use.browser.context.BrowserContext` (via `BrowserContext.__init__`), linking it to the `Browser` instance.
11. **Telemetry:** Instantiates `browser_use.telemetry.service.ProductTelemetry`.

## 3. Running the Agent (`examples/simple.py` - `main()` function)

1.  **Start Execution:** `agent.run()` is called within an `asyncio.run()` loop.

## 4. Agent Execution Loop (`browser_use.agent.service.Agent.run`)

1.  **Logging:** `_log_agent_run()` logs the start for telemetry.
2.  **Main Loop:** Iterates until `max_steps` is reached or a `done` action occurs.
    *   **Check State:** `_raise_if_stopped_or_paused()` checks for interruptions.
    *   **Execute Step:** `Agent.step()` performs one cycle of observation, thought, and action.
    *   **Check Completion:** Breaks loop if `result[-1].is_done` is true.
    *   **Handle Interruptions:** Catches `InterruptedError`.
3.  **Post-Loop:**
    *   **Logging:** `log_completion()` logs run outcome.
    *   **GIF Generation (Optional):** `browser_use.agent.gif.create_history_gif()`.
    *   **History Saving (Optional):** `save_history()`.
    *   **Cleanup:** `Agent.close()`.
    *   **Return:** Returns the `AgentHistoryList`.

## 5. Agent Step (`browser_use.agent.service.Agent.step`)

This method executes a single cycle within the main loop:

1.  **Increment Step:** `self.state.n_steps += 1`.
2.  **Get Browser State:** `BrowserContext.get_state(...)` retrieves the current URL, DOM, screenshot (if vision enabled).
    *   *Lazy Initialization:* On the first call, this triggers `Browser.get_playwright_browser()` -> `Browser._init()` which starts Playwright (`async_playwright().start()`) and launches/connects to the browser (`playwright.chromium.launch()`, etc.).
    *   Uses `DOMService` for DOM processing.
3.  **Memory Update (Optional):** `Memory.create_procedural_memory()` if conditions met.
4.  **Check State:** `_raise_if_stopped_or_paused()`.
5.  **Update Actions (Optional):** `_update_action_models_for_page()` based on page content.
6.  **Add State to History:** `MessageManager.add_state_message()` adds browser state for LLM context.
7.  **Planner (Optional):** `_run_planner()` calls LLM for planning, adds result via `MessageManager.add_plan()`.
8.  **Prepare LLM Input:** `MessageManager.get_messages()`.
9.  **Call LLM for Action:** `Agent.get_next_action()` sends history/state to the LLM.
    *   Uses LangChain's `llm.invoke(...)` or similar.
    *   Parses the JSON response into `AgentOutput` (includes the `ActionModel` chosen by the LLM). Handles errors/retries.
10. **Check State:** `_raise_if_stopped_or_paused()`.
11. **Callbacks/Saving:** Executes `register_new_step_callback` and `save_conversation` if configured.
12. **Update History:**
    *   `MessageManager._remove_last_state_message()` (removes verbose state).
    *   `MessageManager.add_model_output()` (adds LLM response).
13. **Execute Actions:** `Agent.multi_act(model_output.action)` runs the action(s) chosen by the LLM.
    *   Iterates through actions in the sequence.
    *   For each action, calls `browser_use.controller.service.Controller.execute(...)`.
        *   The `Controller` maps the action name to the corresponding method (e.g., `navigate_to_url`).
        *   Action methods use `BrowserContext` and Playwright functions (`page.goto`, `page.click`, etc.) to interact with the browser.
        *   Returns an `ActionResult`.
14. **Store Result:** `self.state.last_result = result`.
15. **Error Handling:** `_handle_step_error()` manages exceptions during the step.
16. **Telemetry:** `ProductTelemetry.capture(AgentStepTelemetryEvent(...))`.
17. **Create History Item:** `_make_history_item()` appends detailed step info (`AgentHistory`, `BrowserStateHistory`) to `self.state.history.history`.

## 6. Agent Cleanup (`browser_use.agent.service.Agent.close`)

Called at the end of `agent.run()`:

1.  **Close Context:** `BrowserContext.close()` closes the current Playwright context.
2.  **Close Browser (Conditional):** If `keep_alive` is false, `Browser.close()` is called.
    *   This closes the Playwright browser instance (`playwright_browser.close()`).
    *   Stops the Playwright connection (`playwright.stop()`).
    *   Cleans up any browser subprocesses.
3.  **Garbage Collection:** `gc.collect()`.

## 7. Finalization (`examples/simple.py`)

1.  **Event Loop:** `asyncio.run(main())` completes when `agent.run()` returns. 