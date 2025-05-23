from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DOMElementNode(BaseModel):
    """
    Represents a node in the DOM tree.

    This model captures essential information about a DOM element,
    including its tag name, attributes, visibility, and relationship
    with other nodes.
    """

    # The HTML tag name of the element (e.g., "div", "a", "input").
    tag_name: str = Field(description="The HTML tag name of the element.")

    # A dictionary of the element's HTML attributes and their values.
    # For example: {"id": "main-content", "class": "container"}
    attributes: Dict[str, str] = Field(
        default_factory=dict, description="HTML attributes of the element."
    )

    # A unique index assigned to interactive elements for easy referencing.
    # This is particularly useful for actions like clicking or typing.
    # Non-interactive elements will have this as None.
    highlight_index: Optional[int] = Field(
        default=None, description="Unique index for interactive elements."
    )

    # Indicates whether the element is currently visible on the page.
    # Visibility is determined by factors like CSS display, visibility,
    # opacity, and dimensions.
    is_visible: bool = Field(
        default=True, description="Whether the element is visible on the page."
    )

    # The XPath expression that uniquely identifies this element in the DOM.
    xpath: str = Field(description="XPath of the element.")

    # A list of child DOMElementNode objects, representing the nested structure.
    children: List[DOMElementNode] = Field(
        default_factory=list, description="Child nodes of this element."
    )

    # A reference to the parent DOMElementNode, if this is not the root.
    # This field is typically populated after the initial tree construction.
    # The `Optional` type and `None` default allow for the root node to have no parent.
    # The `Any` type is used here to avoid circular dependency issues with Pydantic,
    # as `DOMElementNode` would refer to itself. This will be a `DOMElementNode` instance in practice.
    parent: Optional[Any] = Field(
        default=None, description="Parent node of this element."
    )
    
    # The textual content of the element, if it's a text node.
    # This is useful for extracting text from specific parts of the DOM.
    text: Optional[str] = Field(
        default=None, description="Text content if this is a text node."
    )

    # The type of the node, e.g., "element" or "text".
    # This helps in distinguishing between different kinds of DOM nodes.
    type: str = Field(
        default="element", description="Type of the DOM node (e.g., 'element', 'text')."
    )


    class Config:
        """
        Pydantic model configuration.

        `arbitrary_types_allowed = True` is necessary to allow the `parent`
        field to be of type `Any` (which will be `DOMElementNode`) without
        Pydantic raising an error during model validation.
        """
        arbitrary_types_allowed = True


# Update forward references to ensure Pydantic can resolve the self-referencing `children`
# and the `parent` field if it were strictly typed as `DOMElementNode`.
# This is crucial for models that have fields which are instances of the model itself.
DOMElementNode.model_rebuild() 