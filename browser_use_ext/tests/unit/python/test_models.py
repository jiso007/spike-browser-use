import pytest
from typing import TypeVar, Generic, Optional, List, Dict, Any
from pydantic import BaseModel, Field, ValidationError

# Actual project model imports
from browser_use_ext.extension_interface.models import Message, RequestData, ResponseData
from browser_use_ext.browser.views import BrowserState, TabInfo # Assuming DOMElementNode is not directly tested here or is part of BrowserState
# from browser_use_ext.dom.views import DOMElementNode # Uncomment if DOMElementNode is tested separately and is in dom.views

T = TypeVar('T')

# Simplified dummy model for testing generics and nested structures if Message/ResponseData tests need it.
class DummyData(BaseModel):
    item_id: int
    item_name: str
    is_active: Optional[bool] = True

# --- Pytest Tests ---

def test_dummy_data_creation():
    """Test successful creation of DummyData."""
    data = DummyData(item_id=1, item_name="Test Item")
    assert data.item_id == 1
    assert data.item_name == "Test Item"
    assert data.is_active is True

def test_dummy_data_validation_error():
    """Test ValidationError for DummyData with missing fields."""
    with pytest.raises(ValidationError):
        DummyData(item_name="Missing ID") # item_id is required
    with pytest.raises(ValidationError):
        DummyData(item_id=1) # item_name is required

@pytest.mark.parametrize("message_id, message_type, data_payload_model", [
    (1, "request", DummyData(item_id=10, item_name="Payload")),
    (2, "response", {"status": "ok"}), 
    (3, "event", None),
])
def test_message_creation_valid(message_id, message_type, data_payload_model):
    """Test successful creation of imported Message with various data types."""
    payload_type = Any
    if isinstance(data_payload_model, BaseModel):
        payload_type = type(data_payload_model)
    elif isinstance(data_payload_model, dict):
        payload_type = Dict[str, Any]
    elif data_payload_model is None:
        # For Message[Optional[Any]] or Message[NoneType] if Py version supports
        # Pydantic handles Optional[T] by allowing T or None.
        # So if data_payload_model is None, Message[Any] or Message[Optional[SpecificType]] works.
        payload_type = Any # Or a more specific Optional type if context demands, e.g. Optional[DummyData]
    
    message = Message[payload_type](id=message_id, type=message_type, data=data_payload_model)
    assert message.id == message_id
    assert message.type == message_type
    if data_payload_model is not None:
        assert message.data == data_payload_model
    else:
        assert message.data is None

def test_message_creation_specific_generic_type():
    """Test imported Message with a specific Pydantic model as generic type."""
    payload = DummyData(item_id=100, item_name="Specific Payload")
    message = Message[DummyData](id=5, type="data_update", data=payload)
    assert message.id == 5
    assert message.type == "data_update"
    assert isinstance(message.data, DummyData)
    assert message.data.item_id == 100

def test_message_validation_error_missing_fields():
    """Test ValidationError for imported Message with missing required fields."""
    with pytest.raises(ValidationError, match=r"id\s+Field required"):
        Message[Any](type="request") # Missing id

    with pytest.raises(ValidationError, match=r"type\s+Field required"):
        Message[Any](id=1) # Missing type

def test_message_validation_error_incorrect_types():
    """Test ValidationError for imported Message with incorrect data types."""
    with pytest.raises(ValidationError):
        Message[str](id="not-an-int", type="request", data="hello") # id should be int
    with pytest.raises(ValidationError):
        Message[str](id=1, type=123, data="hello") # type should be str

# Tests for actual RequestData from browser_use_ext.extension_interface.models
def test_request_data_get_state_scenario():
    """Test RequestData for a 'get_state' action's data payload."""
    # RequestData here models the 'data' field of a Message where Message.type = "get_state"
    req_data = RequestData(include_screenshot=True, tab_id=123)
    # assert req_data.action_name == "get_state" # action_name is Message.type, not part of RequestData
    assert req_data.include_screenshot is True
    assert req_data.tab_id == 123
    # Ensure other fields are default/None
    assert req_data.highlight_index is None
    assert req_data.text is None

