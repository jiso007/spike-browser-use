import asyncio
import logging
import sys
import os
import json
from typing import List, Any, Dict, Optional

import pytest
from pydantic import BaseModel

# Ensure the test can find the browser_use_ext package
# This assumes that pytest is run from the root of the workspace,
# and pyproject.toml has `pythonpath = ["."]` or similar.
# Or, if running this script directly, ensure the parent directory of browser_use_ext is in sys.path.
# For pytest, this setup is usually handled by conftest.py or pytest.ini/pyproject.toml

from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.browser.context import BrowserContext, BrowserContextConfig
from browser_use_ext.agent.service import Agent, DEFAULT_MAX_STEPS
from browser_use_ext.agent.views import AgentSettings, AgentHistoryList, ActionCommand, AgentLLMOutput, AgentBrain
from browser_use_ext.browser.views import BrowserState

# Mock LLM
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from browser_use_ext.tests.utils.test_mocks import MockLLM

# Basic Logging Setup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

logger.critical("!!! MODULE-LEVEL LOG: test_agent_e2e.py has been loaded and this log statement reached !!!")

# Configuration
# TEST_SERVER_PORT is now defined in conftest.py

def test_synchronous_sanity_check():
    logger.critical("!!! SYNC TEST LOG: test_synchronous_sanity_check IS RUNNING !!!")
    assert True
    logger.critical("!!! SYNC TEST LOG: test_synchronous_sanity_check COMPLETED !!!")

