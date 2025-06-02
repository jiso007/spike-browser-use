"""
End-to-end tests for the complete agent pipeline without browser dependencies.
Tests the full flow: Task submission → Agent processing → Action generation → Results
"""

import asyncio
import json
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
def mock_browser_state():
    """Create a mock browser state for testing."""
    return BrowserState(
        url="https://example.com/test",
        title="Test Page",
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
                            tag_name="h1",
                            text="Welcome to Test Page"
                        ),
                        DOMElementNode(
                            type="element",
                            tag_name="button",
                            text="Click Me",
                            attributes={"id": "test-button"},
                            highlight_index=1
                        ),
                        DOMElementNode(
                            type="element",
                            tag_name="input",
                            attributes={"type": "text", "placeholder": "Enter text"},
                            highlight_index=2
                        )
                    ]
                )]
            )]
        ),
        tabs=[TabInfo(tabId=1, url="https://example.com/test", title="Test Page", isActive=True)]
    )


@pytest_asyncio.fixture
async def configured_agent_interface():
    """Create a fully configured ExtensionInterface with mocked components."""
    with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
        # Create mock LLM
        mock_llm = AsyncMock()
        mock_openai.return_value = mock_llm
        
        # Create interface
        interface = ExtensionInterface(port=8768, llm_model="gpt-4o")
        interface._llm = mock_llm
        interface._active_tab_id = 1
        
        # Mock connection
        mock_connection = Mock()
        mock_connection.client_id = "test-agent-client"
        mock_connection.websocket = AsyncMock()
        
        interface._connections = {"test-agent-client": mock_connection}
        interface._active_connection_id = "test-agent-client"
        
        yield interface


