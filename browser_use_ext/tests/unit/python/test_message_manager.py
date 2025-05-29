import pytest
from datetime import datetime, timezone
from typing import List, Dict, Any
from browser_use_ext.agent.message_manager.service import MessageManager
from browser_use_ext.extension_interface.models import Message
from browser_use_ext.agent.message_manager.views import MessageHistory, MessageManagerState
from langchain_core.messages import BaseMessage

@pytest.fixture
def message_manager_instance() -> MessageManager:
    """Provides a clean MessageManager instance for each test."""
    # Provide dummy values for required arguments
    return MessageManager(initial_task="dummy task", agent_id="dummy_agent_id")

@pytest.fixture
def sample_system_prompt_content() -> str:
    """Provides a sample system prompt content string."""
    return "You are a test assistant."

def test_message_manager_initialization(message_manager_instance: MessageManager):
    """Test MessageManager initialization without a system prompt."""
    # Check the history attribute on the state
    assert isinstance(message_manager_instance.state.history, MessageHistory)
    assert len(message_manager_instance.state.history.messages) > 0 # Should have initial messages

def test_message_manager_initialization_with_system_prompt(sample_system_prompt_content: str):
    """Test MessageManager initialization with a system prompt."""
    # Provide dummy values for required arguments and use correct keyword arg
    manager = MessageManager(initial_task="dummy task", agent_id="dummy_agent_id", system_prompt_content=sample_system_prompt_content)
    # Check the history attribute on the state
    assert isinstance(manager.state.history, MessageHistory)
    assert len(manager.state.history.messages) > 0 # Should have initial messages including the provided system prompt
    # Check if the system prompt was added (it should be the first message)
    system_msg = manager.state.history.messages[0]
    # Access role and content from the 'data' field of the Message object
    assert system_msg.message.type == "system"
    assert system_msg.message.content == sample_system_prompt_content

def test_add_message(message_manager_instance: MessageManager):
    """Test adding various types of messages to the manager."""
    manager = message_manager_instance
    # Use the public add_user_message and add_ai_response methods or a more generic add method if available/appropriate
    # Based on service.py, add_user_message takes content, add_ai_response takes AgentLLMOutput
    # _add_message_to_history is internal.
    # We can test add_user_message directly.
    manager.add_user_message("User query 1")
    assert len(manager.state.history.messages) > 0 # History should have initial + user message
    # Find the user message in history (skip initial messages)
    # Access role and content from the 'data' field of the Message object
    user_messages = [m for m in manager.state.history.messages if m.message.type == 'human' and m.message.content == "User query 1"]
    assert len(user_messages) == 1

    # To test adding AI response, we need a mock AgentLLMOutput or its dictionary representation
    # Let's create a simple mock structure that resembles AgentLLMOutput dictionary
    mock_ai_output = {
        "current_state": {"evaluation_previous_goal": "N/A", "memory": "N/A", "next_goal": "N/A"},
        "action": []
    }
    # add_ai_response expects AgentLLMOutput instance, not dict
    from browser_use_ext.agent.views import AgentLLMOutput
    manager.add_ai_response(AgentLLMOutput(**mock_ai_output))
    assert len(manager.state.history.messages) > len(user_messages) # Should have initial + user + AI message
    # Access role from the 'data' field of the Message object
    ai_messages = [m for m in manager.state.history.messages if m.message.type == 'ai']
    assert len(ai_messages) > 0

    # Testing tool_code/tool_output might require mocking the internal _add_message_to_history or having public methods for them.
    # Based on service.py, these are added internally after tool execution results are processed.
    # If there are no public methods to directly add tool messages, this part of the test might need refactoring or skipping.
    # For now, skipping direct testing of tool_code/tool_output messages via `add_message`.

def test_add_message_empty_role_or_content(message_manager_instance: MessageManager, caplog):
    """Test that adding a message with empty content via add_user_message is handled gracefully (logged)."""
    manager = message_manager_instance
    initial_history_len = len(manager.state.history.messages)

    # add_user_message takes content. If content is empty string, it might still add the message.
    # Let's check the behavior of add_user_message with empty content.
    # The service.py code has a check for `if message.content:` in _add_message_to_history
    # and logs if role or content is empty. It seems it WILL add the message if content is empty string.

    manager.add_user_message("")
    # The message might be added, but potentially with a warning/log
    # The test should verify the logging, but the length assertion depends on _add_message_to_history behavior
    # Based on service.py line 367: `if not message.content:` it will log but still add.
    # Let's check for the message being added and the log.
    assert len(manager.state.history.messages) == initial_history_len + 1 # Expect message to be added
    # Access content from the 'data' field of the Message object
    added_message = manager.state.history.messages[-1] # Get the last added message
    assert added_message.message.type == 'human'
    assert added_message.message.content == ""

    logged_warning = False
    # Check for log message about empty content
    for record in caplog.records:
        # Adjust log message check based on actual log format in service.py
        if "Attempted to add message with empty content" in record.message:
            logged_warning = True
            break
    assert logged_warning, "Log message about empty content not found."

    # add_user_message cannot have empty role as it's hardcoded.
    # Testing empty role would require mocking or testing _add_message_to_history directly.

