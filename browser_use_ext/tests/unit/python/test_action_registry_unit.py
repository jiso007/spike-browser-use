"""
Unit tests for Action Registry models.

Tests the action definition and parameter models from browser_use_ext.controller.registry.views.
"""

import pytest
from typing import Any, Dict, List
from pydantic import ValidationError

from browser_use_ext.controller.registry.views import (
    ActionParam,
    ActionDefinition,
    ClickElementAction,
    InputTextAction,
    GoToURLAction,
    GoToURLParams,
    ClickElementByIndexParams,
    InputTextParams,
    ScrollPageParams,
    ACTION_GO_TO_URL,
    ACTION_CLICK_ELEMENT_BY_INDEX,
    ACTION_INPUT_TEXT,
    ACTION_SCROLL_PAGE
)


class TestActionParam:
    """Test the ActionParam model."""
    
    def test_action_param_minimal_creation(self):
        """Test creating an ActionParam with minimal required fields."""
        param = ActionParam(name="test_param", type="str")
        
        assert param.name == "test_param"
        assert param.type == "str"
        assert param.required is True  # Default value
        assert param.description is None  # Default value
        assert param.default is None  # Default value
    
    def test_action_param_full_creation(self):
        """Test creating an ActionParam with all fields specified."""
        param = ActionParam(
            name="url",
            type="str",
            required=True,
            description="The URL to navigate to",
            default="https://example.com"
        )
        
        assert param.name == "url"
        assert param.type == "str"
        assert param.required is True
        assert param.description == "The URL to navigate to"
        assert param.default == "https://example.com"
    
    def test_action_param_optional_parameter(self):
        """Test creating an optional ActionParam."""
        param = ActionParam(
            name="timeout",
            type="int",
            required=False,
            description="Request timeout in seconds",
            default=30
        )
        
        assert param.name == "timeout"
        assert param.type == "int"
        assert param.required is False
        assert param.description == "Request timeout in seconds"
        assert param.default == 30
    
    def test_action_param_complex_types(self):
        """Test ActionParam with complex type definitions."""
        complex_types = [
            "List[str]",
            "Dict[str, Any]",
            "Optional[int]",
            "Union[str, int]",
            "Literal['up', 'down']",
            "DOMElementNode_highlight_index"
        ]
        
        for type_def in complex_types:
            param = ActionParam(name="complex_param", type=type_def)
            assert param.type == type_def
    
    def test_action_param_serialization(self):
        """Test ActionParam serialization to dict."""
        param = ActionParam(
            name="element_id",
            type="int",
            required=True,
            description="ID of the element to interact with"
        )
        
        data = param.model_dump()
        
        assert data["name"] == "element_id"
        assert data["type"] == "int"
        assert data["required"] is True
        assert data["description"] == "ID of the element to interact with"
        assert data["default"] is None
    
    def test_action_param_deserialization(self):
        """Test creating ActionParam from dict data."""
        data = {
            "name": "scroll_amount",
            "type": "int",
            "required": False,
            "description": "Number of pixels to scroll",
            "default": 100
        }
        
        param = ActionParam.model_validate(data)
        
        assert param.name == "scroll_amount"
        assert param.type == "int"
        assert param.required is False
        assert param.description == "Number of pixels to scroll"
        assert param.default == 100


