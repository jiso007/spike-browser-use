# Prompt: Identify Next Testable Development Step

## Purpose

This prompt guides an AI assistant to analyze the provided project documentation (`CURRENT_PROJECT_GOAL.md`, `CURRENT_PROJECT.md`, and `CURRENT_PROJECT_STATE.md`) to identify the single most critical and actionable next development task. The identified task should be something that can be implemented and tested in relative isolation to demonstrate clear progress.

## Input Documents

*   **`@CURRENT_PROJECT_GOAL.md`**: Outlines the overall modernization goals and phase-by-phase objectives for the new `/browser_use_ext` system.
*   **`@CURRENT_PROJECT.md`**: Describes the operational phases of the legacy `/browser_use` system (for context, not direct implementation).
*   **`@CURRENT_PROJECT_STATE.md`**: Provides a detailed analysis of the current `/browser_use_ext` system's status against the goals, including identified gaps and action items per phase, and an overall project summary with critical next steps.

## Instructions for the AI Assistant

You are tasked with acting as a senior developer or technical lead. Based on your thorough analysis of the three input documents, please perform the following:

1.  **Review Critical Next Steps:** Pay close attention to the "Top 3-4 Critical Next Steps" identified in the "Overall Project Status Summary" of `CURRENT_PROJECT_STATE.md`. Also, consider the high-priority action items listed within each phase analysis in the same document.
2.  **Identify the Single Most Important Next Task:** From your review, determine the single most important task that should be tackled next. This task should:
    *   Address a critical gap or roadblock identified in `CURRENT_PROJECT_STATE.md`.
    *   Enable significant downstream progress by unblocking other dependent tasks or phases.
    *   Be reasonably implementable and testable in isolation (or with minimal, already existing/stable dependencies). "Testable in isolation" means its success can be verified without needing many other incomplete components to be fully functional. For example, implementing a specific backend endpoint and testing it with a mock client, or adding a piece of specific functionality to an extension script and verifying its direct output/behavior through logging or simple UI checks.
3.  **Frame as a Goal:** Present your identified next task as a concise, actionable goal.

## Output Format

Your output should be a clearly defined goal that represents the next best and most important task to implement. Structure your response as follows:

### Next Overall Project Goal to Implement:

*   **Goal Title:** (A brief, descriptive title for the task/goal)
*   **Description:** (1-2 sentences describing what needs to be achieved by implementing this task.)
*   **Rationale for Selection:** (2-3 sentences explaining why this task is the most critical next step, how it addresses current roadblocks highlighted in `CURRENT_PROJECT_STATE.md`, and why it's suitable for isolated implementation and testing. Reference specific points from the input documents if helpful, e.g., "Addresses Major Roadblock #2 in CURRENT_PROJECT_STATE.md" or "Unblocks Phase 3 Action Item 1".)
*   **Key Components Involved:** (List the primary files/modules from `/browser_use_ext` that will be created or modified, e.g., `browser_use_ext/agent/agent_core.py`, `browser_use_ext/extension/content.js`.)
*   **Definition of Done (for this specific goal):** (1-3 bullet points outlining clear, verifiable criteria that would indicate this specific goal/task is successfully completed.)

---

**Example of Expected Output Structure (Illustrative - Do NOT use this content, derive from documents):**

### Next Overall Project Goal to Implement:

*   **Goal Title:** Implement `content_script_ready` Ping in `content.js`
*   **Description:** Complete the two-way "Ready" handshake between `content.js` and `background.js` by having `content.js` send a "content_script_ready" message. This ensures reliable communication initialization as per the `chrome_extension_content_readiness` rule.
*   **Rationale for Selection:** This task addresses a "High" priority item in Phase 1 of `CURRENT_PROJECT_STATE.md` ("The `content.js` script ... is missing the explicit `chrome.runtime.sendMessage({ type: \"content_script_ready\" })` call") and is a prerequisite for any reliable messaging from `background.js` to `content.js`. It's highly isolated, primarily affecting `content.js` and `background.js` interaction, and testable by observing console logs and the `contentScriptsReady` set in `background.js`.
*   **Key Components Involved:**
    *   `browser_use_ext/extension/content.js`
    *   `browser_use_ext/extension/background.js` (for verification)
*   **Definition of Done (for this specific goal):**
    *   `content.js` sends `{ type: "content_script_ready" }` message immediately after its `chrome.runtime.onMessage.addListener` is set up.
    *   `background.js` receives this message for a tab and adds the `sender.tab.id` to its `contentScriptsReady` Set.
    *   Calls to `waitForContentScriptReady(tabId)` in `background.js` for that tab resolve successfully without timing out. 