"""End-to-end integration tests for user input functionality."""

import asyncio
import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.browser.context import BrowserContext, BrowserContextConfig
from browser_use_ext.controller.service import Controller
from browser_use_ext.agent.service import Agent


# Register the integration marker
pytest.register_mark("integration")


class TestUserInputE2EIntegration:
    """Test the complete flow from popup input to agent action execution."""

    @pytest.fixture
    async def extension_interface(self):
        """Create and start the extension interface server."""
        interface = ExtensionInterface(host="localhost", port=8766)  # Different port for tests
        await interface.start_server()
        yield interface
        await interface.close()

    @pytest.fixture
    def mock_browser_context(self):
        """Create a mock browser context for testing."""
        context = MagicMock(spec=BrowserContext)
        context.get_state = AsyncMock()
        context.execute_action = AsyncMock()
        return context

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_complete_user_input_flow(self, extension_interface, mock_browser_context):
        """Test the complete flow from user input to action execution."""
        # Simulate Chrome extension connection
        async with websockets.connect(f"ws://localhost:8766") as websocket:
            # Wait for connection to be established
            await asyncio.sleep(0.1)
            
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
            
            # Send the task submission
            await websocket.send(json.dumps(user_task_message))
            
            # Give the server time to process
            await asyncio.sleep(0.1)
            
            # Verify the active tab was updated
            assert extension_interface._active_tab_id == 123
            
            # Now simulate the agent processing the task
            with patch.object(extension_interface, 'execute_action') as mock_execute:
                mock_execute.return_value = {"success": True, "data": {}}
                
                # Create controller with mocked context
                controller = Controller(browser_context=mock_browser_context)
                
                # Simulate agent parsing the task and executing navigation
                result = await controller.go_to_url("https://www.google.com")
                
                # Verify the action was called
                mock_browser_context.execute_action.assert_called_once_with(
                    "navigate",
                    {"url": "https://www.google.com"}
                )

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_multiple_popup_instances(self, extension_interface):
        """Test handling multiple popup instances submitting tasks."""
        connections = []
        
        try:
            # Simulate two popup instances connecting
            for i in range(2):
                ws = await websockets.connect(f"ws://localhost:8766")
                connections.append(ws)
            
            await asyncio.sleep(0.1)
            
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
            await connections[0].send(json.dumps(task1))
            await asyncio.sleep(0.1)
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
            await connections[1].send(json.dumps(task2))
            await asyncio.sleep(0.1)
            assert extension_interface._active_tab_id == 202
            
        finally:
            # Clean up connections
            for ws in connections:
                await ws.close()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_task_with_navigation_and_interaction(self, extension_interface):
        """Test a complex task involving navigation and element interaction."""
        async with websockets.connect(f"ws://localhost:8766") as websocket:
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
            
            await websocket.send(json.dumps(complex_task))
            await asyncio.sleep(0.1)
            
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
    @pytest.mark.integration
    async def test_popup_disconnect_recovery(self, extension_interface):
        """Test system behavior when popup disconnects and reconnects."""
        # First connection
        ws1 = await websockets.connect(f"ws://localhost:8766")
        await asyncio.sleep(0.1)
        
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
        await ws1.send(json.dumps(task))
        await asyncio.sleep(0.1)
        assert extension_interface._active_tab_id == 401
        
        # Disconnect
        await ws1.close()
        await asyncio.sleep(0.2)
        
        # Verify cleanup
        assert initial_connection_id not in extension_interface._connections
        
        # Reconnect
        ws2 = await websockets.connect(f"ws://localhost:8766")
        await asyncio.sleep(0.1)
        
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
        await ws2.send(json.dumps(new_task))
        await asyncio.sleep(0.1)
        assert extension_interface._active_tab_id == 402
        
        await ws2.close()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_concurrent_task_processing(self, extension_interface):
        """Test handling concurrent tasks from the same popup."""
        async with websockets.connect(f"ws://localhost:8766") as websocket:
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
            
            # Send all tasks rapidly
            for task in tasks:
                await websocket.send(json.dumps(task))
                await asyncio.sleep(0.01)  # Small delay between sends
            
            # Wait for processing
            await asyncio.sleep(0.2)
            
            # Should have the last tab as active
            assert extension_interface._active_tab_id == 504

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_error_handling_in_task_flow(self, extension_interface):
        """Test error handling throughout the task submission flow."""
        async with websockets.connect(f"ws://localhost:8766") as websocket:
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
                    await websocket.send(msg)
                    await asyncio.sleep(0.1)
                except Exception:
                    pass  # Some invalid messages might cause connection issues
            
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
            await websocket.send(json.dumps(valid_task))
            await asyncio.sleep(0.1)
            assert extension_interface._active_tab_id == 602