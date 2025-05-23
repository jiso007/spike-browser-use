// browser-use-ext/extension/content.js
// Interacts with the DOM of the web page.
// Listens for messages from background.js and executes actions on the page.

console.log("Content script loaded and executing.");

// Cache for the most recently built DOM tree and selector map for the current page.
let currentDomCache = {
    tree: null,
    selectorMap: null, // Maps highlight_index to {xpath, element}
    timestamp: 0
};
const CACHE_DURATION = 1000; // Cache for 1 second to avoid re-processing on rapid requests

/**
 * Listener for messages from the background script.
 * Handles requests like 'get_state' and 'execute_action'.
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Content script received message:", message);

    if (message.type === "get_state") {
        handleGetState(message.requestId)
        .then(sendResponse)
        .catch(error => {
                console.error("Error in handleGetState:", error);
                sendResponse({
                    request_id: message.requestId,
                    status: "error",
                    error: `Failed to get state: ${error.message}`
                });
            });
        return true; // Indicates that the response will be sent asynchronously.
    } else if (message.type === "execute_action") {
        handleExecuteAction(message.payload.action, message.payload.params, message.requestId)
        .then(sendResponse)
        .catch(error => {
                console.error("Error in handleExecuteAction:", error);
                sendResponse({
                    request_id: message.requestId,
                    status: "error",
                    error: `Failed to execute action '${message.payload.action}': ${error.message}`
                });
            });
        return true; // Indicates that the response will be sent asynchronously.
    }
    // If message type is not recognized, do not call sendResponse or return true
    return false;
});

/**
 * Handles the 'get_state' request.
 * Builds the DOM tree, gathers page info, and requests a screenshot.
 * @param {string} requestId - The ID of the request.
 */
async function handleGetState(requestId) {
    console.log("Handling get_state request, ID:", requestId);
    try {
        const now = Date.now();
        if (currentDomCache.tree && currentDomCache.selectorMap && (now - currentDomCache.timestamp < CACHE_DURATION)) {
            console.log("Using cached DOM tree and selector map.");
        } else {
            console.log("Building new DOM tree and selector map.");
            const { tree, selectorMap } = buildDomTreeWithMappings(document.documentElement);
            currentDomCache = { tree, selectorMap, timestamp: now };
        }

        // ADDED CONSOLE LOG FOR DEBUGGING
        console.log("Structure of currentDomCache.tree before creating pageState:", JSON.stringify(currentDomCache.tree, null, 2));

        const pageState = {
            html_content: document.documentElement.outerHTML,
            tree: currentDomCache.tree,
            selector_map: stripElementReferencesFromSelectorMap(currentDomCache.selectorMap), // Send serializable map
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight,
            scroll_x: window.scrollX,
            scroll_y: window.scrollY,
            page_content_width: document.documentElement.scrollWidth,
            page_content_height: document.documentElement.scrollHeight,
            url: window.location.href,
            title: document.title
        };

        console.log("Successfully built state for request ID:", requestId);
        return {
            request_id: requestId,
            type: "response", // This identifies it as a response to background.js
            status: "success",
            data: pageState
        };
    } catch (error) {
        console.error("Error processing get_state in content script:", error);
        return {
            request_id: requestId,
            type: "response",
            status: "error",
            error: `Content script error during get_state: ${error.message}`
        };
    }
}

/**
 * Creates a new selector map without direct element references for serialization.
 * @param {object} selectorMap - The original selector map with element references.
 * @returns {object} A new selector map with only XPaths.
 */
function stripElementReferencesFromSelectorMap(selectorMap) {
    if (!selectorMap) return null;
    const newMap = {};
    for (const key in selectorMap) {
        newMap[key] = { xpath: selectorMap[key].xpath };
    }
    return newMap;
}


/**
 * Handles the 'execute_action' request from the background script.
 * @param {string} actionName - The name of the action to execute.
 * @param {object} params - Parameters for the action.
 * @param {string} requestId - The ID of the request.
 */
