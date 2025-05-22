# Pydantic models for action registry, if needed in the future.
# For now, this can remain empty or define base Action classes.
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Literal
import logging

class ActionParam(BaseModel):
    """Describes a parameter for an action."""
    name: str = Field(description="Parameter name")
    type: str = Field(description="Parameter type (e.g., 'str', 'int', 'bool', 'DOMElementNode_highlight_index')")
    required: bool = Field(default=True, description="Is the parameter required?")
    description: Optional[str] = Field(default=None, description="Description of the parameter")
    default: Optional[Any] = Field(default=None, description="Default value if not required or if optional")

class ActionDefinition(BaseModel):
    """Defines a browser action that can be executed."""
    name: str = Field(description="Unique name of the action (e.g., 'click_element_by_index', 'go_to_url')")
    description: str = Field(description="Description of what the action does")
    parameters: List[ActionParam] = Field(default_factory=list, description="List of parameters the action accepts")
    category: Optional[str] = Field(default="General", description="Category of the action (e.g., 'Navigation', 'Interaction', 'Data Extraction')")

    class Config:
        from_attributes = True # Changed from orm_mode for Pydantic v2 compatibility

# Example of a concrete action model - not strictly needed if actions are dynamic strings passed to extension
# but useful if we want to type-check parameters Python-side before sending.
class ClickElementAction(BaseModel):
    index: int = Field(description="The highlight_index of the element to click.")

class InputTextAction(BaseModel):
    index: int = Field(description="The highlight_index of the element to type into.")
    text: str = Field(description="The text to input into the element.")

class GoToURLAction(BaseModel):
    url: str = Field(description="The URL to navigate to.")

# Add more action-specific Pydantic models here if desired for stricter typing 

# --- Example Action Definitions (can be registered or discovered) ---

class GoToURLParams(BaseModel):
    """Parameters for the go_to_url action."""
    url: str = Field(description="The URL to navigate to.")

ACTION_GO_TO_URL = ActionDefinition(
    name="go_to_url",
    description="Navigates the current tab to the specified URL.",
    parameters=[
        ActionParam(name="url", type="str", required=True, description="The URL to navigate to.")
    ],
    category="Navigation"
)

class ClickElementByIndexParams(BaseModel):
    """Parameters for the click_element_by_index action."""
    index: int = Field(description="The highlight_index of the element to click.")

ACTION_CLICK_ELEMENT_BY_INDEX = ActionDefinition(
    name="click_element_by_index",
    description="Clicks an element identified by its highlight_index.",
    parameters=[
        ActionParam(name="index", type="int", required=True, description="The highlight_index of the element.")
    ],
    category="Interaction"
)

class InputTextParams(BaseModel):
    """Parameters for the input_text action."""
    index: int = Field(description="The highlight_index of the input element.")
    text: str = Field(description="The text to input into the element.")

ACTION_INPUT_TEXT = ActionDefinition(
    name="input_text",
    description="Inputs text into an element (e.g., input field, textarea) identified by its highlight_index.",
    parameters=[
        ActionParam(name="index", type="int", required=True, description="The highlight_index of the element."),
        ActionParam(name="text", type="str", required=True, description="The text to input.")
    ],
    category="Interaction"
)

class ScrollPageParams(BaseModel):
    """Parameters for the scroll_page action."""
    direction: Literal["up", "down"] = Field(description="Direction to scroll: 'up' or 'down'.")
    # amount: Optional[int] = Field(default=None, description="Amount in pixels to scroll. Defaults to viewport height if not set.")

ACTION_SCROLL_PAGE = ActionDefinition(
    name="scroll_page",
    description="Scrolls the page up or down. Currently scrolls by a fixed amount (approx. viewport height).",
    parameters=[
        ActionParam(name="direction", type="Literal['up', 'down']", required=True, description="Scroll direction.")
    ],
    category="Navigation"
)


# Registry of available actions (can be populated dynamically or loaded from config)
AVAILABLE_ACTIONS: Dict[str, ActionDefinition] = {
    ACTION_GO_TO_URL.name: ACTION_GO_TO_URL,
    ACTION_CLICK_ELEMENT_BY_INDEX.name: ACTION_CLICK_ELEMENT_BY_INDEX,
    ACTION_INPUT_TEXT.name: ACTION_INPUT_TEXT,
    ACTION_SCROLL_PAGE.name: ACTION_SCROLL_PAGE,
    # Add other pre-defined actions here
}

logger = logging.getLogger(__name__)

# Function to get an action definition
def get_action_definition(name: str) -> Optional[ActionDefinition]:
    """Retrieves an action definition by its name."""
    return AVAILABLE_ACTIONS.get(name)

# Function to list all available actions
def list_available_actions() -> List[ActionDefinition]:
    """Returns a list of all available action definitions."""
    return list(AVAILABLE_ACTIONS.values()) 