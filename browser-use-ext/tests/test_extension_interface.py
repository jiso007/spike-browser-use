import asyncio
import json
import pytest
import pytest_asyncio
import websockets # Added missing import
from unittest.mock import MagicMock, AsyncMock, patch # For async mocking

from websockets.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK, ConnectionClosed

# Adjust imports based on the new project structure `browser-use-ext`
from extension_interface.service import (
    ExtensionInterface,
    RequestMessage,
    ResponseMessage,
    ResponseData,
    ConnectionInfo
)
from browser.views import BrowserState, TabInfo
from dom.views import DOMElementNode

@pytest_asyncio.fixture
async def interface():
    """Fixture to create an ExtensionInterface instance and manage its server lifecycle."""
    iface = ExtensionInterface(host="127.0.0.1", port=8766) # Use a different port for testing
    server_task = asyncio.create_task(iface.start_server(), name=f"TestExtInterfaceServer-{iface.port}")
    await asyncio.sleep(0.2) # Increased delay for server startup
    if not iface.is_server_running:
        # Attempt to wait a bit longer if the server isn't up yet
        await asyncio.sleep(0.5)
        if not iface.is_server_running:
            # If it's still not running, force cleanup and fail the test setup
            if not server_task.done():
                server_task.cancel()
                try: await server_task
                except asyncio.CancelledError: pass
            pytest.fail(f"Test server on port {iface.port} failed to start.")
    yield iface
    # Teardown: stop the server and wait for the task to complete
    await iface.stop_server()
    if not server_task.done():
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass # Expected on cancellation
    await asyncio.sleep(0.2) # Ensure resources are released

@pytest.mark.asyncio
async def test_server_start_and_stop(interface: ExtensionInterface):
    """Test that the WebSocket server starts and stops correctly."""
    assert interface.is_server_running, "Server should be running after start_server() call in fixture"
    # has_active_connection depends on a client connecting, not part of this test directly.
    # initial_active_conn = interface.has_active_connection
    # assert not initial_active_conn, "Should be no active connections initially"

@pytest.mark.asyncio
async def test_handle_connection_and_disconnection(interface: ExtensionInterface):
    """Test that a client can connect and disconnect, updating active_connection status."""
    assert interface.is_server_running, "Server must be running for client to connect."
    initial_connections_count = len(interface._connections)
    initial_active_id = interface._active_connection_id

    async def client_connect_and_close():
        try:
            # Connect client to the server started by the 'interface' fixture
            async with websockets.connect(f"ws://{interface.host}:{interface.port}") as ws_client:
                await asyncio.sleep(0.2) # Give server time to process connection
                assert interface.has_active_connection, "Interface should have an active connection after client connects"
                assert len(interface._connections) > initial_connections_count, "Connection count should increase"
                assert interface._active_connection_id is not None, "Active connection ID should be set"
                # Client automatically closes connection when exiting `async with`
        except Exception as e:
            pytest.fail(f"Client connection failed: {e}")

    connect_task = asyncio.create_task(client_connect_and_close())
    try:
        await asyncio.wait_for(connect_task, timeout=5.0)
    except asyncio.TimeoutError:
        pytest.fail("Client connect and close task timed out.")

    await asyncio.sleep(0.3) # Allow server time to process disconnection
    assert not interface.has_active_connection, "Interface should not have an active connection after client disconnects"
    assert len(interface._connections) == initial_connections_count, "Connection count should revert"
    # Depending on logic, active_connection_id might be None or another if multiple clients were involved.
    # For a single client, it should likely become None.
    if initial_active_id is None: # if it started as None, and only one client connected and disconnected.
        assert interface._active_connection_id is None, "Active connection ID should be None after single client disconnects"