def test_request_data_execute_action_scenario():
    """Test RequestData for an 'input_text' action's data payload."""
    # RequestData here models the 'data' field of a Message where Message.type = "input_text"
    # The original test had params={\"highlight_index\": 5, \"text\": \"hello world\"}
    # The new RequestData model has these fields directly.
    req_data = RequestData(highlight_index=5, text="hello world")
    # assert req_data.action_name == "input_text" # action_name is Message.type
    # assert req_data.params == action_params_dict # params is flattened into RequestData fields
    assert req_data.highlight_index == 5
    assert req_data.text == "hello world"
    # Ensure other fields are default/None or their expected default
    assert req_data.include_screenshot is False # Default for RequestData is False, not None
    assert req_data.tab_id is None

# Tests for actual ResponseData from browser_use_ext.extension_interface.models
def test_response_data_success_with_browser_state():
    """Test ResponseData for a successful response containing BrowserState."""
    # Create TabInfo instances - tabId and isActive are required.
    tabs_data = [TabInfo(tabId=1, url="https://example.com", title="Example", isActive=True)] 
    # Create BrowserState instance - provide all required fields as per its definition
    # Assuming html_content, tree, screenshot, selector_map are effectively required or have defaults tested elsewhere.
    # For BrowserState, `tree` is required. `selector_map` has default_factory. `screenshot` is Optional.
    # The `DOMDocumentNode` needs a `DOMElementNode` child.
    html_element = DOMElementNode(type="element", tag_name="html", children=[
        DOMElementNode(type="element", tag_name="body")
    ])
    doc_node = DOMDocumentNode(children=[html_element])

    state_payload = BrowserState(
        url="https://example.com", title="Example", tabs=tabs_data, 
        tree=doc_node, # DOMDocumentNode required here
        screenshot="base64string", 
        selector_map={},   
        pixels_above=0,    
        pixels_below=0     
    )
    # ResponseData is not generic. Instantiate directly.
    # The fields from BrowserState are directly on ResponseData when success=True
    res_data = ResponseData(success=True, url=state_payload.url, title=state_payload.title, 
                            tabs=state_payload.model_dump()['tabs'], tree=state_payload.model_dump()['tree'],
                            screenshot=state_payload.screenshot, pixels_above=state_payload.pixels_above,
                            pixels_below=state_payload.pixels_below)
    assert res_data.success is True
    assert res_data.error is None
    # Access fields directly from res_data
    assert res_data.url == "https://example.com"
    assert len(res_data.tabs) == 1
    assert isinstance(res_data.tree, dict) # tree is Dict[str, Any] in ResponseData
    assert res_data.screenshot == "base64string"
    assert res_data.pixels_above == 0
    assert res_data.pixels_below == 0

def test_response_data_error():
    """Test ResponseData for an error response."""
    # ResponseData is not generic.
    res_data = ResponseData(success=False, error="Something went wrong")
    assert res_data.success is False
    assert res_data.error == "Something went wrong"
    # The other optional fields should be None by default when not provided
    assert res_data.url is None
    assert res_data.title is None
    assert res_data.tabs is None
    assert res_data.tree is None
    assert res_data.screenshot is None
    assert res_data.pixels_above is None
    assert res_data.pixels_below is None

# Tests for actual TabInfo from browser_use_ext.browser.views
def test_tab_info_creation():
    """Test creation of actual TabInfo model."""
    tab = TabInfo(tabId=1, url="http://test.com", title="Test Page", isActive=False)
    assert tab.tabId == 1
    assert tab.url == "http://test.com"
    assert tab.title == "Test Page"
    assert tab.isActive is False

    tab_active = TabInfo(tabId=2, url="http://noicon.com", title="No Icon", isActive=True)
    assert tab_active.isActive is True

