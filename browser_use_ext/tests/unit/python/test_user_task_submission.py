"""Unit tests for user task submission functionality in ExtensionInterface."""

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.extension_interface.models import Message, ConnectionInfo


class TestUserTaskSubmission:
    """Test cases for user task submission event handling."""

    @pytest.fixture
    def extension_interface(self):
        """Create an ExtensionInterface instance for testing."""
        interface = ExtensionInterface(host="localhost", port=8765)
        # Mock the WebSocket server to avoid actual network operations
        interface._server = MagicMock()
        return interface

    @pytest.fixture
    def mock_websocket(self):
        """Create a mock WebSocket connection."""
        websocket = AsyncMock()
        websocket.remote_address = ("127.0.0.1", 12345)
        websocket.send = AsyncMock()
        websocket.recv = AsyncMock()
        websocket.close = AsyncMock()
        return websocket

    @pytest.fixture
    def mock_connection_info(self, mock_websocket):
        """Create a mock ConnectionInfo object."""
        return ConnectionInfo(
            client_id="test-client-123",
            websocket=mock_websocket,
            handler_task=None
        )

    @pytest.mark.asyncio
    async def test_user_task_submitted_event_handling(self, extension_interface):
        """Test handling of user_task_submitted event."""
        # Setup
        client_id = "test-client-123"
        tab_id = 456
        task_text = "Find cheap laptops on Amazon"
        context = {
            "url": "https://example.com",
            "title": "Example Page",
            "tabId": tab_id
        }

        # Create the event message
        message_data = {
            "type": "extension_event",
            "id": 12345,
            "data": {
                "event_name": "user_task_submitted",
                "task": task_text,
                "context": context,
                "tabId": tab_id
            }
        }

        # Process the message
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            # Simulate message processing
            message = Message[dict].model_validate(message_data)
            
            # Call the internal processing method
            await extension_interface._process_message(client_id, json.dumps(message_data))

            # Verify logging
            mock_logger.info.assert_any_call(
                f"User submitted task from extension popup: '{task_text}' (Tab ID: {tab_id})"
            )
            mock_logger.info.assert_any_call(
                f"Updated active tab ID to {tab_id} from user task submission"
            )
            mock_logger.info.assert_any_call(
                f"Task details - Task: {task_text}, Context: {context}, Tab: {tab_id}"
            )

        # Verify active tab ID was updated
        assert extension_interface._active_tab_id == tab_id

    @pytest.mark.asyncio
    async def test_user_task_submitted_without_tab_id(self, extension_interface):
        """Test handling of user_task_submitted event without tab ID."""
        # Setup
        client_id = "test-client-123"
        task_text = "Search for Python tutorials"
        context = {"url": "https://example.com"}

        # Create the event message without tabId
        message_data = {
            "type": "extension_event",
            "id": 12346,
            "data": {
                "event_name": "user_task_submitted",
                "task": task_text,
                "context": context,
                "tabId": None
            }
        }

        # Process the message
        initial_tab_id = extension_interface._active_tab_id
        
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            await extension_interface._process_message(client_id, json.dumps(message_data))

            # Verify logging
            mock_logger.info.assert_any_call(
                f"User submitted task from extension popup: '{task_text}' (Tab ID: None)"
            )

        # Verify active tab ID was not updated
        assert extension_interface._active_tab_id == initial_tab_id

    @pytest.mark.asyncio
    async def test_user_task_submitted_with_invalid_tab_id(self, extension_interface):
        """Test handling of user_task_submitted event with invalid tab ID."""
        # Setup
        client_id = "test-client-123"
        task_text = "Test task"
        invalid_tab_id = "not-a-number"

        # Create the event message with invalid tabId
        message_data = {
            "type": "extension_event",
            "id": 12347,
            "data": {
                "event_name": "user_task_submitted",
                "task": task_text,
                "context": {},
                "tabId": invalid_tab_id
            }
        }

        # Process the message
        initial_tab_id = extension_interface._active_tab_id
        
        await extension_interface._process_message(client_id, json.dumps(message_data))

        # Verify active tab ID was not updated (not an integer)
        assert extension_interface._active_tab_id == initial_tab_id

    @pytest.mark.asyncio
    async def test_user_task_submitted_empty_task(self, extension_interface):
        """Test handling of user_task_submitted event with empty task."""
        # Setup
        client_id = "test-client-123"
        tab_id = 789
        empty_task = ""

        # Create the event message with empty task
        message_data = {
            "type": "extension_event",
            "id": 12348,
            "data": {
                "event_name": "user_task_submitted",
                "task": empty_task,
                "context": {"tabId": tab_id},
                "tabId": tab_id
            }
        }

        # Process the message
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            await extension_interface._process_message(client_id, json.dumps(message_data))

            # Should still process empty tasks
            mock_logger.info.assert_any_call(
                f"User submitted task from extension popup: '' (Tab ID: {tab_id})"
            )

        # Tab ID should still be updated even with empty task
        assert extension_interface._active_tab_id == tab_id

    @pytest.mark.asyncio
    async def test_user_task_submitted_with_special_characters(self, extension_interface):
        """Test handling of user_task_submitted event with special characters in task."""
        # Setup
        client_id = "test-client-123"
        tab_id = 101
        special_task = "Search for 'quotes' & <special> characters: $€¥"

        # Create the event message
        message_data = {
            "type": "extension_event",
            "id": 12349,
            "data": {
                "event_name": "user_task_submitted",
                "task": special_task,
                "context": {"tabId": tab_id},
                "tabId": tab_id
            }
        }

        # Process the message
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            await extension_interface._process_message(client_id, json.dumps(message_data))

            # Verify special characters are handled correctly
            mock_logger.info.assert_any_call(
                f"User submitted task from extension popup: '{special_task}' (Tab ID: {tab_id})"
            )

    @pytest.mark.asyncio
    async def test_user_task_submitted_updates_active_tab(self, extension_interface):
        """Test that user_task_submitted correctly updates the active tab ID."""
        # Setup multiple task submissions
        client_id = "test-client-123"
        
        # First task
        message_data_1 = {
            "type": "extension_event",
            "id": 1,
            "data": {
                "event_name": "user_task_submitted",
                "task": "First task",
                "context": {"tabId": 100},
                "tabId": 100
            }
        }
        
        # Second task
        message_data_2 = {
            "type": "extension_event",
            "id": 2,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Second task",
                "context": {"tabId": 200},
                "tabId": 200
            }
        }

        # Process first message
        await extension_interface._process_message(client_id, json.dumps(message_data_1))
        assert extension_interface._active_tab_id == 100

        # Process second message
        await extension_interface._process_message(client_id, json.dumps(message_data_2))
        assert extension_interface._active_tab_id == 200

    @pytest.mark.asyncio
    async def test_user_task_submitted_with_full_context(self, extension_interface):
        """Test handling of user_task_submitted with complete context information."""
        # Setup
        client_id = "test-client-123"
        tab_id = 555
        full_context = {
            "url": "https://www.example.com/page",
            "title": "Example Page Title",
            "tabId": tab_id,
            "windowId": 1,
            "favIconUrl": "https://www.example.com/favicon.ico",
            "status": "complete"
        }

        # Create the event message
        message_data = {
            "type": "extension_event",
            "id": 12350,
            "data": {
                "event_name": "user_task_submitted",
                "task": "Complex task with full context",
                "context": full_context,
                "tabId": tab_id
            }
        }

        # Process the message
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            await extension_interface._process_message(client_id, json.dumps(message_data))

            # Verify full context is logged
            mock_logger.info.assert_any_call(
                f"Task details - Task: Complex task with full context, Context: {full_context}, Tab: {tab_id}"
            )

    @pytest.mark.asyncio
    async def test_event_handling_preserves_other_events(self, extension_interface):
        """Test that user_task_submitted doesn't interfere with other event types."""
        client_id = "test-client-123"
        
        # Test content_script_ready event still works
        content_ready_message = {
            "type": "extension_event",
            "id": 1000,
            "data": {
                "event_name": "content_script_ready",
                "tabId": 999
            }
        }
        
        await extension_interface._process_message(client_id, json.dumps(content_ready_message))
        
        # Verify content script ready was tracked
        assert 999 in extension_interface._content_script_ready_tabs
        
        # Test tab_removed event still works
        tab_removed_message = {
            "type": "extension_event",
            "id": 1001,
            "data": {
                "event_name": "tab_removed",
                "tabId": 999
            }
        }
        
        await extension_interface._process_message(client_id, json.dumps(tab_removed_message))
        
        # Verify tab was removed from tracking
        assert 999 not in extension_interface._content_script_ready_tabs

    def test_active_tab_id_property(self, extension_interface):
        """Test that _active_tab_id is properly initialized and accessible."""
        # Initially should be None
        assert extension_interface._active_tab_id is None
        
        # Set a value
        extension_interface._active_tab_id = 123
        assert extension_interface._active_tab_id == 123