@pytest.mark.asyncio
async def test_send_request_and_receive_response(interface: ExtensionInterface):
    """Test sending a request to a mock client and receiving its response."""
    
    # This test is complex because it involves mocking the client-side behavior 
    # that responds to requests from the ExtensionInterface.
    # The ExtensionInterface._handle_connection is the server-side part that receives client messages.
    # The ExtensionInterface._send_request is the part that sends messages to the client.

    # We need a real client to connect so _send_request can proceed.
    # This client will also act as the responder.

    request_id_seen_by_client = None
    response_future = asyncio.Future()

    async def mock_client_responder(ws_client: WebSocketServerProtocol):
        nonlocal request_id_seen_by_client
        try:
            message_str = await ws_client.recv() # Wait for the server's request
            req_data = json.loads(message_str)
            request_id_seen_by_client = req_data["id"]
            assert req_data["type"] == "test_type_action" # Corrected: type is request_type
            assert req_data["data"] == {"param1": "value1"} # Corrected: params are in data field
            
            response_payload = {
                "id": req_data["id"],
                "type": "response",
                "data": {"success": True, "result": "mock_success"} # ensure data field for ResponseData model
            }
            await ws_client.send(json.dumps(response_payload))
            response_future.set_result(None) # Signal response sent
        except ConnectionClosed:
            if not response_future.done():
                response_future.set_exception(ConnectionClosed("Client connection closed before responding", None))
        except Exception as e:
            if not response_future.done():
                response_future.set_exception(e)
            pytest.fail(f"Mock client responder error: {e}")

    client_task = None
    async def client_main_task():
        try:
            async with websockets.connect(f"ws://{interface.host}:{interface.port}") as ws_client:
                await asyncio.sleep(0.1) # ensure server registers connection
                if not interface.has_active_connection: await asyncio.sleep(0.3)
                assert interface.has_active_connection, "Test client connected, server should have active connection."
                await mock_client_responder(ws_client) # This client will handle one request/response
        except Exception as e:
            if not response_future.done():
                response_future.set_exception(e)

    client_task = asyncio.create_task(client_main_task())

    try:
        # Wait for client to be ready (connected and server acknowledges)
        await asyncio.sleep(0.5) 
        assert interface.has_active_connection, "Server should be ready to send request to connected client."

        # Now, call _send_request. The connected mock_client_responder should handle it.
        response_data_obj = await interface._send_request(request_type="test_type_action", data={"param1": "value1"}, timeout=3.0)
        
        assert isinstance(response_data_obj, ResponseData)
        assert response_data_obj.success is True
        # The actual data is nested within the ResponseData model if structure is {success:true, result: "mock_success"}
        # If ResponseData is just {success: true, error: null}, then response_data_obj would be that.
        # Based on mock_client_responder, it sends {"result": "mock_success"} inside data.
        # So, response_data_obj will be a ResponseData model where response_data_obj.result exists IF defined in ResponseData model.
        # Current ResponseData allows extra fields. Let's assume we want to check that specific field.
        assert response_data_obj.model_extra["result"] == "mock_success"

        # Check that the client actually processed a request with a valid ID
        await asyncio.wait_for(response_future, timeout=1.0) # Ensure client finished its part
        assert request_id_seen_by_client is not None
        assert isinstance(request_id_seen_by_client, int)

    except Exception as e:
        pytest.fail(f"_send_request test failed: {e}")
    finally:
        if client_task and not client_task.done():
            client_task.cancel()
            try: await client_task
            except asyncio.CancelledError: pass
        await asyncio.sleep(0.1) # Allow for cleanup

@pytest.mark.asyncio
async def test_get_state_parsing(interface: ExtensionInterface):
    """Test the parsing of a get_state response, focusing on _parse_element_tree_data."""
    mock_response_payload = {
        # This is the structure for the *data* field of a ResponseMessage
        "success": True,
        "url": "http://example.com",
        "title": "Example Page",
        "tabs": [
            {"page_id": 1, "url": "http://example.com", "title": "Example"},
            {"page_id": 2, "url": "http://test.com", "title": "Test Page"}
        ],
        "element_tree": {
            "type": "element", "tag_name": "html", "attributes": {"lang": "en"}, "xpath": "/html", "is_visible": True,
            "children": [
                {"type": "element", "tag_name": "body", "attributes": {}, "xpath": "/html/body", "is_visible": True, "children": [
                    {"type": "element", "tag_name": "div", "attributes": {"id": "main"}, "highlight_index": 0, "xpath": "/html/body/div[1]", "is_visible": True, "text": "Hello"}
                ]}
            ]
        },
        "selector_map": {"0": {"xpath": "/html/body/div[1]"}},
        "screenshot": "data:image/png;base64,fakedata",
        "pixels_above": 10, 
        "pixels_below": 100
    }
    # _send_request returns a ResponseData object
    interface._send_request = AsyncMock(return_value=ResponseData.model_validate(mock_response_payload))

    browser_state = await interface.get_state()

    assert browser_state is not None
    assert isinstance(browser_state, BrowserState)
    assert browser_state.url == "http://example.com"
    assert browser_state.title == "Example Page"
    assert len(browser_state.tabs) == 2
    assert isinstance(browser_state.tabs[0], TabInfo)
    assert browser_state.tabs[0].url == "http://example.com"

    assert browser_state.element_tree is not None
    assert isinstance(browser_state.element_tree, DOMElementNode)
    assert browser_state.element_tree.tag_name == "html"
    assert browser_state.element_tree.type == "element"
    assert len(browser_state.element_tree.children) == 1
    body_node = browser_state.element_tree.children[0]
    assert body_node.tag_name == "body"
    assert len(body_node.children) == 1
    div_node = body_node.children[0]
    assert div_node.tag_name == "div"
    assert div_node.attributes["id"] == "main"
    # Text is not a direct attribute of DOMElementNode in this parsed model unless it's a text node itself.
    # If the extension puts text content directly on an element node, it needs to be mapped. 
    # Current DOMElementNode has an optional text field. The mock data has this. If parsing sets it, it will be there.
    # The current _parse_element_tree_data in ExtensionInterface does NOT assign 'text' to element nodes.
    # It expects 'text' field for type='text' nodes. Let's adjust mock or parsing.
    # For now, assuming _parse_element_tree_data gets `text` for the div if `type` is element and text is present.
    # Based on current _parse_element_tree_data, this text will be ignored for type="element".
    # For test to pass with current code, mock data for element_tree.div should not have "text":"Hello"
    # OR _parse_element_tree_data should handle text for elements.
    # Let's assume the mock element tree is what the extension *could* send, and parsing should improve.
    # For now, this test will fail on div_node.text if _parse_element_tree_data doesn't handle it for elements.
    # Let's assume the `text` field on DOMElementNode is for text nodes, or direct text of an element.
    # Adjusting `_parse_element_tree_data` is better. For now, let this test highlight it.
    # Ok, `DOMElementNode` has `text: Optional[str]`. `_parse_element_tree_data` does not explicitly set it for elements.
    # The Pydantic model will pick it up if `text` is in `element_data` and it's a valid field.
    # Let's ensure the mock data for the div has type: "element".
    assert div_node.text == "Hello" 
    assert div_node.highlight_index == 0
    assert div_node.xpath == "/html/body/div[1]"
    assert browser_state.screenshot == "data:image/png;base64,fakedata"
    assert browser_state.selector_map == {0: {"xpath": "/html/body/div[1]"}} # Keys should be int
    assert browser_state.pixels_above == 10
    assert browser_state.pixels_below == 100

