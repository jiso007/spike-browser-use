import pytest
from pydantic import ValidationError

from browser_use_ext.agent.agent_core import Agent, ActionCommand, InvalidActionError

# Mock ExtensionInterface for Agent initialization if needed for other tests in the future
class MockExtensionInterface:
    async def get_state(self, tab_id=None):
        # Minimal mock, not used by _parse_response directly but good for Agent instantiation
        return None 

@pytest.fixture
def agent_instance():
    """Provides an Agent instance for testing."""
    # The Agent's __init__ expects an extension_interface.
    # For testing _parse_response, the actual interface functionality isn't critical.
    return Agent(extension_interface=MockExtensionInterface())

def test_parse_response_success(agent_instance: Agent):
    """Tests successful parsing of a valid LLM JSON response."""
    test_response_json = '{"action": "click", "params": {"element_id": "btn-123"}, "thought": "User wants to click this button."}'
    expected_action_command = ActionCommand(
        action="click", 
        params={"element_id": "btn-123"},
        thought="User wants to click this button."
    )
    
    result = agent_instance._parse_response(test_response_json)
    assert result == expected_action_command
    assert result.action == "click"
    assert result.params == {"element_id": "btn-123"}
    assert result.thought == "User wants to click this button."

def test_parse_response_validation_error_invalid_action_field(agent_instance: Agent):
    """Tests that _parse_response raises InvalidActionError for an invalid action type (not matching pattern)."""
    # 'perform_magic' is not in the ActionCommand.action pattern ^(click|type|input_text|scroll|navigate|get_state|done)$
    invalid_action_response_json = '{"action": "perform_magic", "params": {"element_id": "crystal-ball"}}'
    
    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_response(invalid_action_response_json)
    
    assert "Malformed LLM response or failed validation" in str(exc_info.value)
    # Check that the original Pydantic ValidationError is chained
    assert isinstance(exc_info.value.__cause__, ValidationError)

def test_parse_response_validation_error_missing_required_field(agent_instance: Agent):
    """Tests that _parse_response raises InvalidActionError if required 'action' field is missing."""
    missing_action_field_json = '{"params": {"element_id": "btn-123"}}'

    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_response(missing_action_field_json)
        
    assert "Malformed LLM response or failed validation" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, ValidationError)

def test_parse_response_not_json(agent_instance: Agent):
    """Tests that _parse_response raises InvalidActionError for a non-JSON string."""
    not_json_response = "This is not a JSON string."
    
    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_response(not_json_response)
    
    assert "Malformed LLM response or failed validation" in str(exc_info.value)

def test_parse_response_empty_string(agent_instance: Agent):
    """Tests that _parse_response raises InvalidActionError for an empty string response."""
    empty_response = ""
    
    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_response(empty_response)

    assert "Malformed LLM response or failed validation" in str(exc_info.value)

def test_parse_response_empty_json_object(agent_instance: Agent):
    """Tests that _parse_response raises InvalidActionError for an empty JSON object (missing 'action')."""
    empty_json_object = "{}"

    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_response(empty_json_object)

    assert "Malformed LLM response or failed validation" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, ValidationError)

# Perplexity's test_action_parsing seemed more like an integration test.
# The one above is a direct unit test for _parse_response.
# If an async test for process_task is needed later, it would look like this:
# @pytest.mark.asyncio
# async def test_process_task_mocked_flow(mock_agent_with_mocked_interface):
#     # This would require more elaborate mocking of get_state, _call_llm, etc.
#     pass 