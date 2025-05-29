import pytest
import json # Assuming json might be used for parsing/mocking
from unittest.mock import MagicMock, patch

# Imports from the application
from browser_use_ext.agent.service import Agent
from browser_use_ext.agent.views import (
    ActionCommand,
    InvalidActionError,
    AgentLLMOutput,
    AgentBrain,  # AgentLLMOutput contains AgentBrain
    AgentSettings
)
# For mocking Agent constructor arguments
from langchain_core.language_models.chat_models import BaseChatModel 
# Assuming ExtensionInterface is imported correctly if its definition is elsewhere
# For this test, we'll mock it simply.
# from browser_use_ext.extension_interface.service import ExtensionInterface 

from pydantic import ValidationError # Import ValidationError

class MockExtensionInterface:
    """A simplified mock for ExtensionInterface for these parsing tests."""
    async def get_state(self, tab_id=None):
        return None # Not critical for _parse_llm_response

    async def execute_action(self, action_name: str, params: dict):
        return {"success": True, "data": {}} # Dummy successful action


@pytest.fixture
def mock_llm():
    """Provides a MagicMock for BaseChatModel."""
    return MagicMock(spec=BaseChatModel)

@pytest.fixture
def mock_extension_interface():
    """Provides a mock for ExtensionInterface."""
    return MockExtensionInterface()

@pytest.fixture
def agent_settings():
    """Provides default AgentSettings."""
    return AgentSettings(max_actions_per_step=1) # Set max_actions for relevant tests

@pytest.fixture
def agent_instance(mock_llm, mock_extension_interface, agent_settings):
    """Provides an Agent instance for testing _parse_llm_response."""
    return Agent(
        task="Test task",
        llm=mock_llm,
        extension_interface=mock_extension_interface,
        settings=agent_settings
    )

# Test cases adapted from the old test_agent_core.py

def test_parse_llm_response_success_single_action(agent_instance: Agent):
    """Tests successful parsing of a valid LLM JSON response with one action."""
    test_response_json = '''{
        "current_state": {
            "evaluation_previous_goal": "Success",
            "memory": "Clicked button.",
            "next_goal": "Proceed to next step."
        },
        "action": [{
            "action": "click",
            "params": {"element_id": "btn-123"},
            "thought": "User wants to click this button."
        }]
    }'''
    expected_brain = AgentBrain(
        evaluation_previous_goal="Success",
        memory="Clicked button.",
        next_goal="Proceed to next step."
    )
    expected_action_command = ActionCommand(
        action="click",
        params={"element_id": "btn-123"},
        thought="User wants to click this button."
    )
    
    result = agent_instance._parse_llm_response(test_response_json)
    
    assert isinstance(result, AgentLLMOutput)
    assert result.current_state == expected_brain
    assert len(result.action) == 1
    assert result.action[0] == expected_action_command
    assert result.action[0].action == "click"
    assert result.action[0].params == {"element_id": "btn-123"}
    assert result.action[0].thought == "User wants to click this button."

def test_parse_llm_response_success_multiple_actions_truncated(agent_instance: Agent):
    """Tests that multiple actions are parsed but truncated by max_actions_per_step in settings."""
    # agent_instance is configured with max_actions_per_step=1
    test_response_json = '''{
        "current_state": {
            "evaluation_previous_goal": "Success",
            "memory": "Initial thoughts.",
            "next_goal": "Perform multiple actions."
        },
        "action": [
            {
                "action": "click",
                "params": {"element_id": "btn-1"},
                "thought": "First click."
            },
            {
                "action": "type",
                "params": {"element_id": "input-1", "text": "hello"},
                "thought": "Then type."
            }
        ]
    }'''
    result = agent_instance._parse_llm_response(test_response_json)
    assert isinstance(result, AgentLLMOutput)
    assert len(result.action) == 1 # Because agent_settings.max_actions_per_step = 1
    assert result.action[0].action == "click"

def test_parse_llm_response_success_no_actions(agent_instance: Agent):
    """Tests successful parsing when LLM proposes no actions."""
    test_response_json = '''{
        "current_state": {
            "evaluation_previous_goal": "Thinking",
            "memory": "Just thinking.",
            "next_goal": "Observe more."
        },
        "action": []
    }'''
    result = agent_instance._parse_llm_response(test_response_json)
    assert isinstance(result, AgentLLMOutput)
    assert len(result.action) == 0

def test_parse_llm_response_error_invalid_action_field_in_action_command(agent_instance: Agent):
    """Tests InvalidActionError for an invalid action type within an ActionCommand."""
    invalid_action_response_json = '''{
        "current_state": {"evaluation_previous_goal": "Test", "memory": "Test", "next_goal": "Test"},
        "action": [{"action": "perform_magic", "params": {"element_id": "crystal-ball"}}]
    }'''
    
    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_llm_response(invalid_action_response_json)
    
    assert "Malformed LLM response or failed validation for AgentLLMOutput" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, ValidationError)

