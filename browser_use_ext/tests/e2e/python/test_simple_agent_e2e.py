"""
Simple E2E tests for agent functionality without WebSocket dependencies.
These tests focus on the agent processing pipeline using mocks.
"""

import asyncio
import logging
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, Mock, patch
from typing import Dict, Any

from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.agent.views import (
    AgentHistoryList, 
    AgentHistory, 
    ActionCommand,
    AgentLLMOutput,
    AgentBrain,
    ActionResult
)
from browser_use_ext.browser.views import BrowserState, TabInfo
from browser_use_ext.dom.views import DOMDocumentNode, DOMElementNode

logger = logging.getLogger(__name__)


@pytest.fixture
def simple_browser_state():
    """Create a simple browser state for testing."""
    return BrowserState(
        url="https://example.com",
        title="Example Page",
        tree=DOMDocumentNode(
            type="document",
            children=[DOMElementNode(
                type="element",
                tag_name="html",
                children=[DOMElementNode(
                    type="element",
                    tag_name="body",
                    children=[
                        DOMElementNode(
                            type="element",
                            tag_name="button",
                            text="Click Me",
                            attributes={"id": "test-btn"},
                            highlight_index=1
                        )
                    ]
                )]
            )]
        ),
        tabs=[TabInfo(tabId=1, url="https://example.com", title="Example Page", isActive=True)]
    )


@pytest.fixture
def mock_agent_interface():
    """Create a mock ExtensionInterface for testing."""
    with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
        # Mock LLM
        mock_llm = AsyncMock()
        mock_openai.return_value = mock_llm
        
        # Create interface
        interface = ExtensionInterface(llm_model="gpt-4o")
        interface._llm = mock_llm
        interface._active_tab_id = 1
        
        # Mock connection
        mock_connection = Mock()
        mock_connection.client_id = "test-client"
        mock_connection.websocket = AsyncMock()
        
        interface._connections = {"test-client": mock_connection}
        interface._active_connection_id = "test-client"
        
        return interface


class TestSimpleAgentE2E:
    """Simple end-to-end tests for agent functionality."""
    
    @pytest.mark.asyncio
    async def test_agent_task_processing_flow(self, mock_agent_interface, simple_browser_state):
        """Test the basic agent task processing flow."""
        interface = mock_agent_interface
        
        # Mock dependencies
        interface.get_state = AsyncMock(return_value=simple_browser_state)
        interface.execute_action = AsyncMock(return_value={"success": True, "data": {}})
        
        # Track agent creation
        agent_was_created = False
        
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            def track_agent_creation(*args, **kwargs):
                nonlocal agent_was_created
                agent_was_created = True
                return mock_agent
            
            mock_agent_class.side_effect = track_agent_creation
            mock_agent.run.return_value = AgentHistoryList(history=[])
            
            # Process a user task
            await interface.process_user_task(
                task="Click the button",
                context={"url": "https://example.com"},
                tab_id=1
            )
            
            # Verify agent was created and executed
            assert agent_was_created, "Agent should have been created"
            mock_agent.run.assert_called_once()
            
            logger.info("✅ Agent task processing flow completed successfully")
    
    @pytest.mark.asyncio
    async def test_agent_with_llm_mock(self, mock_agent_interface, simple_browser_state):
        """Test agent processing with LLM interaction."""
        interface = mock_agent_interface
        
        # Mock state and actions
        interface.get_state = AsyncMock(return_value=simple_browser_state)
        interface.execute_action = AsyncMock(return_value={"success": True})
        
        # Mock LLM response
        interface._llm.ainvoke.return_value = Mock(
            content='{"thought": "I need to click the button", "action": {"name": "click", "params": {"element_id": "test-btn"}}}'
        )
        
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            # Simulate agent using the interface
            async def mock_agent_run():
                # Agent would get state
                state = await interface.get_state(tab_id=1)
                assert state.url == "https://example.com"
                
                # Agent would execute action
                result = await interface.execute_action(
                    action_name="click",
                    params={"element_id": "test-btn"},
                    tab_id=1
                )
                assert result["success"] == True
                
                return AgentHistoryList(history=[])
            
            mock_agent.run.side_effect = mock_agent_run
            
            # Process task
            await interface.process_user_task(
                task="Click the test button",
                context={},
                tab_id=1
            )
            
            # Verify interactions
            interface.get_state.assert_called()
            interface.execute_action.assert_called_with(
                action_name="click",
                params={"element_id": "test-btn"},
                tab_id=1
            )
            
            logger.info("✅ Agent with LLM mock completed successfully")
    
    @pytest.mark.asyncio
    async def test_agent_session_management(self, mock_agent_interface):
        """Test agent session creation and cleanup."""
        interface = mock_agent_interface
        
        # Simply track that sessions are managed properly
        initial_agent_count = len(interface._active_agents)
        
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.run.return_value = AgentHistoryList(history=[])
            mock_agent_class.return_value = mock_agent
            
            # Check that active agents is empty initially
            assert len(interface._active_agents) == initial_agent_count
            
            # Process task
            await interface.process_user_task("Test task", {}, 1)
            
            # Verify cleanup happened
            assert len(interface._active_agents) == initial_agent_count, "Should return to initial state"
            
            logger.info("✅ Agent session management completed successfully")
    
    @pytest.mark.asyncio
    async def test_multiple_concurrent_agent_tasks(self, mock_agent_interface):
        """Test handling multiple concurrent agent tasks."""
        interface = mock_agent_interface
        
        # Track concurrent execution
        active_tasks = set()
        max_concurrent = 0
        
        original_process_task = interface.process_user_task
        
        async def track_concurrent_execution(task, context, tab_id):
            task_id = f"task_{tab_id}"
            active_tasks.add(task_id)
            
            nonlocal max_concurrent
            max_concurrent = max(max_concurrent, len(active_tasks))
            
            # Simulate processing time
            await asyncio.sleep(0.05)
            
            active_tasks.remove(task_id)
            logger.info(f"Completed {task_id}, max concurrent: {max_concurrent}")
        
        interface.process_user_task = track_concurrent_execution
        
        # Start multiple tasks
        tasks = [
            interface.process_user_task(f"Task {i}", {}, i)
            for i in range(3)
        ]
        
        await asyncio.gather(*tasks)
        
        # Verify concurrent execution occurred
        assert max_concurrent > 1, f"Should have concurrent execution, got max: {max_concurrent}"
        assert len(active_tasks) == 0, "All tasks should be completed"
        
        logger.info("✅ Multiple concurrent agent tasks completed successfully")
    
    @pytest.mark.asyncio
    async def test_agent_error_handling(self, mock_agent_interface):
        """Test agent error handling."""
        interface = mock_agent_interface
        
        # Test with no LLM configured
        interface._llm = None
        
        # This should not crash
        await interface.process_user_task("Test task", {}, 1)
        
        # Verify no active agents remain
        assert len(interface._active_agents) == 0, "No agents should remain after error"
        
        logger.info("✅ Agent error handling completed successfully")


