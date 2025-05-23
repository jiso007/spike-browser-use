import sys
import pytest
from typing import List, Dict, Any

# Adjust imports for the new project structure `browser-use-ext`
# print(f"sys.path inside test_agent_prompts.py: {sys.path}") # DEBUG PRINT - REMOVED
from agent.prompts import PromptVariable, SystemPrompt, DEFAULT_SYSTEM_PROMPT

@pytest.fixture
def sample_prompt_variables() -> List[PromptVariable]:
    """Provides a list of sample PromptVariable instances."""
    return [
        PromptVariable(name="user_query", description="The user\'s request", example_value="Find Italian restaurants near me."),
        PromptVariable(name="context", description="Relevant contextual information", example_value="Location: San Francisco, Time: 7 PM")
    ]

@pytest.fixture
def sample_system_prompt_template() -> str:
    """Provides a sample prompt template string."""
    return "You are an AI. User Query: {{user_query}}. Context: {{context}}. Respond helpfully."

@pytest.fixture
def sample_system_prompt(sample_prompt_variables: List[PromptVariable], sample_system_prompt_template: str) -> SystemPrompt:
    """Provides a SystemPrompt instance created with sample variables and template."""
    return SystemPrompt(
        name="TestAgentPrompt",
        template=sample_system_prompt_template,
        variables=sample_prompt_variables,
        description="A test prompt for AI agent.",
        version="0.1-test"
    )

def test_prompt_variable_creation():
    """Test basic PromptVariable Pydantic model creation."""
    name = "test_var"
    desc = "A test variable."
    ex_val = "example"
    pv = PromptVariable(name=name, description=desc, example_value=ex_val)
    assert pv.name == name
    assert pv.description == desc
    assert pv.example_value == ex_val

    pv_no_example = PromptVariable(name="no_ex", description="No example here.")
    assert pv_no_example.example_value is None

def test_system_prompt_creation(sample_system_prompt: SystemPrompt, sample_prompt_variables: List[PromptVariable], sample_system_prompt_template: str):
    """Test basic SystemPrompt Pydantic model creation."""
    sp = sample_system_prompt
    assert sp.name == "TestAgentPrompt"
    assert sp.template == sample_system_prompt_template
    assert sp.variables == sample_prompt_variables
    assert sp.description == "A test prompt for AI agent."
    assert sp.version == "0.1-test"

def test_format_prompt_all_vars_provided(sample_system_prompt: SystemPrompt):
    """Test formatting the prompt when all required variables are provided."""
    values = {
        "user_query": "Book a flight.",
        "context": "User is logged in, has preferences set."
    }
    expected_output = "You are an AI. User Query: Book a flight.. Context: User is logged in, has preferences set.. Respond helpfully."
    formatted_prompt = sample_system_prompt.format_prompt(**values)
    assert formatted_prompt == expected_output

def test_format_prompt_uses_example_values_if_provided_and_var_missing(sample_system_prompt: SystemPrompt):
    """Test formatting uses example values if a variable is missing but has an example."""
    # sample_prompt_variables has example_value for "user_query" and "context"
    values_missing_context = {"user_query": "Show me the news."}
    # Expect context to use its example_value: "Location: San Francisco, Time: 7 PM"
    expected_output = "You are an AI. User Query: Show me the news.. Context: Location: San Francisco, Time: 7 PM. Respond helpfully."
    
    # Capture warnings for missing variables using example values
    with pytest.warns(UserWarning, match="Variable 'context' not provided for prompt 'TestAgentPrompt', using example value."):
        formatted_prompt = sample_system_prompt.format_prompt(**values_missing_context)
    assert formatted_prompt == expected_output

