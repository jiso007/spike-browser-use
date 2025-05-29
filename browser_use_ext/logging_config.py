import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()


def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel('TRACE')
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        # Level already defined, possibly by a previous call or another library
        # We can choose to skip or raise a more informative error
        # For now, let's assume it's okay if it's already defined with the same number
        if getattr(logging, levelName) == levelNum:
            # logging.warning(f"Logging level {levelName} already defined with number {levelNum}.")
            pass # Already defined correctly
        else:
            raise AttributeError(
                f"Logging level {levelName} already defined in logging module with a different number."
            )
        # return # Skip if levelName itself is already an attribute

    # Check for method name conflicts more carefully
    if hasattr(logging, methodName) and not (methodName == levelName.lower() and getattr(logging, levelName, None) == levelNum):
        raise AttributeError(
            f"Method name {methodName} already defined in logging module and does not match new level."
        )
    if hasattr(logging.getLoggerClass(), methodName) and not (methodName == levelName.lower() and getattr(logging, levelName, None) == levelNum):
        raise AttributeError(
            f"Method name {methodName} already defined in logger class and does not match new level."
        )


    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def setup_logging():
    # Try to add RESULT level, but ignore if it already exists
    try:
        addLoggingLevel('RESULT', 35)  # This allows ERROR, FATAL and CRITICAL
    except AttributeError as e:
        # logging.warning(f"Could not add logging level RESULT: {e}")
        pass  # Level already exists or conflict, which might be fine if set up by another part

    log_type = os.getenv('BROWSER_USE_EXT_LOGGING_LEVEL', 'info').lower()

    # Check if handlers are already set up for the root logger to avoid duplication
    if logging.getLogger().hasHandlers():
        # logging.info("Root logger already has handlers. Skipping setup_logging to avoid duplication.")
        return

    # Clear existing handlers from root to ensure clean setup
    root = logging.getLogger()
    root.handlers = []

    class BrowserUseExtFormatter(logging.Formatter):
        def format(self, record):
            if isinstance(record.name, str) and record.name.startswith('browser_use_ext.'):
                # Simplify the logger name for browser_use_ext components
                parts = record.name.split('.')
                if len(parts) > 1:
                    record.name = parts[-2] # a.b.c -> b, browser_use_ext.agent.core -> agent
                else:
                    record.name = parts[0] # browser_use_ext -> browser_use_ext
            elif isinstance(record.name, str) and record.name == 'browser_use_ext':
                record.name = 'main' # or 'app' or 'core' to be more specific if it's the main module
            return super().format(record)

    # Setup single handler for all loggers
    console = logging.StreamHandler(sys.stdout)

    # adittional setLevel here to filter logs
    if log_type == 'result':
        console.setLevel(logging.getLevelName('RESULT')) # Use getLevelName for safety
        console.setFormatter(BrowserUseExtFormatter('%(message)s'))
    else:
        console.setFormatter(BrowserUseExtFormatter('%(levelname)-8s [%(name)s] %(message)s'))

    # Configure root logger only
    root.addHandler(console)

    # switch cases for log_type
    if log_type == 'result':
        root.setLevel(logging.getLevelName('RESULT'))
    elif log_type == 'debug':
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)

    # Configure browser_use_ext logger specifically
    # This logger will inherit the root's level if not set explicitly, 
    # but we can set it to ensure it matches or is more verbose if needed.
    browser_use_ext_logger = logging.getLogger('browser_use_ext')
    # browser_use_ext_logger.propagate = False # Prevent messages from going to the root logger if it has different handlers/formatters we don't want
    # browser_use_ext_logger.addHandler(console) # This would duplicate messages if root also has console handler
    browser_use_ext_logger.setLevel(root.level)  # Ensure it respects the root level setting

    logger = logging.getLogger('browser_use_ext') # For initial info message
    # logger.info('BrowserUseExt logging setup complete with level %s', log_type)
    
    # Silence third-party loggers
    # This is important to keep the logs clean and focused on application events.
    third_party_loggers_to_silence = [
        'WDM',
        'httpx',
        'selenium',
        'playwright',
        'urllib3',
        'asyncio',
        'langchain',
        'openai',
        'httpcore',
        'charset_normalizer',
        'anthropic._base_client',
        'PIL.PngImagePlugin',
        'trafilatura.htmlprocessing',
        'trafilatura',
        'websockets.server', # Added for websockets verbosity
        'websockets.protocol' # Added for websockets verbosity
    ]
    for logger_name in third_party_loggers_to_silence:
        third_party_logger = logging.getLogger(logger_name)
        third_party_logger.setLevel(logging.ERROR) # Or logging.WARNING, depending on how much you want to see
        third_party_logger.propagate = False # Stop these logs from reaching the root handler 