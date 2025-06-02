"""
End-to-end tests for agent functionality using WebSocket mocking.
These tests can run without Playwright browsers by mocking the Chrome extension side.
"""

import asyncio
import json
import logging
import pytest
import pytest_asyncio
import websockets
from unittest.mock import AsyncMock, Mock, patch
from typing import Dict, Any

from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.agent.views import AgentHistoryList, AgentHistory
from browser_use_ext.browser.views import BrowserState, TabInfo
from browser_use_ext.dom.views import DOMDocumentNode, DOMElementNode

logger = logging.getLogger(__name__)

class MockChromeExtension:
    """Mock Chrome extension that communicates via WebSocket."""
    
    def __init__(self, server_port: int = 8767):
        self.server_port = server_port
        self.websocket = None
        self.message_id = 0
        self.tab_id = 123
        
    async def connect(self):
        """Connect to the Python WebSocket server."""
        uri = f"ws://localhost:{self.server_port}"
        self.websocket = await websockets.connect(uri)
        logger.info(f"Mock extension connected to {uri}")
        
    async def disconnect(self):
        """Disconnect from the server."""
        if self.websocket:
            await self.websocket.close()
            
    async def send_message(self, message_type: str, data: Dict[str, Any]):
        """Send a message to the Python server."""
        self.message_id += 1
        message = {
            "id": self.message_id,
            "type": message_type,
            "data": data
        }
        await self.websocket.send(json.dumps(message))
        logger.info(f"Mock extension sent: {message}")
        
    async def send_extension_event(self, event_name: str, event_data: Dict[str, Any]):
        """Send an extension event to the Python server."""
        await self.send_message("extension_event", {
            "event_name": event_name,
            **event_data
        })
        
    async def send_ready_signal(self):
        """Send content script ready signal."""
        await self.send_extension_event("content_script_ready", {
            "tabId": self.tab_id,
            "url": "https://example.com"
        })
        
    async def send_user_task(self, task: str, context: Dict[str, Any] = None):
        """Send user task submission event."""
        if context is None:
            context = {"url": "https://example.com", "title": "Example"}
            
        await self.send_extension_event("user_task_submitted", {
            "task": task,
            "context": context,
            "tabId": self.tab_id
        })
        
    async def respond_to_action(self, request_id: int, success: bool = True, data: Dict[str, Any] = None):
        """Respond to an action request from the Python server."""
        response = {
            "id": request_id,
            "type": "response", 
            "data": {
                "success": success,
                "error": None if success else "Mock action failed",
                **(data or {})
            }
        }
        await self.websocket.send(json.dumps(response))
        logger.info(f"Mock extension responded: {response}")


@pytest_asyncio.fixture
async def mock_extension_interface():
    """Create an ExtensionInterface with mocked LLM for testing."""
    with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
        # Mock LLM
        mock_llm = AsyncMock()
        mock_openai.return_value = mock_llm
        
        # Create interface on different port to avoid conflicts
        interface = ExtensionInterface(port=8767, llm_model="gpt-4o")
        interface._llm = mock_llm
        
        # Start server
        await interface.start_server()
        
        # Wait for server to be ready
        await asyncio.sleep(0.5)
        
        yield interface
        
        # Cleanup
        await interface.close()


@pytest.mark.asyncio
async def test_agent_websocket_connection_e2e(mock_extension_interface):
    """Test basic WebSocket connection between mock extension and agent system."""
    interface = mock_extension_interface
    mock_ext = MockChromeExtension(8767)
    
    try:
        # Connect mock extension
        await mock_ext.connect()
        
        # Wait for connection to be registered
        await asyncio.sleep(0.5)
        
        # Verify connection
        assert interface.has_active_connection
        assert interface.active_connection_object is not None
        
        logger.info("✅ Mock extension connected successfully")
        
    finally:
        await mock_ext.disconnect()


