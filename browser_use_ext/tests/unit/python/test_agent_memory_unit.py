"""
Unit tests for the AgentMemory system.

Tests the AgentMemory class and MemoryItem model from browser_use_ext.agent.memory.service.
"""

import pytest
from datetime import datetime, timezone
from typing import Dict, Any
from unittest.mock import patch, MagicMock

from browser_use_ext.agent.memory.service import AgentMemory, MemoryItem


class TestMemoryItem:
    """Test the MemoryItem Pydantic model."""
    
    def test_memory_item_creation_with_required_fields(self):
        """Test creating a MemoryItem with only required fields."""
        item = MemoryItem(key="test_key", value="test_value")
        
        assert item.key == "test_key"
        assert item.value == "test_value"
        assert isinstance(item.timestamp, datetime)
        assert item.timestamp.tzinfo == timezone.utc
        assert item.metadata == {}
    
    def test_memory_item_creation_with_all_fields(self):
        """Test creating a MemoryItem with all fields specified."""
        custom_timestamp = datetime.now(timezone.utc)
        custom_metadata = {"source": "test", "priority": "high"}
        
        item = MemoryItem(
            key="test_key",
            value="test_value", 
            timestamp=custom_timestamp,
            metadata=custom_metadata
        )
        
        assert item.key == "test_key"
        assert item.value == "test_value"
        assert item.timestamp == custom_timestamp
        assert item.metadata == custom_metadata
    
    def test_memory_item_with_complex_value(self):
        """Test MemoryItem can store complex data structures."""
        complex_value = {
            "nested": {"data": [1, 2, 3]},
            "config": {"active": True, "count": 42}
        }
        
        item = MemoryItem(key="complex", value=complex_value)
        
        assert item.value == complex_value
        assert item.value["nested"]["data"] == [1, 2, 3]
        assert item.value["config"]["active"] is True
    
    def test_memory_item_json_serialization(self):
        """Test that MemoryItem can be serialized to JSON."""
        item = MemoryItem(
            key="test_key",
            value="test_value",
            metadata={"source": "unit_test"}
        )
        
        # Test model_dump (Pydantic v2)
        data = item.model_dump()
        assert data["key"] == "test_key"
        assert data["value"] == "test_value"
        assert "timestamp" in data
        assert data["metadata"] == {"source": "unit_test"}
    
    def test_memory_item_timestamp_auto_generation(self):
        """Test that timestamp is automatically generated if not provided."""
        before_creation = datetime.now(timezone.utc)
        item = MemoryItem(key="test", value="test")
        after_creation = datetime.now(timezone.utc)
        
        assert before_creation <= item.timestamp <= after_creation
        assert item.timestamp.tzinfo == timezone.utc