class TestActionDefinition:
    """Test the ActionDefinition model."""
    
    def test_action_definition_minimal_creation(self):
        """Test creating an ActionDefinition with minimal fields."""
        action = ActionDefinition(
            name="simple_action",
            description="A simple test action"
        )
        
        assert action.name == "simple_action"
        assert action.description == "A simple test action"
        assert action.parameters == []  # Default empty list
        assert action.category == "General"  # Default value
    
    def test_action_definition_full_creation(self):
        """Test creating an ActionDefinition with all fields."""
        parameters = [
            ActionParam(name="url", type="str", required=True),
            ActionParam(name="timeout", type="int", required=False, default=30)
        ]
        
        action = ActionDefinition(
            name="navigate_to_url",
            description="Navigate to a specific URL with optional timeout",
            parameters=parameters,
            category="Navigation"
        )
        
        assert action.name == "navigate_to_url"
        assert action.description == "Navigate to a specific URL with optional timeout"
        assert len(action.parameters) == 2
        assert action.parameters[0].name == "url"
        assert action.parameters[1].name == "timeout"
        assert action.category == "Navigation"
    
    def test_action_definition_with_complex_parameters(self):
        """Test ActionDefinition with various parameter types."""
        parameters = [
            ActionParam(name="element_id", type="int", required=True, description="Element ID"),
            ActionParam(name="text", type="str", required=True, description="Text to input"),
            ActionParam(name="delay", type="float", required=False, default=0.1),
            ActionParam(name="options", type="Dict[str, Any]", required=False),
            ActionParam(name="coordinates", type="List[int]", required=False),
            ActionParam(name="direction", type="Literal['up', 'down']", required=True)
        ]
        
        action = ActionDefinition(
            name="complex_interaction",
            description="A complex interaction action",
            parameters=parameters,
            category="Interaction"
        )
        
        assert action.name == "complex_interaction"
        assert len(action.parameters) == 6
        assert action.parameters[0].type == "int"
        assert action.parameters[2].default == 0.1
        assert action.parameters[5].type == "Literal['up', 'down']"
        assert action.category == "Interaction"
    
    def test_action_definition_serialization(self):
        """Test ActionDefinition serialization."""
        parameters = [
            ActionParam(name="index", type="int", required=True)
        ]
        
        action = ActionDefinition(
            name="click_element",
            description="Click an element",
            parameters=parameters,
            category="Interaction"
        )
        
        data = action.model_dump()
        
        assert data["name"] == "click_element"
        assert data["description"] == "Click an element"
        assert len(data["parameters"]) == 1
        assert data["parameters"][0]["name"] == "index"
        assert data["category"] == "Interaction"
    
    def test_action_definition_deserialization(self):
        """Test creating ActionDefinition from dict data."""
        data = {
            "name": "scroll_page",
            "description": "Scroll the page in a direction",
            "parameters": [
                {
                    "name": "direction",
                    "type": "str",
                    "required": True,
                    "description": "Direction to scroll"
                }
            ],
            "category": "Navigation"
        }
        
        action = ActionDefinition.model_validate(data)
        
        assert action.name == "scroll_page"
        assert action.description == "Scroll the page in a direction"
        assert len(action.parameters) == 1
        assert action.parameters[0].name == "direction"
        assert action.category == "Navigation"


class TestActionModels:
    """Test the specific action parameter models."""
    
    def test_click_element_action(self):
        """Test ClickElementAction model."""
        action = ClickElementAction(index=42)
        
        assert action.index == 42
        
        # Test serialization
        data = action.model_dump()
        assert data["index"] == 42
        
        # Test validation error for missing index
        with pytest.raises(ValidationError):
            ClickElementAction()
    
    def test_input_text_action(self):
        """Test InputTextAction model."""
        action = InputTextAction(index=15, text="Hello World")
        
        assert action.index == 15
        assert action.text == "Hello World"
        
        # Test serialization
        data = action.model_dump()
        assert data["index"] == 15
        assert data["text"] == "Hello World"
        
        # Test validation errors
        with pytest.raises(ValidationError):
            InputTextAction(index=15)  # Missing text
        
        with pytest.raises(ValidationError):
            InputTextAction(text="Hello")  # Missing index
    
    def test_go_to_url_action(self):
        """Test GoToURLAction model."""
        action = GoToURLAction(url="https://example.com")
        
        assert action.url == "https://example.com"
        
        # Test serialization
        data = action.model_dump()
        assert data["url"] == "https://example.com"
        
        # Test validation error
        with pytest.raises(ValidationError):
            GoToURLAction()  # Missing url
    
    def test_go_to_url_params(self):
        """Test GoToURLParams model."""
        params = GoToURLParams(url="https://test.com")
        
        assert params.url == "https://test.com"
        
        # Test with complex URL
        complex_url = "https://example.com/path?param=value&other=123#section"
        params = GoToURLParams(url=complex_url)
        assert params.url == complex_url
    
    def test_click_element_by_index_params(self):
        """Test ClickElementByIndexParams model."""
        params = ClickElementByIndexParams(index=999)
        
        assert params.index == 999
        
        # Test edge cases
        params_zero = ClickElementByIndexParams(index=0)
        assert params_zero.index == 0
        
        params_negative = ClickElementByIndexParams(index=-1)
        assert params_negative.index == -1
    
    def test_input_text_params(self):
        """Test InputTextParams model."""
        params = InputTextParams(index=5, text="Test input text")
        
        assert params.index == 5
        assert params.text == "Test input text"
        
        # Test with special characters
        special_text = "Special chars: !@#$%^&*()_+{}|:<>?[]\\;'\",./"
        params = InputTextParams(index=1, text=special_text)
        assert params.text == special_text
        
        # Test with Unicode
        unicode_text = "Unicode: 你好世界 🌟 Café"
        params = InputTextParams(index=2, text=unicode_text)
        assert params.text == unicode_text
    
    def test_scroll_page_params(self):
        """Test ScrollPageParams model."""
        # Test valid directions
        params_up = ScrollPageParams(direction="up")
        assert params_up.direction == "up"
        
        params_down = ScrollPageParams(direction="down")
        assert params_down.direction == "down"
        
        # Test serialization
        data = params_down.model_dump()
        assert data["direction"] == "down"


