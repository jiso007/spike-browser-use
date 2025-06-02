"""Fixed end-to-end integration tests for user input functionality."""

import asyncio
import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.extension_interface.models import ConnectionInfo, Message
from browser_use_ext.browser.context import BrowserContext, BrowserContextConfig
from browser_use_ext.controller.service import Controller
from browser_use_ext.agent.service import Agent
from browser_use_ext.dom.views import DOMState, ActionableElement


# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


class MockWebSocketServer:
    """Mock WebSocket server for testing."""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connections = []
        self.messages = []
        self.is_running = False
    
    async def accept_connection(self, websocket, path):
        """Accept a mock connection."""
        self.connections.append(websocket)
        self.is_running = True
    
    async def close(self):
        """Close the mock server."""
        self.is_running = False
        for conn in self.connections:
            if hasattr(conn, 'close'):
                await conn.close()


class TestUserInputE2EIntegrationFixed:
    """Test the complete flow from popup input to agent action execution."""

    @pytest_asyncio.fixture
    async def mock_extension_interface(self):
        """Create a fully mocked extension interface server."""
        interface = ExtensionInterface(host="localhost", port=8768)
        
        # Mock the WebSocket server
        interface._server = MockWebSocketServer("localhost", 8768)
        interface._connections = {}
        interface._active_connection_id = None
        interface._active_tab_id = None
        interface._server_task = None
        
        # Override server methods
        async def mock_start_server():
            interface._server.is_running = True
            interface._server_task = asyncio.create_task(asyncio.sleep(0))
        
        async def mock_close():
            if interface._server:
                await interface._server.close()
            if interface._server_task:
                interface._server_task.cancel()
                try:
                    await interface._server_task
                except asyncio.CancelledError:
                    pass
        
        interface.start_server = mock_start_server
        interface.close = mock_close
        
        await interface.start_server()
        
        yield interface
        
        await interface.close()

    @pytest_asyncio.fixture
    def mock_browser_context(self):
        """Create a comprehensive mock browser context."""
        context = MagicMock(spec=BrowserContext)
        context.config = BrowserContextConfig()
        
        # Mock get_state to return a realistic DOM state
        mock_state = DOMState(
            url="https://www.google.com",
            title="Google",
            tabs=1,
            actionable_elements=[
                ActionableElement(
                    highlight_index=1,
                    tag="input",
                    text="",
                    role="searchbox",
                    type="text",
                    attributes={"name": "q", "title": "Search"},
                    element_id="search-box"
                ),
                ActionableElement(
                    highlight_index=2,
                    tag="button",
                    text="Google Search",
                    role="button",
                    type="submit",
                    attributes={"name": "btnK"},
                    element_id="search-button"
                )
            ]
        )
        context.get_state = AsyncMock(return_value=mock_state)
        context.execute_action = AsyncMock(return_value={"success": True})
        
        return context

    @pytest.mark.asyncio
    async def test_complete_user_task_flow(self, mock_extension_interface, mock_browser_context):
        """Test the complete flow from user input to action execution."""
        # Create a mock WebSocket connection
        mock_websocket = AsyncMock()
        mock_websocket.send = AsyncMock()
        mock_websocket.recv = AsyncMock()
        mock_websocket.remote_address = ("127.0.0.1", 12345)
        
        # Establish connection
        conn_info = ConnectionInfo(
            client_id="test-client-e2e",
            websocket=mock_websocket,
            handler_task=None
        )
        mock_extension_interface._connections["test-client-e2e"] = conn_info
        mock_extension_interface._active_connection_id = "test-client-e2e"
        
        # Simulate user submitting a task from popup
        user_task_message = {
            "type": "extension_event",
            "id": 1001,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Search for Python tutorials on Google",
                "context": {
                    "url": "about:blank",
                    "title": "New Tab",
                    "tabId": 123,
                    "windowId": 1
                },
                "tabId": 123
            }
        }
        
        # Process the message
        task_processed = False
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            await mock_extension_interface._process_message("test-client-e2e", json.dumps(user_task_message))
            
            # Check that the task was logged
            for call in mock_logger.info.call_args_list:
                if "User submitted task from extension popup" in str(call):
                    task_processed = True
                    break
        
        assert task_processed, "Task was not processed"
        assert mock_extension_interface._active_tab_id == 123
        
        # Now test the full agent flow
        controller = Controller(browser_context=mock_browser_context)
        
        # Execute navigation
        nav_result = await controller.go_to_url("https://www.google.com")
        mock_browser_context.execute_action.assert_called_with(
            "navigate",
            {"url": "https://www.google.com"}
        )
        
        # Get state and find search box
        state = await mock_browser_context.get_state()
        assert len(state.actionable_elements) > 0
        
        # Find search box element
        search_box = None
        for element in state.actionable_elements:
            if element.attributes.get("name") == "q":
                search_box = element
                break
        
        assert search_box is not None
        
        # Click and type in search box
        await controller.click_element_by_index(search_box.highlight_index)
        await controller.input_text(search_box.highlight_index, "Python tutorials")
        
        # Verify actions were called
        assert mock_browser_context.execute_action.call_count >= 3

    @pytest.mark.asyncio
    async def test_concurrent_popup_connections(self, mock_extension_interface):
        """Test handling multiple concurrent popup connections."""
        connections = []
        
        # Create 3 mock connections
        for i in range(3):
            mock_ws = AsyncMock()
            mock_ws.send = AsyncMock()
            mock_ws.remote_address = ("127.0.0.1", 12345 + i)
            
            conn_info = ConnectionInfo(
                client_id=f"popup-{i}",
                websocket=mock_ws,
                handler_task=None
            )
            
            mock_extension_interface._connections[f"popup-{i}"] = conn_info
            connections.append(conn_info)
        
        # Set first as active
        mock_extension_interface._active_connection_id = "popup-0"
        
        # Submit tasks from different popups
        for i in range(3):
            task = {
                "type": "extension_event",
                "id": 2000 + i,
                "data": {
                    "event_name": "user_task_submitted",
                    "task": f"Task from popup {i}",
                    "context": {"tabId": 200 + i},
                    "tabId": 200 + i
                }
            }
            
            await mock_extension_interface._process_message(f"popup-{i}", json.dumps(task))
            
            # Verify tab update
            assert mock_extension_interface._active_tab_id == 200 + i
        
        # All connections should still exist
        assert len(mock_extension_interface._connections) == 3

    @pytest.mark.asyncio
    async def test_complex_task_execution(self, mock_extension_interface, mock_browser_context):
        """Test execution of a complex multi-step task."""
        # Setup connection
        mock_ws = AsyncMock()
        conn_info = ConnectionInfo(
            client_id="complex-task-client",
            websocket=mock_ws,
            handler_task=None
        )
        mock_extension_interface._connections["complex-task-client"] = conn_info
        mock_extension_interface._active_connection_id = "complex-task-client"
        
        # Submit complex task
        complex_task = {
            "type": "extension_event",
            "id": 3001,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Go to Amazon, search for 'laptop', and filter by price under $500",
                "context": {
                    "url": "https://www.google.com",
                    "title": "Google",
                    "tabId": 301
                },
                "tabId": 301
            }
        }
        
        await mock_extension_interface._process_message("complex-task-client", json.dumps(complex_task))
        
        # Create controller
        controller = Controller(browser_context=mock_browser_context)
        
        # Simulate the steps an agent would take
        steps = [
            ("navigate", {"url": "https://www.amazon.com"}),
            ("click", {"element_id": "twotabsearchtextbox"}),
            ("input_text", {"element_id": "twotabsearchtextbox", "text": "laptop"}),
            ("click", {"element_id": "nav-search-submit-button"}),
            ("click", {"element_id": "price-filter-500"})
        ]
        
        # Execute each step
        for i, (action, params) in enumerate(steps):
            mock_browser_context.execute_action.return_value = {
                "success": True,
                "data": {"message": f"Step {i+1} completed"}
            }
            
            # Call the appropriate controller method
            if action == "navigate":
                await controller.go_to_url(params["url"])
            elif action == "click":
                await controller.click_element_by_index(1)  # Mock index
            elif action == "input_text":
                await controller.input_text(1, params["text"])
        
        # Verify all actions were executed
        assert mock_browser_context.execute_action.call_count >= len(steps)

    @pytest.mark.asyncio
    async def test_error_recovery_scenarios(self, mock_extension_interface):
        """Test various error scenarios and recovery."""
        mock_ws = AsyncMock()
        conn_info = ConnectionInfo(
            client_id="error-test",
            websocket=mock_ws,
            handler_task=None
        )
        mock_extension_interface._connections["error-test"] = conn_info
        mock_extension_interface._active_connection_id = "error-test"
        
        # Test 1: Invalid JSON
        try:
            await mock_extension_interface._process_message("error-test", "invalid{json")
        except json.JSONDecodeError:
            pass  # Expected
        
        # Connection should still be active
        assert "error-test" in mock_extension_interface._connections
        
        # Test 2: Missing required fields
        incomplete_task = {
            "type": "extension_event",
            "id": 4001,
            "data": {
                "event_name": "user_task_submitted",
                # Missing "task" field
                "tabId": 401
            }
        }
        
        # Should handle gracefully
        await mock_extension_interface._process_message("error-test", json.dumps(incomplete_task))
        
        # Test 3: Valid task after errors
        valid_task = {
            "type": "extension_event",
            "id": 4002,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Valid task after errors",
                "context": {"tabId": 402},
                "tabId": 402
            }
        }
        
        await mock_extension_interface._process_message("error-test", json.dumps(valid_task))
        assert mock_extension_interface._active_tab_id == 402

    @pytest.mark.asyncio
    async def test_connection_lifecycle(self, mock_extension_interface):
        """Test full connection lifecycle from connect to disconnect."""
        # Phase 1: Connection establishment
        mock_ws = AsyncMock()
        mock_ws.remote_address = ("127.0.0.1", 12345)
        
        conn_info = ConnectionInfo(
            client_id="lifecycle-test",
            websocket=mock_ws,
            handler_task=None
        )
        
        mock_extension_interface._connections["lifecycle-test"] = conn_info
        mock_extension_interface._active_connection_id = "lifecycle-test"
        
        assert mock_extension_interface.has_active_connection
        
        # Phase 2: Task submission
        task = {
            "type": "extension_event",
            "id": 5001,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Test lifecycle task",
                "context": {"tabId": 501},
                "tabId": 501
            }
        }
        
        await mock_extension_interface._process_message("lifecycle-test", json.dumps(task))
        assert mock_extension_interface._active_tab_id == 501
        
        # Phase 3: Disconnection
        await mock_extension_interface._remove_client("lifecycle-test")
        
        assert "lifecycle-test" not in mock_extension_interface._connections
        assert mock_extension_interface._active_connection_id is None
        assert not mock_extension_interface.has_active_connection
        
        # Phase 4: Reconnection
        new_ws = AsyncMock()
        new_ws.remote_address = ("127.0.0.1", 12346)
        
        new_conn = ConnectionInfo(
            client_id="lifecycle-test-2",
            websocket=new_ws,
            handler_task=None
        )
        
        mock_extension_interface._connections["lifecycle-test-2"] = new_conn
        mock_extension_interface._active_connection_id = "lifecycle-test-2"
        
        assert mock_extension_interface.has_active_connection
        assert mock_extension_interface._active_connection_id == "lifecycle-test-2"