import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock

from browser_use_ext.controller.service import Controller
from browser_use_ext.browser.context import BrowserContext
# Assuming ExtensionInterface is part of BrowserContext's 'extension' attribute
# from browser_use_ext.extension_interface.service import ExtensionInterface

# --- Fixtures ---

@pytest_asyncio.fixture
async def mock_browser_context():
    """Fixture to create a mock BrowserContext."""
    mock_context = AsyncMock(spec=BrowserContext)
    # The Controller calls browser_context.extension.execute_action
    mock_context.extension = AsyncMock() 
    mock_context.extension.execute_action = AsyncMock()
    
    # Mock _cached_state for the logger in Controller.__init__
    mock_context._cached_state = MagicMock()
    mock_context._cached_state.url = "http://mock.url"
    return mock_context

@pytest_asyncio.fixture
async def controller_instance(mock_browser_context: AsyncMock):
    """Fixture to create a Controller instance with a mock BrowserContext."""
    # Patch logger for Controller initialization if necessary
    # with patch('browser_use_ext.controller.service.logging.getLogger') as mock_get_logger:
    #     mock_logger_instance = MagicMock()
    #     mock_get_logger.return_value = mock_logger_instance
    controller = Controller(browser_context=mock_browser_context)
    #     controller.logger = mock_logger_instance # If direct logger access is needed
    return controller

# --- Tests ---

@pytest.mark.asyncio
async def test_controller_initialization(mock_browser_context: AsyncMock):
    """Test that the Controller initializes correctly with a BrowserContext."""
    controller = Controller(browser_context=mock_browser_context)
    assert controller.browser_context == mock_browser_context
    # Add logger assertion if logger is patched and checked

@pytest.mark.asyncio
async def test_controller_execute_action_direct(controller_instance: Controller, mock_browser_context: AsyncMock):
    """Test direct call to Controller.execute_action."""
    action_name = "test_action"
    params = {"key": "value"}
    timeout = 15.0
    expected_result = {"success": True, "data": "action_completed"}

    # Configure the mock return value for browser_context.extension.execute_action
    mock_browser_context.extension.execute_action.return_value = expected_result

    result = await controller_instance.execute_action(action_name=action_name, params=params, timeout=timeout)

    # Assert that the extension's execute_action was called correctly
    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name=action_name,
        params=params,
        timeout=timeout
    )
    # Assert that the result from Controller.execute_action matches the expected result
    assert result == expected_result

@pytest.mark.asyncio
async def test_controller_go_to_url(controller_instance: Controller, mock_browser_context: AsyncMock):
    """Test the go_to_url wrapper method."""
    url_to_navigate = "https://example.com"
    expected_params = {"url": url_to_navigate}
    default_timeout = 30.0 # As per Controller method default
    expected_result = {"status": "navigation_success"}

    mock_browser_context.extension.execute_action.return_value = expected_result

    result = await controller_instance.go_to_url(url=url_to_navigate) # Use default timeout

    # Assert that execute_action on the extension was called with correct 'go_to_url' action and params
    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="go_to_url",
        params=expected_params,
        timeout=default_timeout # Controller's go_to_url default
    )
    assert result == expected_result

@pytest.mark.asyncio
async def test_controller_click_element_by_index(controller_instance: Controller, mock_browser_context: AsyncMock):
    """Test the click_element_by_index wrapper method."""
    element_index = 5
    expected_params = {"highlight_index": element_index}
    custom_timeout = 20.0
    expected_result = {"status": "click_success", "element_id": element_index}

    mock_browser_context.extension.execute_action.return_value = expected_result

    result = await controller_instance.click_element_by_index(index=element_index, timeout=custom_timeout)

    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="click_element_by_index",
        params=expected_params,
        timeout=custom_timeout
    )
    assert result == expected_result

@pytest.mark.asyncio
async def test_controller_input_text(controller_instance: Controller, mock_browser_context: AsyncMock):
    """Test the input_text wrapper method."""
    index = 1
    text_to_input = "Hello World"
    expected_params = {"highlight_index": index, "text": text_to_input}
    default_timeout = 30.0
    expected_result = {"status": "input_success"}

    mock_browser_context.extension.execute_action.return_value = expected_result
    
    result = await controller_instance.input_text(index=index, text=text_to_input) # Use default timeout

    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="input_text",
        params=expected_params,
        timeout=default_timeout
    )
    assert result == expected_result

@pytest.mark.asyncio
async def test_controller_scroll_page(controller_instance: Controller, mock_browser_context: AsyncMock):
    """Test the scroll_page wrapper method."""
    direction = "down"
    expected_params = {"direction": direction}
    default_timeout = 30.0
    expected_result = {"status": "scroll_success"}

    mock_browser_context.extension.execute_action.return_value = expected_result
    
    result = await controller_instance.scroll_page(direction=direction)

    mock_browser_context.extension.execute_action.assert_awaited_once_with(
        action_name="scroll_page",
        params=expected_params,
        timeout=default_timeout
    )
    assert result == expected_result

@pytest.mark.asyncio
async def test_controller_scroll_page_invalid_direction(controller_instance: Controller, mock_browser_context: AsyncMock):
    """Test scroll_page with an invalid direction."""
    invalid_direction = "sideways"
    expected_error_result = {"error": "Invalid scroll direction"}
    
    result = await controller_instance.scroll_page(direction=invalid_direction)

    # Assert that execute_action was NOT called for invalid direction
    mock_browser_context.extension.execute_action.assert_not_called()
    assert result == expected_error_result
    
# TODO: Add tests for other controller methods like go_back, extract_content, send_keys,
# open_tab, switch_tab, close_tab, list_actions, get_current_browser_state.
# For tab management methods, consider how BrowserContext's get_state(force_refresh=True)
# might need to be mocked or asserted if the controller calls it. 