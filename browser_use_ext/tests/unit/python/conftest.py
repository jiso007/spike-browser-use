import pytest
import asyncio
import logging
from typing import AsyncGenerator

from browser_use_ext.extension_interface.service import ExtensionInterface

logger = logging.getLogger(__name__)

TEST_SERVER_PORT = 8766 # Use a different port than the default to avoid conflicts

@pytest.fixture(scope="function")
async def extension_interface(request) -> AsyncGenerator[ExtensionInterface, None]:
    """
    Pytest fixture to start and stop the ExtensionInterface server for each test function.
    """
    logger.info("Pytest fixture: Starting ExtensionInterface server...")
    interface = ExtensionInterface(host="localhost", port=TEST_SERVER_PORT)
    try:
        await interface.start_server()
        logger.info("Pytest fixture: ExtensionInterface server started.")
        
        # Yield the interface instance to the test function
        yield interface
        
    except Exception as e:
        logger.error(f"Pytest fixture: Error during server startup or test execution: {e}", exc_info=True)
        # The test using the fixture will likely fail and report the error
    finally:
        logger.info("Pytest fixture: Stopping ExtensionInterface server...")
        if interface:
            await interface.close()
            logger.info("Pytest fixture: ExtensionInterface server stopped.")

# You would then modify your test function (e.g., test_agent_run_navigate_and_get_heading)
# to accept this fixture:
# async def test_agent_run_navigate_and_get_heading(extension_interface: ExtensionInterface):
#     # Use extension_interface instead of creating a new instance and managing lifecycle
#     agent = Agent(..., extension_interface=extension_interface, ...)
#     await agent.run()
#     # ... assertions ... 