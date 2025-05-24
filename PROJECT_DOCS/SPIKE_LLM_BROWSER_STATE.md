# Initial Browser State for LLM Interaction

This document explains the state of the browser when the agent first retrieves it and provides an example of the data structure passed to the LLM.

## Browser State at Initial Retrieval

**Question:** Is the browser already open when the *initial* browser state is grabbed?

**Answer:** No, not typically. The browser launch/connection is usually **lazy-initialized**. As noted in `SPIKE_FLOW.md` (Section 5, Point 2, Sub-point, Line 60):

> *   *Lazy Initialization:* On the first call, this triggers `Browser.get_playwright_browser()` -> `Browser._init()` which starts Playwright (`async_playwright().start()`) and launches/connects to the browser (`playwright.chromium.launch()`, etc.).

This means the browser instance is created *as part of* the first call to `BrowserContext.get_state()` within the initial `Agent.step()`.

## Data Structure of Browser State

**Question:** What is the exact data output format?

**Answer:** The `BrowserContext.get_state()` method returns a structured object, likely a Pydantic model instance (e.g., `BrowserState`). This object contains key information about the current web page, processed for the LLM. Common fields include:

*   **URL:** Current page URL (`url`).
*   **Title:** Page title (`title`).
*   **DOM Representation:** Often a simplified tree (`tree`) or list of interactive elements, not necessarily the full raw HTML (though raw HTML might also be included `html_content`).
*   **Screenshot:** Base64 encoded image string if vision is enabled (`screenshot`).
*   **Selector Map:** Mapping from simplified IDs used in prompts to actual CSS/XPath selectors (`selector_map`).
*   **Tabs:** Information about open tabs (`tabs`).

## Example: Initial `BrowserState` (Blank Page)

When the browser first launches, it opens to `about:blank`. The initial state object would look something like this:

```json
{
  "url": "about:blank",
  "title": "",
  "html_content": "<html><head></head><body></body></html>",
  "tree": {
    "type": "document",
    "children": [
      {
        "type": "element",
        "name": "html",
        "attributes": {},
        "children": [
          {"type": "element", "name": "head", "attributes": {}, "children": []},
          {"type": "element", "name": "body", "attributes": {}, "children": []}
        ]
      }
    ]
  },
  "screenshot": null, // Or base64 string of a blank image
  "selector_map": {},
  "tabs": [
    {
      "tabId": 1,
      "url": "about:blank",
      "title": "",
      "isActive": true
    }
  ]
}
```

This minimal state is then combined with the task description and sent to the LLM via `Agent.get_next_action()` to determine the first actual browser action (e.g., navigating to a specific URL). 