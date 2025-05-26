# browser_use_ext/tests/test_content_script_ready.py

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock

# Attempt to import ExtensionInterface. Adjust path if necessary based on project structure and how pytest is run.
# This assumes that when pytest runs, 'browser_use_ext' is on the python path.
# (e.g., running pytest from the project root directory that contains browser_use_ext)
from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.extension_interface.models import Message, ExtensionEvent, Response, ActionPayload, ActionRequest # Assuming BrowserState is in models not views
from browser_use_ext.browser.views import BrowserState # Keep this if BrowserState is indeed here

class TestContentScriptReadiness:
    """Test suite for content script ready handshake mechanism from Python side"""
    
    @pytest.fixture
    def mock_websocket(self):
        """Mock websocket for testing"""
        mock_ws = AsyncMock() 
        mock_ws.send = AsyncMock() 
        mock_ws.recv = AsyncMock() 
        mock_ws.closed = False 
        mock_ws.ensure_open = AsyncMock() 
        mock_ws.wait_closed = AsyncMock() 
        return mock_ws
    
    @pytest.fixture
    async def extension_interface(self, mock_websocket):
        """Create ExtensionInterface instance with mocked websocket and start/stop server"""
        interface = ExtensionInterface(host="localhost", port=8766) 
        interface.websocket = mock_websocket 
        interface.active_connection = mock_websocket 
        interface.client_id_counter = 1
        interface.clients = {"client_1": mock_websocket}
        interface.message_counter = 1 # Start from 1 as 0 might be special
        interface.pending_requests = {}
        return interface

    @pytest.mark.asyncio
    async def test_wait_for_content_script_ready_success(self, extension_interface, mock_websocket):
        """Test successful wait for content script readiness from Python side via get_state"""
        tab_id_to_test = 123
        request_id_sent_from_python = None

        async def send_side_effect(message_str):
            nonlocal request_id_sent_from_python
            message_obj = json.loads(message_str)
            request_id_sent_from_python = message_obj.get("id")
            if message_obj.get("type") == "get_state":
                 response_from_extension = {
                    "type": "response",
                    "id": request_id_sent_from_python, 
                    "data": {
                        "success": True,
                        "url": "https://example.com",
                        "title": "Example Page",
                        "actionable_elements": [],
                        "tabs": [],
                        "screenshot": None,
                        "html_content": "<html></html>",
                        "tree": { "type": "document", "children": []},
                        "selector_map": {},
                        "pixels_above": 0,
                        "pixels_below": 0,
                        "viewport_height": 600, # Added missing fields for BrowserState
                        "viewport_width": 800,
                        "scroll_x": 0,
                        "scroll_y": 0,
                        "page_content_height": 600,
                        "page_content_width": 800,
                        "relevant_elements": [],
                        "extracted_text": "",
                        "error_message": None
                    }
                }
                 # Ensure recv is an awaitable mock that returns the value
                 extension_interface.pending_requests[request_id_sent_from_python].set_result(response_from_extension)
            return None # send itself doesn't return anything significant

        mock_websocket.send.side_effect = send_side_effect
        
        state = await extension_interface.get_state(tab_id=tab_id_to_test)
        
        assert state is not None
        assert state.url == "https://example.com"
        
        get_state_call_args = None
        for call in mock_websocket.send.call_args_list:
            sent_message = json.loads(call[0][0]) 
            if sent_message.get("type") == "get_state":
                get_state_call_args = sent_message
                break
        
        assert get_state_call_args is not None
        assert get_state_call_args["data"]["tabId"] == tab_id_to_test

    @pytest.mark.asyncio
    async def test_get_state_timeout_if_content_script_never_ready(self, extension_interface, mock_websocket):
        """Test get_state returns None if background.js indicates content script not ready"""
        tab_id_to_test = 456
        request_id_sent_from_python = None

        async def send_side_effect(message_str):
            nonlocal request_id_sent_from_python
            message_obj = json.loads(message_str)
            request_id_sent_from_python = message_obj.get("id")
            if message_obj.get("type") == "get_state":
                response_from_extension = {
                    "type": "response",
                    "id": request_id_sent_from_python,
                    "data": {
                        "success": False,
                        "error": f"Content script in tab {tab_id_to_test} not ready after Xms"
                    }
                }
                extension_interface.pending_requests[request_id_sent_from_python].set_result(response_from_extension)
            return None

        mock_websocket.send.side_effect = send_side_effect
        
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            state_result = await extension_interface.get_state(tab_id=tab_id_to_test, timeout_seconds=1)
        
        assert state_result is None
        get_state_call_args = None
        for call in mock_websocket.send.call_args_list:
            sent_message = json.loads(call[0][0])
            if sent_message.get("type") == "get_state":
                get_state_call_args = sent_message
                break
        assert get_state_call_args is not None
        assert get_state_call_args["data"]["tabId"] == tab_id_to_test
        
        error_logged = False
        for call_args in mock_logger.error.call_args_list:
            log_message = call_args[0][0]
            if (f"Error from extension for get_state on tab {tab_id_to_test}" in log_message and 
                f"Content script in tab {tab_id_to_test} not ready" in log_message):
                error_logged = True
                break
        assert error_logged, "Error from extension about content script not ready was not logged by service.py for get_state"

    @pytest.mark.asyncio
    async def test_execute_action_waits_for_readiness_and_succeeds(self, extension_interface, mock_websocket):
        """Test that execute_action succeeds if background.js reports content script ready"""
        tab_id_to_test = 789
        action_to_execute = ActionPayload(action="click", params={"element_id": "btn-1"})
        request_id_sent_from_python = None

        async def send_side_effect(message_str):
            nonlocal request_id_sent_from_python
            message_obj = json.loads(message_str)
            request_id_sent_from_python = message_obj.get("id")
            if message_obj.get("type") == "execute_action":
                response_from_extension = {
                    "type": "response",
                    "id": request_id_sent_from_python,
                    "data": {
                        "success": True,
                        "result": "Action click completed on btn-1"
                    }
                }
                extension_interface.pending_requests[request_id_sent_from_python].set_result(response_from_extension)
            return None

        mock_websocket.send.side_effect = send_side_effect
        
        result = await extension_interface.execute_action(tab_id=tab_id_to_test, action_payload=action_to_execute)
        
        assert result is not None
        assert result.get("success") is True
        assert result.get("result") == "Action click completed on btn-1"

        execute_action_call_args = None
        for call in mock_websocket.send.call_args_list:
            sent_message = json.loads(call[0][0])
            if sent_message.get("type") == "execute_action":
                execute_action_call_args = sent_message
                break
        assert execute_action_call_args is not None
        assert execute_action_call_args["data"]["action"] == "click"
        assert execute_action_call_args["data"]["params"]["element_id"] == "btn-1"
        assert execute_action_call_args["data"]["tabId"] == tab_id_to_test

    @pytest.mark.asyncio
    async def test_execute_action_fails_if_content_script_not_ready(self, extension_interface, mock_websocket):
        """Test execute_action failure if background.js indicates content script not ready"""
        tab_id_to_test = 101
        action_to_execute = ActionPayload(action="input", params={"element_id": "text-1", "text": "hello"})
        request_id_sent_from_python = None

        async def send_side_effect(message_str):
            nonlocal request_id_sent_from_python
            message_obj = json.loads(message_str)
            request_id_sent_from_python = message_obj.get("id")
            if message_obj.get("type") == "execute_action":
                response_from_extension = {
                    "type": "response",
                    "id": request_id_sent_from_python,
                    "data": {
                        "success": False,
                        "error": f"Content script in tab {tab_id_to_test} not ready for execute_action"
                    }
                }
                extension_interface.pending_requests[request_id_sent_from_python].set_result(response_from_extension)
            return None

        mock_websocket.send.side_effect = send_side_effect

        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            result = await extension_interface.execute_action(tab_id=tab_id_to_test, action_payload=action_to_execute)

        assert result is not None
        assert result.get("success") is False
        assert f"Content script in tab {tab_id_to_test} not ready" in result.get("error", "")
        
        error_logged = False
        for call_args in mock_logger.error.call_args_list:
            log_message = call_args[0][0]
            # Corrected the multi-line condition using parentheses for implicit continuation
            if (f"Error from extension during execute_action for tab {tab_id_to_test}" in log_message and 
                f"Content script in tab {tab_id_to_test} not ready" in log_message):
                error_logged = True
                break
        assert error_logged, "Error from extension about content script not ready was not logged by service.py for execute_action"

    # Comments from original PERPLEXITY_OUTPUT.md regarding JS tests moved/covered by JS test files.
    # Python ExtensionInterface doesn't have wait_for_content_script_ready; it's implicit in background.js.

    # The PERPLEXITY_OUTPUT.md test `