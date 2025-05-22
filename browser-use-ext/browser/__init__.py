# This file makes the browser directory a Python package. 

# Optionally, import key classes for easier access from this package level
from .browser import Browser, BrowserConfig
from .context import BrowserContext, BrowserContextConfig, ExtensionPageProxy
from .views import BrowserState, TabInfo

__all__ = [
    "Browser",
    "BrowserConfig",
    "BrowserContext",
    "BrowserContextConfig",
    "ExtensionPageProxy",
    "BrowserState",
    "TabInfo",
] 