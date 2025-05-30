"""
Unit tests for DOM models.

Tests the DOMElementNode and DOMDocumentNode models from browser_use_ext.dom.views.
"""

import pytest
from typing import Any, Dict, List
from pydantic import ValidationError

from browser_use_ext.dom.views import DOMElementNode, DOMDocumentNode


class TestDOMElementNode:
    """Test the DOMElementNode Pydantic model."""
    
    def test_dom_element_node_minimal_creation(self):
        """Test creating a DOMElementNode with minimal required fields."""
        element = DOMElementNode(type="element")
        
        assert element.type == "element"
        assert element.tag_name is None
        assert element.attributes == {}
        assert element.text is None
        assert element.children == []
        assert element.xpath is None
        assert element.highlight_index is None
        assert element.is_visible is True  # Default value
        assert element.is_interactive is False  # Default value
        assert element.value is None
        assert element.raw_html_outer is None
        assert element.raw_html_inner is None
    
    def test_dom_element_node_full_creation(self):
        """Test creating a DOMElementNode with all fields specified."""
        attributes = {"id": "test-id", "class": "test-class", "data-test": "value"}
        children = [DOMElementNode(type="element", tag_name="span")]
        
        element = DOMElementNode(
            type="element",
            tag_name="div",
            attributes=attributes,
            text="Hello World",
            children=children,
            xpath="//div[@id='test-id']",
            highlight_index=42,
            is_visible=True,
            is_interactive=True,
            value="input-value",
            raw_html_outer="<div id='test-id'>Hello World</div>",
            raw_html_inner="Hello World"
        )
        
        assert element.type == "element"
        assert element.tag_name == "div"
        assert element.attributes == attributes
        assert element.text == "Hello World"
        assert len(element.children) == 1
        assert element.children[0].tag_name == "span"
        assert element.xpath == "//div[@id='test-id']"
        assert element.highlight_index == 42
        assert element.is_visible is True
        assert element.is_interactive is True
        assert element.value == "input-value"
        assert element.raw_html_outer == "<div id='test-id'>Hello World</div>"
        assert element.raw_html_inner == "Hello World"
    
    def test_dom_element_node_missing_type_field(self):
        """Test that creating a DOMElementNode without type field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            DOMElementNode(tag_name="div")
        
        error = exc_info.value
        assert "type" in str(error)
        assert "Field required" in str(error)
    
    def test_dom_element_node_nested_children(self):
        """Test creating a DOMElementNode with nested children."""
        # Create a deeply nested structure
        grandchild = DOMElementNode(
            type="element",
            tag_name="span",
            text="Nested text"
        )
        
        child = DOMElementNode(
            type="element",
            tag_name="p",
            children=[grandchild],
            text="Parent text"
        )
        
        parent = DOMElementNode(
            type="element",
            tag_name="div",
            children=[child],
            attributes={"class": "container"}
        )
        
        assert parent.tag_name == "div"
        assert len(parent.children) == 1
        assert parent.children[0].tag_name == "p"
        assert len(parent.children[0].children) == 1
        assert parent.children[0].children[0].tag_name == "span"
        assert parent.children[0].children[0].text == "Nested text"
    
    def test_dom_element_node_complex_attributes(self):
        """Test DOMElementNode with complex attribute structures."""
        complex_attributes = {
            "id": "complex-element",
            "class": "class1 class2 class3",
            "data-config": '{"enabled": true, "count": 5}',
            "style": "color: red; font-size: 14px;",
            "aria-label": "Complex test element",
            "data-numbers": [1, 2, 3],  # Should handle complex types
            "custom-attr": None,  # Should handle None values
            "boolean-attr": True,
            "numeric-attr": 42
        }
        
        element = DOMElementNode(
            type="element",
            tag_name="div",
            attributes=complex_attributes
        )
        
        assert element.attributes == complex_attributes
        assert element.attributes["id"] == "complex-element"
        assert element.attributes["data-numbers"] == [1, 2, 3]
        assert element.attributes["boolean-attr"] is True
        assert element.attributes["numeric-attr"] == 42
    
    def test_dom_element_node_interactive_properties(self):
        """Test interactive element properties."""
        # Non-interactive element
        static_element = DOMElementNode(
            type="element",
            tag_name="div",
            is_visible=True,
            is_interactive=False
        )
        
        assert static_element.is_visible is True
        assert static_element.is_interactive is False
        assert static_element.highlight_index is None
        
        # Interactive element
        interactive_element = DOMElementNode(
            type="element",
            tag_name="button",
            is_visible=True,
            is_interactive=True,
            highlight_index=123
        )
        
        assert interactive_element.is_visible is True
        assert interactive_element.is_interactive is True
        assert interactive_element.highlight_index == 123
    
    def test_dom_element_node_input_elements(self):
        """Test input element specific properties."""
        input_element = DOMElementNode(
            type="element",
            tag_name="input",
            attributes={"type": "text", "name": "username", "placeholder": "Enter username"},
            value="john_doe",
            is_interactive=True
        )
        
        assert input_element.tag_name == "input"
        assert input_element.attributes["type"] == "text"
        assert input_element.attributes["name"] == "username"
        assert input_element.value == "john_doe"
        assert input_element.is_interactive is True
    
    def test_dom_element_node_xpath_generation(self):
        """Test XPath field functionality."""
        element_with_xpath = DOMElementNode(
            type="element",
            tag_name="button",
            attributes={"id": "submit-btn"},
            xpath="//button[@id='submit-btn']"
        )
        
        assert element_with_xpath.xpath == "//button[@id='submit-btn']"
        
        # Element without XPath
        element_without_xpath = DOMElementNode(type="element", tag_name="div")
        assert element_without_xpath.xpath is None
    
    def test_dom_element_node_html_content(self):
        """Test raw HTML content fields."""
        element = DOMElementNode(
            type="element",
            tag_name="div",
            attributes={"class": "content"},
            text="Hello",
            raw_html_outer='<div class="content">Hello <span>World</span></div>',
            raw_html_inner='Hello <span>World</span>'
        )
        
        assert element.raw_html_outer == '<div class="content">Hello <span>World</span></div>'
        assert element.raw_html_inner == 'Hello <span>World</span>'
        assert element.text == "Hello"  # Direct text content only
    
    def test_dom_element_node_serialization(self):
        """Test serialization of DOMElementNode to dict."""
        element = DOMElementNode(
            type="element",
            tag_name="a",
            attributes={"href": "https://example.com", "target": "_blank"},
            text="Click here",
            is_interactive=True,
            highlight_index=5
        )
        
        data = element.model_dump()
        
        assert data["type"] == "element"
        assert data["tag_name"] == "a"
        assert data["attributes"]["href"] == "https://example.com"
        assert data["text"] == "Click here"
        assert data["is_interactive"] is True
        assert data["highlight_index"] == 5
        assert data["children"] == []  # Empty list by default
    
    def test_dom_element_node_deserialization(self):
        """Test creating DOMElementNode from dict data."""
        data = {
            "type": "element",
            "tag_name": "form",
            "attributes": {"method": "POST", "action": "/submit"},
            "children": [
                {
                    "type": "element",
                    "tag_name": "input",
                    "attributes": {"type": "text", "name": "email"},
                    "is_interactive": True
                }
            ],
            "is_visible": True
        }
        
        element = DOMElementNode.model_validate(data)
        
        assert element.type == "element"
        assert element.tag_name == "form"
        assert element.attributes["method"] == "POST"
        assert len(element.children) == 1
        
        # Note: Due to DOMNode = Any, children come back as dicts, not DOMElementNode objects
        # This is a limitation of the current model definition
        child_data = element.children[0]
        if isinstance(child_data, dict):
            assert child_data["tag_name"] == "input"
            assert child_data["attributes"]["type"] == "text"
            assert child_data["is_interactive"] is True
        else:
            # If the model is updated to properly handle recursive types
            assert child_data.tag_name == "input"
            assert child_data.attributes["type"] == "text"
            assert child_data.is_interactive is True
    
    def test_dom_element_node_multiple_children(self):
        """Test DOMElementNode with multiple children."""
        children = [
            DOMElementNode(type="element", tag_name="h1", text="Title"),
            DOMElementNode(type="element", tag_name="p", text="Paragraph 1"),
            DOMElementNode(type="element", tag_name="p", text="Paragraph 2"),
            DOMElementNode(
                type="element", 
                tag_name="ul",
                children=[
                    DOMElementNode(type="element", tag_name="li", text="Item 1"),
                    DOMElementNode(type="element", tag_name="li", text="Item 2")
                ]
            )
        ]
        
        container = DOMElementNode(
            type="element",
            tag_name="article",
            children=children
        )
        
        assert len(container.children) == 4
        assert container.children[0].text == "Title"
        assert container.children[1].text == "Paragraph 1"
        assert container.children[3].tag_name == "ul"
        assert len(container.children[3].children) == 2
        assert container.children[3].children[0].text == "Item 1"


class TestDOMDocumentNode:
    """Test the DOMDocumentNode Pydantic model."""
    
    def test_dom_document_node_creation(self):
        """Test creating a DOMDocumentNode with default values."""
        doc = DOMDocumentNode(children=[])
        
        assert doc.type == "document"
        assert doc.children == []
    
    def test_dom_document_node_with_html_child(self):
        """Test creating a DOMDocumentNode with an HTML element child."""
        html_element = DOMElementNode(
            type="element",
            tag_name="html",
            children=[
                DOMElementNode(type="element", tag_name="head"),
                DOMElementNode(
                    type="element", 
                    tag_name="body",
                    children=[
                        DOMElementNode(type="element", tag_name="h1", text="Hello World")
                    ]
                )
            ]
        )
        
        doc = DOMDocumentNode(children=[html_element])
        
        assert doc.type == "document"
        assert len(doc.children) == 1
        assert doc.children[0].tag_name == "html"
        assert len(doc.children[0].children) == 2
        assert doc.children[0].children[0].tag_name == "head"
        assert doc.children[0].children[1].tag_name == "body"
    
    def test_dom_document_node_custom_type(self):
        """Test creating a DOMDocumentNode with custom type."""
        doc = DOMDocumentNode(type="custom_document", children=[])
        
        assert doc.type == "custom_document"
    
    def test_dom_document_node_serialization(self):
        """Test serialization of DOMDocumentNode."""
        html_child = DOMElementNode(
            type="element",
            tag_name="html",
            attributes={"lang": "en"}
        )
        
        doc = DOMDocumentNode(children=[html_child])
        data = doc.model_dump()
        
        assert data["type"] == "document"
        assert len(data["children"]) == 1
        assert data["children"][0]["tag_name"] == "html"
        assert data["children"][0]["attributes"]["lang"] == "en"
    
    def test_dom_document_node_deserialization(self):
        """Test creating DOMDocumentNode from dict data."""
        data = {
            "type": "document",
            "children": [
                {
                    "type": "element",
                    "tag_name": "html",
                    "attributes": {"lang": "en"},
                    "children": [
                        {
                            "type": "element",
                            "tag_name": "body",
                            "children": []
                        }
                    ]
                }
            ]
        }
        
        doc = DOMDocumentNode.model_validate(data)
        
        assert doc.type == "document"
        assert len(doc.children) == 1
        assert doc.children[0].tag_name == "html"
        assert doc.children[0].attributes["lang"] == "en"
        assert len(doc.children[0].children) == 1
        
        # Note: Due to DOMNode = Any in the model, nested children come back as dicts
        body_data = doc.children[0].children[0]
        if isinstance(body_data, dict):
            assert body_data["tag_name"] == "body"
        else:
            assert body_data.tag_name == "body"


class TestDOMModelIntegration:
    """Test integration scenarios between DOM models."""
    
    def test_complete_dom_tree_structure(self):
        """Test building a complete DOM tree structure."""
        # Build a realistic DOM tree
        document = DOMDocumentNode(
            children=[
                DOMElementNode(
                    type="element",
                    tag_name="html",
                    attributes={"lang": "en"},
                    children=[
                        DOMElementNode(
                            type="element",
                            tag_name="head",
                            children=[
                                DOMElementNode(
                                    type="element",
                                    tag_name="title",
                                    text="Test Page"
                                ),
                                DOMElementNode(
                                    type="element",
                                    tag_name="meta",
                                    attributes={"charset": "utf-8"}
                                )
                            ]
                        ),
                        DOMElementNode(
                            type="element",
                            tag_name="body",
                            children=[
                                DOMElementNode(
                                    type="element",
                                    tag_name="header",
                                    children=[
                                        DOMElementNode(
                                            type="element",
                                            tag_name="h1",
                                            text="Welcome"
                                        )
                                    ]
                                ),
                                DOMElementNode(
                                    type="element",
                                    tag_name="main",
                                    children=[
                                        DOMElementNode(
                                            type="element",
                                            tag_name="form",
                                            attributes={"method": "POST"},
                                            children=[
                                                DOMElementNode(
                                                    type="element",
                                                    tag_name="input",
                                                    attributes={"type": "text", "name": "username"},
                                                    is_interactive=True,
                                                    highlight_index=1
                                                ),
                                                DOMElementNode(
                                                    type="element",
                                                    tag_name="button",
                                                    attributes={"type": "submit"},
                                                    text="Submit",
                                                    is_interactive=True,
                                                    highlight_index=2
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
        
        # Verify the structure
        assert document.type == "document"
        html = document.children[0]
        assert html.tag_name == "html"
        assert html.attributes["lang"] == "en"
        
        head, body = html.children
        assert head.tag_name == "head"
        assert body.tag_name == "body"
        
        # Check title in head
        title = head.children[0]
        assert title.tag_name == "title"
        assert title.text == "Test Page"
        
        # Check interactive elements in body
        header, main = body.children
        form = main.children[0]
        input_elem, button_elem = form.children
        
        assert input_elem.is_interactive is True
        assert input_elem.highlight_index == 1
        assert button_elem.is_interactive is True
        assert button_elem.highlight_index == 2
        assert button_elem.text == "Submit"
    
    def test_find_interactive_elements(self):
        """Test finding interactive elements in a DOM tree."""
        def find_interactive_elements(node: DOMElementNode) -> List[DOMElementNode]:
            """Recursively find all interactive elements."""
            interactive = []
            if hasattr(node, 'is_interactive') and node.is_interactive:
                interactive.append(node)
            
            for child in node.children:
                if isinstance(child, DOMElementNode):
                    interactive.extend(find_interactive_elements(child))
            
            return interactive
        
        # Create a DOM tree with mixed interactive elements
        root = DOMElementNode(
            type="element",
            tag_name="div",
            children=[
                DOMElementNode(
                    type="element",
                    tag_name="button",
                    text="Click me",
                    is_interactive=True,
                    highlight_index=1
                ),
                DOMElementNode(
                    type="element",
                    tag_name="div",
                    children=[
                        DOMElementNode(
                            type="element",
                            tag_name="a",
                            attributes={"href": "#"},
                            text="Link",
                            is_interactive=True,
                            highlight_index=2
                        ),
                        DOMElementNode(
                            type="element",
                            tag_name="span",
                            text="Non-interactive"
                        )
                    ]
                ),
                DOMElementNode(
                    type="element",
                    tag_name="input",
                    attributes={"type": "text"},
                    is_interactive=True,
                    highlight_index=3
                )
            ]
        )
        
        interactive_elements = find_interactive_elements(root)
        
        assert len(interactive_elements) == 3
        assert interactive_elements[0].tag_name == "button"
        assert interactive_elements[0].highlight_index == 1
        assert interactive_elements[1].tag_name == "a"
        assert interactive_elements[1].highlight_index == 2
        assert interactive_elements[2].tag_name == "input"
        assert interactive_elements[2].highlight_index == 3
    
    def test_dom_tree_serialization_roundtrip(self):
        """Test serializing a DOM tree to dict and back."""
        original_doc = DOMDocumentNode(
            children=[
                DOMElementNode(
                    type="element",
                    tag_name="div",
                    attributes={"class": "container", "id": "main"},
                    children=[
                        DOMElementNode(
                            type="element",
                            tag_name="p",
                            text="Hello World",
                            is_visible=True
                        ),
                        DOMElementNode(
                            type="element",
                            tag_name="button",
                            text="Click",
                            is_interactive=True,
                            highlight_index=42,
                            xpath="//button[1]"
                        )
                    ]
                )
            ]
        )
        
        # Serialize to dict
        data = original_doc.model_dump()
        
        # Deserialize back to model
        reconstructed_doc = DOMDocumentNode.model_validate(data)
        
        # Verify they are equivalent
        assert reconstructed_doc.type == original_doc.type
        assert len(reconstructed_doc.children) == len(original_doc.children)
        
        original_div = original_doc.children[0]
        reconstructed_div = reconstructed_doc.children[0]
        
        assert reconstructed_div.tag_name == original_div.tag_name
        assert reconstructed_div.attributes == original_div.attributes
        assert len(reconstructed_div.children) == len(original_div.children)
        
        # Check button element
        original_button = original_div.children[1]
        reconstructed_button_data = reconstructed_div.children[1]
        
        # Note: Due to DOMNode = Any, nested children come back as dicts
        if isinstance(reconstructed_button_data, dict):
            assert reconstructed_button_data["tag_name"] == original_button.tag_name
            assert reconstructed_button_data["text"] == original_button.text
            assert reconstructed_button_data["is_interactive"] == original_button.is_interactive
            assert reconstructed_button_data["highlight_index"] == original_button.highlight_index
            assert reconstructed_button_data["xpath"] == original_button.xpath
        else:
            # If model properly handles recursive types
            assert reconstructed_button_data.tag_name == original_button.tag_name
            assert reconstructed_button_data.text == original_button.text
            assert reconstructed_button_data.is_interactive == original_button.is_interactive
            assert reconstructed_button_data.highlight_index == original_button.highlight_index
            assert reconstructed_button_data.xpath == original_button.xpath


class TestDOMModelEdgeCases:
    """Test edge cases and error scenarios for DOM models."""
    
    def test_empty_attributes_dict(self):
        """Test handling of empty attributes."""
        element = DOMElementNode(type="element", attributes={})
        assert element.attributes == {}
    
    def test_none_text_content(self):
        """Test handling of None text content."""
        element = DOMElementNode(type="element", text=None)
        assert element.text is None
    
    def test_empty_children_list(self):
        """Test handling of empty children list."""
        element = DOMElementNode(type="element", children=[])
        assert element.children == []
    
    def test_invalid_highlight_index(self):
        """Test various highlight index values."""
        # Negative highlight index
        element1 = DOMElementNode(type="element", highlight_index=-1)
        assert element1.highlight_index == -1
        
        # Zero highlight index
        element2 = DOMElementNode(type="element", highlight_index=0)
        assert element2.highlight_index == 0
        
        # Large highlight index
        element3 = DOMElementNode(type="element", highlight_index=999999)
        assert element3.highlight_index == 999999
    
    def test_boolean_field_variations(self):
        """Test boolean field edge cases."""
        # Explicit False values
        element = DOMElementNode(
            type="element",
            is_visible=False,
            is_interactive=False
        )
        assert element.is_visible is False
        assert element.is_interactive is False
    
    def test_complex_xpath_values(self):
        """Test complex XPath expressions."""
        complex_xpaths = [
            "//div[@class='container']//button[@id='submit'][1]",
            "/html/body/div[2]/form/input[@type='text' and @name='email']",
            "//ul[@class='menu']/li[contains(@class, 'active')]/a",
            "//*[@data-testid='user-profile-button']",
            "//table//tr[position()>1]//td[3]",
            "//div[contains(text(), 'Hello') and @class='greeting']"
        ]
        
        for xpath in complex_xpaths:
            element = DOMElementNode(type="element", xpath=xpath)
            assert element.xpath == xpath
    
    def test_unicode_in_text_content(self):
        """Test Unicode characters in text content."""
        unicode_texts = [
            "Hello 世界",
            "Café ☕",
            "🎉 Celebration 🎊",
            "Русский текст",
            "العربية",
            "Emoji test: 🔥🚀✨"
        ]
        
        for text in unicode_texts:
            element = DOMElementNode(type="element", text=text)
            assert element.text == text
    
    def test_large_dom_tree(self):
        """Test performance with a large DOM tree."""
        # Create a large nested structure
        def create_nested_div(depth: int, children_per_level: int = 3) -> DOMElementNode:
            if depth == 0:
                return DOMElementNode(
                    type="element",
                    tag_name="span",
                    text=f"Leaf node",
                    is_interactive=True
                )
            
            children = [
                create_nested_div(depth - 1, children_per_level)
                for _ in range(children_per_level)
            ]
            
            return DOMElementNode(
                type="element",
                tag_name="div",
                attributes={"data-depth": str(depth)},
                children=children
            )
        
        # Create a tree with depth 5 and 3 children per level = 3^5 = 243 leaf nodes
        large_tree = create_nested_div(5, 3)
        
        # Test serialization doesn't crash
        data = large_tree.model_dump()
        assert data["tag_name"] == "div"
        assert data["attributes"]["data-depth"] == "5"
        
        # Test deserialization doesn't crash
        reconstructed = DOMElementNode.model_validate(data)
        assert reconstructed.tag_name == "div"
        assert reconstructed.attributes["data-depth"] == "5"


if __name__ == "__main__":
    pytest.main([__file__])