import asyncio
import logging
import os
import platform
import signal
import time
from functools import wraps
from sys import stderr
from typing import Any, Callable, Coroutine, List, Optional, ParamSpec, TypeVar

logger = logging.getLogger(__name__)

# Global flag to prevent duplicate exit messages
_exiting = False

# Define generic type variables for return type and parameters
R = TypeVar('R')
P = ParamSpec('P')


class SignalHandler:
    """
    A modular and reusable signal handling system for managing SIGINT (Ctrl+C), SIGTERM,
    and other signals in asyncio applications.

    This class provides:
    - Configurable signal handling for SIGINT and SIGTERM
    - Support for custom pause/resume callbacks
    - Management of event loop state across signals
    - Standardized handling of first and second Ctrl+C presses
    - Cross-platform compatibility (with simplified behavior on Windows)
    """

    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        pause_callback: Optional[Callable[[], None]] = None,
        resume_callback: Optional[Callable[[], None]] = None,
        custom_exit_callback: Optional[Callable[[], None]] = None,
        exit_on_second_int: bool = True,
        interruptible_task_patterns: Optional[List[str]] = None, # Modified default to None
    ):
        """
        Initialize the signal handler.

        Args:
            loop: The asyncio event loop to use. Defaults to current event loop.
            pause_callback: Function to call when system is paused (first Ctrl+C)
            resume_callback: Function to call when system is resumed
            custom_exit_callback: Function to call on exit (second Ctrl+C or SIGTERM)
            exit_on_second_int: Whether to exit on second SIGINT (Ctrl+C)
            interruptible_task_patterns: List of patterns to match task names that should be
                                         canceled on first Ctrl+C (default: ['step', 'multi_act', 'get_next_action'])
        """
        self.loop = loop or asyncio.get_event_loop()
        self.pause_callback = pause_callback
        self.resume_callback = resume_callback
        self.custom_exit_callback = custom_exit_callback
        self.exit_on_second_int = exit_on_second_int
        # Provide a default list if None is passed, as in the original
        self.interruptible_task_patterns = interruptible_task_patterns if interruptible_task_patterns is not None else ['step', 'multi_act', 'get_next_action']
        self.is_windows = platform.system() == 'Windows'

        # Initialize loop state attributes
        self._initialize_loop_state()

        # Store original signal handlers to restore them later if needed
        self.original_sigint_handler = None
        self.original_sigterm_handler = None

    def _initialize_loop_state(self) -> None:
        """Initialize loop state attributes used for signal handling."""
        setattr(self.loop, 'ctrl_c_pressed', False)
        setattr(self.loop, 'waiting_for_input', False)

    def register(self) -> None:
        """Register signal handlers for SIGINT and SIGTERM."""
        try:
            if self.is_windows:
                # On Windows, use simple signal handling with immediate exit on Ctrl+C
                def windows_handler(sig, frame):
                    print('\n\n🛑 Got Ctrl+C. Exiting immediately on Windows...\n', file=stderr)
                    # Run the custom exit callback if provided
                    if self.custom_exit_callback:
                        self.custom_exit_callback()
                    os._exit(0)

                self.original_sigint_handler = signal.signal(signal.SIGINT, windows_handler)
            else:
                # On Unix-like systems, use asyncio's signal handling for smoother experience
                self.original_sigint_handler = self.loop.add_signal_handler(signal.SIGINT, lambda: self.sigint_handler())
                self.original_sigterm_handler = self.loop.add_signal_handler(signal.SIGTERM, lambda: self.sigterm_handler())

        except Exception:
            # there are situations where signal handlers are not supported, e.g.
            # - when running in a thread other than the main thread
            # - some operating systems
            # - inside jupyter notebooks
            pass

    def unregister(self) -> None:
        """Unregister signal handlers and restore original handlers if possible."""
        try:
            if self.is_windows:
                # On Windows, just restore the original SIGINT handler
                if self.original_sigint_handler:
                    signal.signal(signal.SIGINT, self.original_sigint_handler)
            else:
                # On Unix-like systems, use asyncio's signal handler removal
                if hasattr(self.loop, 'remove_signal_handler'): # Check if method exists
                    if self.original_sigint_handler: # Ensure it was actually set by our handler
                        try:
                            self.loop.remove_signal_handler(signal.SIGINT)
                        except (ValueError, RuntimeError) as e:
                            logger.debug(f"Could not remove SIGINT handler: {e}")
                            # Fallback to restoring original if remove_signal_handler fails or wasn't used
                            if signal.getsignal(signal.SIGINT) != self.original_sigint_handler and self.original_sigint_handler is not None:
                                signal.signal(signal.SIGINT, self.original_sigint_handler)
                    if self.original_sigterm_handler: # Ensure it was actually set
                        try:
                            self.loop.remove_signal_handler(signal.SIGTERM)
                        except (ValueError, RuntimeError) as e:
                            logger.debug(f"Could not remove SIGTERM handler: {e}")
                            if signal.getsignal(signal.SIGTERM) != self.original_sigterm_handler and self.original_sigterm_handler is not None:
                                signal.signal(signal.SIGTERM, self.original_sigterm_handler)
                else: # Fallback for loops without remove_signal_handler or if it failed
                    if self.original_sigint_handler:
                        signal.signal(signal.SIGINT, self.original_sigint_handler)
                    if self.original_sigterm_handler:
                        signal.signal(signal.SIGTERM, self.original_sigterm_handler)

        except Exception as e:
            logger.warning(f'Error while unregistering signal handlers: {e}')

    def _handle_second_ctrl_c(self) -> None:
        """
        Handle a second Ctrl+C press by performing cleanup and exiting.
        This is shared logic used by both sigint_handler and wait_for_resume.
        """
        global _exiting

        if not _exiting:
            _exiting = True

            # Call custom exit callback if provided
            if self.custom_exit_callback:
                try:
                    self.custom_exit_callback()
                except Exception as e:
                    logger.error(f'Error in exit callback: {e}')

        # Force immediate exit - more reliable than sys.exit()
        print('\n\n🛑  Got second Ctrl+C. Exiting immediately...\n', file=stderr)
        # write carriage return + newline + ASNI reset to both stdout and stderr to clear any color codes
        print('\r\033[0m', end='', flush=True, file=stderr)
        print('\r\033[0m', end='', flush=True)
        os._exit(0)

    def sigint_handler(self) -> None:
        """
        SIGINT (Ctrl+C) handler.

        First Ctrl+C: Cancel current step and pause.
        Second Ctrl+C: Exit immediately if exit_on_second_int is True.
        """
        global _exiting

        if _exiting:
            # Already exiting, force exit immediately
            os._exit(0)

        if getattr(self.loop, 'ctrl_c_pressed', False):
            # If we're in the waiting for input state, let the pause method handle it
            if getattr(self.loop, 'waiting_for_input', False):
                return

            # Second Ctrl+C - exit immediately if configured to do so
            if self.exit_on_second_int:
                self._handle_second_ctrl_c()
            return # Avoid proceeding if already handling second C or not configured for it

        # Mark that Ctrl+C was pressed
        self.loop.ctrl_c_pressed = True

        # Cancel current tasks that should be interruptible - this is crucial for immediate pausing
        self._cancel_interruptible_tasks()

        # Call pause callback if provided - this sets the paused flag
        if self.pause_callback:
            try:
                self.pause_callback()
            except Exception as e:
                logger.error(f'Error in pause callback: {e}')

        # Log pause message after pause_callback is called (not before)
        print('----------------------------------------------------------------------', file=stderr)

    def sigterm_handler(self) -> None:
        """
        SIGTERM handler.

        Always exits the program completely.
        """
        global _exiting
        if not _exiting:
            _exiting = True
            print('\n\n🛑 SIGTERM received. Exiting immediately...\n\n', file=stderr)

            # Call custom exit callback if provided
            if self.custom_exit_callback:
                self.custom_exit_callback()

        os._exit(0)

    def _cancel_interruptible_tasks(self) -> None:
        """Cancel current tasks that should be interruptible."""
        current_task = asyncio.current_task(self.loop)
        for task in asyncio.all_tasks(self.loop):
            if task != current_task and not task.done():
                task_name = task.get_name() if hasattr(task, 'get_name') else str(task)
                # Cancel tasks that match certain patterns
                if any(pattern in task_name for pattern in self.interruptible_task_patterns):
                    logger.debug(f'Cancelling task: {task_name}')
                    task.cancel()
                    # Add exception handler to silence "Task exception was never retrieved" warnings
                    task.add_done_callback(lambda t: t.exception() if t.cancelled() else None)

        # Also cancel the current task if it's interruptible
        if current_task and not current_task.done():
            task_name = current_task.get_name() if hasattr(current_task, 'get_name') else str(current_task)
            if any(pattern in task_name for pattern in self.interruptible_task_patterns):
                logger.debug(f'Cancelling current task: {task_name}')
                current_task.cancel()
                current_task.add_done_callback(lambda t: t.exception() if t.cancelled() else None)


    def wait_for_resume(self) -> None:
        """
        Wait for user input to resume or exit.

        This method should be called after handling the first Ctrl+C.
        It temporarily restores default signal handling to allow catching
        a second Ctrl+C directly.
        """
        # Set flag to indicate we're waiting for input
        setattr(self.loop, 'waiting_for_input', True)

        # Temporarily restore default signal handling for SIGINT
        # This ensures KeyboardInterrupt will be raised during input()
        original_handler = signal.getsignal(signal.SIGINT)
        try:
            signal.signal(signal.SIGINT, signal.default_int_handler)
        except (ValueError, AttributeError): # AttributeError for threading._shutdown issues
            # we are running in a thread other than the main thread
            # or signal handlers are not supported for some other reason
            pass

        green = '\x1b[32;1m'
        red = '\x1b[31m'
        blink = '\033[33;5m'
        unblink = '\033[0m'
        reset = '\x1b[0m'

        try:  # escape code is to blink the ...
            print(
                f'➡️  Press {green}[Enter]{reset} to resume or {red}[Ctrl+C]{reset} again to exit{blink}...{unblink} ',
                end='',
                flush=True,
                file=stderr
            )
            input()  # Wait for user to press Enter
            # If input() returns, it means Enter was pressed
            if self.resume_callback:
                try:
                    self.resume_callback()
                except Exception as e:
                    logger.error(f'Error in resume callback: {e}')
            self.loop.ctrl_c_pressed = False  # Reset flag after resuming
            print('Resuming...', file=stderr)
        except KeyboardInterrupt:
            # Second Ctrl+C pressed during input() - exit immediately
            if self.exit_on_second_int:
                self._handle_second_ctrl_c()
            else:
                 print('\nIgnoring second Ctrl+C as exit_on_second_int is False.', file=stderr)
                 if self.resume_callback: # Still try to resume if not exiting
                    self.resume_callback()
                 self.loop.ctrl_c_pressed = False
                 print('Resuming...', file=stderr)
        finally:
            # Restore original signal handler
            try:
                signal.signal(signal.SIGINT, original_handler)
            except (ValueError, AttributeError):
                pass # Ignore if it cannot be restored (e.g. in thread)
            # Reset waiting_for_input flag
            setattr(self.loop, 'waiting_for_input', False)

    def reset(self) -> None:
        """Reset the Ctrl+C pressed flag."""
        self.loop.ctrl_c_pressed = False


def time_execution_sync(additional_text: str = '') -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.debug(
                f'{additional_text} {func.__name__} executed in {end_time - start_time:.4f} seconds'
            )
            return result
        return wrapper
    return decorator

def time_execution_async(
    additional_text: str = '',
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
    def decorator(func: Callable[P, Coroutine[Any, Any, R]]) -> Callable[P, Coroutine[Any, Any, R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            logger.debug(
                f'{additional_text} {func.__name__} executed in {end_time - start_time:.4f} seconds'
            )
            return result
        return wrapper
    return decorator

def singleton(cls):
    instances = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

def check_env_variables(keys: list[str], any_or_all=all) -> bool:
    # check if any or all environment variables are set
    return any_or_all(os.getenv(key) for key in keys) 