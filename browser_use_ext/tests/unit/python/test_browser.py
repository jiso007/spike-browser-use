import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# Adjust imports based on the new project structure `browser-use-ext`
from browser_use_ext.browser.browser import Browser, BrowserConfig
from browser_use_ext.browser.context import BrowserContext, BrowserContextConfig
# Import the service module directly to use with patch.object
from browser_use_ext.extension_interface import service as ei_service
from browser_use_ext.extension_interface.service import ExtensionInterface # For spec in mock

@pytest.fixture
def browser_config():
    """Provides a default BrowserConfig for testing.
       Ensure port is different from other tests if they run in parallel or don't clean up properly.
    """
    return BrowserConfig(extension_host="127.0.0.1", extension_port=8777) # Changed port

@pytest.fixture
def mock_extension_interface_instance():
    """Provides a mock instance of ExtensionInterface."""
    mock_instance = AsyncMock(spec=ExtensionInterface)
    mock_instance.start_server = AsyncMock(return_value=None)
    mock_instance.stop_server = AsyncMock(return_value=None)
    # Simulate server running state after start_server is called
    async def mock_start_server():
        mock_instance.is_server_running = True
        return None
    mock_instance.start_server = AsyncMock(side_effect=mock_start_server)
    mock_instance.is_server_running = False # Initial state
    mock_instance.has_active_connection = False # No connection initially
    return mock_instance


@pytest.fixture
def patched_extension_interface_cls(mock_extension_interface_instance: AsyncMock):
    """Patches the ExtensionInterface class to return a specific mock instance."""
    # Patch where ExtensionInterface is IMPORTED by the Browser class
    with patch("browser_use_ext.browser.browser.ExtensionInterface", return_value=mock_extension_interface_instance, autospec=True) as mock_cls:
        yield mock_cls # Yield the mock class itself for assertions on constructor calls


@pytest.mark.asyncio
async def test_browser_launch_and_close(browser_config: BrowserConfig, patched_extension_interface_cls: MagicMock, mock_extension_interface_instance: AsyncMock):
    """Test the Browser.launch and Browser.close methods, ensuring ExtensionInterface is managed."""
    browser = Browser(config=browser_config)
    
    # Test launch
    launched_browser = await browser.launch()
    assert launched_browser == browser
    assert browser.is_launched is True
    assert browser._extension_interface == mock_extension_interface_instance
    
    # Check that ExtensionInterface was instantiated with correct host/port from browser_config
    # This assertion is on the mock CLASS returned by the patch fixture
    patched_extension_interface_cls.assert_called_once_with(
        host=browser_config.extension_host, 
        port=browser_config.extension_port
    )
    # Check that start_server was called on the INSTANCE
    mock_extension_interface_instance.start_server.assert_awaited_once()
    assert mock_extension_interface_instance.is_server_running is True # Check side effect of mock_start_server

    # Test close
    await browser.close()
    assert browser.is_launched is False
    mock_extension_interface_instance.stop_server.assert_awaited_once()
    # The _extension_interface is not set to None in the current Browser.close()
    # assert browser._extension_interface is None 

@pytest.mark.asyncio
async def test_browser_async_context_manager(browser_config: BrowserConfig, patched_extension_interface_cls: MagicMock, mock_extension_interface_instance: AsyncMock):
    """Test that Browser can be used as an asynchronous context manager."""
    async with Browser(config=browser_config) as browser:
        assert browser.is_launched is True
        assert browser._extension_interface == mock_extension_interface_instance
        patched_extension_interface_cls.assert_called_once_with(host=browser_config.extension_host, port=browser_config.extension_port)
        mock_extension_interface_instance.start_server.assert_awaited_once()
        assert mock_extension_interface_instance.is_server_running is True
        
    assert browser.is_launched is False
    mock_extension_interface_instance.stop_server.assert_awaited_once()

@pytest.mark.asyncio
async def test_browser_new_context(browser_config: BrowserConfig, patched_extension_interface_cls: MagicMock, mock_extension_interface_instance: AsyncMock):
    """Test Browser.new_context() creates a BrowserContext correctly."""
    async with Browser(config=browser_config) as browser:
        context_config_override = BrowserContextConfig(view_port_height=768) # Use a field from BrowserContextConfig
        browser_context = await browser.new_context(context_config=context_config_override)
        
        assert isinstance(browser_context, BrowserContext)
        assert browser_context.config == context_config_override
        # Ensure it uses the browser's (mocked) extension interface instance
        assert browser_context._extension == mock_extension_interface_instance 