@pytest.mark.asyncio
# Add the fixture here
async def test_agent_run_navigate_and_get_heading(extension_interface: ExtensionInterface):
    logger.info("!!! ASYNC TEST LOG: test_agent_run_navigate_and_get_heading IS STARTING (Restoring Full Logic) !!!")
    
    # The interface is now provided by the fixture
    # interface = None # Remove this line
    try:
        # Server startup is now handled by the fixture
        # logger.info("Attempting to initialize ExtensionInterface...") # Remove this line
        # interface = ExtensionInterface(host="localhost", port=TEST_SERVER_PORT) # Remove this line
        # logger.info(f"ExtensionInterface initialized: {interface}") # Remove this line
        
        # logger.info("Attempting to start server...") # Remove this line
        # await interface.start_server() # Remove this line
        logger.info(f"WebSocket server is managed by fixture on ws://{{extension_interface.host}}:{{extension_interface.port}}.") # Modified log
        
        await asyncio.sleep(3.0) # Increased to 3 seconds
        logger.info("Proceeding to wait for extension connection.")

        logger.info("Waiting for the Chrome extension to connect...")
        connection_attempts = 0
        max_connection_attempts = 20 # 10 seconds
        # Use the interface provided by the fixture
        while not extension_interface.has_active_connection and connection_attempts < max_connection_attempts:
            active_conn_obj = extension_interface.active_connection_object
            # CRITICAL log for connection attempts
            logger.critical(f"TEST_DEBUG: Connection attempt {connection_attempts + 1}/{max_connection_attempts}, has_active: {extension_interface.has_active_connection}, active_conn_obj: {active_conn_obj.client_id if active_conn_obj else 'No active object'}")
            await asyncio.sleep(0.5)
            connection_attempts += 1
        
        # Use the interface provided by the fixture
        if not extension_interface.has_active_connection:
            logger.error("Extension did not connect within the timeout period. Test cannot proceed.")
            logger.warning("Ensure a browser with the extension loaded (and reloaded), WS_URL pointing to ws://localhost:8766, and an active tab is open.")
            pytest.fail("Chrome extension did not connect within timeout.")

        # Use the interface provided by the fixture
        active_conn_obj_final = extension_interface.active_connection_object
        # CRITICAL log for successful connection
        logger.critical(f"TEST_INFO: Chrome extension connected: Client ID {active_conn_obj_final.client_id if active_conn_obj_final else 'N/A'}")
        # logger.info("!!! ASYNC TEST LOG: Connection part successful !!!") # Removed intermediate log

        logger.info(f"Waiting for ExtensionInterface to report an active tab (timeout: 5s)...")
        # Use the interface provided by the fixture
        await extension_interface.wait_for_active_tab(timeout_seconds=5.0)
        # logger.info(f"ExtensionInterface reported active tab ID: {interface._active_tab_id}") # Redundant due to internal logging in wait_for_active_tab

        # ADD A SMALL DELAY HERE TO ALLOW INITIAL TAB EVENT PROCESSING
        logger.info("Allowing a brief moment for initial tab event processing by ExtensionInterface...")
        await asyncio.sleep(1.0) # Wait 1 second for tab event to be processed

        # --- Restore Agent Logic & Assertions --- 
        navigate_brain = AgentBrain(evaluation_previous_goal="Initial state", memory="Just started", next_goal="Navigate to example.com")
        navigate_action = ActionCommand(action="navigate", params={"url": "https://example.com"})
        llm_response_1 = AgentLLMOutput(current_state=navigate_brain, action=[navigate_action]).model_dump_json()

        extract_brain = AgentBrain(evaluation_previous_goal="Navigation to example.com likely successful", memory="On example.com", next_goal="Find the main heading (H1) and report it.")
        extract_action = ActionCommand(
            action="extract_content", 
            # CORRECTED: Use element_id based on typical output for example.com's H1
            # The exact ID can vary, but structure is usually like this.
            # Let's assume a common ID structure or one observed from example.com state.
            # A more robust test might first get state, then pick an ID.
            # For mock, we hardcode an expected one.
            params={"element_id": "struct_div[0]_h1[0]", "attribute": "innerText", "extraction_type": "text", "query_or_goal": extract_brain.next_goal}
        )
        llm_response_2 = AgentLLMOutput(current_state=extract_brain, action=[extract_action]).model_dump_json()
        
        done_brain = AgentBrain(evaluation_previous_goal="Extracted H1 content", memory="Found H1: 'Example Domain'", next_goal="Report task as complete.")
        done_action = ActionCommand(action="done", params={"success": True, "message": "Found heading: Example Domain"})
        llm_response_3 = AgentLLMOutput(current_state=done_brain, action=[done_action]).model_dump_json()

        mock_llm = MockLLM(responses=[llm_response_1, llm_response_2, llm_response_3])

        agent_settings = AgentSettings(
            max_steps_per_run=5, 
            delay_between_steps_ms=100, # Faster for tests
            use_vision=False
        )
        
        task = "Go to example.com and report the main heading."
        # Pass the interface from the fixture to the Agent
        agent = Agent(task=task, llm=mock_llm, extension_interface=extension_interface, settings=agent_settings)

        logger.info(f"Running agent for task: {task}")
        
        logger.info("PLEASE ENSURE A BROWSER WINDOW IS OPEN AND HAS AN ACTIVE TAB (e.g., example.com). Test will proceed in 5 seconds...")
        await asyncio.sleep(5) # Original sleep for manual browser setup
        logger.info("Proceeding to agent.run().")

        history: AgentHistoryList = await agent.run()

        logger.info("Agent run finished. Analyzing history...")
        assert history is not None
        assert len(history.history) > 0, "Agent history should not be empty"
        
        navigate_action_found = any(
            action_res.action_name == "navigate" and action_res.params.get("url") == "https://example.com"
            for step in history.history
            for action_res in step.action_results
        )
        assert navigate_action_found, "Navigate action to example.com not found in history."

        # ADDED: Longer delay after navigate action completes in history
        if navigate_action_found:
            logger.info("Navigate action found in history. Adding a 5-second delay to allow page/CS to stabilize before next step...")
            await asyncio.sleep(5.0) # Increased to 5 seconds
            
        extract_action_found = any(
            action_res.action_name == "extract_content" and action_res.params.get("element_id") == "struct_div[0]_h1[0]"
            for step in history.history
            for action_res in step.action_results
        )
        assert extract_action_found, "Extract content action for element_id struct_div[0]_h1[0] not found in history."

        last_step = history.history[-1]
        assert last_step is not None
        assert len(last_step.action_results) > 0
        last_action_result = last_step.action_results[-1]
        assert last_action_result.is_done_action, "Last action was not a 'done' action."
        assert last_action_result.success, "\'Done\' action was not successful."
        assert "Found heading: Example Domain" in (last_action_result.returned_data if isinstance(last_action_result.returned_data, str) else last_action_result.params.get("text", "")), "Final message in done action incorrect."

        logger.info("test_agent_run_navigate_and_get_heading assertions passed!")
        # --- End of Restored Logic ---

        # Assert the number of times the MockLLM was called
        logger.info(f"Asserting MockLLM call count. Expected: 3, Actual: {mock_llm.call_count}")
        assert mock_llm.call_count == 3, f"MockLLM was called {mock_llm.call_count} times, expected 3."

    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)
        pytest.fail(f"Test failed due to an exception: {e}")
    finally:
        # Server shutdown is now handled by the fixture
        # if interface: # Remove this check
        #     logger.info("Attempting to stop server in finally block...") # Remove this line
        #     await interface.close() # Remove this line
        #     logger.info("Server stopped in finally block.") # Remove this line
        # else: # Remove this else block
        #     logger.info("No interface to stop in finally block.") # Remove this line
        logger.info("Server lifecycle managed by pytest fixture.") # Add a log indicating fixture management

    logger.info("!!! ASYNC TEST LOG: test_agent_run_navigate_and_get_heading COMPLETED (Full Logic Restored) !!!")
    # assert True # Removed basic assertion, relies on internal assertions now

# To run this test:
# 1. Make sure you have a Chromium browser open.
# 2. Load the 'browser-use-ext' extension in developer mode.
# 3. IMPORTANT: Edit the extension's background.js to change WS_URL to "ws://localhost:8766"
# 4. Ensure an active tab is open in the browser before starting the test.
# 5. Run pytest from your project root directory:
#    pytest browser_use_ext/tests/python/test_agent_e2e.py
#
# You might need to manually open a tab in the browser for the extension to activate on,
# or the test might need to command the extension to open a new tab as its first action. 