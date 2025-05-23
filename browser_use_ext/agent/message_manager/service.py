# Standard library imports
import logging
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone

# Third-party imports
from pydantic import BaseModel, Field

# Initialize logger for this module
logger = logging.getLogger(__name__)

class Message(BaseModel):
    """Represents a single message in a conversation or interaction history."""
    role: Literal["user", "assistant", "system", "tool_code", "tool_output"] = Field(description="The role of the message sender.")
    content: str = Field(description="The textual content of the message.")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of when the message was created.")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional metadata associated with the message.")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() # Ensure datetime is serialized to ISO format
        }

class MessageManager:
    """
    Manages a list of messages, representing a conversation history.
    Provides methods to add messages and retrieve the history.
    """
    def __init__(self, system_prompt: Optional[str] = None):
        """
        Initializes the MessageManager.
        Args:
            system_prompt: An optional system prompt to pre-pend to the message history.
        """
        self.history: List[Message] = []
        if system_prompt:
            self.add_message(role="system", content=system_prompt)
        logger.info(f"MessageManager initialized. System prompt {'set' if system_prompt else 'not set'}.")

    def add_message(self, role: Literal["user", "assistant", "system", "tool_code", "tool_output"], content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Adds a new message to the history.
        Args:
            role: The role of the message sender.
            content: The content of the message.
            metadata: Optional metadata for the message.
        """
        if not role or not content:
            logger.warning("Attempted to add message with empty role or content. Skipping.")
            return
            
        message = Message(role=role, content=content, metadata=metadata or {})
        self.history.append(message)
        logger.debug(f"Added message: Role='{role}', Content='{content[:50]}...'")

    def get_history(self) -> List[Message]:
        """Returns the current message history."""
        return self.history

    def get_history_as_dicts(self) -> List[Dict[str, Any]]:
        """Returns the current message history as a list of dictionaries, with datetimes as ISO strings."""
        # Using model_dump with mode='json' ensures that json_encoders are applied.
        return [msg.model_dump(mode='json', exclude_none=True) for msg in self.history]

    def clear_history(self) -> None:
        """Clears all messages from the history."""
        self.history = []
        logger.info("Message history cleared.")

    def add_user_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Convenience method to add a user message."""
        self.add_message(role="user", content=content, metadata=metadata)

    def add_assistant_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Convenience method to add an assistant message."""
        self.add_message(role="assistant", content=content, metadata=metadata)

# Example Usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # Initialize with a system prompt
    manager = MessageManager(system_prompt="You are a helpful AI assistant.")
    manager.add_user_message("Hello, assistant!")
    manager.add_assistant_message("Hello, user! How can I help you today?")
    manager.add_message(role="tool_code", content="print('Hello from tool')")
    manager.add_message(role="tool_output", content="Hello from tool")

    history = manager.get_history()
    for msg in history:
        logger.info(f"[{msg.timestamp.isoformat()}] {msg.role.upper()}: {msg.content}")

    history_dicts = manager.get_history_as_dicts()
    logger.info(f"History as dicts: {history_dicts}")

    manager.clear_history()
    logger.info(f"History count after clear: {len(manager.get_history())}") 