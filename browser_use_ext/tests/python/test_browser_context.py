import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# Adjust imports based on the new project structure `browser-use-ext`
from browser_use_ext.browser.context import BrowserContext, BrowserContextConfig, ExtensionPageProxy
from browser_use_ext.extension_interface.service import ExtensionInterface
from browser_use_ext.browser.views import BrowserState, TabInfo
from browser_use_ext.dom.views import DOMElementNode, DOMDocumentNode
from browser_use_ext.extension_interface.models import ResponseData

@pytest.fixture
def mock_extension_interface():
    """Provides a mock ExtensionInterface."""
    mock_iface = AsyncMock(spec=ExtensionInterface)
    mock_iface.get_state = AsyncMock()
    mock_iface.execute_action = AsyncMock()
    return mock_iface

@pytest.fixture
def browser_context_config():
    """Provides a default BrowserContextConfig."""
    return BrowserContextConfig()

@pytest.fixture
def browser_context(browser_context_config: BrowserContextConfig, mock_extension_interface: AsyncMock) -> BrowserContext:
    """Provides a BrowserContext instance initialized with a mock interface. Now synchronous."""
    context = BrowserContext(config=browser_context_config, extension_interface=mock_extension_interface)
    return context

@pytest.fixture
def mock_browser_context() -> MagicMock:
    """Provides a MagicMock instance of BrowserContext for testing ExtensionPageProxy."""
    mock_context = MagicMock(spec=BrowserContext)
    # Configure necessary attributes/methods that ExtensionPageProxy might call
    mock_context.get_state = AsyncMock() # ExtensionPageProxy calls await self.browser_context.get_state()
    mock_context.extension = AsyncMock(spec=ExtensionInterface) # Proxy accesses context.extension
    # Add other commonly used attributes if ExtensionPageProxy uses them, e.g., _cached_state if directly accessed.
    # For now, focusing on what ExtensionPageProxy.__init__ and its methods directly use.
    mock_context._cached_browser_state = MagicMock(spec=BrowserState) # If methods rely on this being pre-populated
    mock_context._cached_browser_state.url = "http://initialmock.com"
    mock_context._cached_browser_state.title = "Initial Mock Title"
    return mock_context

@pytest.fixture
def sample_browser_state() -> BrowserState:
    """Provides a sample BrowserState for testing."""
    # A simple DOM tree for testing
    # The top-level element for the document tree should be <html>
    html_element = DOMElementNode(
        tag_name="html", type="element", xpath="/html", attributes={}, children=[
            DOMElementNode(tag_name="body", type="element", xpath="/html/body", attributes={}, children=[
                DOMElementNode(tag_name="div", type="element", attributes={"id": "test-div"}, text="Click me", highlight_index=0, xpath="/html/body/div[1]"),
                DOMElementNode(tag_name="input", type="element", attributes={"type": "text", "id": "test-input"}, highlight_index=1, xpath="/html/body/input[1]")
            ])
        ]
    )
    sample_document_tree = DOMDocumentNode(type="document", children=[html_element])

    return BrowserState(
        url="http://example.com",
        title="Test Page",
        tabs=[TabInfo(tabId=1, url="http://example.com", title="Test Page", isActive=True)],
        tree=sample_document_tree, # Corrected: provide DOMDocumentNode
        selector_map={
            0: {"xpath": "/html/body/div[1]", "tag_name": "div"},
            1: {"xpath": "/html/body/input[1]", "tag_name": "input"}
        },
        pixels_above=0,
        pixels_below=0,
        screenshot="data:image/png;base64,fakescreenshotdata"
    )