class TestPredefinedActions:
    """Test the predefined action definitions."""
    
    def test_action_go_to_url(self):
        """Test the predefined ACTION_GO_TO_URL."""
        action = ACTION_GO_TO_URL
        
        assert action.name == "go_to_url"
        assert "navigates" in action.description.lower()
        assert len(action.parameters) == 1
        assert action.parameters[0].name == "url"
        assert action.parameters[0].type == "str"
        assert action.parameters[0].required is True
        assert action.category == "Navigation"
    
    def test_action_click_element_by_index(self):
        """Test the predefined ACTION_CLICK_ELEMENT_BY_INDEX."""
        action = ACTION_CLICK_ELEMENT_BY_INDEX
        
        assert action.name == "click_element_by_index"
        assert "clicks" in action.description.lower()
        assert "highlight_index" in action.description.lower()
        assert len(action.parameters) == 1
        assert action.parameters[0].name == "index"
        assert action.parameters[0].type == "int"
        assert action.parameters[0].required is True
        assert action.category == "Interaction"
    
    def test_action_input_text(self):
        """Test the predefined ACTION_INPUT_TEXT."""
        action = ACTION_INPUT_TEXT
        
        assert action.name == "input_text"
        assert "inputs text" in action.description.lower()
        assert len(action.parameters) == 2
        
        # Check index parameter
        index_param = next(p for p in action.parameters if p.name == "index")
        assert index_param.type == "int"
        assert index_param.required is True
        
        # Check text parameter
        text_param = next(p for p in action.parameters if p.name == "text")
        assert text_param.type == "str"
        assert text_param.required is True
        
        assert action.category == "Interaction"
    
    def test_action_scroll_page(self):
        """Test the predefined ACTION_SCROLL_PAGE."""
        action = ACTION_SCROLL_PAGE
        
        assert action.name == "scroll_page"
        assert "scrolls" in action.description.lower()
        assert len(action.parameters) == 1
        assert action.parameters[0].name == "direction"
        assert action.parameters[0].type == "Literal['up', 'down']"
        assert action.parameters[0].required is True
        assert action.category == "Navigation"