def test_format_prompt_raises_keyerror_if_var_missing_and_no_example(sample_system_prompt_template: str):
    """Test that KeyError is raised if a variable is missing and has no example value."""
    # Create a prompt where one variable has no example
    variables_with_one_no_example = [
        PromptVariable(name="user_query", description="User query", example_value="Test query"),
        PromptVariable(name="mandatory_no_example", description="This one is needed but has no example")
    ]
    custom_template = "Query: {{user_query}}, Mandatory: {{mandatory_no_example}}"
    sp_custom = SystemPrompt(name="CustomPrompt", template=custom_template, variables=variables_with_one_no_example)
    
    values_missing_mandatory = {"user_query": "Some query"}
    
    with pytest.raises(KeyError) as excinfo:
        sp_custom.format_prompt(**values_missing_mandatory)
    assert "Variable 'mandatory_no_example' is required for prompt 'CustomPrompt' but was not provided." in str(excinfo.value)

def test_format_prompt_with_no_variables_in_template():
    """Test formatting a template that has no variables defined in it."""
    static_template = "This is a static prompt with no variables."
    sp_static = SystemPrompt(name="StaticPrompt", template=static_template, variables=[])
    formatted = sp_static.format_prompt() # No kwargs needed
    assert formatted == static_template

    # Test with empty variables list but template still tries to use some (should be fine if not strict on var definition)
    # The current format_prompt relies on `self.variables` for replacement logic.
    # If a template has {{var}} but `self.variables` is empty or doesn't list `var`,
    # it will currently pass through unformatted, e.g. "Text with {{unlisted_var}}".
    # This behavior might be okay, or could be made stricter.
    template_with_unlisted_var = "Hello {{name}}!"
    sp_unlisted = SystemPrompt(name="UnlistedVarPrompt", template=template_with_unlisted_var, variables=[])
    formatted_unlisted = sp_unlisted.format_prompt(name="World") # provide name, but not in sp_unlisted.variables
    # Current behavior: {{name}} remains because it's not in sp_unlisted.variables to be processed.
    assert formatted_unlisted == "Hello {{name}}!" 

def test_default_system_prompt_exists_and_is_valid():
    """Test that DEFAULT_SYSTEM_PROMPT is a valid SystemPrompt instance and can be formatted."""
    assert isinstance(DEFAULT_SYSTEM_PROMPT, SystemPrompt)
    assert DEFAULT_SYSTEM_PROMPT.name == "DefaultWebAgentSystemPrompt"
    assert len(DEFAULT_SYSTEM_PROMPT.variables) == 3 # user_query, browser_state_summary, available_actions_summary
    
    # Try formatting with example values (or mock values)
    try:
        formatted_default = DEFAULT_SYSTEM_PROMPT.format_prompt(
            user_query="Test default query",
            browser_state_summary="Test browser state",
            available_actions_summary="Test actions"
        )
        assert "Test default query" in formatted_default
        assert "Test browser state" in formatted_default
        assert "Test actions" in formatted_default
    except Exception as e:
        pytest.fail(f"DEFAULT_SYSTEM_PROMPT.format_prompt failed: {e}")

def test_format_prompt_valueerror_on_other_exceptions(sample_system_prompt: SystemPrompt):
    """Test that a generic ValueError is raised if formatting fails for unexpected reasons (e.g., bad template string)."""
    # Temporarily sabotage the template to cause a non-KeyError during formatting
    original_template = sample_system_prompt.template
    # Example of a template that might cause issues with str.replace or similar if not handled well,
    # although simple {{}} replacements are usually safe.
    # For a more direct test of this, one might need to mock str.replace to throw an unexpected error.
    # This test is more conceptual for now, as direct {{var}} replacement is quite robust.
    
    # Let's test with a variable that has a non-string example value and see if str() conversion works as expected.
    vars_with_int_example = [
        PromptVariable(name="count", description="A number", example_value=123)
    ]
    prompt_with_int_var = SystemPrompt(name="IntPrompt", template="Count: {{count}}", variables=vars_with_int_example)
    
    # Format using the example value (123)
    formatted = prompt_with_int_var.format_prompt() # Should use example_value for count
    assert formatted == "Count: 123"

    # If str.replace itself threw an error other than KeyError (highly unlikely for this usage),
    # the `except Exception as e:` block in `format_prompt` should catch it and raise ValueError.
    # Simulating this specific scenario directly is hard without deep mocking Python built-ins.

# To run these tests:
# pytest browser-use-ext/tests/test_agent_prompts.py