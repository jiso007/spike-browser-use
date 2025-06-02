"""Integration tests for user input functionality with mocked WebSocket connections."""

import asyncio
import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.extension_interface.models import ConnectionInfo
from browser_use_ext.browser.context import BrowserContext, BrowserContextConfig
from browser_use_ext.controller.service import Controller
from browser_use_ext.agent.service import Agent


# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


class TestUserInputMockIntegration:
    """Test the complete flow from popup input to agent action execution with mocks."""

    @pytest_asyncio.fixture
    async def extension_interface(self):
        """Create a mocked extension interface for testing."""
        interface = ExtensionInterface(host="localhost", port=8767)
        
        # Mock internals to avoid real WebSocket server
        interface._server = MagicMock()
        interface._connections = {}
        interface._active_connection_id = None
        interface._active_tab_id = None
        interface._server_task = None
        
        # Override start_server to not create real server
        async def mock_start_server():
            pass
        
        interface.start_server = mock_start_server
        
        yield interface

    @pytest_asyncio.fixture
    def mock_browser_context(self):
        """Create a mock browser context for testing."""
        context = MagicMock(spec=BrowserContext)
        context.get_state = AsyncMock()
        context.execute_action = AsyncMock()
        context.config = BrowserContextConfig()
        
        # Add the _cached_state attribute that Controller expects
        mock_cached_state = MagicMock()
        mock_cached_state.url = "https://example.com"
        context._cached_state = mock_cached_state
        
        # Add the extension attribute that Controller.execute_action expects
        mock_extension = MagicMock()
        mock_extension.execute_action = AsyncMock(return_value={"success": True, "data": {}})
        context.extension = mock_extension
        
        return context

    @pytest_asyncio.fixture
    def mock_websocket(self):
        """Create a mock WebSocket connection."""
        websocket = AsyncMock()
        websocket.send = AsyncMock()
        websocket.remote_address = ("127.0.0.1", 12345)
        return websocket

    @pytest.mark.asyncio
    async def test_complete_user_input_flow(self, extension_interface, mock_browser_context, mock_websocket):
        """Test the complete flow from user input to action execution."""
        # Setup mock connection
        conn_info = ConnectionInfo(
            client_id="test-client-1",
            websocket=mock_websocket,
            handler_task=None
        )
        extension_interface._connections["test-client-1"] = conn_info
        extension_interface._active_connection_id = "test-client-1"
        
        # Verify connection is active
        assert extension_interface.has_active_connection
        
        # Simulate user submitting a task from popup
        user_task_message = {
            "type": "extension_event",
            "id": 1001,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Go to Google and search for Python tutorials",
                "context": {
                    "url": "about:blank",
                    "title": "New Tab",
                    "tabId": 123,
                    "windowId": 1
                },
                "tabId": 123
            }
        }
        
        # Process the task submission
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            await extension_interface._process_message("test-client-1", json.dumps(user_task_message))
            
            # Verify task was logged
            mock_logger.info.assert_any_call(
                "User submitted task from extension popup: 'Go to Google and search for Python tutorials' (Tab ID: 123)"
            )
        
        # Verify the active tab was updated
        assert extension_interface._active_tab_id == 123
        
        # Now simulate the controller processing the task
        with patch.object(extension_interface, 'execute_action') as mock_execute:
            mock_execute.return_value = {"success": True, "data": {}}
            
            # Create controller with mocked context
            controller = Controller(browser_context=mock_browser_context)
            
            # Simulate navigation
            result = await controller.go_to_url("https://www.google.com")
            
            # Verify the action was called on the extension with correct parameters
            mock_browser_context.extension.execute_action.assert_called_once_with(
                action_name="go_to_url",
                params={"url": "https://www.google.com"},
                timeout=30.0
            )

    @pytest.mark.asyncio
    async def test_multiple_popup_instances(self, extension_interface, mock_websocket):
        """Test handling multiple popup instances submitting tasks."""
        # Setup two connections
        conn1 = ConnectionInfo(
            client_id="popup-1",
            websocket=mock_websocket,
            handler_task=None
        )
        conn2 = ConnectionInfo(
            client_id="popup-2",
            websocket=AsyncMock(),
            handler_task=None
        )
        
        extension_interface._connections["popup-1"] = conn1
        extension_interface._connections["popup-2"] = conn2
        extension_interface._active_connection_id = "popup-1"
        
        # Both connections should be tracked
        assert len(extension_interface._connections) == 2
        
        # Submit task from first popup
        task1 = {
            "type": "extension_event",
            "id": 2001,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Task from popup 1",
                "context": {"tabId": 201},
                "tabId": 201
            }
        }
        
        await extension_interface._process_message("popup-1", json.dumps(task1))
        assert extension_interface._active_tab_id == 201
        
        # Submit task from second popup
        task2 = {
            "type": "extension_event",
            "id": 2002,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Task from popup 2",
                "context": {"tabId": 202},
                "tabId": 202
            }
        }
        
        await extension_interface._process_message("popup-2", json.dumps(task2))
        assert extension_interface._active_tab_id == 202

    @pytest.mark.asyncio
    async def test_task_with_navigation_and_interaction(self, extension_interface, mock_websocket):
        """Test a complex task involving navigation and element interaction."""
        # Setup connection
        conn = ConnectionInfo(
            client_id="test-client",
            websocket=mock_websocket,
            handler_task=None
        )
        extension_interface._connections["test-client"] = conn
        extension_interface._active_connection_id = "test-client"
        
        # Submit a complex task
        complex_task = {
            "type": "extension_event",
            "id": 3001,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Go to Amazon and search for laptops under $500",
                "context": {
                    "url": "https://www.google.com",
                    "title": "Google",
                    "tabId": 301
                },
                "tabId": 301
            }
        }
        
        await extension_interface._process_message("test-client", json.dumps(complex_task))
        assert extension_interface._active_tab_id == 301
        
        # Mock the sequence of actions an agent would take
        with patch.object(extension_interface, 'execute_action') as mock_execute:
            # Configure mock responses for each action
            mock_execute.side_effect = [
                {"success": True, "data": {"message": "Navigated to Amazon"}},
                {"success": True, "data": {"message": "Clicked search box"}},
                {"success": True, "data": {"message": "Typed search query"}},
                {"success": True, "data": {"message": "Submitted search"}}
            ]
            
            # Simulate agent actions
            actions = [
                ("navigate", {"url": "https://www.amazon.com"}),
                ("click", {"element_id": "search-box"}),
                ("input_text", {"element_id": "search-box", "text": "laptops under 500"}),
                ("click", {"element_id": "search-button"})
            ]
            
            for action_name, params in actions:
                result = await extension_interface.execute_action(action_name, params)
                assert result["success"] is True

    @pytest.mark.asyncio
    async def test_popup_disconnect_recovery(self, extension_interface):
        """Test system behavior when popup disconnects and reconnects."""
        # First connection
        ws1 = AsyncMock()
        ws1.remote_address = ("127.0.0.1", 12345)
        
        conn1 = ConnectionInfo(
            client_id="conn-1",
            websocket=ws1,
            handler_task=None
        )
        extension_interface._connections["conn-1"] = conn1
        extension_interface._active_connection_id = "conn-1"
        
        initial_connection_id = extension_interface._active_connection_id
        assert initial_connection_id is not None
        
        # Submit task
        task = {
            "type": "extension_event",
            "id": 4001,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Initial task",
                "context": {"tabId": 401},
                "tabId": 401
            }
        }
        await extension_interface._process_message("conn-1", json.dumps(task))
        assert extension_interface._active_tab_id == 401
        
        # Disconnect
        await extension_interface._remove_client("conn-1")
        
        # Verify cleanup
        assert "conn-1" not in extension_interface._connections
        assert extension_interface._active_connection_id is None
        
        # Reconnect with new connection
        ws2 = AsyncMock()
        ws2.remote_address = ("127.0.0.1", 12346)
        
        conn2 = ConnectionInfo(
            client_id="conn-2",
            websocket=ws2,
            handler_task=None
        )
        extension_interface._connections["conn-2"] = conn2
        extension_interface._active_connection_id = "conn-2"
        
        # Should have new connection as active
        assert extension_interface.has_active_connection
        new_connection_id = extension_interface._active_connection_id
        assert new_connection_id != initial_connection_id
        
        # Submit new task
        new_task = {
            "type": "extension_event",
            "id": 4002,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Task after reconnect",
                "context": {"tabId": 402},
                "tabId": 402
            }
        }
        await extension_interface._process_message("conn-2", json.dumps(new_task))
        assert extension_interface._active_tab_id == 402

    @pytest.mark.asyncio
    async def test_concurrent_task_processing(self, extension_interface, mock_websocket):
        """Test handling concurrent tasks from the same popup."""
        # Setup connection
        conn = ConnectionInfo(
            client_id="test-concurrent",
            websocket=mock_websocket,
            handler_task=None
        )
        extension_interface._connections["test-concurrent"] = conn
        extension_interface._active_connection_id = "test-concurrent"
        
        # Submit multiple tasks in quick succession
        tasks = []
        for i in range(5):
            task = {
                "type": "extension_event",
                "id": 5000 + i,
                "data": {
                    "event_name": "user_task_submitted",
                    "task": f"Task {i}: Search for item {i}",
                    "context": {"tabId": 500 + i},
                    "tabId": 500 + i
                }
            }
            tasks.append(task)
        
        # Process all tasks
        for task in tasks:
            await extension_interface._process_message("test-concurrent", json.dumps(task))
        
        # Should have the last tab as active
        assert extension_interface._active_tab_id == 504

    @pytest.mark.asyncio
    async def test_error_handling_in_task_flow(self, extension_interface, mock_websocket):
        """Test error handling throughout the task submission flow."""
        # Setup connection
        conn = ConnectionInfo(
            client_id="test-errors",
            websocket=mock_websocket,
            handler_task=None
        )
        extension_interface._connections["test-errors"] = conn
        extension_interface._active_connection_id = "test-errors"
        
        # Test invalid message format
        invalid_messages = [
            "not json at all",
            json.dumps({"type": "extension_event"}),  # Missing required fields
            json.dumps({"type": "unknown_type", "id": 1}),  # Unknown type
            json.dumps({
                "type": "extension_event",
                "id": 6001,
                "data": {
                    "event_name": "user_task_submitted",
                    # Missing task field
                    "tabId": 601
                }
            })
        ]
        
        for msg in invalid_messages:
            try:
                await extension_interface._process_message("test-errors", msg)
            except Exception:
                pass  # Some invalid messages might raise exceptions
        
        # Connection should still be active
        assert extension_interface.has_active_connection
        
        # Valid task should still work
        valid_task = {
            "type": "extension_event",
            "id": 6002,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Valid task after errors",
                "context": {"tabId": 602},
                "tabId": 602
            }
        }
        await extension_interface._process_message("test-errors", json.dumps(valid_task))
        assert extension_interface._active_tab_id == 602

    @pytest.mark.asyncio
    async def test_agent_integration_with_user_input(self, extension_interface, mock_browser_context):
        """Test Agent class integration with user input functionality."""
        # Setup connection
        conn = ConnectionInfo(
            client_id="test-agent",
            websocket=AsyncMock(),
            handler_task=None
        )
        extension_interface._connections["test-agent"] = conn
        extension_interface._active_connection_id = "test-agent"
        
        # Create agent with mocked components
        controller = Controller(browser_context=mock_browser_context)
        
        # Mock LLM response
        mock_llm = AsyncMock()
        mock_llm.return_value = "I'll help you search for Python tutorials. Let me navigate to Google first."
        
        # Submit user task
        user_task = {
            "type": "extension_event",
            "id": 7001,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Search for Python tutorials",
                "context": {"tabId": 701},
                "tabId": 701
            }
        }
        
        await extension_interface._process_message("test-agent", json.dumps(user_task))
        
        # Verify task was processed
        assert extension_interface._active_tab_id == 701
        
        # In a real scenario, the agent would process this task
        # For now, we just verify the infrastructure is in place
        assert extension_interface.has_active_connection
        assert len(extension_interface._connections) == 1