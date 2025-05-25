from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# Forward reference for recursive models
if True: #TYPE_CHECKING:
    DOMNode = Any # Simplified for this context, could be Union[DOMElementNode, DOMTextNode, DOMDocumentNode]
else:
    DOMNode = Any


class DOMElementNode(BaseModel):
    """
    Represents an element node in the DOM tree.
    """
    # MODIFIED: 'type' will be set by the context or sending script, not defaulted here.
    # Pydantic model will still expect 'type' in the data it validates.
    # type: str = Field(default="element", description="Type of the DOM node, e.g., 'element', 'text'.")
    
    # MODIFIED: Changed 'name' to 'tag_name' for consistency with browser APIs like tagName.
    tag_name: Optional[str] = Field(None, description="Tag name of the element (e.g., 'div', 'a', 'input'). Populated for element nodes.")
    
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Dictionary of HTML attributes of the element.")
    
    # Direct text content of the element, if any (excluding text from children).
    # For a node like <div>Hello <span>World</span></div>, text would be "Hello ".
    text: Optional[str] = Field(None, description="Direct text content of the node, if applicable.")

    # Children of this node. Can be other elements or text nodes.
    # MODIFIED: Using DOMNode for children to allow for mixed types if we had specific text nodes, etc.
    # For now, parsing logic primarily creates DOMElementNode instances.
    children: List[DOMNode] = Field(default_factory=list, description="List of child nodes.")
    
    # XPath to uniquely identify the element in the DOM.
    xpath: Optional[str] = Field(default=None, description="XPath of the element (optional).")

    # Optional unique ID assigned by the content script for highlighting and interaction.
    highlight_index: Optional[int] = Field(None, description="Unique ID for highlighting interactive elements.")

    # Visibility status of the element.
    is_visible: bool = Field(default=True, description="Whether the element is currently visible in the viewport.")
    
    # Interactability status, determined by content script (e.g., visible, not disabled).
    is_interactive: bool = Field(default=False, description="Whether the element is considered interactive.")

    # For input elements, this holds their current value.
    value: Optional[str] = Field(None, description="Value of the input element, if applicable.")
    
    # Raw outerHTML of the element, if provided by the extension.
    raw_html_outer: Optional[str] = Field(None, description="Raw outerHTML of the element.")
    # Raw innerHTML of the element, if provided by the extension.
    raw_html_inner: Optional[str] = Field(None, description="Raw innerHTML of the element.")
    
    # Field to indicate the type of node, crucial for parsing and differentiation.
    # This is expected to be present in the data from the extension.
    type: str = Field(description="Type of the DOM node, e.g., 'element', 'text'.")


    class Config:
        # Allows Pydantic to handle the forward reference for List[DOMElementNode]
        # and potentially other complex types if added later.
        arbitrary_types_allowed = True

# NEW MODEL
class DOMDocumentNode(BaseModel):
    """
    Represents the root document node of a DOM tree.
    Its children are typically a single HTML element node.
    """
    type: str = Field(default="document", description="Type of the DOM node, always 'document'.")
    children: List[DOMElementNode] = Field(description="List of child nodes, typically a single HTML element.")

    class Config:
        arbitrary_types_allowed = True

# Update forward references to ensure Pydantic can resolve the self-referencing `children`
# and the `parent` field if it were strictly typed as `DOMElementNode`.
# This is crucial for models that have fields which are instances of the model itself.
DOMElementNode.model_rebuild() 