# Tests for actual BrowserState from browser_use_ext.browser.views
def test_browser_state_creation_with_tabs():
    """Test creation of actual BrowserState model with tabs."""
    tab1 = TabInfo(tabId=1, url="http://page1.com", title="Page 1", isActive=True)
    tab2 = TabInfo(tabId=2, url="http://page2.com", title="Page 2", isActive=False)
    
    html_element = DOMElementNode(type="element", tag_name="html", children=[
        DOMElementNode(type="element", tag_name="body")
    ])
    doc_node = DOMDocumentNode(children=[html_element])

    state = BrowserState(
        url="http://page1.com", title="Page 1", tabs=[tab1, tab2],
        tree=doc_node, # DOMDocumentNode required
        screenshot="sbase64==", selector_map={},
        pixels_above=10, pixels_below=20
    )
    assert state.url == "http://page1.com"
    assert state.title == "Page 1"
    assert len(state.tabs) == 2
    assert state.tabs[0].title == "Page 1"
    assert state.screenshot == "sbase64=="
    assert state.pixels_above == 10

def test_browser_state_required_fields():
    """Test BrowserState creation focusing on required fields and defaults."""
    # Assuming url, title, tabs, tree, pixels_above, pixels_below are required.
    # Screenshot, element_tree (old name), selector_map are Optional or have defaults.
    # DOMDocumentNode for the tree
    html_element = DOMElementNode(type="element", tag_name="html", children=[
        DOMElementNode(type="element", tag_name="body")
    ])
    doc_node = DOMDocumentNode(children=[html_element])

    state = BrowserState(
        url="http://required.com", title="Required Test", tabs=[],
        tree=doc_node,  # Provide the required tree
        pixels_above=0, pixels_below=0
        # screenshot, selector_map will use defaults (e.g. None or {})
    )
    assert state.url == "http://required.com"
    assert state.title == "Required Test"
    assert len(state.tabs) == 0
    assert state.screenshot is None # Default for Optional[str]
    assert isinstance(state.tree, DOMDocumentNode) # Check that tree is present and of correct type
    assert state.selector_map == {} # Default for Optional[Dict] or if Field(default_factory=dict)
    assert state.pixels_above == 0
    assert state.pixels_below == 0

# Consider adding tests for DOMElementNode if it has complex validation or behavior not covered by BrowserState tests. 

# --- Tests for DOMElementNode ---
# Assuming DOMElementNode is imported from browser_use_ext.dom.views
from browser_use_ext.dom.views import DOMElementNode

def test_dom_element_node_creation_minimal():
    """Test minimal creation of DOMElementNode with only required fields."""
    # 'type' is the primary required field based on its definition without a default.
    node = DOMElementNode(type="element")
    assert node.type == "element"
    assert node.tag_name is None
    assert node.attributes == {} # default_factory
    assert node.text is None
    assert node.children == [] # default_factory
    assert node.xpath is None
    assert node.highlight_index is None
    assert node.is_visible is True # default
    assert node.is_interactive is False # default
    assert node.value is None
    assert node.raw_html_outer is None
    assert node.raw_html_inner is None

def test_dom_element_node_creation_with_data():
    """Test DOMElementNode creation with various data fields populated."""
    attrs = {"id": "test-id", "class": "sample"}
    child_node = DOMElementNode(type="element", tag_name="span", text="child text")
    node = DOMElementNode(
        type="element",
        tag_name="div",
        attributes=attrs,
        text="Parent text",
        children=[child_node],
        xpath="/html/body/div[1]",
        highlight_index=0,
        is_visible=False,
        is_interactive=True,
        value="some value",
        raw_html_outer="<div>...</div>",
        raw_html_inner="..."
    )
    assert node.type == "element"
    assert node.tag_name == "div"
    assert node.attributes == attrs
    assert node.text == "Parent text"
    assert len(node.children) == 1
    assert node.children[0].tag_name == "span"
    assert node.children[0].text == "child text"
    assert node.xpath == "/html/body/div[1]"
    assert node.highlight_index == 0
    assert node.is_visible is False
    assert node.is_interactive is True
    assert node.value == "some value"
    assert node.raw_html_outer == "<div>...</div>"
    assert node.raw_html_inner == "..."

