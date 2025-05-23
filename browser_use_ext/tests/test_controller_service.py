import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Adjust imports based on the new project structure `browser-use-ext`
from controller.service import Controller
from browser.context import BrowserContext
from extension_interface.service import ExtensionInterface # Added for type hinting
from browser.views import BrowserState # Added for type hinting
from controller.registry.views import ActionDefinition, list_available_actions # For testing list_actions

# --- Fixtures ---

@pytest.fixture
def mock_browser_context() -> MagicMock:
    """Provides a mock BrowserContext instance for testing the Controller."""
    mock_context = MagicMock(spec=BrowserContext)
    
    # Configure the _cached_state attribute for the Controller's __init__
    # The controller accesses browser_context._cached_state.url
    mock_cached_state = MagicMock()
    mock_cached_state.url = "http://mockurl.com" # Provide a mock URL
    mock_context._cached_state = mock_cached_state 
    
    # Also mock the extension attribute of the browser_context, as Controller accesses it.
    # Controller.execute_action -> self.browser_context.extension.execute_action
    mock_extension_interface = AsyncMock(spec=ExtensionInterface)
    mock_context.extension = mock_extension_interface
    
    # Mock methods of BrowserContext that Controller's helper methods might call indirectly.
    # For get_current_browser_state_wrapper:
    mock_browser_state_instance = MagicMock(spec=BrowserState)
    mock_browser_state_instance.model_dump.return_value = {"url": "http://mockurl.com/current", "title": "Mock Page"}
    mock_context.get_state = AsyncMock(return_value=mock_browser_state_instance)

    # For close_tab wrapper when tab_id is None:
    mock_page_proxy = MagicMock()
    mock_page_proxy.page_id = "active_mock_tab_id"
    mock_context.active_page = AsyncMock(return_value=mock_page_proxy)

    return mock_context

@pytest.fixture
def controller(mock_browser_context: MagicMock) -> Controller:
    """Provides a Controller instance initialized with a mock BrowserContext."""
    return Controller(browser_context=mock_browser_context)

# --- Test Cases ---

def test_controller_initialization(controller: Controller, mock_browser_context: MagicMock):
    """Test that the Controller initializes correctly with a BrowserContext."""
    assert controller.browser_context == mock_browser_context

@pytest.mark.asyncio
async def test_controller_execute_action_direct_call(controller: Controller, mock_browser_context: MagicMock):
    """Test the main execute_action method for direct calls to extension."""
    action_name = "test_extension_action"
    params = {"key": "value"}
    expected_response = {"success": True, "data": "action_completed"}
    
    mock_browser_context.extension.execute_action = AsyncMock(return_value=expected_response)
    
    result = await controller.execute_action(action_name=action_name, params=params, timeout=10.0)
    
    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name=action_name,
        params=params,
        timeout=10.0
    )
    assert result == expected_response

@pytest.mark.asyncio
async def test_controller_execute_action_handles_extension_error(controller: Controller, mock_browser_context: MagicMock):
    """Test that execute_action returns an error dict if extension call fails."""
    action_name = "failing_action"
    params = {}
    mock_browser_context.extension.execute_action = AsyncMock(side_effect=RuntimeError("Extension communication failed"))
    
    result = await controller.execute_action(action_name=action_name, params=params)
    
    assert isinstance(result, dict)
    assert "error" in result
    assert "Extension communication failed" in result["error"]

# --- Test Wrapper Methods ---

@pytest.mark.asyncio
async def test_controller_go_to_url_wrapper(controller: Controller, mock_browser_context: MagicMock):
    target_url = "https://example.com"
    mock_response = {"success": True, "new_url": target_url}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_response)
    
    result = await controller.go_to_url(target_url)
    
    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="go_to_url",
        params={"url": target_url},
        timeout=30.0
    )
    assert result == mock_response

@pytest.mark.asyncio
async def test_controller_click_element_by_index_wrapper(controller: Controller, mock_browser_context: MagicMock):
    element_idx = 5
    mock_response = {"success": True, "message": "Element clicked"}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_response)

    result = await controller.click_element_by_index(element_idx)

    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="click_element_by_index",
        params={"highlight_index": element_idx},
        timeout=30.0
    )
    assert result == mock_response

@pytest.mark.asyncio
async def test_controller_input_text_wrapper(controller: Controller, mock_browser_context: MagicMock):
    element_idx = 3
    text_to_input = "Hello, world!"
    mock_response = {"success": True, "message": "Text input successful"}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_response)

    result = await controller.input_text(element_idx, text_to_input)

    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="input_text",
        params={"highlight_index": element_idx, "text": text_to_input},
        timeout=30.0
    )
    assert result == mock_response

@pytest.mark.asyncio
async def test_controller_scroll_page_wrapper(controller: Controller, mock_browser_context: MagicMock):
    scroll_direction = "down"
    mock_response = {"success": True, "scroll_position_y": 1000}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_response)

    result = await controller.scroll_page(scroll_direction)

    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="scroll_page",
        params={"direction": scroll_direction},
        timeout=30.0
    )
    assert result == mock_response

@pytest.mark.asyncio
async def test_controller_scroll_page_invalid_direction(controller: Controller, mock_browser_context: MagicMock):
    result = await controller.scroll_page("sideways")
    assert isinstance(result, dict)
    assert "error" in result
    assert "Invalid scroll direction" in result["error"]
    mock_browser_context.extension.execute_action.assert_not_called()

