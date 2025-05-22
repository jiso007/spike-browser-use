import pytest
from datetime import datetime, timezone
from typing import List, Dict, Any
from agent.message_manager.service import Message, MessageManager

@pytest.fixture
def message_manager_instance() -> MessageManager:
    """Provides a clean MessageManager instance for each test."""
    return MessageManager()

@pytest.fixture
def sample_system_prompt() -> str:
    """Provides a sample system prompt string."""
    return "You are a test assistant."

def test_message_creation():
    """Test basic Message Pydantic model creation and default values."""
    content = "Test message content"
    role = "user"
    msg = Message(role=role, content=content)
    
    assert msg.role == role
    assert msg.content == content
    assert isinstance(msg.timestamp, datetime)
    assert msg.timestamp.tzinfo == timezone.utc
    assert msg.metadata == {}

    # Test with metadata
    meta = {"source": "test"}
    msg_with_meta = Message(role="assistant", content="Meta content", metadata=meta)
    assert msg_with_meta.metadata == meta

def test_message_manager_initialization(message_manager_instance: MessageManager):
    """Test MessageManager initialization without a system prompt."""
    assert message_manager_instance.history == []

def test_message_manager_initialization_with_system_prompt(sample_system_prompt: str):
    """Test MessageManager initialization with a system prompt."""
    manager = MessageManager(system_prompt=sample_system_prompt)
    assert len(manager.history) == 1
    system_msg = manager.history[0]
    assert system_msg.role == "system"
    assert system_msg.content == sample_system_prompt

def test_add_message(message_manager_instance: MessageManager):
    """Test adding various types of messages to the manager."""
    manager = message_manager_instance
    manager.add_message(role="user", content="User query 1")
    assert len(manager.history) == 1
    assert manager.history[0].role == "user"
    assert manager.history[0].content == "User query 1"

    manager.add_message(role="assistant", content="Assistant response", metadata={"tool_used": "search"})
    assert len(manager.history) == 2
    assert manager.history[1].role == "assistant"
    assert manager.history[1].metadata == {"tool_used": "search"}

    manager.add_message(role="tool_code", content="print('tool code')")
    assert len(manager.history) == 3
    assert manager.history[2].role == "tool_code"

    manager.add_message(role="tool_output", content="Tool output result")
    assert len(manager.history) == 4
    assert manager.history[3].role == "tool_output"

def test_add_message_empty_role_or_content(message_manager_instance: MessageManager, caplog):
    """Test that adding a message with empty role or content is handled gracefully (logged and skipped)."""
    manager = message_manager_instance
    initial_history_len = len(manager.history)

    manager.add_message(role="", content="Some content")
    assert len(manager.history) == initial_history_len
    assert "Attempted to add message with empty role or content" in caplog.text
    caplog.clear()

    manager.add_message(role="user", content="")
    assert len(manager.history) == initial_history_len
    assert "Attempted to add message with empty role or content" in caplog.text
    caplog.clear()

    manager.add_message(role="", content="")
    assert len(manager.history) == initial_history_len
    assert "Attempted to add message with empty role or content" in caplog.text

def test_convenience_add_methods(message_manager_instance: MessageManager):
    """Test the add_user_message and add_assistant_message convenience methods."""
    manager = message_manager_instance
    manager.add_user_message("This is a user message.")
    assert len(manager.history) == 1
    assert manager.history[0].role == "user"
    assert manager.history[0].content == "This is a user message."

    manager.add_assistant_message("This is an assistant reply.", metadata={"id": 123})
    assert len(manager.history) == 2
    assert manager.history[1].role == "assistant"
    assert manager.history[1].content == "This is an assistant reply."
    assert manager.history[1].metadata == {"id": 123}

def test_get_history(message_manager_instance: MessageManager):
    """Test retrieving the message history."""
    manager = message_manager_instance
    manager.add_user_message("Query")
    manager.add_assistant_message("Reply")
    
    history: List[Message] = manager.get_history()
    assert len(history) == 2
    assert history[0].content == "Query"
    assert history[1].content == "Reply"
    # Ensure it returns a copy, not the internal list (though current implementation returns the list itself)
    # To test for a copy, you might append to `history` and check `manager.history`
    # For now, this basic check is fine.

def test_get_history_as_dicts(message_manager_instance: MessageManager):
    """Test retrieving history as a list of dictionaries."""
    manager = message_manager_instance
    time_before_add = datetime.now(timezone.utc)
    manager.add_user_message("Hi", metadata={"seq": 1})
    manager.add_assistant_message("Hello")

    history_dicts: List[Dict[str, Any]] = manager.get_history_as_dicts()
    assert len(history_dicts) == 2

    msg1_dict = history_dicts[0]
    assert msg1_dict["role"] == "user"
    assert msg1_dict["content"] == "Hi"
    assert msg1_dict["metadata"] == {"seq": 1}
    assert isinstance(msg1_dict["timestamp"], str) # Serialized to ISO format
    dt_obj1 = datetime.fromisoformat(msg1_dict["timestamp"])
    assert dt_obj1 >= time_before_add

    msg2_dict = history_dicts[1]
    assert msg2_dict["role"] == "assistant"
    assert msg2_dict["content"] == "Hello"
    assert msg2_dict["metadata"] == {}
    assert isinstance(msg2_dict["timestamp"], str)
    dt_obj2 = datetime.fromisoformat(msg2_dict["timestamp"])
    assert dt_obj2 >= dt_obj1

def test_clear_history(message_manager_instance: MessageManager):
    """Test clearing the message history."""
    manager = message_manager_instance
    manager.add_user_message("Message 1")
    manager.add_assistant_message("Message 2")
    assert len(manager.history) == 2

    manager.clear_history()
    assert len(manager.history) == 0
    assert manager.get_history() == []

def test_clear_history_with_system_prompt(sample_system_prompt: str):
    """Test that clearing history does not remove an initial system prompt if manager is re-initialized."""
    # The current clear_history() simply resets self.history = []. 
    # If a system prompt was added at initialization, it will be cleared too.
    # This test reflects the current behavior.
    manager = MessageManager(system_prompt=sample_system_prompt)
    assert len(manager.history) == 1
    manager.add_user_message("User question")
    assert len(manager.history) == 2

    manager.clear_history()
    assert len(manager.history) == 0 # System prompt is also cleared

    # If the requirement was to preserve the system prompt on clear, 
    # clear_history() would need to be implemented differently, e.g.:
    # self.history = [msg for msg in self.history if msg.role == "system"]
    # or re-add the system prompt if one was configured initially.

# To run these tests:
# pytest browser-use-ext/tests/test_message_manager.py 