@pytest.mark.asyncio
async def test_browser_context_get_state(browser_context: BrowserContext, mock_extension_interface: AsyncMock, sample_browser_state: BrowserState):
    """Test that BrowserContext.get_state calls the extension interface and updates its internal state."""
    # Explicitly construct the dictionary that BrowserState.model_validate will receive
    result_dict_for_browser_state = {
        "url": sample_browser_state.url,
        "title": sample_browser_state.title,
        "tabs": [t.model_dump() for t in sample_browser_state.tabs],
        "tree": sample_browser_state.tree.model_dump(), # Assuming tree is never None for a valid sample_browser_state
        "selector_map": sample_browser_state.selector_map,
        "screenshot": sample_browser_state.screenshot,
        "pixels_above": sample_browser_state.pixels_above,
        "pixels_below": sample_browser_state.pixels_below,
        "error_message": None # Explicitly add error_message for comparison consistency
    }
    mock_response = ResponseData(success=True, result=result_dict_for_browser_state)
    mock_extension_interface.get_state.return_value = mock_response

    retrieved_state = await browser_context.get_state()
    
    mock_extension_interface.get_state.assert_called_once_with(include_screenshot=False, tab_id=None) # Default for get_state
    
    print(f"RETRIEVED STATE (test_browser_context_get_state):\n{retrieved_state.model_dump_json(indent=2)}")
    print(f"SAMPLE BROWSER STATE (test_browser_context_get_state):\n{sample_browser_state.model_dump_json(indent=2)}")
    
    assert retrieved_state.model_dump_json() == sample_browser_state.model_dump_json()
    assert browser_context._cached_browser_state.model_dump_json() == sample_browser_state.model_dump_json()
    assert browser_context._cached_selector_map == sample_browser_state.selector_map

@pytest.mark.asyncio
async def test_browser_context_get_state_caching(browser_context: BrowserContext, mock_extension_interface: AsyncMock, sample_browser_state: BrowserState):
    """Test that BrowserContext._cached_state and _cached_selector_map are updated after get_state."""
    # Explicitly construct the dictionary for the first call
    result_dict_for_browser_state_initial = {
        "url": sample_browser_state.url,
        "title": sample_browser_state.title,
        "tabs": [t.model_dump() for t in sample_browser_state.tabs],
        "tree": sample_browser_state.tree.model_dump(),
        "selector_map": sample_browser_state.selector_map,
        "screenshot": sample_browser_state.screenshot,
        "pixels_above": sample_browser_state.pixels_above,
        "pixels_below": sample_browser_state.pixels_below,
        "error_message": None # Explicitly add error_message for comparison consistency
    }
    mock_response_initial = ResponseData(success=True, result=result_dict_for_browser_state_initial)
    mock_extension_interface.get_state.return_value = mock_response_initial

    # Initial state of caches (should be None or empty)
    assert browser_context._cached_browser_state is None
    assert browser_context._cached_selector_map == {}

    # Call get_state
    retrieved_state = await browser_context.get_state()

    # Verify extension was called for the first state
    mock_extension_interface.get_state.assert_any_call(include_screenshot=False, tab_id=None)
    
    print(f"RETRIEVED STATE 1 (test_browser_context_get_state_caching):\n{retrieved_state.model_dump_json(indent=2)}")
    print(f"SAMPLE BROWSER STATE (test_browser_context_get_state_caching):\n{sample_browser_state.model_dump_json(indent=2)}")
    assert retrieved_state.model_dump_json() == sample_browser_state.model_dump_json()
    
    # Verify caches are populated
    assert browser_context._cached_browser_state.model_dump_json() == sample_browser_state.model_dump_json()
    assert browser_context._cached_selector_map == sample_browser_state.selector_map

    # Call get_state again
    # In current implementation, get_state always fetches, so mock should be called again.
    # And caches should be updated again.
    another_sample_state_data = sample_browser_state.model_copy(update={"title": "Updated Title"}).model_dump()
    # Construct the dict for the updated state
    result_dict_for_browser_state_updated = {
        "url": another_sample_state_data["url"],
        "title": another_sample_state_data["title"],
        "tabs": [TabInfo.model_validate(t_data).model_dump() for t_data in another_sample_state_data["tabs"]], # Re-validate and dump
        "tree": DOMDocumentNode.model_validate(another_sample_state_data["tree"]).model_dump(), # Re-validate and dump
        "selector_map": another_sample_state_data["selector_map"],
        "screenshot": another_sample_state_data["screenshot"],
        "pixels_above": another_sample_state_data["pixels_above"],
        "pixels_below": another_sample_state_data["pixels_below"],
        "error_message": None # Explicitly add error_message for comparison consistency
    }
    mock_response_updated = ResponseData(success=True, result=result_dict_for_browser_state_updated)
    mock_extension_interface.get_state.return_value = mock_response_updated
    
    second_retrieved_state = await browser_context.get_state(include_screenshot=True, tab_id=1) # Pass tab_id=1

    mock_extension_interface.get_state.assert_any_call(include_screenshot=True, tab_id=1) # Second call with new params
    
    print(f"RETRIEVED STATE 2 (test_browser_context_get_state_caching):\n{second_retrieved_state.model_dump_json(indent=2)}")
    # Compare against a BrowserState instance created from the dict for an apples-to-apples comparison
    expected_updated_state = BrowserState.model_validate(result_dict_for_browser_state_updated)
    assert second_retrieved_state.model_dump_json() == expected_updated_state.model_dump_json()
    assert browser_context._cached_browser_state.model_dump_json() == expected_updated_state.model_dump_json()
    assert browser_context._cached_selector_map == expected_updated_state.selector_map

    print(f"EXPECTED UPDATED STATE (test_browser_context_get_state_caching):\n{expected_updated_state.model_dump_json(indent=2)}")