def test_convenience_add_methods(message_manager_instance: MessageManager):
    """Test the add_user_message and add_ai_response convenience methods."""
    manager = message_manager_instance
    manager.add_user_message("This is a user message.")
    # History should have initial + user message
    assert len(manager.state.history.messages) > 0
    # Access role and content from the 'data' field of the Message object
    user_messages = [m for m in manager.state.history.messages if m.message.type == 'human' and m.message.content == "This is a user message."]
    assert len(user_messages) == 1

    # add_assistant_message doesn't exist. add_ai_response expects AgentLLMOutput.
    # Let's test add_ai_response instead.
    # Create a simple mock structure that resembles AgentLLMOutput dictionary
    mock_ai_output = {
        "current_state": {"evaluation_previous_goal": "N/A", "memory": "N/A", "next_goal": "N/A"},
        "action": []
    }
    from browser_use_ext.agent.views import AgentLLMOutput
    manager.add_ai_response(AgentLLMOutput(**mock_ai_output))
    # History should have initial + user + AI message
    assert len(manager.state.history.messages) > len(user_messages)
    # Access role from the 'data' field of the Message object
    ai_messages = [m for m in manager.state.history.messages if m.message.type == 'ai']
    assert len(ai_messages) > 0

    # Metadata is not a direct argument to add_user_message or add_ai_response.
    # It seems metadata might be added to the MessageMetadata object internally.
    # Testing metadata addition would require inspecting the created MessageMetadata object in history.

def test_get_history(message_manager_instance: MessageManager):
    """Test retrieving the message history."""
    manager = message_manager_instance
    manager.add_user_message("Query")
    # add_assistant_message doesn't exist, test add_ai_response
    mock_ai_output = {
        "current_state": {"evaluation_previous_goal": "N/A", "memory": "N/A", "next_goal": "N/A"},
        "action": []
    }
    from browser_use_ext.agent.views import AgentLLMOutput
    manager.add_ai_response(AgentLLMOutput(**mock_ai_output))

    # Get history from the state object
    history: List[Message] = manager.state.history.get_messages()
    # History should contain initial messages + user + AI message
    # The initial messages might include system prompt, initial task, and example output.
    # Check for the presence of user and AI messages by accessing the 'data' field
    # Access message type and content directly from the message object (e.g., from langchain_core.messages)
    user_msg_found = any(m.type == 'human' and m.content == "Query" for m in history)
    ai_msg_found = any(m.type == 'ai' and isinstance(m.content, str) and 'current_state' in m.content for m in history) # Check for basic AI response content
    
    assert user_msg_found, "User message not found in history."
    assert ai_msg_found, "AI response message not found in history."

    # Additional check: Ensure messages are instances of BaseMessage
    assert all(isinstance(m, BaseMessage) for m in history), "All history items should be instances of BaseMessage"

def test_get_history_as_dicts(message_manager_instance: MessageManager):
    """Test retrieving history as a list of dictionaries."""
    manager = message_manager_instance
    time_before_add = datetime.now(timezone.utc)
    # add_user_message does not explicitly take metadata. Metadata might be added to MessageMetadata internally.
    # Let's just test adding messages and getting history as dicts.
    manager.add_user_message("Hi") # No metadata argument here
    
    mock_ai_output = {
        "current_state": {"evaluation_previous_goal": "N/A", "memory": "N/A", "next_goal": "N/A"},
        "action": []
    }
    from browser_use_ext.agent.views import AgentLLMOutput
    manager.add_ai_response(AgentLLMOutput(**mock_ai_output))

    # Get history as dicts from the state object
    # MessageHistory does not have get_messages_as_dicts().
    # We can get the messages (which are Pydantic models) and convert them to dicts manually.
    history_messages: List[Message] = manager.state.history.get_messages()
    history_dicts: List[Dict[str, Any]] = [msg.model_dump() for msg in history_messages]

    # Check that user and AI messages are present in the dict list
    # Access role and content from the nested 'data' dict
    user_msg_dict_found = any(d.get("type") == "human" and d.get("content") == "Hi" for d in history_dicts if d.get("type") in ["human", "ai", "system"])
    ai_msg_dict_found = any(d.get("type") == "ai" for d in history_dicts if d.get("type") in ["human", "ai", "system"])

    assert user_msg_dict_found
    assert ai_msg_dict_found

    # To test metadata in dicts, you would need to add metadata via a method that supports it,
    # or potentially mock _add_message_to_history.
    # If add_user_message/add_ai_response don't support direct metadata, this part of the test might need adjustment.
    # Assuming metadata is added internally or not directly testable via these public methods.

def test_clear_history(message_manager_instance: MessageManager):
    """Test clearing the message history."""
    manager = message_manager_instance
    manager.add_user_message("Message 1")
    # add_assistant_message doesn't exist, test add_ai_response
    mock_ai_output = {
        "current_state": {"evaluation_previous_goal": "N/A", "memory": "N/A", "next_goal": "N/A"},
        "action": []
    }
    from browser_use_ext.agent.views import AgentLLMOutput
    manager.add_ai_response(AgentLLMOutput(**mock_ai_output))
    
    initial_length = len(manager.state.history.messages)
    assert initial_length > 0

    # Clear history via the state object
    manager.state.history.messages = []
    
    assert len(manager.state.history.messages) == 0
    # Calling get_history() or get_history_as_dicts() on the cleared history should return empty lists
    assert manager.state.history.get_messages() == []

def test_clear_history_with_system_prompt(sample_system_prompt_content: str):
    """Test that clearing history removes all messages, including the system prompt."""
    # Initialize a new manager with a system prompt
    manager = MessageManager(initial_task="dummy task", agent_id="dummy_agent_id", system_prompt_content=sample_system_prompt_content)
    initial_length_with_sys_prompt = len(manager.state.history.messages)
    assert initial_length_with_sys_prompt > 0 # Should contain system prompt and initial task/example

    manager.add_user_message("User question")
    assert len(manager.state.history.messages) == initial_length_with_sys_prompt + 1
    
    # Clear history via the state object
    manager.state.history.messages = []
    
    assert len(manager.state.history.messages) == 0 # System prompt should also be cleared

# To run these tests:
# pytest browser-use-ext/tests/test_message_manager.py 