@pytest.mark.asyncio
async def test_controller_go_back_wrapper(controller: Controller, mock_browser_context: MagicMock):
    mock_response = {"success": True}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_response)

    result = await controller.go_back()

    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="go_back",
        params={},
        timeout=30.0
    )
    assert result == mock_response

@pytest.mark.asyncio
async def test_controller_extract_content_wrapper(controller: Controller, mock_browser_context: MagicMock):
    mock_page_content_response = {"success": True, "content": "Full page text."}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_page_content_response)
    
    result_page = await controller.extract_content(content_type="text")
    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="extract_content",
        params={"content_type": "text"}, 
        timeout=30.0
    )
    assert result_page == mock_page_content_response

    mock_browser_context.extension.execute_action.reset_mock() 
    element_idx = 7
    mock_element_content_response = {"success": True, "content": "Element text."}
    mock_browser_context.extension.execute_action.return_value = mock_element_content_response

    result_element = await controller.extract_content(index=element_idx, content_type="html")
    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="extract_content",
        params={"content_type": "html", "highlight_index": element_idx},
        timeout=30.0
    )
    assert result_element == mock_element_content_response

@pytest.mark.asyncio
async def test_controller_send_keys_wrapper(controller: Controller, mock_browser_context: MagicMock):
    keys_to_send = "Enter"
    mock_response = {"success": True}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_response)

    result_active = await controller.send_keys(keys_to_send)
    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="send_keys",
        params={"keys": keys_to_send}, 
        timeout=30.0
    )
    assert result_active == mock_response
    
    mock_browser_context.extension.execute_action.reset_mock()
    element_idx = 2
    result_element = await controller.send_keys(keys_to_send, index=element_idx)
    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="send_keys",
        params={"keys": keys_to_send, "highlight_index": element_idx},
        timeout=30.0
    )
    assert result_element == mock_response

@pytest.mark.asyncio
async def test_controller_open_tab_wrapper(controller: Controller, mock_browser_context: MagicMock):
    test_url = "https://example.com/new"
    mock_response = {"success": True, "new_tab_id": "tabXYZ"}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_response)
    mock_browser_context.get_state = AsyncMock() 

    result = await controller.open_tab(test_url)

    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="open_tab",
        params={"url": test_url},
        timeout=30.0
    )
    assert result == mock_response
    mock_browser_context.get_state.assert_awaited_once_with(force_refresh=True)

@pytest.mark.asyncio
async def test_controller_switch_tab_wrapper(controller: Controller, mock_browser_context: MagicMock):
    target_tab_id = "tab123"
    mock_response = {"success": True, "active_tab_id": target_tab_id}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_response)
    mock_browser_context.get_state = AsyncMock()

    result = await controller.switch_tab(target_tab_id)

    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="switch_tab",
        params={"tab_id": target_tab_id},
        timeout=30.0
    )
    assert result == mock_response
    mock_browser_context.get_state.assert_awaited_once_with(force_refresh=True)

@pytest.mark.asyncio
async def test_controller_close_tab_wrapper_with_id(controller: Controller, mock_browser_context: MagicMock):
    target_tab_id = "tab_to_close"
    mock_response = {"success": True, "closed_tab_id": target_tab_id}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_response)
    mock_browser_context.get_state = AsyncMock()

    result = await controller.close_tab(target_tab_id)

    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="close_tab",
        params={"tab_id": target_tab_id},
        timeout=30.0
    )
    assert result == mock_response
    mock_browser_context.get_state.assert_awaited_once_with(force_refresh=True)

@pytest.mark.asyncio
async def test_controller_close_tab_wrapper_active_tab(controller: Controller, mock_browser_context: MagicMock):
    active_tab_id_from_mock = "active_mock_tab_id"
    mock_response = {"success": True, "closed_tab_id": active_tab_id_from_mock}
    mock_browser_context.extension.execute_action = AsyncMock(return_value=mock_response)
    
    result = await controller.close_tab()

    mock_browser_context.active_page.assert_awaited_once() 
    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="close_tab",
        params={"tab_id": active_tab_id_from_mock}, 
        timeout=30.0
    )
    assert result == mock_response
    assert mock_browser_context.get_state.await_args.kwargs.get('force_refresh') is True


@pytest.mark.asyncio
async def test_controller_list_actions(controller: Controller):
    actions_list = await controller.list_actions()
    assert isinstance(actions_list, list)
    registered_action_names = [a.name for a in list_available_actions()]
    returned_action_names = [a.name for a in actions_list]
    assert all(name in registered_action_names for name in returned_action_names)
    assert len(actions_list) > 0 

@pytest.mark.asyncio
async def test_controller_get_current_browser_state_wrapper(controller: Controller, mock_browser_context: MagicMock):
    expected_state_dict = {"url": "http://mockurl.com/current", "title": "Mock Page"} 
    mock_browser_context.get_state.reset_mock() 

    state_dict = await controller.get_current_browser_state(force_refresh=True)

    mock_browser_context.get_state.assert_awaited_once_with(force_refresh=True)
    assert state_dict == expected_state_dict

# To run tests (from the root of the browser-use-ext project):
# pytest tests/test_controller_service.py 