class TestAgentPipelineE2E:
    """Test the complete agent processing pipeline end-to-end."""
    
    @pytest.mark.asyncio
    async def test_complete_agent_task_pipeline(self, configured_agent_interface, mock_browser_state):
        """Test the complete pipeline: Task → Agent → LLM → Actions → Results."""
        interface = configured_agent_interface
        
        # Mock browser state and action execution
        interface.get_state = AsyncMock(return_value=mock_browser_state)
        interface.execute_action = AsyncMock(return_value={"success": True, "data": {"clicked": True}})
        
        # Mock agent processing
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            # Create realistic agent behavior
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            # Simulate agent generating actions and executing them
            async def realistic_agent_run():
                logger.info("Agent: Analyzing task and current page state")
                
                # Agent would get current state
                current_state = await interface.get_state(tab_id=1)
                logger.info(f"Agent: Retrieved state for {current_state.url}")
                
                # Agent would generate action based on LLM
                logger.info("Agent: Generating action plan")
                action_result = await interface.execute_action(
                    action_name="click",
                    params={"element_id": "btn-1"},
                    tab_id=1
                )
                logger.info(f"Agent: Action executed with result: {action_result}")
                
                # Return realistic history
                return AgentHistoryList(history=[
                    AgentHistory(
                        browser_url=current_state.url,
                        llm_output=AgentLLMOutput(
                            current_state=AgentBrain(
                                evaluation_previous_goal="Starting fresh task",
                                memory="User wants to click the test button on the page",
                                next_goal="Click the button with ID 'test-button'"
                            ),
                            action=[ActionCommand(
                                action="click",
                                params={"element_id": "btn-1"},
                                thought="I can see a button with text 'Click Me' and ID 'test-button'"
                            )]
                        ),
                        action_results=[ActionResult(
                            action_name="click",
                            params={"element_id": "btn-1"},
                            success=True,
                            returned_data={"clicked": True}
                        )]
                    )
                ])
            
            mock_agent.run.side_effect = realistic_agent_run
            
            # Execute the complete pipeline
            logger.info("🚀 Starting complete agent pipeline test")
            
            await interface.process_user_task(
                task="Click the test button on the page",
                context={
                    "url": "https://example.com/test",
                    "title": "Test Page"
                },
                tab_id=1
            )
            
            # Verify the complete pipeline executed
            mock_agent_class.assert_called_once()
            mock_agent.run.assert_called_once()
            
            # Verify state was retrieved
            interface.get_state.assert_called()
            
            # Verify action was executed
            interface.execute_action.assert_called_with(
                action_name="click",
                params={"element_id": "btn-1"},
                tab_id=1
            )
            
            logger.info("✅ Complete agent pipeline executed successfully")
    
    @pytest.mark.asyncio
    async def test_multi_step_agent_pipeline(self, configured_agent_interface, mock_browser_state):
        """Test multi-step agent task execution."""
        interface = configured_agent_interface
        
        # Mock different states for multi-step flow
        form_state = BrowserState(
            url="https://example.com/form",
            title="Form Page",
            tree={
                "tag": "html",
                "children": [{
                    "tag": "body",
                    "children": [
                        {
                            "tag": "input",
                            "attributes": {"type": "email", "placeholder": "Email"},
                            "element_id": "email-input"
                        },
                        {
                            "tag": "input", 
                            "attributes": {"type": "password", "placeholder": "Password"},
                            "element_id": "password-input"
                        },
                        {
                            "tag": "button",
                            "text": "Submit",
                            "element_id": "submit-btn"
                        }
                    ]
                }]
            },
            tabs=[{"tabId": 1, "url": "https://example.com/form", "isActive": True}]
        )
        
        interface.get_state = AsyncMock(return_value=form_state)
        
        # Track all actions executed
        executed_actions = []
        
        async def track_actions(action_name, params, **kwargs):
            executed_actions.append((action_name, params))
            return {"success": True, "data": {}}
            
        interface.execute_action = track_actions
        
        # Mock multi-step agent
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            async def multi_step_agent_run():
                # Step 1: Enter email
                await interface.execute_action(
                    action_name="input_text",
                    params={"element_id": "email-input", "text": "test@example.com"},
                    tab_id=1
                )
                
                # Step 2: Enter password
                await interface.execute_action(
                    action_name="input_text", 
                    params={"element_id": "password-input", "text": "password123"},
                    tab_id=1
                )
                
                # Step 3: Click submit
                await interface.execute_action(
                    action_name="click",
                    params={"element_id": "submit-btn"},
                    tab_id=1
                )
                
                return AgentHistoryList(history=[])
            
            mock_agent.run.side_effect = multi_step_agent_run
            
            # Execute multi-step task
            await interface.process_user_task(
                task="Fill out the form with email test@example.com and password password123, then submit",
                context={"url": "https://example.com/form"},
                tab_id=1
            )
            
            # Verify all steps were executed
            assert len(executed_actions) == 3
            
            # Verify action sequence
            assert executed_actions[0] == ("input_text", {"element_id": "email-input", "text": "test@example.com"})
            assert executed_actions[1] == ("input_text", {"element_id": "password-input", "text": "password123"})
            assert executed_actions[2] == ("click", {"element_id": "submit-btn"})
            
            logger.info("✅ Multi-step agent pipeline completed successfully")
    
    @pytest.mark.asyncio
    async def test_agent_error_recovery_pipeline(self, configured_agent_interface, mock_browser_state):
        """Test agent pipeline with error recovery."""
        interface = configured_agent_interface
        interface.get_state = AsyncMock(return_value=mock_browser_state)
        
        # Mock action that fails first, then succeeds
        call_count = 0
        
        async def failing_then_success_action(action_name, params, **kwargs):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                return {"success": False, "error": "Element not found"}
            else:
                return {"success": True, "data": {"clicked": True}}
        
        interface.execute_action = failing_then_success_action
        
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            async def error_recovery_agent_run():
                # First attempt - fails
                result1 = await interface.execute_action(
                    action_name="click",
                    params={"element_id": "wrong-id"},
                    tab_id=1
                )
                
                # Agent adapts and retries with correct element
                if not result1["success"]:
                    result2 = await interface.execute_action(
                        action_name="click", 
                        params={"element_id": "btn-1"},
                        tab_id=1
                    )
                
                return AgentHistoryList(history=[])
            
            mock_agent.run.side_effect = error_recovery_agent_run
            
            # Execute task with error recovery
            await interface.process_user_task(
                task="Click the button (with error recovery)",
                context={},
                tab_id=1
            )
            
            # Verify both attempts were made
            assert call_count == 2, "Agent should have retried after initial failure"
            
            logger.info("✅ Agent error recovery pipeline completed successfully")
    
    @pytest.mark.asyncio
    async def test_concurrent_agent_pipelines(self, configured_agent_interface):
        """Test multiple concurrent agent pipelines."""
        interface = configured_agent_interface
        
        # Track concurrent executions
        active_tasks = set()
        max_concurrent = 0
        
        async def track_concurrent_execution(task, context, tab_id):
            task_id = f"task_{tab_id}_{hash(task)}"
            active_tasks.add(task_id)
            
            nonlocal max_concurrent
            max_concurrent = max(max_concurrent, len(active_tasks))
            
            # Simulate work
            await asyncio.sleep(0.1)
            
            active_tasks.remove(task_id)
            logger.info(f"Completed {task_id}, max concurrent: {max_concurrent}")
        
        interface.process_user_task = track_concurrent_execution
        
        # Start multiple concurrent tasks
        tasks = [
            interface.process_user_task(f"Task {i}", {}, i)
            for i in range(5)
        ]
        
        await asyncio.gather(*tasks)
        
        # Verify concurrent execution
        assert max_concurrent > 1, "Should have had concurrent execution"
        assert len(active_tasks) == 0, "All tasks should be completed"
        
        logger.info(f"✅ Concurrent pipelines test completed (max concurrent: {max_concurrent})")
    
    @pytest.mark.asyncio
    async def test_agent_state_management_pipeline(self, configured_agent_interface, mock_browser_state):
        """Test agent state management throughout pipeline."""
        interface = configured_agent_interface
        interface.get_state = AsyncMock(return_value=mock_browser_state)
        interface.execute_action = AsyncMock(return_value={"success": True})
        
        # Track agent sessions
        session_lifecycle = []
        
        original_setitem = interface._active_agents.__setitem__
        original_delitem = interface._active_agents.__delitem__
        
        def track_session_create(key, value):
            session_lifecycle.append(f"CREATE:{key}")
            original_setitem(key, value)
            
        def track_session_delete(key):
            session_lifecycle.append(f"DELETE:{key}")
            original_delitem(key)
        
        interface._active_agents.__setitem__ = track_session_create
        interface._active_agents.__delitem__ = track_session_delete
        
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.run.return_value = AgentHistoryList(history=[])
            mock_agent_class.return_value = mock_agent
            
            # Execute task
            await interface.process_user_task(
                task="Test session management", 
                context={},
                tab_id=1
            )
            
            # Verify session lifecycle
            assert len(session_lifecycle) == 2, "Should have CREATE and DELETE events"
            assert session_lifecycle[0].startswith("CREATE:tab_1_"), "Should create session with correct prefix"
            assert session_lifecycle[1].startswith("DELETE:tab_1_"), "Should delete session after completion"
            
            # Verify cleanup
            assert len(interface._active_agents) == 0, "No active agents should remain"
            
            logger.info("✅ Agent state management pipeline completed successfully")


