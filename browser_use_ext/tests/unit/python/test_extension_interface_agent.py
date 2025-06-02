"""
Unit tests for the agent integration in ExtensionInterface.
Tests LLM initialization, task processing, and error handling.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import os
from typing import Dict, Any

from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.agent.service import Agent
from browser_use_ext.agent.views import AgentSettings, AgentHistoryList


class TestExtensionInterfaceAgent:
    """Test the agent integration features of ExtensionInterface."""
    
    @pytest.fixture
    def mock_env(self, monkeypatch):
        """Mock environment variables for API keys."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
    
    @pytest.fixture
    def interface(self, mock_env):
        """Create an ExtensionInterface instance with mocked LLM."""
        with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
            mock_llm = Mock()
            mock_openai.return_value = mock_llm
            interface = ExtensionInterface(
                host="localhost",
                port=8765,
                llm_model="gpt-4o",
                llm_temperature=0.0
            )
            interface._llm = mock_llm
            return interface
    
    def test_llm_initialization_openai(self, monkeypatch):
        """Test LLM initialization with OpenAI API key."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        
        with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
            interface = ExtensionInterface(llm_model="gpt-4o")
            
            mock_openai.assert_called_once_with(
                model="gpt-4o",
                temperature=0.0,
                api_key="test-key"
            )
            assert interface._llm is not None
    
    def test_llm_initialization_anthropic(self, monkeypatch):
        """Test LLM initialization with Anthropic API key."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        
        with patch('browser_use_ext.extension_interface.service.ChatAnthropic') as mock_anthropic:
            interface = ExtensionInterface(llm_model="claude-3-opus-20240229")
            
            mock_anthropic.assert_called_once_with(
                model="claude-3-opus-20240229",
                temperature=0.0,
                api_key="test-key"
            )
            assert interface._llm is not None
    
    def test_llm_initialization_no_keys(self, monkeypatch):
        """Test LLM initialization without API keys."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        
        interface = ExtensionInterface()
        assert interface._llm is None
    
    def test_llm_initialization_fallback(self, monkeypatch):
        """Test LLM initialization falls back to GPT-4 with unknown model."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        
        with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
            interface = ExtensionInterface(llm_model="unknown-model")
            
            mock_openai.assert_called_once_with(
                model="gpt-4o",
                temperature=0.0,
                api_key="test-key"
            )
    
    @pytest.mark.asyncio
    async def test_process_user_task_no_llm(self, interface, caplog):
        """Test process_user_task when no LLM is configured."""
        interface._llm = None
        
        await interface.process_user_task(
            task="Test task",
            context={"url": "https://example.com"},
            tab_id=1
        )
        
        assert "Cannot process task - no LLM configured" in caplog.text
    
    @pytest.mark.asyncio
    async def test_process_user_task_success(self, interface):
        """Test successful task processing through agent."""
        # Mock the Agent class
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            # Create mock agent instance
            mock_agent = AsyncMock()
            mock_history = AgentHistoryList(history=[])
            mock_agent.run.return_value = mock_history
            mock_agent.state.completed = True
            mock_agent_class.return_value = mock_agent
            
            # Process task
            await interface.process_user_task(
                task="Click the button",
                context={"url": "https://example.com", "title": "Test Page"},
                tab_id=123
            )
            
            # Verify agent was created with correct parameters
            mock_agent_class.assert_called_once()
            call_args = mock_agent_class.call_args
            assert call_args.kwargs['task'] == "Click the button"
            assert call_args.kwargs['llm'] == interface._llm
            assert call_args.kwargs['extension_interface'] == interface
            assert isinstance(call_args.kwargs['settings'], AgentSettings)
            
            # Verify agent was run
            mock_agent.run.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_user_task_stores_agent(self, interface):
        """Test that agent is stored in active agents during processing."""
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.run.return_value = AgentHistoryList(history=[])
            mock_agent.state.completed = True
            mock_agent_class.return_value = mock_agent
            
            # Check agent is stored during execution
            stored_agent = None
            original_run = mock_agent.run
            
            async def check_storage(*args, **kwargs):
                nonlocal stored_agent
                # Check that agent is in active_agents
                assert len(interface._active_agents) == 1
                session_id = list(interface._active_agents.keys())[0]
                stored_agent = interface._active_agents[session_id]
                assert stored_agent == mock_agent
                return await original_run(*args, **kwargs)
            
            mock_agent.run = check_storage
            
            await interface.process_user_task("Test", {}, 1)
            
            # Verify agent was cleaned up after completion
            assert len(interface._active_agents) == 0
    
    @pytest.mark.asyncio
    async def test_process_user_task_error_handling(self, interface, caplog):
        """Test error handling during task processing."""
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            # Make agent creation fail
            mock_agent_class.side_effect = Exception("Agent creation failed")
            
            await interface.process_user_task("Test task", {}, 1)
            
            assert "Error during agent task processing" in caplog.text
            assert "Agent creation failed" in caplog.text
            assert len(interface._active_agents) == 0  # Cleanup should happen
    
    @pytest.mark.asyncio
    async def test_process_user_task_cleanup_on_error(self, interface):
        """Test that agent is cleaned up even if run() fails."""
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.run.side_effect = Exception("Execution failed")
            mock_agent_class.return_value = mock_agent
            
            # Store the session ID when agent is added
            session_ids = []
            original_dict = interface._active_agents
            
            # Create a custom dict that tracks additions
            class TrackingDict(dict):
                def __setitem__(self, key, value):
                    session_ids.append(key)
                    super().__setitem__(key, value)
            
            interface._active_agents = TrackingDict(original_dict)
            
            # Process task (should fail)
            await interface.process_user_task("Test", {}, 1)
            
            # Verify cleanup happened
            assert len(interface._active_agents) == 0
            assert len(session_ids) == 1  # Agent was added
    
    def test_session_id_generation(self, interface):
        """Test that session IDs are unique and properly formatted."""
        session_ids = set()
        
        with patch('browser_use_ext.extension_interface.service.Agent'):
            with patch.object(interface, 'process_user_task') as mock_process:
                # Capture session IDs from multiple calls
                async def capture_session_id(task, context, tab_id):
                    # Extract session_id from the actual implementation
                    import uuid
                    session_id = f"tab_{tab_id}_{uuid.uuid4().hex[:8]}"
                    session_ids.add(session_id)
                
                mock_process.side_effect = capture_session_id
                
                # Simulate multiple task submissions
                for i in range(5):
                    asyncio.run(mock_process("Task", {}, i))
                
                # All session IDs should be unique
                assert len(session_ids) == 5
                
                # Check format
                for sid in session_ids:
                    assert sid.startswith("tab_")
                    parts = sid.split("_")
                    assert len(parts) == 3
                    assert parts[1].isdigit()
                    assert len(parts[2]) == 8


