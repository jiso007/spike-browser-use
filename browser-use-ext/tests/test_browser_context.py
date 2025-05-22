import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# Adjust imports based on the new project structure `browser-use-ext`
from browser.context import BrowserContext, BrowserContextConfig, ExtensionPageProxy
from extension_interface.service import ExtensionInterface
from browser.views import BrowserState, TabInfo
from dom.views import DOMElementNode

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
    mock_context._cached_state = MagicMock(spec=BrowserState) # If methods rely on this being pre-populated
    mock_context._cached_state.url = "http://initialmock.com"
    mock_context._cached_state.title = "Initial Mock Title"
    return mock_context

@pytest.fixture
def sample_browser_state() -> BrowserState:
    """Provides a sample BrowserState for testing."""
    # A simple DOM tree for testing
    sample_dom = DOMElementNode(
        tag_name="html", type="element", xpath="/html", attributes={}, children=[
            DOMElementNode(tag_name="body", type="element", xpath="/html/body", attributes={}, children=[
                DOMElementNode(tag_name="div", type="element", attributes={"id": "test-div"}, text="Click me", highlight_index=0, xpath="/html/body/div[1]"),
                DOMElementNode(tag_name="input", type="element", attributes={"type": "text", "id": "test-input"}, highlight_index=1, xpath="/html/body/input[1]")
            ])
        ]
    )
    # The BrowserState model expects element_tree to be a DOMElementNode, and tabs to be List[TabInfo]
    # The selector_map keys are integers (highlight_index).
    return BrowserState(
        url="http://example.com", # Changed from active_tab_id to direct url/title
        title="Test Page",
        tabs=[TabInfo(page_id=1, url="http://example.com", title="Test Page")], # Simplified active flag logic
        element_tree=sample_dom,
        selector_map={
            0: {"xpath": "/html/body/div[1]", "tag_name": "div"}, # Using int keys, consistent value structure
            1: {"xpath": "/html/body/input[1]", "tag_name": "input"} 
        },
        # viewport_width=1280, viewport_height=720, # These are not in BrowserState
        # scroll_x=0, scroll_y=0, # These are not in BrowserState
        # page_content_width=1280, page_content_height=1000, # These are not in BrowserState
        pixels_above=0, # Added default for BrowserState field
        pixels_below=0, # Added default for BrowserState field
        screenshot="data:image/png;base64,fakescreenshotdata"
    )

@pytest.mark.asyncio
async def test_browser_context_get_state(browser_context: BrowserContext, mock_extension_interface: AsyncMock, sample_browser_state: BrowserState):
    """Test that BrowserContext.get_state calls the extension interface and updates its internal state."""
    mock_extension_interface.get_state.return_value = sample_browser_state
    
    retrieved_state = await browser_context.get_state()
    
    mock_extension_interface.get_state.assert_called_once_with(include_screenshot=False) # Default for get_state
    assert retrieved_state == sample_browser_state
    assert browser_context._cached_browser_state == sample_browser_state # MODIFIED: _cached_state -> _cached_browser_state
    assert browser_context._cached_selector_map == sample_browser_state.selector_map # Corrected attribute name

@pytest.mark.asyncio
async def test_browser_context_get_state_caching(browser_context: BrowserContext, mock_extension_interface: AsyncMock, sample_browser_state: BrowserState):
    """Test that BrowserContext._cached_state and _cached_selector_map are updated after get_state."""
    # Mock the call to the underlying extension interface
    mock_extension_interface.get_state.return_value = sample_browser_state

    # Initial state of caches (should be None or empty)
    assert browser_context._cached_browser_state is None
    assert browser_context._cached_selector_map == {}

    # Call get_state
    retrieved_state = await browser_context.get_state()

    # Verify extension was called
    mock_extension_interface.get_state.assert_called_once_with(include_screenshot=False)
    assert retrieved_state == sample_browser_state
    
    # Verify caches are populated
    assert browser_context._cached_browser_state == sample_browser_state
    assert browser_context._cached_selector_map == sample_browser_state.selector_map

    # Call get_state again
    # In current implementation, get_state always fetches, so mock should be called again.
    # And caches should be updated again.
    another_sample_state = sample_browser_state.model_copy(update={"title": "Updated Title"})
    mock_extension_interface.get_state.return_value = another_sample_state # New state for second call
    
    second_retrieved_state = await browser_context.get_state(include_screenshot=True) # Test with different param

    mock_extension_interface.get_state.assert_called_with(include_screenshot=True) # Check last call
    assert mock_extension_interface.get_state.call_count == 2
    assert second_retrieved_state == another_sample_state
    assert browser_context._cached_browser_state == another_sample_state
    assert browser_context._cached_selector_map == another_sample_state.selector_map

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
    
    expected_title = "Test Page Title"
    mock_page_state_for_title = MagicMock(spec=BrowserState)
    mock_page_state_for_title.title = expected_title
    mock_page_state_for_title.url = "http://someurlforthestate.com" # ADDED .url attribute for the mock
    mock_browser_context.get_state.return_value = mock_page_state_for_title
    
    title = await page_proxy.title()
    
    mock_browser_context.get_state.assert_awaited_once()
    assert title == expected_title