async function handleExecuteAction(actionName, params, requestId) {
    console.log(`Executing action: ${actionName} with params:`, params, "Request ID:", requestId);
    let resultData = {};
    let status = "success";
    let error = null;

    try {
        const element = params && params.highlight_index !== undefined && currentDomCache.selectorMap
            ? currentDomCache.selectorMap[params.highlight_index]?.element
            : null;

        // Ensure element is available if required by the action
        if ((actionName === "click_element_by_index" || actionName === "input_text" || actionName === "extract_content") && !element) {
            throw new Error(`Element with highlight_index ${params.highlight_index} not found or DOM cache is stale.`);
        }

        switch (actionName) {
            case "click_element_by_index":
                if (element instanceof HTMLElement) element.click();
                else throw new Error("Target for click is not an HTMLElement");
                console.log("Clicked element with index:", params.highlight_index);
                break;
            case "input_text":
                if (element instanceof HTMLInputElement || element instanceof HTMLTextAreaElement) {
                    element.value = params.text;
                    // Dispatch input and change events to simulate user interaction
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                } else {
                    throw new Error("Target for input_text is not an input or textarea element");
                }
                console.log("Input text '", params.text, "' into element with index:", params.highlight_index);
                break;
            case "go_to_url":
        window.location.href = params.url;
                console.log("Navigating to URL:", params.url);
                // For navigations, a response might not be reliably sent back if the page unloads too quickly.
                // The server should handle timeouts for actions that cause navigation.
                break;
            case "go_back":
        window.history.back();
                console.log("Navigating back.");
                break;
            case "scroll_page": // Renamed from scroll_down/scroll_up to generic scroll_page
                if (params.direction === "down") {
                    window.scrollBy(0, window.innerHeight * 0.8); // Scroll 80% of viewport height
                } else if (params.direction === "up") {
                    window.scrollBy(0, -window.innerHeight * 0.8);
                } else if (params.pixels) {
                    window.scrollBy(0, params.pixels);
                }
                console.log("Scrolled page", params.direction ? params.direction : `by ${params.pixels}px`);
                break;
            case "extract_content":
                resultData.extracted_text = element.innerText || element.textContent;
                resultData.extracted_html = element.innerHTML;
                console.log("Extracted content from element with index:", params.highlight_index);
                break;
            case "send_keys":
                 // This is a placeholder. True key event simulation is complex and often requires the debugger API (from background)
                 // or careful dispatching of KeyboardEvent objects.
                console.warn("send_keys action is a placeholder in content.js. For complex key events, background script involvement might be needed.");
                if (element && typeof element.focus === 'function') element.focus(); // Focus element if possible
                // Simplified: if text is provided, append to value if input/textarea
                if (element && (element instanceof HTMLInputElement || element instanceof HTMLTextAreaElement) && params.keys) {
                    element.value += params.keys; 
                }
                resultData.note = "send_keys is a simplified implementation.";
                break;
            // Add more actions as needed
            default:
                throw new Error(`Unknown action: ${actionName}`);
        }
        // Brief delay for actions like click/input to allow potential async DOM updates to settle
        // This is a simple approach; more robust solutions might use MutationObserver or specific event listeners.
        if (actionName === "click_element_by_index" || actionName === "input_text") {
            await new Promise(resolve => setTimeout(resolve, 150)); 
        }

    } catch (e) {
        console.error(`Error executing action ${actionName}:`, e);
        status = "error";
        error = e.message;
    }

        return {
        request_id: requestId,
        type: "response",
        status: status,
        data: resultData, // Contains action-specific results, e.g., extracted text
        error: error
    };
}

// --- DOM Processing Functions ---
let highlightCounter = 0;

/**
 * Recursively builds a simplified DOM tree and a map of highlightable elements to their XPaths.
 * @param {Node} element - The current DOM element to process.
 * @param {object} selectorMap - The map to store highlight_index to {xpath, element} for interactable elements.
 * @param {string} currentXPath - The XPath being built for the current element.
 * @returns {object} An object containing the DOM tree node and the selectorMap.
 */