@pytest.mark.asyncio
async def test_browser_context_click_element_by_highlight_index(browser_context: BrowserContext, mock_extension_interface: AsyncMock, sample_browser_state: BrowserState):
    """Test clicking an element by its highlight_index."""
    browser_context._cached_browser_state = sample_browser_state # MODIFIED: _cached_state -> _cached_browser_state
    browser_context._cached_selector_map = sample_browser_state.selector_map
    
    target_highlight_index = 0 # Corresponds to the div with id "test-div"
    # The click_element_by_highlight_index method in BrowserContext uses _click_element_node,
    # which expects a DOMElementNode. get_dom_element_by_index provides this.
    # _click_element_node then calls extension.execute_action with "click_element_by_index" and the index.

    # We need to mock get_dom_element_by_index to return a node that _click_element_node can use.
    # Or, ensure sample_browser_state.element_tree has this index correctly.
    # The current sample_browser_state fixture creates DOMElementNodes with highlight_index.
    
    mock_extension_interface.execute_action.return_value = {"success": True, "message": "Clicked"}
    
    # This method is not directly on BrowserContext in the latest version. 
    # It seems to be an old test. The controller has click_element_by_index.
    # BrowserContext has _click_element_node(DOMElementNode) and get_dom_element_by_index(int).
    # Let's assume this test meant to test the underlying mechanism that would be used by a controller.
    # To test the flow: get_dom_element_by_index -> _click_element_node
    
    element_to_click = await browser_context.get_dom_element_by_index(target_highlight_index)
    assert element_to_click.highlight_index == target_highlight_index

    await browser_context._click_element_node(element_to_click)
    
    mock_extension_interface.execute_action.assert_called_once_with(
        "click_element_by_index", # Action name used by _click_element_node
        {"index": target_highlight_index}
    )
    # The result of _click_element_node is None (download path), not the extension response dict.
    # So, no assertion on result directly here unless behavior of _click_element_node changes.