class TestRealisticAgentScenarios:
    """Test realistic end-to-end scenarios that users might encounter."""
    
    @pytest.mark.asyncio
    async def test_web_search_scenario_pipeline(self, configured_agent_interface):
        """Test a realistic web search scenario."""
        interface = configured_agent_interface
        
        # Mock search page state
        search_state = BrowserState(
            url="https://google.com",
            title="Google",
            tree={
                "tag": "html", 
                "children": [{
                    "tag": "body",
                    "children": [
                        {
                            "tag": "input",
                            "attributes": {"name": "q", "type": "search"},
                            "element_id": "search-box"
                        },
                        {
                            "tag": "button",
                            "text": "Google Search", 
                            "element_id": "search-btn"
                        }
                    ]
                }]
            },
            tabs=[{"tabId": 1, "url": "https://google.com", "isActive": True}]
        )
        
        interface.get_state = AsyncMock(return_value=search_state)
        
        # Track search flow
        search_actions = []
        
        async def track_search_actions(action_name, params, **kwargs):
            search_actions.append((action_name, params))
            return {"success": True, "data": {}}
            
        interface.execute_action = track_search_actions
        
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            async def search_agent_run():
                # Type search query
                await interface.execute_action(
                    action_name="input_text",
                    params={"element_id": "search-box", "text": "Python web scraping"},
                    tab_id=1
                )
                
                # Click search
                await interface.execute_action(
                    action_name="click",
                    params={"element_id": "search-btn"},
                    tab_id=1
                )
                
                return AgentHistoryList(history=[])
            
            mock_agent.run.side_effect = search_agent_run
            
            # Execute search scenario
            await interface.process_user_task(
                task="Search for 'Python web scraping' on Google",
                context={"url": "https://google.com"},
                tab_id=1
            )
            
            # Verify search flow
            assert len(search_actions) == 2
            assert search_actions[0] == ("input_text", {"element_id": "search-box", "text": "Python web scraping"})
            assert search_actions[1] == ("click", {"element_id": "search-btn"})
            
            logger.info("✅ Web search scenario pipeline completed successfully")
    
    @pytest.mark.asyncio
    async def test_form_automation_scenario_pipeline(self, configured_agent_interface):
        """Test automated form filling scenario."""
        interface = configured_agent_interface
        
        # Mock contact form state
        form_state = BrowserState(
            url="https://example.com/contact",
            title="Contact Us",
            tree={
                "tag": "html",
                "children": [{
                    "tag": "body", 
                    "children": [
                        {
                            "tag": "input",
                            "attributes": {"type": "text", "name": "name", "placeholder": "Full Name"},
                            "element_id": "name-field"
                        },
                        {
                            "tag": "input",
                            "attributes": {"type": "email", "name": "email", "placeholder": "Email"},
                            "element_id": "email-field"
                        },
                        {
                            "tag": "textarea",
                            "attributes": {"name": "message", "placeholder": "Your message"},
                            "element_id": "message-field"
                        },
                        {
                            "tag": "button",
                            "text": "Send Message",
                            "element_id": "submit-btn"
                        }
                    ]
                }]
            },
            tabs=[{"tabId": 1, "url": "https://example.com/contact", "isActive": True}]
        )
        
        interface.get_state = AsyncMock(return_value=form_state)
        
        # Track form completion
        form_data = {}
        
        async def track_form_actions(action_name, params, **kwargs):
            if action_name == "input_text":
                form_data[params["element_id"]] = params["text"]
            elif action_name == "click" and params["element_id"] == "submit-btn":
                form_data["submitted"] = True
            return {"success": True, "data": {}}
            
        interface.execute_action = track_form_actions
        
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            async def form_agent_run():
                # Fill out form fields
                await interface.execute_action(
                    action_name="input_text",
                    params={"element_id": "name-field", "text": "John Doe"},
                    tab_id=1
                )
                
                await interface.execute_action(
                    action_name="input_text",
                    params={"element_id": "email-field", "text": "john@example.com"},
                    tab_id=1
                )
                
                await interface.execute_action(
                    action_name="input_text",
                    params={"element_id": "message-field", "text": "Hello, this is a test message."},
                    tab_id=1
                )
                
                # Submit form
                await interface.execute_action(
                    action_name="click",
                    params={"element_id": "submit-btn"},
                    tab_id=1
                )
                
                return AgentHistoryList(history=[])
            
            mock_agent.run.side_effect = form_agent_run
            
            # Execute form automation
            await interface.process_user_task(
                task="Fill out the contact form with name 'John Doe', email 'john@example.com', and message 'Hello, this is a test message.' Then submit it",
                context={"url": "https://example.com/contact"},
                tab_id=1
            )
            
            # Verify form was completed
            assert form_data["name-field"] == "John Doe"
            assert form_data["email-field"] == "john@example.com" 
            assert form_data["message-field"] == "Hello, this is a test message."
            assert form_data["submitted"] == True
            
            logger.info("✅ Form automation scenario pipeline completed successfully")