def test_dom_element_node_missing_type_validation_error():
    """Test ValidationError when 'type' field is missing for DOMElementNode."""
    with pytest.raises(ValidationError, match=r"type\s+Field required"):
        # Not providing 'type' which is a required field without a default.
        DOMElementNode(tag_name="div")

def test_dom_element_node_incorrect_field_type():
    """Test ValidationError for incorrect data type for a DOMElementNode field."""
    with pytest.raises(ValidationError):
        # highlight_index should be int, providing str
        DOMElementNode(type="element", highlight_index="not-an-integer")
    with pytest.raises(ValidationError):
        # attributes should be Dict, providing list
        DOMElementNode(type="element", attributes=["attr1", "attr2"])
    with pytest.raises(ValidationError):
        # is_visible should be bool, providing str
        DOMElementNode(type="element", is_visible="true_string")

def test_dom_element_node_recursive_children():
    """Test DOMElementNode with nested children (recursive structure)."""
    grand_child = DOMElementNode(type="element", tag_name="span", text="grandchild")
    child = DOMElementNode(type="element", tag_name="p", children=[grand_child])
    parent = DOMElementNode(type="element", tag_name="div", children=[child])

    assert parent.children[0].tag_name == "p"
    assert parent.children[0].children[0].tag_name == "span"
    assert parent.children[0].children[0].text == "grandchild"
    assert parent.children[0].children[0].type == "element" # Ensure type is set for nested
    assert child.type == "element"
    assert parent.type == "element"


# Consider adding tests for DOMDocumentNode as well if its usage becomes more complex
# or if it's not implicitly covered by other tests (e.g. BrowserState testing if element_tree can be DOMDocumentNode).
# For now, its structure is very simple (type: "document", children: List[DOMElementNode]).
# A basic test for DOMDocumentNode:
from browser_use_ext.dom.views import DOMDocumentNode

def test_dom_document_node_creation():
    """Test basic creation of DOMDocumentNode."""
    el_child = DOMElementNode(type="element", tag_name="html")
    doc_node = DOMDocumentNode(children=[el_child]) # 'type' has a default for DOMDocumentNode
    
    assert doc_node.type == "document"
    assert len(doc_node.children) == 1
    assert doc_node.children[0].tag_name == "html"
    assert doc_node.children[0].type == "element"

def test_dom_document_node_validation_error_missing_children():
    """Test ValidationError for DOMDocumentNode if 'children' is missing."""
    with pytest.raises(ValidationError, match=r"children\s+Field required"):
        DOMDocumentNode() # children is required

def test_dom_document_node_validation_error_incorrect_child_type_dict_coercion():
    """Test if a dict that can be coerced into DOMElementNode passes validation for children.
    Pydantic will attempt to convert dicts in a List[ModelType] into ModelType instances.
    """
    # This dict can be coerced into a DOMElementNode(type="text", tag_name=None, ... extras={ 'content': 'just text'})
    # Thus, this should NOT raise a ValidationError for List[DOMElementNode]
    try:
        doc_node = DOMDocumentNode(children=[{"type": "text", "content": "just text"}])
        assert isinstance(doc_node.children[0], DOMElementNode)
        assert doc_node.children[0].type == "text"
    except ValidationError as e:
        pytest.fail(f"Unexpected ValidationError for coercible dict: {e}")

def test_dom_document_node_validation_error_incorrect_child_type_int():
    """Test ValidationError for DOMDocumentNode if a child is a non-coercible type like int."""
    with pytest.raises(ValidationError, match=r"Input should be a valid dictionary or instance of DOMElementNode"):
        DOMDocumentNode(children=[123])


# More tests for BrowserState if DOMElementNode interactions become more complex
# e.g. methods on BrowserState that deeply traverse or manipulate the element_tree
# or specific validation rules related to the structure of element_tree. 