@pytest.mark.asyncio
async def test_browser_context_input_text_by_highlight_index(browser_context: BrowserContext, mock_extension_interface: AsyncMock, sample_browser_state: BrowserState):
    """Test inputting text into an element by its highlight_index."""
    browser_context._cached_browser_state = sample_browser_state # MODIFIED: _cached_state -> _cached_browser_state
    browser_context._cached_selector_map = sample_browser_state.selector_map

    target_highlight_index = 1 # Corresponds to the input with id "test-input"
    text_to_input = "Hello, world!"
    # Similar to click, this tests the internal flow get_dom_element_by_index -> _input_text_element_node

    element_to_input = await browser_context.get_dom_element_by_index(target_highlight_index)
    assert element_to_input.highlight_index == target_highlight_index

    await browser_context._input_text_element_node(element_to_input, text_to_input)

    mock_extension_interface.execute_action.assert_called_once_with(
        "input_text", # Action name used by _input_text_element_node
        {"index": target_highlight_index, "text": text_to_input}
    )

@pytest.mark.asyncio
async def test_extension_page_proxy_goto(mock_browser_context: MagicMock, mock_extension_interface: AsyncMock):
    """Test ExtensionPageProxy.goto() method."""
    # Ensure the mock_browser_context.extension returns our specific mock_extension_interface for this test
    mock_browser_context.extension = mock_extension_interface

    page_proxy = ExtensionPageProxy(extension=mock_extension_interface, browser_context=mock_browser_context)
    url_to_go = "http://newexample.com"
    
    # Mock get_state on the browser_context that page_proxy will call
    mock_page_state_after_goto = MagicMock(spec=BrowserState)
    mock_page_state_after_goto.url = url_to_go
    mock_page_state_after_goto.title = "New Example Page"
    mock_browser_context.get_state.return_value = mock_page_state_after_goto

    await page_proxy.goto(url_to_go)
    
    mock_extension_interface.execute_action.assert_awaited_once_with("go_to_url", {"url": url_to_go})
    mock_browser_context.get_state.assert_awaited_once() # Ensure state was refreshed by page_proxy
    assert page_proxy.url == url_to_go
    assert page_proxy.title_val == "New Example Page"

@pytest.mark.asyncio
async def test_extension_page_proxy_wait_for_load_state(mock_browser_context: MagicMock, mock_extension_interface: AsyncMock):
    """Test ExtensionPageProxy.wait_for_load_state() method."""
    mock_browser_context.extension = mock_extension_interface
    page_proxy = ExtensionPageProxy(extension=mock_extension_interface, browser_context=mock_browser_context)
    
    # Mock get_state on the browser_context
    mock_page_state_after_load = MagicMock(spec=BrowserState)
    mock_page_state_after_load.url = "http://loaded.com"
    mock_page_state_after_load.title = "Loaded Page"
    mock_browser_context.get_state.return_value = mock_page_state_after_load
    
    await page_proxy.wait_for_load_state("networkidle") # State string is illustrative
    
    mock_browser_context.get_state.assert_awaited_once()
    assert page_proxy.url == "http://loaded.com"
    assert page_proxy.title_val == "Loaded Page"

@pytest.mark.asyncio
async def test_extension_page_proxy_content(mock_browser_context: MagicMock, mock_extension_interface: AsyncMock):
    """Test ExtensionPageProxy.content() method."""
    mock_browser_context.extension = mock_extension_interface
    page_proxy = ExtensionPageProxy(extension=mock_extension_interface, browser_context=mock_browser_context)
    
    mock_page_content_state = MagicMock(spec=BrowserState)
    mock_page_content_state.url = "http://contentpage.com"
    mock_page_content_state.title = "Content Page Title"
    # Simulate element_tree for content generation
    mock_page_content_state.element_tree = DOMElementNode(tag_name="html", type="element", xpath="/html", children=[
        DOMElementNode(tag_name="head", type="element", xpath="/html/head", children=[
            DOMElementNode(tag_name="title", type="element", xpath="/html/head/title", text="Content Page Title")
        ]),
        DOMElementNode(tag_name="body", type="element", xpath="/html/body", text="Body content here") # This text is not used by current proxy.content()
    ])
    mock_browser_context.get_state.return_value = mock_page_content_state
    
    content = await page_proxy.content()
    
    mock_browser_context.get_state.assert_awaited_once() # content() calls _update_state -> get_state
    
    # ExtensionPageProxy.content() returns a template, not actual page content from element_tree
    expected_content_template_part_url = f"Content of {mock_page_content_state.url}"
    expected_content_template_part_title = f"<title>{mock_page_content_state.title}</title>"
    
    assert expected_content_template_part_title in content
    assert expected_content_template_part_url in content
    assert "Body content here" not in content # Verify the mock body text is NOT in the output