def test_parse_llm_response_error_missing_required_action_field_in_action_command(agent_instance: Agent):
    """Tests InvalidActionError if 'action' field is missing in an ActionCommand."""
    missing_action_field_json = '''{
        "current_state": {"evaluation_previous_goal": "Test", "memory": "Test", "next_goal": "Test"},
        "action": [{"params": {"element_id": "btn-123"}}]
    }'''

    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_llm_response(missing_action_field_json)
        
    assert "Malformed LLM response or failed validation for AgentLLMOutput" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, ValidationError)

def test_parse_llm_response_error_missing_current_state_field(agent_instance: Agent):
    """Tests InvalidActionError if 'current_state' field is missing in AgentLLMOutput."""
    missing_current_state_json = '''{
        "action": [{"action": "click", "params": {"element_id": "btn-123"}}]
    }'''
    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_llm_response(missing_current_state_json)
    assert "Malformed LLM response or failed validation for AgentLLMOutput" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, ValidationError)

def test_parse_llm_response_error_not_json(agent_instance: Agent):
    """Tests InvalidActionError for a non-JSON string."""
    not_json_response = "This is not a JSON string."
    
    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_llm_response(not_json_response)
    
    assert "Could not parse LLM response" in str(exc_info.value) # Error message changed in service._parse_llm_response

def test_parse_llm_response_error_empty_string(agent_instance: Agent):
    """Tests InvalidActionError for an empty string response."""
    empty_response = ""
    
    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_llm_response(empty_response)

    # The specific error message depends on how json.loads('') behaves vs model_validate_json('')
    # Usually it's a JSONDecodeError which gets wrapped.
    assert "Could not parse LLM response" in str(exc_info.value) 

def test_parse_llm_response_error_empty_json_object(agent_instance: Agent):
    """Tests InvalidActionError for an empty JSON object (missing 'current_state' and 'action')."""
    empty_json_object = "{}"

    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_llm_response(empty_json_object)

    assert "Malformed LLM response or failed validation for AgentLLMOutput" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, ValidationError)

# Example of how to test for parameter validation within ActionCommand (if needed)
# This depends on the specific validation logic in ActionCommand's model_validator
def test_action_command_param_validation_navigate_missing_url(agent_instance: Agent):
    """Tests that ActionCommand validation catches missing URL for navigate action."""
    invalid_navigate_json = '''{
        "current_state": {"evaluation_previous_goal": "Test", "memory": "Test", "next_goal": "Test"},
        "action": [{
            "action": "navigate",
            "params": {}, "thought": "Navigate somewhere"
        }]
    }'''
    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_llm_response(invalid_navigate_json)
    
    assert isinstance(exc_info.value.__cause__, ValidationError)
    # Check for a message specific to the 'navigate' action's 'url' parameter
    # This requires knowing how your ActionCommand validator reports errors.
    # Example: Look for 'url' and 'Field required' in the error details.
    errors = exc_info.value.__cause__.errors()
    assert any(
        err['type'] == 'missing' and err['loc'][0] == 'action' and err['loc'][2] == 'params' and 'url' in str(err['msg']).lower()
        for err_list in [e.get('ctx', {}).get('error', {}).errors() for e in errors if e['loc'][0] == 'action' and e['loc'][2] == 'params'] if err_list for err in err_list
    ) or any(
         'url' in str(err['msg']).lower() and 'required' in str(err['msg']).lower() for err in errors if err['loc'][0] == 'action' and err['loc'][1] == 0 and err['loc'][2] == 'params'
    )


def test_action_command_param_validation_click_missing_element_id(agent_instance: Agent):
    """Tests that ActionCommand validation catches missing element_id for click action."""
    invalid_click_json = '''{
        "current_state": {"evaluation_previous_goal": "Test", "memory": "Test", "next_goal": "Test"},
        "action": [{
            "action": "click",
            "params": {}, "thought": "Click something"
        }]
    }'''
    with pytest.raises(InvalidActionError) as exc_info:
        agent_instance._parse_llm_response(invalid_click_json)
    
    assert isinstance(exc_info.value.__cause__, ValidationError)
    errors = exc_info.value.__cause__.errors()
    assert any(
        err['type'] == 'missing' and err['loc'][0] == 'action' and err['loc'][2] == 'params' and 'element_id' in str(err['msg']).lower()
        for err_list in [e.get('ctx', {}).get('error', {}).errors() for e in errors if e['loc'][0] == 'action' and e['loc'][2] == 'params'] if err_list for err in err_list
    ) or any(
         'element_id' in str(err['msg']).lower() and 'required' in str(err['msg']).lower() for err in errors if err['loc'][0] == 'action' and err['loc'][1] == 0 and err['loc'][2] == 'params'
    )
    

# Add more tests as needed for other ActionCommand parameter validations (input_text, scroll, etc.)
# and for other aspects of _parse_llm_response if its logic expands. 