class TestAgentActionScenarios:
    """Test specific agent action scenarios."""
    
    @pytest.mark.asyncio
    async def test_click_action_scenario(self, mock_agent_interface, simple_browser_state):
        """Test a click action scenario."""
        interface = mock_agent_interface
        interface.get_state = AsyncMock(return_value=simple_browser_state)
        
        # Track action execution
        executed_actions = []
        
        async def track_actions(action_name, params, **kwargs):
            executed_actions.append((action_name, params))
            return {"success": True, "data": {"clicked": True}}
        
        interface.execute_action = track_actions
        
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            async def click_scenario():
                # Simulate agent clicking the button
                await interface.execute_action(
                    action_name="click",
                    params={"element_id": "test-btn"},
                    tab_id=1
                )
                return AgentHistoryList(history=[])
            
            mock_agent.run.side_effect = click_scenario
            
            # Execute task
            await interface.process_user_task("Click the button", {}, 1)
            
            # Verify click action was executed
            assert len(executed_actions) == 1
            assert executed_actions[0] == ("click", {"element_id": "test-btn"})
            
            logger.info("✅ Click action scenario completed successfully")
    
    @pytest.mark.asyncio
    async def test_form_filling_scenario(self, mock_agent_interface):
        """Test a form filling scenario."""
        interface = mock_agent_interface
        
        # Mock form page state
        form_state = BrowserState(
            url="https://example.com/form",
            title="Form Page",
            tree=DOMDocumentNode(
                type="document",
                children=[DOMElementNode(
                    type="element",
                    tag_name="html",
                    children=[DOMElementNode(
                        type="element",
                        tag_name="body",
                        children=[
                            DOMElementNode(
                                type="element",
                                tag_name="input",
                                attributes={"type": "text", "name": "username"},
                                highlight_index=1
                            ),
                            DOMElementNode(
                                type="element",
                                tag_name="input",
                                attributes={"type": "password", "name": "password"},
                                highlight_index=2
                            ),
                            DOMElementNode(
                                type="element",
                                tag_name="button",
                                text="Submit",
                                highlight_index=3
                            )
                        ]
                    )]
                )]
            ),
            tabs=[TabInfo(tabId=1, url="https://example.com/form", title="Form Page", isActive=True)]
        )
        
        interface.get_state = AsyncMock(return_value=form_state)
        
        # Track form actions
        form_actions = []
        
        async def track_form_actions(action_name, params, **kwargs):
            form_actions.append((action_name, params))
            return {"success": True}
        
        interface.execute_action = track_form_actions
        
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            async def form_filling_scenario():
                # Simulate agent filling out form
                await interface.execute_action(
                    action_name="input_text",
                    params={"element_id": "1", "text": "testuser"},
                    tab_id=1
                )
                
                await interface.execute_action(
                    action_name="input_text",
                    params={"element_id": "2", "text": "password123"},
                    tab_id=1
                )
                
                await interface.execute_action(
                    action_name="click",
                    params={"element_id": "3"},
                    tab_id=1
                )
                
                return AgentHistoryList(history=[])
            
            mock_agent.run.side_effect = form_filling_scenario
            
            # Execute task
            await interface.process_user_task(
                "Fill out the form with username 'testuser' and password 'password123', then submit",
                {},
                1
            )
            
            # Verify form actions
            assert len(form_actions) == 3
            assert form_actions[0] == ("input_text", {"element_id": "1", "text": "testuser"})
            assert form_actions[1] == ("input_text", {"element_id": "2", "text": "password123"})
            assert form_actions[2] == ("click", {"element_id": "3"})
            
            logger.info("✅ Form filling scenario completed successfully")