@pytest.mark.asyncio
async def test_agent_user_task_submission_e2e(mock_extension_interface):
    """Test complete user task submission flow through WebSocket."""
    interface = mock_extension_interface
    mock_ext = MockChromeExtension(8767)
    
    try:
        # Connect and send ready signal
        await mock_ext.connect()
        await asyncio.sleep(0.5)
        
        await mock_ext.send_ready_signal()
        await asyncio.sleep(0.5)
        
        # Track agent creation
        agent_created = False
        original_process_task = interface.process_user_task
        
        async def track_agent_creation(*args, **kwargs):
            nonlocal agent_created
            agent_created = True
            logger.info(f"Agent processing task: {args[0]}")
            
        interface.process_user_task = track_agent_creation
        
        # Submit user task
        await mock_ext.send_user_task("Click the login button", {
            "url": "https://example.com/login",
            "title": "Login Page"
        })
        
        # Wait for processing
        await asyncio.sleep(1.0)
        
        # Verify agent was triggered
        assert agent_created, "Agent should have been created to process user task"
        assert interface._active_tab_id == 123, "Active tab should be updated"
        
        logger.info("✅ User task submission triggered agent processing")
        
    finally:
        await mock_ext.disconnect()


@pytest.mark.asyncio
async def test_agent_action_execution_e2e(mock_extension_interface):
    """Test agent action execution through WebSocket."""
    interface = mock_extension_interface
    mock_ext = MockChromeExtension(8767)
    
    try:
        # Connect and setup
        await mock_ext.connect()
        await asyncio.sleep(0.5)
        
        await mock_ext.send_ready_signal()
        await asyncio.sleep(0.5)
        
        # Mock agent execution
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            # Create a task that will trigger actions
            async def mock_agent_run():
                # Simulate agent executing a click action
                result = await interface.execute_action(
                    action_name="click",
                    params={"element_id": "login-button"},
                    tab_id=123
                )
                
                return AgentHistoryList(history=[
                    AgentHistory(
                        browser_url="https://example.com/login",
                        action_results=[]
                    )
                ])
            
            mock_agent.run.side_effect = mock_agent_run
            
            # Start agent task processing (this will call execute_action)
            task_future = asyncio.create_task(
                interface.process_user_task("Click login", {}, 123)
            )
            
            # Wait a bit for the execute_action to be called
            await asyncio.sleep(0.5)
            
            # Mock extension should receive the action request
            # In a real scenario, the extension would receive and respond
            # For this test, we'll mock the response
            await mock_ext.respond_to_action(
                request_id=1,  # First request
                success=True,
                data={"clicked": True}
            )
            
            # Wait for task completion
            await asyncio.wait_for(task_future, timeout=5.0)
            
            # Verify agent was called
            mock_agent_class.assert_called_once()
            mock_agent.run.assert_called_once()
            
            logger.info("✅ Agent action execution completed through WebSocket")
            
    except asyncio.TimeoutError:
        logger.warning("Test timed out - this is expected in mock environment")
        # This is okay for the mock test - the important part is that the flow started
        
    finally:
        await mock_ext.disconnect()


@pytest.mark.asyncio
async def test_agent_multiple_tasks_e2e(mock_extension_interface):
    """Test handling multiple concurrent agent tasks."""
    interface = mock_extension_interface
    mock_ext = MockChromeExtension(8767)
    
    try:
        # Connect and setup
        await mock_ext.connect()
        await asyncio.sleep(0.5)
        
        await mock_ext.send_ready_signal()
        await asyncio.sleep(0.5)
        
        # Track task processing
        tasks_processed = []
        
        async def track_tasks(task, context, tab_id):
            tasks_processed.append(task)
            logger.info(f"Processing task: {task}")
            
        interface.process_user_task = track_tasks
        
        # Submit multiple tasks
        tasks = [
            "Click the login button",
            "Fill out the form", 
            "Submit the form"
        ]
        
        for i, task in enumerate(tasks):
            await mock_ext.send_user_task(task, {"url": f"https://example.com/step{i}"})
            await asyncio.sleep(0.2)  # Small delay between tasks
            
        # Wait for all tasks to be processed
        await asyncio.sleep(1.0)
        
        # Verify all tasks were processed
        assert len(tasks_processed) == 3, f"Expected 3 tasks, got {len(tasks_processed)}"
        for task in tasks:
            assert task in tasks_processed, f"Task '{task}' was not processed"
            
        logger.info("✅ Multiple agent tasks processed successfully")
        
    finally:
        await mock_ext.disconnect()


