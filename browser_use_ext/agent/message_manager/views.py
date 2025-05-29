from __future__ import annotations

from typing import TYPE_CHECKING, Any, List # Added List
from warnings import filterwarnings

from langchain_core._api import LangChainBetaWarning
from langchain_core.load import dumpd, load
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage # Removed ToolMessage for now, add if needed
from pydantic import BaseModel, ConfigDict, Field, model_serializer, model_validator

filterwarnings('ignore', category=LangChainBetaWarning)

# No longer importing AgentOutput from the old views
# if TYPE_CHECKING:
#     from browser_use_ext.agent.views import AgentLLMOutput # If needed for type hinting in future

import logging # Ensure logging is imported

class MessageMetadata(BaseModel):
    """Metadata for a message"""
    tokens: int = 0
    message_type: str | None = None # e.g., 'init', 'state', 'model_output', 'action_result'

class ManagedMessage(BaseModel):
    """A message with its metadata, supporting Langchain BaseMessage serialization."""
    message: Any # Changed from BaseMessage to Any temporarily
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode='before')
    @classmethod
    def pre_validate_message_field(cls, data: Any) -> Any:
        if isinstance(data, dict):
            msg_value = data.get('message')
            if not isinstance(msg_value, BaseMessage):
                # If it's a dict (potentially from JSON), try to load it via Langchain
                # This re-enables the previous custom_validator logic for deserialization
                if isinstance(msg_value, (str, bytes)):
                    try:
                        data['message'] = load(msg_value)
                    except Exception as e:
                        logging.getLogger(__name__).warning(f"Could not load message via langchain.load in pre_validate: {e}. Value: {str(msg_value)[:100]}...")
                elif isinstance(msg_value, dict) and not isinstance(msg_value, BaseMessage):
                     # Attempt to create a generic BaseMessage or specific type if identifiable
                     # This part is tricky if it's just a dict without clear type info for BaseMessage hierarchy
                     # For now, if it's a dict but not BaseMessage, Pydantic might error or we let it pass to main validation
                     pass 
            # If msg_value is already a BaseMessage, do nothing, let it pass through.
        return data

    # Custom serializer to handle BaseMessage correctly with Langchain's tools
    @model_serializer(mode='wrap')
    def to_json_custom_serializer(self, original_dump_method):
        data = original_dump_method(self)
        if isinstance(self.message, BaseMessage):
            data['message'] = dumpd(self.message) # Use Langchain's serialization
        return data

class MessageHistory(BaseModel):
    """History of messages with metadata, for use within MessageManager."""
    messages: List[ManagedMessage] = Field(default_factory=list)
    current_tokens: int = 0

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def add_message(self, message: BaseMessage, metadata: MessageMetadata, position: int | None = None) -> None:
        """Add message with metadata to history."""
        managed_msg = ManagedMessage(message=message, metadata=metadata)
        if position is None:
            self.messages.append(managed_msg)
        else:
            self.messages.insert(position, managed_msg)
        self.current_tokens += metadata.tokens

    # add_model_output is removed from here, will be handled by MessageManager service class

    def get_messages(self) -> List[BaseMessage]:
        """Get all BaseMessage objects from the history."""
        return [m.message for m in self.messages]

    def get_total_tokens(self) -> int:
        """Get total tokens in history based on stored metadata."""
        # Recalculate to be safe, or trust self.current_tokens if updates are perfect
        return sum(m.metadata.tokens for m in self.messages)
        # return self.current_tokens 

    def remove_oldest_message_if_needed(self) -> ManagedMessage | None:
        """Remove the oldest non-SystemMessage if there are messages to remove.
           Returns the removed message or None.
        """
        # Find the first non-SystemMessage to remove. System messages are usually kept.
        for i, msg_item in enumerate(self.messages):
            if not isinstance(msg_item.message, SystemMessage):
                self.current_tokens -= msg_item.metadata.tokens
                return self.messages.pop(i)
        return None # No non-system message found to remove

    def remove_last_n_messages(self, n: int) -> List[ManagedMessage]:
        """Removes the last N messages that are not SystemMessages.
           Returns the list of removed messages.
        """
        removed_messages = []
        count_removed = 0
        idx = len(self.messages) - 1
        while idx >= 0 and count_removed < n:
            if not isinstance(self.messages[idx].message, SystemMessage):
                removed_msg = self.messages.pop(idx)
                self.current_tokens -= removed_msg.metadata.tokens
                removed_messages.append(removed_msg)
                count_removed += 1
            idx -= 1
        return list(reversed(removed_messages)) # Return in order they were in history

class MessageManagerState(BaseModel):
    """Holds the state for MessageManager, primarily the message history."""
    history: MessageHistory = Field(default_factory=MessageHistory)
    # tool_id: int = 1 # Removed, as direct tool_id management might not be needed if not using tool_calls for AgentLLMOutput

    model_config = ConfigDict(arbitrary_types_allowed=True) 