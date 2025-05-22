# Standard library imports
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

# Third-party imports
from pydantic import BaseModel, Field

# Initialize logger for this module
logger = logging.getLogger(__name__)

class MemoryItem(BaseModel):
    """Represents a single item stored in the agent's memory."""
    key: str = Field(description="Unique key for the memory item.")
    value: Any = Field(description="The value associated with the key.")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of when the memory item was last updated or created.")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional metadata for the memory item (e.g., source, relevance score).")
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AgentMemory:
    """
    A simple in-memory storage for an agent.
    Provides basic CRUD operations for memory items.
    This can be expanded to use databases or vector stores for more complex memory management.
    """

    def __init__(self):
        """Initializes the AgentMemory with an empty dictionary for storage."""
        self._storage: Dict[str, MemoryItem] = {}
        logger.info("AgentMemory initialized.")

    def store(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Stores or updates an item in memory.
        Args:
            key: The unique key for the item.
            value: The value to store.
            metadata: Optional metadata associated with the item.
        """
        if not key:
            logger.warning("Attempted to store memory item with empty key. Skipping.")
            return
            
        item = MemoryItem(key=key, value=value, metadata=metadata or {})
        self._storage[key] = item
        logger.debug(f"Stored/Updated memory item with key: '{key}'")

    def retrieve(self, key: str) -> Optional[MemoryItem]:
        """
        Retrieves an item from memory by its key.
        Args:
            key: The key of the item to retrieve.
        Returns:
            The MemoryItem if found, otherwise None.
        """
        item = self._storage.get(key)
        if item:
            logger.debug(f"Retrieved memory item with key: '{key}'")
        else:
            logger.debug(f"Memory item with key: '{key}' not found.")
        return item

    def retrieve_value(self, key: str) -> Optional[Any]:
        """
        Retrieves only the value of an item from memory by its key.
        Args:
            key: The key of the item.
        Returns:
            The value if the key is found, otherwise None.
        """
        item = self.retrieve(key)
        return item.value if item else None

    def delete(self, key: str) -> bool:
        """
        Deletes an item from memory by its key.
        Args:
            key: The key of the item to delete.
        Returns:
            True if the item was deleted, False if the key was not found.
        """
        if key in self._storage:
            del self._storage[key]
            logger.debug(f"Deleted memory item with key: '{key}'")
            return True
        logger.debug(f"Attempted to delete non-existent memory item with key: '{key}'")
        return False

    def list_keys(self) -> List[str]:
        """Returns a list of all keys currently in memory."""
        return list(self._storage.keys())

    def get_all_items(self) -> List[MemoryItem]:
        """Returns all items currently in memory."""
        return list(self._storage.values())

    def clear_memory(self) -> None:
        """Clears all items from memory."""
        self._storage = {}
        logger.info("Agent memory cleared.")

# Example Usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    memory = AgentMemory()

    # Store items
    memory.store("user_preference_theme", "dark", metadata={"source": "user_settings"})
    memory.store("last_visited_url", "https://example.com/path", metadata={"type": "navigation_history"})
    memory.store("complex_object", {"data": [1, 2, 3], "config": {"active": True}})

    # Retrieve items
    theme = memory.retrieve_value("user_preference_theme")
    logger.info(f"User theme preference: {theme}")

    last_url_item = memory.retrieve("last_visited_url")
    if last_url_item:
        logger.info(f"Last visited URL item: Key='{last_url_item.key}', Value='{last_url_item.value}', Timestamp='{last_url_item.timestamp.isoformat()}', Meta={last_url_item.metadata}")

    non_existent = memory.retrieve("non_existent_key")
    logger.info(f"Non-existent item: {non_existent}")

    # List keys and items
    logger.info(f"All keys in memory: {memory.list_keys()}")
    # logger.info(f"All items: {memory.get_all_items()}") # Can be verbose

    # Delete an item
    deleted = memory.delete("last_visited_url")
    logger.info(f"Deletion of 'last_visited_url' successful: {deleted}")
    logger.info(f"Keys after deletion: {memory.list_keys()}")

    # Clear memory
    memory.clear_memory()
    logger.info(f"Keys after clearing memory: {memory.list_keys()}") 