import asyncio
import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch

from browser_use_ext.extension_interface.service import ExtensionInterface, ResponseData, ConnectionInfo
from browser_use_ext.extension_interface.models import Message
from browser_use_ext.browser.views import BrowserState, TabInfo
from browser_use_ext.dom.views import DOMDocumentNode


@pytest_asyncio.fixture
async def interface():
    """Fixture to create an ExtensionInterface instance and manage its server lifecycle."""
    iface = ExtensionInterface(host="127.0.0.1", port=8768)  # Use a different port for testing
    await iface.start_server()
    await asyncio.sleep(0.1)  # Give server a moment to be ready
    
    yield iface

    # Teardown: close the server
    await iface.close()
    await asyncio.sleep(0.1)  # Small delay to ensure resources are released


@pytest.mark.asyncio
async def test_get_state_full_integration():
    """Integration test: Tests full get_state flow with simulated WebSocket communication."""
    iface = ExtensionInterface(host="localhost", port=8769)
    
    # Mock websocket and connection setup
    mock_websocket = AsyncMock()
    client_id = "test_client_integration"
    
    # Set up the connection properly
    mock_conn_info = ConnectionInfo(client_id=client_id, websocket=mock_websocket, handler_task=asyncio.current_task())
    iface._connections[client_id] = mock_conn_info
    iface._active_connection_id = client_id
    iface._active_tab_id = 1
    
    # Expected response data from the "extension"
    expected_response_data = {
        "url": "http://integration-test.com",
        "title": "Integration Test Page",
        "tabs": [{"tabId": 1, "url": "http://integration-test.com", "title": "Integration Test Page", "isActive": True}],
        "screenshot": "data:image/png;base64,testdata",
        "tree": {"type": "document", "children": []},
        "selector_map": {0: {"xpath": "//html"}},
        "pixels_above": 5,
        "pixels_below": 200
    }
    
    request_id_sent = None
    
    # Mock websocket.send to capture the sent message and simulate response
    async def mock_send_with_response(message_str):
        nonlocal request_id_sent
        sent_message = json.loads(message_str)
        request_id_sent = sent_message.get("id")
        
        # Verify the request structure
        assert sent_message["type"] == "get_state"
        assert sent_message["data"]["action"] == "get_state"
        assert sent_message["data"]["params"]["for_vision"] is True
        
        # Schedule a response to be processed
        async def send_response():
            await asyncio.sleep(0.01)  # Small delay to simulate network
            
            response_message = Message(
                type="response",
                id=request_id_sent,
                data={
                    "success": True,
                    **expected_response_data
                }
            )
            
            # Process the response as if it came from the extension
            await iface._process_message(client_id, response_message.model_dump_json())
        
        # Schedule the response
        asyncio.create_task(send_response())
    
    mock_websocket.send.side_effect = mock_send_with_response
    
    # Mock _wait_for_content_script_ready to avoid that complexity
    with patch.object(iface, '_wait_for_content_script_ready', new_callable=AsyncMock):
        
        # Call the method under test
        result = await iface.get_state(for_vision=True, tab_id=1)
        
        # Verify the result
        assert isinstance(result, BrowserState)
        assert result.url == "http://integration-test.com"
        assert result.title == "Integration Test Page"
        assert len(result.tabs) == 1
        assert result.tabs[0].tabId == 1
        assert result.tabs[0].url == "http://integration-test.com"
        assert result.screenshot == "data:image/png;base64,testdata"
        assert result.pixels_above == 5
        assert result.pixels_below == 200
        
        # Verify websocket.send was called
        mock_websocket.send.assert_awaited_once()
        
        # Verify the request was properly handled and cleaned up
        assert request_id_sent is not None
        assert request_id_sent not in iface._pending_requests  # Should be cleaned up after processing


@pytest.mark.asyncio 
async def test_get_state_integration_error_response():
    """Integration test: Tests get_state handling of error responses."""
    iface = ExtensionInterface(host="localhost", port=8770)
    
    # Mock websocket and connection setup
    mock_websocket = AsyncMock()
    client_id = "test_client_error"
    
    mock_conn_info = ConnectionInfo(client_id=client_id, websocket=mock_websocket, handler_task=asyncio.current_task())
    iface._connections[client_id] = mock_conn_info
    iface._active_connection_id = client_id
    iface._active_tab_id = 1
    
    request_id_sent = None
    
    # Mock websocket.send to simulate error response
    async def mock_send_with_error(message_str):
        nonlocal request_id_sent
        sent_message = json.loads(message_str)
        request_id_sent = sent_message.get("id")
        
        # Schedule an error response
        async def send_error_response():
            await asyncio.sleep(0.01)
            
            error_message = Message(
                type="response", 
                id=request_id_sent,
                data={
                    "success": False,
                    "error": "Content script not ready"
                }
            )
            
            await iface._process_message(client_id, error_message.model_dump_json())
        
        asyncio.create_task(send_error_response())
    
    mock_websocket.send.side_effect = mock_send_with_error
    
    # Mock _wait_for_content_script_ready to avoid that complexity  
    with patch.object(iface, '_wait_for_content_script_ready', new_callable=AsyncMock):
        
        # Call the method and expect an error
        with pytest.raises(RuntimeError) as exc_info:
            await iface.get_state(for_vision=False, tab_id=1)
        
        # Verify the error message contains the extension error
        assert "Content script not ready" in str(exc_info.value)
        
        # Verify websocket.send was called
        mock_websocket.send.assert_awaited_once()
        
        # Verify cleanup happened
        assert request_id_sent not in iface._pending_requests


@pytest.mark.asyncio
async def test_get_state_integration_timeout():
    """Integration test: Tests get_state timeout when no response is received."""
    iface = ExtensionInterface(host="localhost", port=8771)
    
    # Mock websocket and connection setup  
    mock_websocket = AsyncMock()
    client_id = "test_client_timeout"
    
    mock_conn_info = ConnectionInfo(client_id=client_id, websocket=mock_websocket, handler_task=asyncio.current_task())
    iface._connections[client_id] = mock_conn_info
    iface._active_connection_id = client_id
    iface._active_tab_id = 1
    
    # Mock websocket.send to NOT send any response (simulating timeout)
    mock_websocket.send.side_effect = AsyncMock()
    
    # Mock _wait_for_content_script_ready to avoid that complexity
    with patch.object(iface, '_wait_for_content_script_ready', new_callable=AsyncMock):
        
        # Call the method with a short timeout and expect timeout error
        with pytest.raises(RuntimeError) as exc_info:
            await iface.get_state(for_vision=False, tab_id=1)
        
        # Verify the error indicates a timeout
        assert "timed out" in str(exc_info.value).lower()
        
        # Verify websocket.send was called
        mock_websocket.send.assert_awaited_once()