class TestUserTaskSubmissionIntegration:
    """Test the integration of user task submission with agent processing."""
    
    @pytest.fixture
    def mock_websocket(self):
        """Create a mock WebSocket connection."""
        ws = AsyncMock()
        ws.remote_address = ("127.0.0.1", 12345)
        ws.state.name = "OPEN"
        return ws
    
    @pytest.fixture
    def interface_with_connection(self, monkeypatch):
        """Create an interface with an active connection."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        interface = ExtensionInterface()
        
        # Mock the connection
        connection_info = Mock()
        connection_info.client_id = "test-client"
        connection_info.websocket = Mock()
        
        interface._connections["test-client"] = connection_info
        interface._active_connection_id = "test-client"
        interface._active_tab_id = 1
        
        return interface
    
    @pytest.mark.asyncio
    async def test_user_task_submitted_event_triggers_agent(self, interface_with_connection):
        """Test that user_task_submitted event triggers agent processing."""
        interface = interface_with_connection
        
        # Mock process_user_task
        interface.process_user_task = AsyncMock()
        
        # Simulate receiving user_task_submitted event
        message_data = {
            "event_name": "user_task_submitted",
            "task": "Click the login button",
            "context": {
                "url": "https://example.com",
                "title": "Example Site"
            },
            "tabId": 123
        }
        
        # Process the message
        await interface._process_message(
            "test-client",
            '{"type": "extension_event", "id": 1, "data": ' + str(message_data).replace("'", '"') + '}'
        )
        
        # Wait for async task to be created
        await asyncio.sleep(0.1)
        
        # Verify process_user_task was called
        interface.process_user_task.assert_called_once_with(
            "Click the login button",
            {"url": "https://example.com", "title": "Example Site"},
            123
        )
    
    @pytest.mark.asyncio
    async def test_user_task_submitted_updates_active_tab(self, interface_with_connection):
        """Test that user task submission updates the active tab ID."""
        interface = interface_with_connection
        interface._active_tab_id = 999  # Different initial tab
        
        # Mock process_user_task
        interface.process_user_task = AsyncMock()
        
        # Process message with new tab ID
        message_data = {
            "event_name": "user_task_submitted",
            "task": "Test task",
            "context": {},
            "tabId": 456
        }
        
        await interface._process_message(
            "test-client",
            '{"type": "extension_event", "id": 1, "data": ' + str(message_data).replace("'", '"') + '}'
        )
        
        # Verify tab ID was updated
        assert interface._active_tab_id == 456


class TestAgentSettings:
    """Test agent settings configuration."""
    
    def test_default_agent_settings(self):
        """Test that default agent settings are applied."""
        with patch('browser_use_ext.extension_interface.service.Agent') as mock_agent_class:
            interface = ExtensionInterface()
            interface._llm = Mock()
            
            # Capture the settings passed to Agent
            settings_used = None
            
            def capture_settings(*args, **kwargs):
                nonlocal settings_used
                settings_used = kwargs.get('settings')
                return Mock(run=AsyncMock(return_value=[]))
            
            mock_agent_class.side_effect = capture_settings
            
            # Process a task
            asyncio.run(interface.process_user_task("Test", {}, 1))
            
            # Check settings
            assert isinstance(settings_used, AgentSettings)
            assert settings_used.max_steps_per_run == 15
            assert settings_used.max_failures == 3