class TestActionRegistryIntegration:
    """Test integration scenarios for action registry."""
    
    def test_action_registry_collection(self):
        """Test collecting all predefined actions."""
        predefined_actions = [
            ACTION_GO_TO_URL,
            ACTION_CLICK_ELEMENT_BY_INDEX,
            ACTION_INPUT_TEXT,
            ACTION_SCROLL_PAGE
        ]
        
        # Verify all actions are valid
        for action in predefined_actions:
            assert isinstance(action, ActionDefinition)
            assert len(action.name) > 0
            assert len(action.description) > 0
            assert isinstance(action.parameters, list)
            assert len(action.category) > 0
        
        # Verify unique names
        action_names = [action.name for action in predefined_actions]
        assert len(action_names) == len(set(action_names))
    
    def test_action_parameter_validation_integration(self):
        """Test parameter validation with action definitions."""
        # Test valid parameters for each action
        test_cases = [
            (ACTION_GO_TO_URL, {"url": "https://example.com"}),
            (ACTION_CLICK_ELEMENT_BY_INDEX, {"index": 42}),
            (ACTION_INPUT_TEXT, {"index": 1, "text": "Hello"}),
            (ACTION_SCROLL_PAGE, {"direction": "down"})
        ]
        
        for action, params in test_cases:
            # Verify all required parameters are provided
            required_params = [p.name for p in action.parameters if p.required]
            provided_params = set(params.keys())
            required_set = set(required_params)
            
            assert required_set.issubset(provided_params), f"Missing required params for {action.name}"
    
    def test_action_categories(self):
        """Test action categorization."""
        navigation_actions = [ACTION_GO_TO_URL, ACTION_SCROLL_PAGE]
        interaction_actions = [ACTION_CLICK_ELEMENT_BY_INDEX, ACTION_INPUT_TEXT]
        
        for action in navigation_actions:
            assert action.category == "Navigation"
        
        for action in interaction_actions:
            assert action.category == "Interaction"
    
    def test_parameter_type_consistency(self):
        """Test consistency of parameter types across actions."""
        # Collect all parameters
        all_params = []
        for action in [ACTION_GO_TO_URL, ACTION_CLICK_ELEMENT_BY_INDEX, ACTION_INPUT_TEXT, ACTION_SCROLL_PAGE]:
            all_params.extend(action.parameters)
        
        # Group by name and verify type consistency
        param_types = {}
        for param in all_params:
            if param.name in param_types:
                # Same parameter name should have same type
                assert param_types[param.name] == param.type, f"Inconsistent type for parameter '{param.name}'"
            else:
                param_types[param.name] = param.type
        
        # Verify expected common parameters
        if "index" in param_types:
            assert param_types["index"] == "int"
        if "text" in param_types:
            assert param_types["text"] == "str"
        if "url" in param_types:
            assert param_types["url"] == "str"
    
    def test_action_definition_roundtrip(self):
        """Test serialization and deserialization of action definitions."""
        original_action = ActionDefinition(
            name="test_action",
            description="A test action for roundtrip testing",
            parameters=[
                ActionParam(name="param1", type="str", required=True, description="First param"),
                ActionParam(name="param2", type="int", required=False, default=10)
            ],
            category="Testing"
        )
        
        # Serialize to dict
        data = original_action.model_dump()
        
        # Deserialize back to object
        reconstructed_action = ActionDefinition.model_validate(data)
        
        # Verify equivalence
        assert reconstructed_action.name == original_action.name
        assert reconstructed_action.description == original_action.description
        assert reconstructed_action.category == original_action.category
        assert len(reconstructed_action.parameters) == len(original_action.parameters)
        
        for orig_param, recon_param in zip(original_action.parameters, reconstructed_action.parameters):
            assert recon_param.name == orig_param.name
            assert recon_param.type == orig_param.type
            assert recon_param.required == orig_param.required
            assert recon_param.description == orig_param.description
            assert recon_param.default == orig_param.default


class TestActionRegistryEdgeCases:
    """Test edge cases and error scenarios."""
    
    def test_empty_action_name(self):
        """Test validation with empty action name."""
        # Empty string should still be valid for Pydantic str field
        action = ActionDefinition(name="", description="Test")
        assert action.name == ""
    
    def test_special_characters_in_names(self):
        """Test special characters in action and parameter names."""
        special_names = [
            "action-with-dashes",
            "action_with_underscores",
            "action.with.dots",
            "action123",
            "action@special#chars"
        ]
        
        for name in special_names:
            action = ActionDefinition(name=name, description="Test action")
            assert action.name == name
            
            param = ActionParam(name=name, type="str")
            assert param.name == name
    
    def test_long_descriptions(self):
        """Test handling of very long descriptions."""
        long_description = "A " * 1000  # 2000 character description
        
        action = ActionDefinition(
            name="long_desc_action",
            description=long_description
        )
        assert len(action.description) == 2000
        
        param = ActionParam(
            name="long_desc_param",
            type="str",
            description=long_description
        )
        assert len(param.description) == 2000
    
    def test_complex_default_values(self):
        """Test complex default values in parameters."""
        complex_defaults = [
            None,
            [],
            {},
            {"key": "value", "nested": {"data": [1, 2, 3]}},
            [1, 2, 3, "mixed", {"type": "data"}],
            42,
            3.14159,
            True,
            False,
            "string default"
        ]
        
        for default_value in complex_defaults:
            param = ActionParam(
                name="complex_param",
                type="Any",
                required=False,
                default=default_value
            )
            assert param.default == default_value
    
    def test_many_parameters(self):
        """Test action with many parameters."""
        many_params = [
            ActionParam(name=f"param_{i}", type="str", required=i % 2 == 0)
            for i in range(50)
        ]
        
        action = ActionDefinition(
            name="many_params_action",
            description="Action with many parameters",
            parameters=many_params
        )
        
        assert len(action.parameters) == 50
        assert action.parameters[0].name == "param_0"
        assert action.parameters[49].name == "param_49"
        
        # Check required/optional alternating pattern
        for i, param in enumerate(action.parameters):
            assert param.required == (i % 2 == 0)


if __name__ == "__main__":
    pytest.main([__file__])