# Error Remediation Tasks: Extension Interface - Content Script Readiness Synchronization

This document tracks the implementation steps to address the "Could not establish connection. Receiving end does not exist." error by implementing explicit content script readiness synchronization in the Python `ExtensionInterface`.

Based on the Solution Architecture Document, the following implementation steps are required:

- [x] 1. **Modify `ExtensionInterface` State:** Add the `_content_script_ready_tabs: Dict[int, bool]` dictionary to the `ExtensionInterface` class in `browser_use_ext/extension_interface/service.py` to track tabs that have signaled readiness.
- [x] 2. **Implement `_wait_for_content_script_ready`:** Add a new asynchronous waiting method `async def _wait_for_content_script_ready(self, tab_id: int, timeout_seconds: float) -> None` to `ExtensionInterface` that waits for a specific `tab_id` to be marked as ready.
- [x] 3. **Update `_process_message`:** Modify the `_process_message` method in `browser_use_ext/extension_interface/service.py` to handle the `content_script_ready` event (marking the tab as ready) and potentially the `tab_removed` event (for cleanup) in `_content_script_ready_tabs`.
- [x] 4. **Integrate Wait in `get_state`:** Add a call to `await self._wait_for_content_script_ready(...)` near the beginning of the `get_state` method in `browser_use_ext/extension_interface/service.py` and remove the temporary `asyncio.sleep(0.5)`.
- [x] 5. **Integrate Wait in `execute_action`:** Add a call to `await self._wait_for_content_script_ready(...)` near the beginning of the `execute_action` method in `browser_use_ext/extension_interface/service.py`.
- [x] 6. **Review `manifest.json`:** Check and potentially update the `run_at` setting for `content.js` in `browser_use_ext/extension/manifest.json` to `document_idle` or `document_end`.
- [ ] 7. **Add/Update Unit Tests (Optional but Recommended):** Write unit tests for the new `_wait_for_content_script_ready` method and related logic. (Note: This step is marked optional in the plan and will not be implemented unless requested.)
- [ ] 8. **Test Locally (E2E):** Run the `pytest browser_use_ext/tests/python/test_agent_e2e.py` test locally multiple times to confirm the fix and verify logs. 