class TestAgentMemory:
    """Test the AgentMemory class."""
    
    def test_agent_memory_initialization(self):
        """Test AgentMemory initializes with empty storage."""
        with patch('browser_use_ext.agent.memory.service.logger') as mock_logger:
            memory = AgentMemory()
            
            assert memory._storage == {}
            assert memory.list_keys() == []
            assert memory.get_all_items() == []
            mock_logger.info.assert_called_once_with("AgentMemory initialized.")
    
    def test_store_basic_item(self):
        """Test storing a basic memory item."""
        memory = AgentMemory()
        
        with patch('browser_use_ext.agent.memory.service.logger') as mock_logger:
            memory.store("test_key", "test_value")
            
            assert "test_key" in memory._storage
            stored_item = memory._storage["test_key"]
            assert isinstance(stored_item, MemoryItem)
            assert stored_item.key == "test_key"
            assert stored_item.value == "test_value"
            assert stored_item.metadata == {}
            mock_logger.debug.assert_called_once_with("Stored/Updated memory item with key: 'test_key'")
    
    def test_store_item_with_metadata(self):
        """Test storing a memory item with metadata."""
        memory = AgentMemory()
        metadata = {"source": "user_input", "priority": "high"}
        
        memory.store("test_key", "test_value", metadata=metadata)
        
        stored_item = memory._storage["test_key"]
        assert stored_item.metadata == metadata
    
    def test_store_overwrites_existing_item(self):
        """Test that storing with same key overwrites existing item."""
        memory = AgentMemory()
        
        # Store initial item
        memory.store("same_key", "original_value")
        original_timestamp = memory._storage["same_key"].timestamp
        
        # Wait a bit to ensure different timestamp (in real usage)
        import time
        time.sleep(0.001)
        
        # Store new item with same key
        memory.store("same_key", "updated_value", metadata={"updated": True})
        
        stored_item = memory._storage["same_key"]
        assert stored_item.value == "updated_value"
        assert stored_item.metadata == {"updated": True}
        assert stored_item.timestamp >= original_timestamp
    
    def test_store_empty_key_warning(self):
        """Test that storing with empty key logs warning and doesn't store."""
        memory = AgentMemory()
        
        with patch('browser_use_ext.agent.memory.service.logger') as mock_logger:
            memory.store("", "test_value")
            memory.store(None, "test_value")  # Should also be rejected
            
            assert len(memory._storage) == 0
            assert memory.list_keys() == []
            # Should have 2 warning calls for empty string and None
            assert mock_logger.warning.call_count == 2
            mock_logger.warning.assert_called_with("Attempted to store memory item with empty key. Skipping.")
    
    def test_retrieve_existing_item(self):
        """Test retrieving an existing memory item."""
        memory = AgentMemory()
        memory.store("test_key", "test_value", metadata={"source": "test"})
        
        with patch('browser_use_ext.agent.memory.service.logger') as mock_logger:
            retrieved_item = memory.retrieve("test_key")
            
            assert retrieved_item is not None
            assert isinstance(retrieved_item, MemoryItem)
            assert retrieved_item.key == "test_key"
            assert retrieved_item.value == "test_value"
            assert retrieved_item.metadata == {"source": "test"}
            mock_logger.debug.assert_called_once_with("Retrieved memory item with key: 'test_key'")
    
    def test_retrieve_nonexistent_item(self):
        """Test retrieving a non-existent memory item returns None."""
        memory = AgentMemory()
        
        with patch('browser_use_ext.agent.memory.service.logger') as mock_logger:
            retrieved_item = memory.retrieve("nonexistent_key")
            
            assert retrieved_item is None
            mock_logger.debug.assert_called_once_with("Memory item with key: 'nonexistent_key' not found.")
    
    def test_retrieve_value_existing_item(self):
        """Test retrieving only the value of an existing memory item."""
        memory = AgentMemory()
        test_value = {"complex": "data", "numbers": [1, 2, 3]}
        memory.store("test_key", test_value)
        
        retrieved_value = memory.retrieve_value("test_key")
        
        assert retrieved_value == test_value
        assert retrieved_value is not None
    
    def test_retrieve_value_nonexistent_item(self):
        """Test retrieving value of non-existent item returns None."""
        memory = AgentMemory()
        
        retrieved_value = memory.retrieve_value("nonexistent_key")
        
        assert retrieved_value is None
    
    def test_delete_existing_item(self):
        """Test deleting an existing memory item."""
        memory = AgentMemory()
        memory.store("test_key", "test_value")
        
        with patch('browser_use_ext.agent.memory.service.logger') as mock_logger:
            result = memory.delete("test_key")
            
            assert result is True
            assert "test_key" not in memory._storage
            assert memory.list_keys() == []
            mock_logger.debug.assert_called_once_with("Deleted memory item with key: 'test_key'")
    
    def test_delete_nonexistent_item(self):
        """Test deleting a non-existent memory item."""
        memory = AgentMemory()
        
        with patch('browser_use_ext.agent.memory.service.logger') as mock_logger:
            result = memory.delete("nonexistent_key")
            
            assert result is False
            mock_logger.debug.assert_called_once_with("Attempted to delete non-existent memory item with key: 'nonexistent_key'")
    
    def test_list_keys_empty_memory(self):
        """Test listing keys from empty memory."""
        memory = AgentMemory()
        
        keys = memory.list_keys()
        
        assert keys == []
        assert isinstance(keys, list)
    
    def test_list_keys_with_items(self):
        """Test listing keys with multiple items in memory."""
        memory = AgentMemory()
        memory.store("key1", "value1")
        memory.store("key2", "value2")
        memory.store("key3", "value3")
        
        keys = memory.list_keys()
        
        assert len(keys) == 3
        assert set(keys) == {"key1", "key2", "key3"}
        assert isinstance(keys, list)
    
    def test_get_all_items_empty_memory(self):
        """Test getting all items from empty memory."""
        memory = AgentMemory()
        
        items = memory.get_all_items()
        
        assert items == []
        assert isinstance(items, list)
    
    def test_get_all_items_with_items(self):
        """Test getting all items with multiple items in memory."""
        memory = AgentMemory()
        memory.store("key1", "value1", metadata={"type": "test1"})
        memory.store("key2", "value2", metadata={"type": "test2"})
        
        items = memory.get_all_items()
        
        assert len(items) == 2
        assert all(isinstance(item, MemoryItem) for item in items)
        
        # Check that both items are present (order not guaranteed)
        keys = [item.key for item in items]
        values = [item.value for item in items]
        assert set(keys) == {"key1", "key2"}
        assert set(values) == {"value1", "value2"}
    
    def test_clear_memory_empty(self):
        """Test clearing empty memory."""
        memory = AgentMemory()
        
        with patch('browser_use_ext.agent.memory.service.logger') as mock_logger:
            memory.clear_memory()
            
            assert memory._storage == {}
            assert memory.list_keys() == []
            mock_logger.info.assert_called_once_with("Agent memory cleared.")
    
    def test_clear_memory_with_items(self):
        """Test clearing memory that contains items."""
        memory = AgentMemory()
        memory.store("key1", "value1")
        memory.store("key2", "value2")
        memory.store("key3", "value3")
        
        # Verify items exist before clearing
        assert len(memory.list_keys()) == 3
        
        with patch('browser_use_ext.agent.memory.service.logger') as mock_logger:
            memory.clear_memory()
            
            assert memory._storage == {}
            assert memory.list_keys() == []
            assert memory.get_all_items() == []
            mock_logger.info.assert_called_once_with("Agent memory cleared.")
    
    def test_memory_workflow_integration(self):
        """Test a complete workflow using the memory system."""
        memory = AgentMemory()
        
        # Store various types of data
        memory.store("user_preference", "dark_mode", metadata={"source": "settings"})
        memory.store("navigation_history", ["home", "about", "contact"])
        memory.store("session_data", {
            "start_time": "2024-01-01T10:00:00Z",
            "user_id": 12345,
            "features_enabled": ["chat", "export"]
        })
        
        # Verify storage
        assert len(memory.list_keys()) == 3
        assert "user_preference" in memory.list_keys()
        
        # Retrieve and verify data
        preference = memory.retrieve_value("user_preference")
        assert preference == "dark_mode"
        
        history = memory.retrieve("navigation_history")
        assert history.value == ["home", "about", "contact"]
        
        session = memory.retrieve_value("session_data")
        assert session["user_id"] == 12345
        assert "chat" in session["features_enabled"]
        
        # Update existing data
        memory.store("user_preference", "light_mode", metadata={"source": "updated_settings"})
        updated_preference = memory.retrieve("user_preference")
        assert updated_preference.value == "light_mode"
        assert updated_preference.metadata["source"] == "updated_settings"
        
        # Delete specific item
        deleted = memory.delete("navigation_history")
        assert deleted is True
        assert len(memory.list_keys()) == 2
        
        # Clear all data
        memory.clear_memory()
        assert len(memory.list_keys()) == 0
    
    def test_memory_item_timestamp_immutability(self):
        """Test that timestamps are preserved correctly during storage operations."""
        memory = AgentMemory()
        
        # Store item and capture timestamp
        memory.store("test_key", "original_value")
        original_item = memory.retrieve("test_key")
        original_timestamp = original_item.timestamp
        
        # Retrieve same item again
        retrieved_again = memory.retrieve("test_key")
        assert retrieved_again.timestamp == original_timestamp
        
        # Update the item (should get new timestamp)
        import time
        time.sleep(0.001)  # Ensure different timestamp
        memory.store("test_key", "updated_value")
        updated_item = memory.retrieve("test_key")
        
        assert updated_item.timestamp >= original_timestamp
        assert updated_item.value == "updated_value"