@pytest.mark.asyncio
async def test_extension_page_proxy_url(mock_browser_context: MagicMock, mock_extension_interface: AsyncMock):
    """Test that ExtensionPageProxy.url property is updated after actions like goto."""
    mock_browser_context.extension = mock_extension_interface
    page_proxy = ExtensionPageProxy(extension=mock_extension_interface, browser_context=mock_browser_context)
    target_url = "http://testurl.com"

    mock_page_state_for_url = MagicMock(spec=BrowserState)
    mock_page_state_for_url.url = target_url
    mock_page_state_for_url.title = "Test URL Page"
    mock_browser_context.get_state.return_value = mock_page_state_for_url

    await page_proxy.goto(target_url) # Action that updates URL (and calls get_state via _update_state)
    assert page_proxy.url == target_url

@pytest.mark.asyncio
async def test_click_element_not_found_in_map(browser_context: BrowserContext, mock_extension_interface: AsyncMock, sample_browser_state: BrowserState):
    """Test getting an element by highlight_index that is not in the selector_map raises ValueError."""
    # Populate cache so get_dom_element_by_index doesn't try to fetch state itself initially for this test path
    browser_context._cached_browser_state = sample_browser_state # MODIFIED: _cached_state -> _cached_browser_state
    browser_context._cached_selector_map = sample_browser_state.selector_map # map is {0:..., 1:...}

    invalid_highlight_index = 99 # This index is not in sample_browser_state.selector_map

    with pytest.raises(ValueError, match=f"Element with index {invalid_highlight_index} not found in selector_map"):
        await browser_context.get_dom_element_by_index(invalid_highlight_index)
    
    # Ensure no interaction with extension interface if element not found in map before any action call
    mock_extension_interface.execute_action.assert_not_called()

@pytest.mark.asyncio
async def test_input_text_element_not_found_in_map(browser_context: BrowserContext, mock_extension_interface: AsyncMock, sample_browser_state: BrowserState):
    """Test getting an element by highlight_index for input that is not in the selector_map raises ValueError."""
    browser_context._cached_browser_state = sample_browser_state # MODIFIED: _cached_state -> _cached_browser_state
    browser_context._cached_selector_map = sample_browser_state.selector_map

    invalid_highlight_index = 100
    # text_to_input = "Test text" # Not used as get_dom_element_by_index will fail first

    with pytest.raises(ValueError, match=f"Element with index {invalid_highlight_index} not found in selector_map"):
        await browser_context.get_dom_element_by_index(invalid_highlight_index)
        # If we were testing a combined operation:
        # element_node = await browser_context.get_dom_element_by_index(invalid_highlight_index)
        # await browser_context._input_text_element_node(element_node, text_to_input)
    
    mock_extension_interface.execute_action.assert_not_called()

# Example of how DOMElementNode.to_html() might be used if it existed
# This is for the purpose of testing ExtensionPageProxy.content()
# Ideally, DOMElementNode would have a method to convert itself to an HTML string.
# For now, a simplified helper function is used within the test_extension_page_proxy_content test.

# Add more tests for other ExtensionPageProxy methods (e.g., close, screenshot, etc.)
# and other BrowserContext functionalities as they are implemented.

# To run this test, you would typically use pytest in your terminal:
# pytest browser-use/tests/test_browser_context.py 