import pytest
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch # Added patch
import os # For manipulating os.getcwd and path checks

# Functions to be tested are in conftest.py, which pytest discovers automatically.
# We need to import them directly if we want to call them outside a fixture context,
# or we can test them via fixtures that use them.
from browser_use_ext.tests.conftest import get_extension_path, wait_for_extension_connection, TEST_SERVER_PORT
from browser_use_ext.extension_interface.service import ExtensionInterface

# Test for get_extension_path()

# To properly test get_extension_path, we need to simulate different directory structures
# or ensure the test runs from a context where the relative paths make sense.

@pytest.fixture
def mock_extension_path(tmp_path: Path) -> Path:
    """Creates a mock extension directory structure for testing get_extension_path."""
    # Simulates the structure expected by get_extension_path: .../browser_use_ext/extension/
    # tmp_path will be the root for this test's files.
    # We'll make tmp_path mimic the project root for this test.
    base_dir = tmp_path / "browser_use_ext"
    ext_dir = base_dir / "extension"
    ext_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a dummy file inside conftest.py's expected location relative to this structure
    # This helps get_extension_path() orient itself using Path(__file__)
    tests_dir = base_dir / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    # (Path(__file__).parent.parent / "extension")
    # For this mock, we don't actually create conftest.py, we mock where get_extension_path THINKS it is.
    return ext_dir


def test_get_extension_path_standard_layout(mock_extension_path: Path):
    """Tests get_extension_path when the extension is found via relative path from conftest.py."""
    # We need to make Path(__file__) in get_extension_path point to our mock conftest.py location
    # The conftest.py is assumed to be in browser_use_ext/tests/conftest.py
    # So, __file__ would be <something>/browser_use_ext/tests/conftest.py
    # mock_extension_path gives us <tmp_path>/browser_use_ext/extension
    # The parent of mock_extension_path is <tmp_path>/browser_use_ext
    
    # Path to the simulated conftest.py file based on the mock_extension_path fixture
    simulated_conftest_file_path = mock_extension_path.parent / "tests" / "conftest.py"

    with patch("browser_use_ext.tests.conftest.Path") as mock_path_class:
        # Mock Path(__file__) to return our simulated conftest.py path
        mock_path_instance = MagicMock(spec=Path)
        mock_path_instance.parent = MagicMock(spec=Path) # Mock the first parent
        mock_path_instance.parent.parent = MagicMock(spec=Path) # Mock the second parent
        mock_path_class.return_value = mock_path_instance
        
        # Mock exists() and is_dir() for the primary lookup path
        # (current_file.parent.parent / "extension")
        # This path should be mock_extension_path
        primary_lookup_path_mock = MagicMock(spec=Path)
        primary_lookup_path_mock.exists.return_value = True
        primary_lookup_path_mock.is_dir.return_value = True
        primary_lookup_path_mock.resolve.return_value = mock_extension_path.resolve()
        primary_lookup_path_mock.absolute.return_value = mock_extension_path.resolve()
        primary_lookup_path_mock.resolve().absolute() # Ensure it exists
        # This is what (Path(__file__).parent.parent / "extension") would evaluate to
        #(simulated_conftest_file_path.parent.parent / "extension").mkdir(exist_ok=True) # ensure it exists
        #mock_path_instance.parent.parent / "extension" = primary_lookup_path_mock
        
        # Need to mock __truediv__ for the / operator on the parent.parent mock object
        # We configure the MagicMock to return the primary_lookup_path_mock when __truediv__ is called
        # on mock_path_instance.parent.parent
        # The / operator calls __truediv__ on the object on the left.
        # So we need to mock __truediv__ on the object that is mock_path_instance.parent.parent
        
        # Get the mock object that represents parent.parent
        parent_parent_mock = mock_path_instance.parent.parent
        
        # Configure its __truediv__ method's return value
        parent_parent_mock.__truediv__ = MagicMock(return_value=primary_lookup_path_mock)

        found_path_str = get_extension_path()
        found_path = Path(found_path_str)
        
        assert found_path.exists(), "Path found by get_extension_path should exist."
        assert found_path.is_dir(), "Path found should be a directory."
        # mock_extension_path is already absolute from tmp_path fixture
        assert str(found_path.resolve()) == str(mock_extension_path.resolve()), \
            f"Expected {mock_extension_path.resolve()}, but got {found_path.resolve()}"


def test_get_extension_path_fallback_layout(tmp_path: Path):
    """Tests get_extension_path when the extension is found via os.getcwd() fallback."""
    # Create the actual extension directory structure that the fallback should find
    project_root_sim = tmp_path / "project_root"
    project_root_sim.mkdir()
    
    mock_ext_dir = project_root_sim / "browser_use_ext" / "extension"
    mock_ext_dir.mkdir(parents=True)

    # Use a simpler approach - patch only what we need
    with patch("browser_use_ext.tests.conftest.Path") as mock_path_class, \
         patch("browser_use_ext.tests.conftest.os.getcwd") as mock_getcwd:
        
        # Set up getcwd to return our project root
        mock_getcwd.return_value = str(project_root_sim)
        
        # Mock Path() to behave differently based on the argument
        def path_side_effect(arg):
            if arg == "__file__":
                # Return a mock for __file__ that makes the primary lookup fail
                mock_file_path = MagicMock()
                mock_file_path.parent.parent = tmp_path / "nonexistent"  # This will make the primary lookup fail
                return mock_file_path
            else:
                # For all other calls (like Path(os.getcwd())), use the real Path class
                return Path(arg)
        
        mock_path_class.side_effect = path_side_effect
        
        # Patch __file__ to return our mock file string
        with patch("browser_use_ext.tests.conftest.__file__", "__file__"):
            # Call the function
            found_path_str = get_extension_path()
            found_path = Path(found_path_str)
            
            assert found_path.exists(), "Path found by get_extension_path fallback should exist."
            assert found_path.is_dir(), "Path found by fallback should be a directory."
            assert str(found_path.resolve()) == str(mock_ext_dir.resolve()), \
                f"Expected fallback path {mock_ext_dir.resolve()}, but got {found_path.resolve()}"