class TestAgentMemoryEdgeCases:
    """Test edge cases and error scenarios for AgentMemory."""
    
    def test_store_none_value(self):
        """Test storing None as a value."""
        memory = AgentMemory()
        
        memory.store("none_key", None)
        
        retrieved_value = memory.retrieve_value("none_key")
        assert retrieved_value is None
        
        retrieved_item = memory.retrieve("none_key")
        assert retrieved_item is not None
        assert retrieved_item.value is None
    
    def test_store_large_data(self):
        """Test storing large data structures."""
        memory = AgentMemory()
        
        # Create a large data structure
        large_data = {
            "large_list": list(range(1000)),
            "nested": {f"key_{i}": f"value_{i}" for i in range(100)},
            "text": "A" * 10000  # 10KB string
        }
        
        memory.store("large_data", large_data)
        
        retrieved = memory.retrieve_value("large_data")
        assert retrieved == large_data
        assert len(retrieved["large_list"]) == 1000
        assert len(retrieved["text"]) == 10000
    
    def test_special_characters_in_keys(self):
        """Test using special characters in memory keys."""
        memory = AgentMemory()
        
        special_keys = [
            "key-with-dashes",
            "key_with_underscores", 
            "key.with.dots",
            "key/with/slashes",
            "key with spaces",
            "key@with#special$chars%",
            "🔑emoji_key",
            "key123numbers"
        ]
        
        for key in special_keys:
            memory.store(key, f"value_for_{key}")
        
        # Verify all keys stored successfully
        stored_keys = memory.list_keys()
        for key in special_keys:
            assert key in stored_keys
            assert memory.retrieve_value(key) == f"value_for_{key}"
    
    def test_unicode_values(self):
        """Test storing Unicode and international text."""
        memory = AgentMemory()
        
        unicode_data = {
            "english": "Hello World",
            "spanish": "¡Hola Mundo!",
            "chinese": "你好世界",
            "arabic": "مرحبا بالعالم",
            "emoji": "🌍🚀✨",
            "mixed": "Hello 世界 🌟 مرحبا"
        }
        
        for key, value in unicode_data.items():
            memory.store(f"unicode_{key}", value)
        
        # Verify all Unicode data stored and retrieved correctly
        for key, expected_value in unicode_data.items():
            retrieved_value = memory.retrieve_value(f"unicode_{key}")
            assert retrieved_value == expected_value
    
    def test_concurrent_operation_simulation(self):
        """Test rapid consecutive operations to simulate concurrent usage."""
        memory = AgentMemory()
        
        # Rapidly store, retrieve, update, and delete items
        for i in range(100):
            key = f"item_{i}"
            memory.store(key, f"value_{i}")
            
            # Immediate retrieval
            retrieved = memory.retrieve_value(key)
            assert retrieved == f"value_{i}"
            
            # Update
            memory.store(key, f"updated_value_{i}")
            
            # Verify update
            updated = memory.retrieve_value(key)
            assert updated == f"updated_value_{i}"
            
            # Delete every other item
            if i % 2 == 0:
                deleted = memory.delete(key)
                assert deleted is True
        
        # Verify final state
        remaining_keys = memory.list_keys()
        assert len(remaining_keys) == 50  # Half were deleted
        
        # Verify remaining items are the odd-numbered ones
        for key in remaining_keys:
            assert "value_" in memory.retrieve_value(key)


if __name__ == "__main__":
    pytest.main([__file__])