@pytest.mark.asyncio
async def test_browser_new_context_uses_default_config_if_none_provided(browser_config: BrowserConfig, patched_extension_interface_cls: MagicMock, mock_extension_interface_instance: AsyncMock):
    """Test Browser.new_context() uses default BrowserContextConfig if no override is given."""
    async with Browser(config=browser_config) as browser:
        browser_context = await browser.new_context() # No config override, should use browser_config.default_context_config
        
        assert isinstance(browser_context, BrowserContext)
        # Check that it used the default BrowserContextConfig instance from the BrowserConfig
        assert browser_context.config == browser_config.default_context_config
        assert browser_context._extension == mock_extension_interface_instance

@pytest.mark.asyncio
async def test_browser_launch_already_launched(browser_config: BrowserConfig, patched_extension_interface_cls: MagicMock, mock_extension_interface_instance: AsyncMock):
    """Test that attempting to launch an already launched browser does not call start_server again."""
    browser = Browser(config=browser_config)
    await browser.launch() # First launch
    assert browser.is_launched
    mock_extension_interface_instance.start_server.assert_awaited_once() # Called once

    await browser.launch() # Second launch attempt
    assert browser.is_launched # Still launched
    # Ensure start_server was not called again
    mock_extension_interface_instance.start_server.assert_awaited_once() 
    await browser.close() # Cleanup

@pytest.mark.asyncio
async def test_browser_new_context_when_not_launched(browser_config: BrowserConfig):
    """Test that attempting to create a new context when browser is not launched raises an error."""
    browser = Browser(config=browser_config) # Not launched yet
    assert not browser.is_launched
    with pytest.raises(RuntimeError, match="Browser must be launched and ExtensionInterface server running before creating a context."):
        await browser.new_context()

@pytest.mark.asyncio
async def test_browser_close_when_not_launched(browser_config: BrowserConfig, mock_extension_interface_instance: AsyncMock):
    """Test that closing a browser that was never launched does not error and does not call stop_server."""
    # This test needs to ensure that if Browser is instantiated but not launched,
    # its _extension_interface (which would be real if not for other tests' patching)
    # doesn't get stop_server called.
    # We use a direct mock_extension_interface_instance to simulate the _extension_interface for an unlaunched browser.
    
    browser = Browser(config=browser_config)
    # Manually assign a (potentially real or pre-mocked) extension interface if Browser.__init__ always creates one.
    # Current Browser.__init__ *does* create one. So this test relies on the global patch from other fixtures if it runs after them,
    # or it would create a real one.
    # For isolation, explicitly mock what an unlaunched browser might have or do.
    # However, the current Browser() immediately creates an ei_service.ExtensionInterface().
    # So this test implicitly relies on patching if other tests use patched_extension_interface_cls.
    # A truly isolated test would patch 'browser_use_ext.browser.browser.ExtensionInterface' just for this test scope.

    assert not browser.is_launched
    
    # Store the _extension_interface that Browser created. If patched_extension_interface_cls fixture is active,
    # this will be mock_extension_interface_instance.
    # If no global patch active, it's a real one.
    # Let's assume for this test that the interest is that stop_server on *whatever* interface it has isn't called.
    # The mock_extension_interface_instance passed as arg isn't automatically browser's _extension_interface here without launch & patching.
    # So, we check the one Browser itself creates.
    
    # To be robust, let's patch just for this test to control the instance
    with patch("browser_use_ext.browser.browser.ExtensionInterface", return_value=mock_extension_interface_instance) as temp_mock_cls:
        fresh_browser = Browser(config=browser_config)
        assert not fresh_browser.is_launched
        assert fresh_browser._extension_interface == mock_extension_interface_instance

        await fresh_browser.close() # Call close on unlaunched browser
        
        assert not fresh_browser.is_launched
        # stop_server should NOT have been called on the interface of an unlaunched browser
        mock_extension_interface_instance.stop_server.assert_not_called()

# Consider adding tests for error handling during ExtensionInterface start/stop if applicable,
# e.g., if start_server could fail and Browser needs to handle that gracefully. 