function buildDomTreeWithMappings(element, selectorMap = {}, currentXPath = '/HTML[1]') {
    if (!element || !element.tagName) return null;

    const tagName = element.tagName.toLowerCase();

    // Skip script, style, meta, link, noscript, and comment nodes, but process their children if body/head
    const  SKIP_TAGS = ["script", "style", "meta", "link", "noscript", "#comment"];
    if (SKIP_TAGS.includes(tagName)) {
        // For critical layout tags like <head>, we might want to process children
        // but for this general purpose tree, skipping them is fine if they are not visible elements.
        return null; 
    }

    const attributes = getElementAttributes(element);
    let textContent = null;

    // Get direct text content, excluding children's text
    if (element.childNodes && element.childNodes.length > 0) {
        let directText = '';
        for (let i = 0; i < element.childNodes.length; i++) {
            if (element.childNodes[i].nodeType === Node.TEXT_NODE) {
                directText += element.childNodes[i].nodeValue.trim();
            }
        }
        if (directText) textContent = directText;
    }

    const isVisible = isElementGenerallyVisible(element);
    const isInteractable = isVisible && isElementInteractable(element);
    let highlightIndex = null;

    if (isInteractable || (isVisible && (tagName === 'p' || tagName.match(/^h[1-6]$/) || tagName === 'span' || tagName === 'div'))) {
        highlightCounter++;
        highlightIndex = highlightCounter;
        selectorMap[highlightIndex] = {
            xpath: currentXPath,
            element: element // Store direct reference for action execution
        };
    }

        const children = [];
    if (element.children) {
        for (let i = 0; i < element.children.length; i++) {
            const childElement = element.children[i];
            const childXPath = getXPathForElement(childElement, currentXPath); // Generate XPath for child
            const childNode = buildDomTreeWithMappings(childElement, selectorMap, childXPath);
            if (childNode && childNode.tree) { // Ensure childNode and its tree are not null
                 children.push(childNode.tree);
            }
        }
    }
    
    // Reset counter for next full build if this is the root call (document.documentElement)
    if (element === document.documentElement) {
        highlightCounter = 0;
    }

        return {
        tree: {
            type: "element",
            tag_name: tagName,
            attributes: attributes,
            text: textContent,
            children: children,
            highlight_index: highlightIndex,
            xpath: currentXPath,
            is_visible: isVisible,
            is_interactable: isInteractable
        },
        selectorMap: selectorMap
    };
}

/**
 * Checks if an element is generally visible (simplified check).
 * @param {Element} element - The DOM element.
 * @returns {boolean} True if the element is likely visible.
 */
function isElementGenerallyVisible(element) {
    if (!element) return false;
  const style = window.getComputedStyle(element);
    return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && element.offsetParent !== null;
}

/**
 * Checks if an element is interactable (not disabled, readonly, etc.).
 * @param {Element} element - The DOM element.
 * @returns {boolean} True if the element is interactable.
 */
function isElementInteractable(element) {
  if (!element) return false;
    if (element.hasAttribute('disabled') || element.hasAttribute('readonly')) {
        return false;
    }
    // Consider common interactable elements
    const interactableTags = ['a', 'button', 'input', 'select', 'textarea', 'details'];
    if (interactableTags.includes(element.tagName.toLowerCase())) {
    return true;
  }
    // Check for contentEditable attribute
  if (element.isContentEditable) {
      return true;
  }
    // Check for explicit role attribute suggesting interactivity
    const role = element.getAttribute('role');
    if (role && ['button', 'link', 'checkbox', 'radio', 'tab', 'menuitem'].includes(role)) {
        return true;
    }
  return false;
}

/**
 * Extracts attributes from an element.
 * @param {Element} element - The DOM element.
 * @returns {object} A dictionary of attributes.
 */
function getElementAttributes(element) {
    const attrs = {};
  if (element.attributes) {
        for (let i = 0; i < element.attributes.length; i++) {
            const attr = element.attributes[i];
            // Limit attribute value length to prevent overly large state
            attrs[attr.name] = attr.value.length > 200 ? attr.value.substring(0, 197) + '...' : attr.value;
        }
    }
    return attrs;
}

/**
 * Generates an XPath for a given element relative to its parent's XPath.
 * This is a simplified XPath generator.
 * @param {Element} element - The DOM element.
 * @param {string} parentXPath - The XPath of the parent element.
 * @returns {string} The generated XPath for the element.
 */
function getXPathForElement(element, parentXPath) {
    if (!element || !element.parentElement) return parentXPath + '/[unknown]'; // Should ideally not happen for document children

        let index = 1;
        let sibling = element.previousElementSibling;
        while (sibling) {
            if (sibling.tagName === element.tagName) {
                index++;
            }
            sibling = sibling.previousElementSibling;
        }
    return `${parentXPath}/${element.tagName.toUpperCase()}[${index}]`;
}

// --- Initialization ---

// Send a message to the background script indicating the content script is ready
// This helps background script know when it's safe to send messages to this content script.
console.log("content.js: Attempting to send content_script_ready message to background script.");
try {
    chrome.runtime.sendMessage({ type: "content_script_ready" }, response => {
        if (chrome.runtime.lastError) {
            console.error('content.js: Error sending content_script_ready:', chrome.runtime.lastError.message);
        } else {
            console.log("content.js: Background script acknowledged content_script_ready.", response);
        }
    });
} catch (e) {
    console.error("content.js: Exception thrown while trying to send content_script_ready message:", e);
}

console.log("content.js: Script execution finished. 'content_script_ready' message has been dispatched (or attempted).");

console.log("Content script setup complete and listeners active."); 