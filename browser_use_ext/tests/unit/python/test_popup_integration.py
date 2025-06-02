"""Integration tests for popup-to-backend communication flow."""

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.extension_interface.models import Message, ConnectionInfo


class TestPopupIntegration:
    """Test the complete flow from popup to Python backend."""

    @pytest.fixture
    def extension_interface(self):
        """Create an ExtensionInterface instance for testing."""
        interface = ExtensionInterface(host="localhost", port=8765)
        interface._server = MagicMock()
        interface._active_connection_id = None  # Start with no active connection
        interface._connections = {}
        return interface

    @pytest.fixture
    def mock_websocket(self):
        """Create a mock WebSocket connection."""
        websocket = AsyncMock()
        websocket.send = AsyncMock()
        websocket.remote_address = ("127.0.0.1", 12345)
        return websocket

    @pytest.mark.asyncio
    async def test_popup_status_request_flow(self, extension_interface, mock_websocket):
        """Test the flow when popup requests connection status."""
        # Setup connection
        conn_info = ConnectionInfo(
            client_id="test-connection",
            websocket=mock_websocket,
            handler_task=None
        )
        extension_interface._connections["test-connection"] = conn_info
        extension_interface._active_connection_id = "test-connection"  # Set active connection

        # Simulate popup requesting status (this would come through background.js)
        # In real flow: popup -> background.js -> checks websocket status
        
        # Verify the interface reports active connection
        assert extension_interface.has_active_connection is True
        assert extension_interface.active_connection_object is not None
        assert extension_interface.active_connection_object.client_id == "test-connection"

    @pytest.mark.asyncio
    async def test_task_submission_full_flow(self, extension_interface, mock_websocket):
        """Test complete task submission flow from popup to backend."""
        # Setup
        client_id = "test-connection"
        conn_info = ConnectionInfo(
            client_id=client_id,
            websocket=mock_websocket,
            handler_task=None
        )
        extension_interface._connections[client_id] = conn_info
        extension_interface._active_connection_id = client_id

        # Simulate the full message flow
        task_data = {
            "type": "extension_event",
            "id": 12345,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Find the best Python tutorials",
                "context": {
                    "url": "https://python.org",
                    "title": "Python.org",
                    "tabId": 456,
                    "windowId": 1
                },
                "tabId": 456
            }
        }

        # Process the message
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            await extension_interface._process_message(client_id, json.dumps(task_data))

            # Verify the task was processed
            mock_logger.info.assert_any_call(
                "User submitted task from extension popup: 'Find the best Python tutorials' (Tab ID: 456)"
            )

        # Verify active tab was updated
        assert extension_interface._active_tab_id == 456

    @pytest.mark.asyncio
    async def test_multiple_task_submissions(self, extension_interface):
        """Test handling multiple task submissions in sequence."""
        client_id = "test-connection"
        
        # Submit first task
        task1 = {
            "type": "extension_event",
            "id": 1,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Task 1",
                "context": {"tabId": 100},
                "tabId": 100
            }
        }
        
        await extension_interface._process_message(client_id, json.dumps(task1))
        assert extension_interface._active_tab_id == 100

        # Submit second task from different tab
        task2 = {
            "type": "extension_event",
            "id": 2,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Task 2",
                "context": {"tabId": 200},
                "tabId": 200
            }
        }
        
        await extension_interface._process_message(client_id, json.dumps(task2))
        assert extension_interface._active_tab_id == 200

    @pytest.mark.asyncio
    async def test_popup_task_with_navigation(self, extension_interface):
        """Test task submission that includes navigation intent."""
        client_id = "test-connection"
        
        # Task with navigation intent
        task_data = {
            "type": "extension_event",
            "id": 12346,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Go to Amazon and find laptops under $500",
                "context": {
                    "url": "about:blank",  # Starting from blank tab
                    "title": "New Tab",
                    "tabId": 789
                },
                "tabId": 789
            }
        }

        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            await extension_interface._process_message(client_id, json.dumps(task_data))

            # Verify task was logged
            mock_logger.info.assert_any_call(
                "User submitted task from extension popup: 'Go to Amazon and find laptops under $500' (Tab ID: 789)"
            )
            
            # Verify context shows blank tab
            mock_logger.info.assert_any_call(
                "Task details - Task: Go to Amazon and find laptops under $500, "
                "Context: {'url': 'about:blank', 'title': 'New Tab', 'tabId': 789}, Tab: 789"
            )

    @pytest.mark.asyncio
    async def test_task_submission_error_scenarios(self, extension_interface):
        """Test error handling in task submission."""
        client_id = "test-connection"
        
        # Test with malformed JSON
        with pytest.raises(json.JSONDecodeError):
            await extension_interface._process_message(client_id, "invalid json{")
        
        # Test with missing event_name
        invalid_event = {
            "type": "extension_event",
            "id": 123,
            "data": {
                # Missing event_name
                "task": "Test task"
            }
        }
        
        # Should process but handle as unknown event
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            await extension_interface._process_message(client_id, json.dumps(invalid_event))
            
            # Should log unknown event
            mock_logger.info.assert_any_call(
                f"Received event 'unknown_event' from {client_id}: {invalid_event['data']}"
            )

    @pytest.mark.asyncio
    async def test_concurrent_popup_connections(self, extension_interface):
        """Test handling multiple popup connections."""
        # First connection
        conn1 = ConnectionInfo(
            client_id="popup-1",
            websocket=AsyncMock(),
            handler_task=None
        )
        extension_interface._connections["popup-1"] = conn1
        extension_interface._active_connection_id = "popup-1"
        
        # Second connection (e.g., from another window)
        conn2 = ConnectionInfo(
            client_id="popup-2",
            websocket=AsyncMock(),
            handler_task=None
        )
        extension_interface._connections["popup-2"] = conn2
        
        # Task from first popup
        task1 = {
            "type": "extension_event",
            "id": 1,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Task from popup 1",
                "context": {"tabId": 111},
                "tabId": 111
            }
        }
        
        await extension_interface._process_message("popup-1", json.dumps(task1))
        assert extension_interface._active_tab_id == 111
        
        # Task from second popup should also work
        task2 = {
            "type": "extension_event",
            "id": 2,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Task from popup 2",
                "context": {"tabId": 222},
                "tabId": 222
            }
        }
        
        await extension_interface._process_message("popup-2", json.dumps(task2))
        assert extension_interface._active_tab_id == 222

    @pytest.mark.asyncio
    async def test_popup_disconnection_handling(self, extension_interface):
        """Test handling when popup disconnects."""
        client_id = "popup-connection"
        conn = ConnectionInfo(
            client_id=client_id,
            websocket=AsyncMock(),
            handler_task=None
        )
        extension_interface._connections[client_id] = conn
        extension_interface._active_connection_id = client_id
        
        # Verify connection exists
        assert extension_interface.has_active_connection is True
        
        # Simulate disconnection
        await extension_interface._remove_client(client_id)
        
        # Verify cleanup
        assert client_id not in extension_interface._connections
        assert extension_interface._active_connection_id is None
        assert extension_interface.has_active_connection is False

    def test_connection_state_properties(self, extension_interface):
        """Test connection state property methods."""
        # No connection
        assert extension_interface.has_active_connection is False
        assert extension_interface.active_connection_object is None
        
        # Add connection
        conn = ConnectionInfo(
            client_id="test",
            websocket=MagicMock(),
            handler_task=None
        )
        extension_interface._connections["test"] = conn
        extension_interface._active_connection_id = "test"
        
        # Verify properties
        assert extension_interface.has_active_connection is True
        assert extension_interface.active_connection_object is conn
        assert extension_interface.active_connection_object.client_id == "test"