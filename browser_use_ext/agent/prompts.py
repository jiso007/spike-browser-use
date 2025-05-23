# Standard library imports
import logging
from typing import List, Optional, Dict, Any

# Third-party imports
from pydantic import BaseModel, Field

# Initialize logger for this module
logger = logging.getLogger(__name__)

class PromptVariable(BaseModel):
    """Describes a variable that can be injected into a prompt template."""
    name: str = Field(description="Name of the variable (e.g., '{{user_query}}')")
    description: str = Field(description="Description of what the variable represents")
    example_value: Optional[Any] = Field(default=None, description="An example value for the variable")

class SystemPrompt(BaseModel):
    """
    Defines the structure and content of a system prompt for an LLM-based agent.
    A system prompt guides the behavior, persona, and constraints of the language model.
    """
    name: str = Field(description="Unique name for this system prompt configuration")
    template: str = Field(description="The actual prompt template string. Use {{variable_name}} for placeholders.")
    variables: List[PromptVariable] = Field(default_factory=list, description="List of variables expected by the template.")
    description: Optional[str] = Field(default=None, description="Description of the prompt's purpose or when to use it.")
    version: str = Field(default="1.0.0", description="Version of the prompt template.")

    def format_prompt(self, **kwargs: Any) -> str:
        """
        Formats the prompt template with the provided keyword arguments.
        Args:
            **kwargs: Keyword arguments where keys match variable names in the template.
        Returns:
            The formatted prompt string.
        Raises:
            KeyError: If a required variable is not provided in kwargs.
        """
        try:
            # Simple .format() might be okay for basic cases, but str.format_map is safer
            # For more complex templating, consider Jinja2 or similar.
            # For now, a loop for direct replacement to handle {{var}} syntax clearly.
            formatted_template = self.template
            for var in self.variables:
                placeholder = f"{{{{{var.name}}}}}" # e.g. {{user_query}}
                if var.name in kwargs:
                    formatted_template = formatted_template.replace(placeholder, str(kwargs[var.name]))
                elif var.example_value is not None: # Use example if real value not provided (for testing/defaults)
                    # logger.warning(f"Variable '{var.name}' not provided for prompt '{self.name}', using example value.")
                    # Use warnings.warn for conditions that tests or calling code might want to specifically catch.
                    import warnings # Import locally or at module level if preferred
                    warnings.warn(
                        f"Variable '{var.name}' not provided for prompt '{self.name}', using example value.",
                        UserWarning
                    )
                    formatted_template = formatted_template.replace(placeholder, str(var.example_value))
                else:
                    # This check might be too strict if some variables are truly optional in the template
                    # and the template handles their absence gracefully.
                    # Consider adding a 'required' field to PromptVariable if needed.
                    logger.error(f"Required variable '{var.name}' not provided for prompt '{self.name}'.")
                    raise KeyError(f"Variable '{var.name}' is required for prompt '{self.name}' but was not provided.")
            return formatted_template
        except KeyError as e:
            raise e # Re-raise key errors related to missing variables
        except Exception as e:
            logger.error(f"Error formatting prompt '{self.name}': {e}", exc_info=True)
            # Return the unformatted template or raise a more specific error
            raise ValueError(f"Failed to format prompt '{self.name}': {e}")

# Example of a default system prompt
DEFAULT_SYSTEM_PROMPT_TEMPLATE = (
    "You are an AI assistant designed to interact with web pages based on user instructions. "
    "Your goal is to understand the user's request and the current state of the web page, "
    "then decide on the best action to take to achieve the user's goal.\n\n"
    "Current User Query: {{user_query}}\n"
    "Current Web Page State (summary):\n{{browser_state_summary}}\n\n"
    "Available Actions: {{available_actions_summary}}\n\n"
    "Based on the above, determine the next best action and its parameters. "
    "If you believe the task is complete or cannot proceed, indicate that clearly."
)

DEFAULT_SYSTEM_PROMPT = SystemPrompt(
    name="DefaultWebAgentSystemPrompt",
    template=DEFAULT_SYSTEM_PROMPT_TEMPLATE,
    variables=[
        PromptVariable(name="user_query", description="The user's current instruction or question.", example_value="Find the latest news about AI."),
        PromptVariable(name="browser_state_summary", description="A textual summary of the current web page state, including URL, title, and key elements.", example_value="Page: Google News, Title: AI News, Key Elements: List of articles..."),
        PromptVariable(name="available_actions_summary", description="A list or description of actions the agent can perform (e.g., click, type, scroll).", example_value="click(element_id), type(element_id, text), scroll(direction)")
    ],
    description="A default system prompt for a general web interaction agent."
)

# More specific prompts can be defined here, e.g., for data extraction, form filling, etc.
# class DataExtractionPrompt(SystemPrompt):
#     task_description: str = Field(description="Specific instructions for what data to extract.")
#     output_format: str = Field(default="JSON", description="Desired format for the extracted data.")

#     def get_full_content(self) -> str:
#         return f"{self.content}\n\nTask: {self.task_description}\nOutput Format: {self.output_format}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    logger.info(f"Default Prompt Name: {DEFAULT_SYSTEM_PROMPT.name}")
    logger.info(f"Default Prompt Template:\n{DEFAULT_SYSTEM_PROMPT.template}")
    logger.info(f"Default Prompt Variables: {[v.name for v in DEFAULT_SYSTEM_PROMPT.variables]}")

    try:
        formatted = DEFAULT_SYSTEM_PROMPT.format_prompt(
            user_query="Book a flight to Paris for next week.",
            browser_state_summary="Currently on Kayak.com homepage. Search fields visible.",
            available_actions_summary="type(element_id, text), click(element_id), select_date(date)"
        )
        logger.info(f"\nFormatted Prompt:\n{formatted}")
    except Exception as e:
        logger.error(f"Error formatting default prompt in example: {e}")

    # Example of a prompt that might be used for a different purpose
    SUMMARIZE_PAGE_PROMPT_TEMPLATE = (
        "Please summarize the key information from the following web page content.\n\n"
        "Page Title: {{page_title}}\n"
        "Page URL: {{page_url}}\n\n"
        "Visible Text Content Snippet:\n{{visible_text_snippet}}\n\n"
        "Your Summary:"
    )
    SUMMARIZE_PAGE_PROMPT = SystemPrompt(
        name="SummarizeWebPagePrompt",
        template=SUMMARIZE_PAGE_PROMPT_TEMPLATE,
        variables=[
            PromptVariable(name="page_title", description="Title of the web page."),
            PromptVariable(name="page_url", description="URL of the web page."),
            PromptVariable(name="visible_text_snippet", description="A snippet of the visible text from the page.")
        ],
        description="A prompt to guide an LLM to summarize a web page."
    )

    try:
        formatted_summary_prompt = SUMMARIZE_PAGE_PROMPT.format_prompt(
            page_title="Awesome AI Innovations",
            page_url="https://example.com/ai-news/awesome-innovations",
            visible_text_snippet="Researchers today announced a breakthrough in AI that allows... (rest of content)"
        )
        logger.info(f"\nFormatted Summarize Prompt:\n{formatted_summary_prompt}")
    except Exception as e:
        logger.error(f"Error formatting summary prompt: {e}") 