@pytest.mark.asyncio
async def test_extension_page_proxy_title(mock_browser_context: MagicMock, mock_extension_interface: AsyncMock):
    """Test ExtensionPageProxy.title() method."""
    mock_browser_context.extension = mock_extension_interface
    page_proxy = ExtensionPageProxy(extension=mock_extension_interface, browser_context=mock_browser_context)

    mock_title_state = MagicMock(spec=BrowserState)
    mock_title_state.title = "Proxy Test Title"
    mock_title_state.url = "http://someurl.com/title_test" # Added missing url attribute
    mock_browser_context.get_state.return_value = mock_title_state
    
    title = await page_proxy.title()

    mock_browser_context.get_state.assert_awaited_once()
    assert title == "Proxy Test Title"

@pytest.mark.asyncio
async def test_extension_page_proxy_url(mock_browser_context: MagicMock, mock_extension_interface: AsyncMock):
    """Test ExtensionPageProxy.url attribute after state update."""
    mock_browser_context.extension = mock_extension_interface
    page_proxy = ExtensionPageProxy(extension=mock_extension_interface, browser_context=mock_browser_context)

    mock_url_state = MagicMock(spec=BrowserState)
    mock_url_state.url = "http://proxypage.url/test"
    mock_url_state.title = "Proxy Page Title for URL Test" # Added missing title attribute
    mock_browser_context.get_state.return_value = mock_url_state

    # Trigger state update by accessing a property that calls _update_state or calling it directly if it were public
    await page_proxy.title() # Accessing title will call _update_state -> get_state
    
    assert page_proxy.url == "http://proxypage.url/test"

@pytest.mark.asyncio
async def test_click_element_not_found_in_map(browser_context: BrowserContext, mock_extension_interface: AsyncMock, sample_browser_state: BrowserState):
    """Test clicking an element that is not in the selector_map raises an error."""
    browser_context._cached_browser_state = sample_browser_state
    browser_context._cached_selector_map = sample_browser_state.selector_map
    
    non_existent_highlight_index = 999
    
    with pytest.raises(ValueError, match=f"No DOM element found for highlight index {non_existent_highlight_index} in the cached DOM tree."):
        await browser_context.get_dom_element_by_index(non_existent_highlight_index)
    
    # Consequently, _click_element_node would not be called if get_dom_element_by_index fails.
    mock_extension_interface.execute_action.assert_not_called()

@pytest.mark.asyncio
async def test_input_text_element_not_found_in_map(browser_context: BrowserContext, mock_extension_interface: AsyncMock, sample_browser_state: BrowserState):
    """Test inputting text to an element not in selector_map raises an error."""
    browser_context._cached_browser_state = sample_browser_state
    browser_context._cached_selector_map = sample_browser_state.selector_map

    non_existent_highlight_index = 888
    text_to_input = "test text"

    with pytest.raises(ValueError, match=f"No DOM element found for highlight index {non_existent_highlight_index} in the cached DOM tree."):
        await browser_context.get_dom_element_by_index(non_existent_highlight_index)
        
    mock_extension_interface.execute_action.assert_not_called()

# Additional tests could cover:
# - Error handling from mock_extension_interface.execute_action calls
# - Behavior when sample_browser_state.element_tree is None or malformed
# - Specific logic within DOMElementNode related methods if BrowserContext uses them more directly
# - Test active_page() property of BrowserContext
