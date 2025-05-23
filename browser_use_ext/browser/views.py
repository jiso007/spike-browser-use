from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from ..dom.views import DOMElementNode


class TabInfo(BaseModel):
    """
    Represents information about a single browser tab.

    This model stores key details of a tab, such as its unique ID,
    current URL, title, and active state. This is useful for managing
    multiple tabs and providing context to the agent.
    """

    # A unique identifier for the tab, often assigned by the browser or extension.
    # This ID helps in distinguishing and targeting specific tabs for actions.
    tabId: int = Field(description="Unique identifier for the tab (from browser's tab.id).")

    # The current URL loaded in the tab.
    url: str = Field(description="Current URL of the tab.")

    # The title of the webpage currently displayed in the tab.
    title: str = Field(description="Title of the tab.")

    # Whether the tab is currently active.
    isActive: bool = Field(description="Whether the tab is currently active.")


class BrowserState(BaseModel):
    """
    Represents the complete state of the browser at a given moment.

    This model aggregates all relevant information about the browser's
    current condition, including the active tab's URL, title, raw HTML,
    DOM structure, information about all open tabs, and optionally a screenshot.
    It also includes scroll position information.
    """

    # The URL of the currently active tab.
    url: str = Field(description="URL of the active page.")

    # The title of the currently active tab.
    title: str = Field(description="Title of the active page.")

    # The raw HTML content of the active page.
    html_content: Optional[str] = Field(default=None, description="Raw HTML content of the active page (optional).")

    # The DOM structure of the active page, represented as a tree of DOMElementNode objects.
    # This provides a structured way to understand and interact with the page content.
    tree: DOMElementNode = Field(description="DOM structure of the active page.")

    # A mapping of highlight indices to their corresponding XPath expressions or element references.
    # This allows for quick lookup of interactive elements identified by the content script.
    # The keys are integers (highlight_index) and values can be XPaths (strings) or other identifiers.
    selector_map: Dict[int, Any] = Field(
        default_factory=dict, description="Map of highlight indices to selectors/elements."
    )

    # A list of TabInfo objects, representing all currently open tabs in the browser.
    # This provides an overview of the user's browsing session across multiple tabs.
    tabs: List[TabInfo] = Field(
        default_factory=list, description="List of all open tabs."
    )

    # A base64 encoded string of the screenshot of the visible part of the active page.
    # This is optional and only included if requested. We will keep this null for now.
    screenshot: Optional[str] = Field(
        default=None, description="Base64 encoded screenshot of the page (kept as null for now)."
    )

    # The number of pixels scrolled above the visible viewport.
    # This gives context about the vertical scroll position of the page.
    pixels_above: int = Field(
        default=0, description="Number of pixels scrolled above the viewport."
    )

    # The number of pixels remaining below the visible viewport that can be scrolled.
    # This indicates how much more content is available by scrolling down.
    pixels_below: int = Field(
        default=0, description="Number of pixels scrollable below the viewport."
    ) 