def test_get_extension_path_not_found(tmp_path: Path):
    """Tests get_extension_path when the extension directory cannot be found by any method."""
    # Create a CWD where no 'browser_use_ext/extension' exists
    cwd_sim = tmp_path / "random_cwd"
    cwd_sim.mkdir()

    with patch("browser_use_ext.tests.conftest.Path") as mock_path_class, \
         patch("browser_use_ext.tests.conftest.os.getcwd") as mock_getcwd:

        # Set up getcwd to return a directory without extension
        mock_getcwd.return_value = str(cwd_sim)
        
        # Mock Path() to behave differently based on the argument
        def path_side_effect(arg):
            if arg == "__file__":
                # Return a mock for __file__ that makes the primary lookup fail
                mock_file_path = MagicMock()
                mock_file_path.parent.parent = tmp_path / "nonexistent"  # This will make the primary lookup fail
                return mock_file_path
            else:
                # For all other calls (like Path(os.getcwd())), use the real Path class
                return Path(arg)
        
        mock_path_class.side_effect = path_side_effect
        
        # Patch __file__ to return our mock file string
        with patch("browser_use_ext.tests.conftest.__file__", "__file__"):
            with pytest.raises(FileNotFoundError) as excinfo:
                get_extension_path()
            
            # Verify the error message mentions both attempted paths
            error_msg = str(excinfo.value)
            assert "Extension directory not found" in error_msg


# Test for wait_for_extension_connection()

@pytest.mark.asyncio
async def test_wait_for_extension_connection_connects_quickly():
    """Tests wait_for_extension_connection when connection is established quickly."""
    mock_interface = AsyncMock(spec=ExtensionInterface)
    mock_interface.has_active_connection = False
    
    # Simulate connection becoming true after a short delay
    async def set_connected_after_delay():
        await asyncio.sleep(0.1) # Short delay
        mock_interface.has_active_connection = True
        # Mock the active_connection attribute that gets logged
        mock_interface.active_connection = MagicMock()
        mock_interface.active_connection.client_id = "test_client_123"

    asyncio.create_task(set_connected_after_delay())
    
    result = await wait_for_extension_connection(mock_interface, timeout_seconds=1.0)
    assert result is True, "Should return True if connection established within timeout."
    assert mock_interface.has_active_connection is True

@pytest.mark.asyncio
async def test_wait_for_extension_connection_already_connected():
    """Tests wait_for_extension_connection when connection is already established."""
    mock_interface = AsyncMock(spec=ExtensionInterface)
    mock_interface.has_active_connection = True
    mock_interface.active_connection = MagicMock()
    mock_interface.active_connection.client_id = "test_client_456"
    
    result = await wait_for_extension_connection(mock_interface, timeout_seconds=0.1) # Short timeout
    assert result is True, "Should return True immediately if already connected."

@pytest.mark.asyncio
async def test_wait_for_extension_connection_timeout():
    """Tests wait_for_extension_connection when connection times out."""
    mock_interface = AsyncMock(spec=ExtensionInterface)
    mock_interface.has_active_connection = False # Connection never established
    
    result = await wait_for_extension_connection(mock_interface, timeout_seconds=0.2) # Short timeout
    assert result is False, "Should return False if connection times out."
    assert mock_interface.has_active_connection is False

@pytest.mark.asyncio
async def test_wait_for_extension_connection_timeout_exact():
    """Tests wait_for_extension_connection behavior around the exact timeout moment."""
    mock_interface = AsyncMock(spec=ExtensionInterface)
    mock_interface.has_active_connection = False
    timeout_duration = 0.25 # seconds

    # Use a precise way to check time passing
    loop = asyncio.get_event_loop()
    start_time = loop.time()

    result = await wait_for_extension_connection(mock_interface, timeout_seconds=timeout_duration)
    
    end_time = loop.time()
    duration = end_time - start_time

    assert result is False, "Should return False on timeout."
    # Check that the function waited for at least the timeout duration (approximately)
    # Allow for a small delta due to event loop scheduling and sleep precision.
    assert duration >= timeout_duration - 0.05, \
        f"Function exited too quickly. Expected ~{timeout_duration}s, got {duration:.4f}s"
    # And it shouldn't wait excessively longer either, though this is harder to assert tightly
    assert duration < timeout_duration + 0.2, \
         f"Function waited too long. Expected ~{timeout_duration}s, got {duration:.4f}s" 