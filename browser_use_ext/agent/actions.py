# Standard library imports
from typing import Optional, Dict, Any, Literal

# Third-party imports
from pydantic import BaseModel, Field

# --- Action Parameter Models ---

class CommonElementParams(BaseModel):
    """Common parameters for actions targeting a specific element."""
    element_id: str = Field(description="The unique ID of the target element provided by the get_state observation.")

class ClickParams(CommonElementParams):
    """Parameters for the 'click' action."""
    # element_id is inherited
    pass # No other specific params for click, element_id is enough

class InputTextParams(CommonElementParams):
    """Parameters for the 'input_text' action (typing into an element)."""
    # element_id is inherited
    text: str = Field(description="The text to type into the element.")
    # append: bool = Field(default=False, description="Whether to append text or overwrite existing text. Default is overwrite.") # Future consideration

class ScrollParams(BaseModel):
    """Parameters for the 'scroll' action."""
    direction: Literal["up", "down", "left", "right", "element"] = Field(description="Direction to scroll. 'element' to scroll a specific element into view.")
    # Common scroll parameters
    pixels: Optional[int] = Field(default=None, description="Number of pixels to scroll. Used if direction is up, down, left, or right.")
    # Element-specific scroll parameters (used if direction is 'element')
    element_id: Optional[str] = Field(default=None, description="The ID of the element to scroll into view. Required if direction is 'element'.")
    # Page scroll (percentage or specific positions)
    # percentage: Optional[float] = Field(default=None, gt=0, le=100, description="Percentage of the page/element to scroll.")
    # scroll_to: Optional[Literal["top", "bottom", "leftmost", "rightmost"]] = Field(default=None, description="Scroll to a specific edge of the page/element.")

class NavigateParams(BaseModel):
    """Parameters for the 'navigate' action."""
    url: str = Field(description="The absolute URL to navigate to.")

class GetStateParams(BaseModel):
    """Parameters for the 'get_state' action."""
    include_screenshot: bool = Field(default=False, description="Whether to include a base64 encoded screenshot of the current viewport.")
    # tab_id: Optional[int] = Field(default=None, description="Optional specific tab ID to get state from. Defaults to active tab if None.") # Handled by ExtensionInterface directly

class DoneParams(BaseModel):
    """Parameters for the 'done' action, signaling task completion."""
    success: bool = Field(description="Whether the overall task was completed successfully.")
    message: str = Field(description="A final message summarizing the outcome or providing extracted information.")
    # extracted_data: Optional[Dict[str, Any]] = Field(default=None, description="Any structured data extracted as part of task completion.") # Future consideration

class ExtractContentParams(BaseModel):
    """Parameters for the 'extract_content' action."""
    # element_id: Optional[str] = Field(default=None, description="Optional ID of a specific element to extract content from. If None, extracts from the whole page.")
    query_or_goal: str = Field(description="A natural language query or goal describing what content to extract (e.g., 'all email addresses', 'the main article text', 'product price').")
    # extraction_schema: Optional[Dict[str, Any]] = Field(default=None, description="Optional Pydantic model or JSON schema for structured extraction.") # Future consideration

# --- Union of all Action Parameter Models (for discriminated union in ActionCommand) ---
# This will be defined in views.py where ActionCommand is, after these are importable. 