@pytest.mark.asyncio
async def test_execute_action(interface: ExtensionInterface):
    """Test the execute_action method."""
    expected_action_payload = {"success": True, "status": "some_action_status", "details": "action_completed"}
    # _send_request should return a ResponseData object
    interface._send_request = AsyncMock(return_value=ResponseData.model_validate(expected_action_payload))
    
    action_to_execute = "do_something"
    action_params = {"param_x": "value_x"}
    
    # Call execute_action with `action` not `action_name`
    result_dict = await interface.execute_action(action=action_to_execute, params=action_params)
    
    # execute_action returns a dict (model_dump of ResponseData)
    assert result_dict["success"] is True
    assert result_dict["status"] == "some_action_status"
    assert result_dict["details"] == "action_completed"

    # Verify that _send_request was called with the correct structure for execute_action
    interface._send_request.assert_called_once_with(
        request_type="execute_action", 
        data={"action": action_to_execute, "params": action_params}, 
        timeout=30.0 # Default timeout from execute_action method
    )

@pytest.mark.asyncio
async def test_send_request_timeout(interface: ExtensionInterface):
    """Test that _send_request correctly raises TimeoutError if the future times out."""
    
    client_connected_event = asyncio.Event()
    client_task = None

    async def non_responsive_client_main():
        try:
            # This client connects but never sends a response, forcing a timeout on the server.
            async with websockets.connect(f"ws://{interface.host}:{interface.port}") as ws_client:
                # Connection established. The server now has this in its _connections.
                # Set active_connection_id on the interface if it's the first one (done by _handle_connection).
                client_connected_event.set() # Signal that client is connected
                await ws_client.wait_closed() # Keep connection open indefinitely
        except ConnectionClosedOK:
            pass # Expected if server closes it during test cleanup
        except Exception as e:
            if not client_connected_event.is_set(): # If failed before setting event
                 client_connected_event.set() # Unblock the test, though it will fail
            # Don't fail test here, primary test is for server timeout
            print(f"NonResponsiveClient error: {e}") 
        finally:
            if not client_connected_event.is_set():
                client_connected_event.set() # Ensure main test proceeds

    client_task = asyncio.create_task(non_responsive_client_main())
    
    try:
        await asyncio.wait_for(client_connected_event.wait(), timeout=3.0)
        await asyncio.sleep(0.2) # Ensure server has processed the connection
        assert interface.has_active_connection, "Client should be connected and active connection set by server"

        with pytest.raises(TimeoutError):
            # Use a short timeout for the request itself to trigger the error quickly
            await interface._send_request(request_type="timeout_action", data={}, timeout=0.1)
    finally:
        if client_task and not client_task.done():
            client_task.cancel()
            try: await client_task
            except asyncio.CancelledError: pass
        await asyncio.sleep(0.1) # Allow for cleanup