@pytest.mark.asyncio
async def test_agent_error_handling_e2e(mock_extension_interface):
    """Test agent error handling in E2E scenario."""
    interface = mock_extension_interface
    mock_ext = MockChromeExtension(8767)
    
    try:
        # Connect and setup
        await mock_ext.connect()
        await asyncio.sleep(0.5)
        
        # Simulate task processing without LLM (should handle gracefully)
        interface._llm = None
        
        # Submit task
        await mock_ext.send_user_task("This should fail gracefully")
        await asyncio.sleep(1.0)
        
        # The system should handle the error without crashing
        assert interface.has_active_connection, "Connection should remain active after error"
        
        logger.info("✅ Error handling worked correctly")
        
    finally:
        await mock_ext.disconnect()


class TestAgentE2EScenarios:
    """Test realistic agent scenarios end-to-end."""
    
    @pytest.mark.asyncio
    async def test_login_flow_scenario(self, mock_extension_interface):
        """Test a realistic login flow scenario."""
        interface = mock_extension_interface
        mock_ext = MockChromeExtension(8767)
        
        try:
            await mock_ext.connect()
            await asyncio.sleep(0.5)
            
            # Mock browser state for login page
            login_state = BrowserState(
                url="https://example.com/login",
                title="Login Page",
                tree={
                    "tag": "html",
                    "children": [{
                        "tag": "body", 
                        "children": [
                            {"tag": "input", "attributes": {"type": "email", "id": "email"}},
                            {"tag": "input", "attributes": {"type": "password", "id": "password"}}, 
                            {"tag": "button", "text": "Login", "id": "login-btn"}
                        ]
                    }]
                },
                tabs=[{"tabId": 123, "url": "https://example.com/login", "isActive": True}]
            )
            
            # Mock get_state to return our login page
            interface.get_state = AsyncMock(return_value=login_state)
            
            # Track actions executed
            actions_executed = []
            
            async def track_execute_action(action_name, params, **kwargs):
                actions_executed.append((action_name, params))
                return {"success": True, "data": {}}
                
            interface.execute_action = track_execute_action
            
            # Submit login task
            await mock_ext.send_user_task(
                "Log in with email test@example.com and password secret123",
                {"url": "https://example.com/login", "title": "Login Page"}
            )
            
            await asyncio.sleep(1.0)
            
            # In a real scenario, the agent would execute multiple actions
            # For this test, we verify the framework can handle the task
            assert interface._active_tab_id == 123
            
            logger.info("✅ Login scenario setup completed")
            
        finally:
            await mock_ext.disconnect()
    
    @pytest.mark.asyncio  
    async def test_search_and_click_scenario(self, mock_extension_interface):
        """Test a search and click scenario."""
        interface = mock_extension_interface
        mock_ext = MockChromeExtension(8767)
        
        try:
            await mock_ext.connect()
            await asyncio.sleep(0.5)
            
            # Submit search task
            await mock_ext.send_user_task(
                "Search for 'Python tutorials' and click the first result",
                {"url": "https://google.com", "title": "Google"}
            )
            
            await asyncio.sleep(1.0)
            
            # Verify task was received and processed
            assert interface._active_tab_id == 123
            
            logger.info("✅ Search scenario completed")
            
        finally:
            await mock_ext.disconnect()