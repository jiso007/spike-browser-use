console.log("CONTENT.JS TOP LEVEL EXECUTION - Script Start"); // VERY FIRST LINE
// browser-use-ext/extension/content.js
// Interacts with the DOM of the web page.
// Listens for messages from background.js and executes actions on the page.

// Set to true for verbose logging of element ID generation and actionability checks.
const DEBUG_ELEMENT_IDENTIFICATION = false; 
// Enables detailed logging for the element ID generation process.
// Helps in debugging how IDs are created and why certain strategies are chosen.

// Enables detailed logging for the actionability check of each element.
// Helps in understanding why an element is or is not considered actionable.
const DEBUG_ACTIONABILITY_CHECK = false; 

console.log('Content script starting initialization...'); // MODIFIED LINE to match PERPLEXITY_OUTPUT.md

// --- Global Variables & Constants ---
// Tracks IDs used in the current scan to ensure uniqueness. Cleared on each new detectActionableElements call.
let currentScanUsedIds = new Set();

// --- Message Listener for Background Script ---
/**
 * Listener for messages from the background script.
 * Handles requests like 'get_state' and 'execute_action'.
 */
/*
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Content script received message:", message);

    if (message.type === "get_state") {
        // Handles request to get the current state of the page.
        // The requestId is used to correlate responses if multiple requests are in flight.
        handleGetState(message.requestId)
            .then(response => {
                // Adding request_id to the response for background script to map.
                sendResponse({ request_id: message.requestId, ...response });
            })
            .catch(error => {
                console.error("Error in handleGetState:", error);
                sendResponse({
                    request_id: message.requestId,
                    type: "response", // Standard type for responses.
                    status: "error",
                    error: `Failed to get state: ${error.message}`
                });
            });
        return true; // Indicates that the response will be sent asynchronously.
    } else if (message.type === "execute_action") {
        // Handles request to execute an action on the page.
        // The action and its parameters are in message.payload.
        // The requestId is used for correlating responses.
        handleExecuteAction(message.payload, message.requestId) // Pass the entire payload
            .then(response => {
                 // Adding request_id to the response for background script to map.
                sendResponse({ request_id: message.requestId, ...response });
            })
            .catch(error => {
                console.error("Error in handleExecuteAction:", error);
                sendResponse({
                    request_id: message.requestId,
                    type: "response", // Standard type for responses.
                    status: "error",
                    error: `Failed to execute action \'${message.payload && message.payload.action}\': ${error.message}`
                });
            });
        return true; // Indicates that the response will be sent asynchronously.
    }
    // If message type is not recognized, return false to allow other listeners to process it.
    return false;
});
*/
// ADDED CODE based on PERPLEXITY_OUTPUT.md
let isContentScriptReady = false;
let messageListener = null;

// Establish the message listener first
function setupMessageListener() {
    if (messageListener) {
        console.warn('Message listener already established');
        return;
    }

    messageListener = function(request, sender, sendResponse) {
        console.log('Content script received message:', request);
        
        if (!isContentScriptReady) {
            console.warn('Content script received message before ready state');
            sendResponse({ error: 'Content script not ready' });
            return false; // Return false for sync response, or true if planning async for error
        }

        // Handle different message types
        switch (request.type) {
            case 'get_state':
                // Pass requestId from the original request if available
                handleGetState(request.requestId)
                    .then(response => {
                        sendResponse({ request_id: request.requestId, ...response });
                    })
                    .catch(error => {
                        console.error("Error in handleGetState:", error);
                        sendResponse({
                            request_id: request.requestId,
                            type: "response",
                            status: "error",
                            error: `Failed to get state: ${error.message}`
                        });
                    });
                return true; // Indicates async response
            case 'execute_action':
                 // Pass requestId from the original request if available
                handleExecuteAction(request.payload, request.requestId)
                    .then(response => {
                        sendResponse({ request_id: request.requestId, ...response });
                    })
                    .catch(error => {
                        console.error("Error in handleExecuteAction:", error);
                        sendResponse({
                            request_id: request.requestId,
                            type: "response",
                            status: "error",
                            error: `Failed to execute action \'${request.payload && request.payload.action}\': ${error.message}`
                        });
                    });
                return true; // Indicates async response
            case 'ping':
                sendResponse({ status: 'ready', timestamp: Date.now() });
                return false; // Synchronous response
            default:
                console.warn('Unknown message type:', request.type);
                sendResponse({ error: 'Unknown message type' });
                return false; // Synchronous response
        }
    };

    chrome.runtime.onMessage.addListener(messageListener);
    console.log('Message listener established');
}

// Send ready signal to background script
function signalContentScriptReady() {
    const maxRetries = 3;
    const baseDelay = 100; // milliseconds
    
    function attemptSignal(retryCount = 0) {
        console.log(`Attempting to signal ready state (attempt ${retryCount + 1}/${maxRetries})`);
        
        // The PERPLEXITY_OUTPUT.md shows tabId: null, but content scripts usually don't know their tabId
        // when sending to background. background.js can get it from the sender object.
        chrome.runtime.sendMessage(
            { type: "content_script_ready", timestamp: Date.now() }, 
            function(response) {
                if (chrome.runtime.lastError) {
                    console.error('Error sending ready signal:', chrome.runtime.lastError.message);
                    
                    if (retryCount < maxRetries -1 ) { // Corrected retry condition
                        const delay = baseDelay * Math.pow(2, retryCount);
                        console.log(`Retrying ready signal in ${delay}ms`);
                        setTimeout(() => attemptSignal(retryCount + 1), delay);
                    } else {
                        console.error('Failed to signal ready state after all retries');
                    }
                } else {
                    console.log('Content script ready signal acknowledged by background:', response);
                    isContentScriptReady = true;
                }
            }
        );
    }
    
    attemptSignal();
}

// Initialize content script
function initializeContentScript() {
    console.log('Initializing content script...');
    
    try {
        // Set up message handling first
        setupMessageListener();
        
        // Perform any other initialization tasks
        // ... existing initialization code ...
        // (Assuming existing initialization like unique ID generation setup, etc., remains)
        
        // Signal readiness after all setup is complete
        signalContentScriptReady();
        
    } catch (error) {
        console.error('Content script initialization failed:', error);
        // Could implement additional error recovery here
    }
}
// END ADDED CODE


// --- Enhanced Element Identification System ---

/**
 * Generates a stable and unique string ID for a given DOM element.
 * Tries multiple strategies in order of preference: unique attributes, structural position, XPath, text content.
 * Falls back to a timestamp-based ID if no other stable ID can be generated.
 * @param {HTMLElement} element - The DOM element to generate an ID for.
 * @returns {string} A string ID for the element.
 */
function generateStableElementId(element) {
    // Array of strategy functions to generate element IDs.
    // Each strategy aims to find a unique and stable identifier.
    const strategies = [
        { name: "UniqueAttributes", fn: () => generateIdByUniqueAttributes(element) },
        { name: "StructuralPosition", fn: () => generateIdByStructuralPosition(element) },
        { name: "XPath", fn: () => generateIdByXPath(element) },
        { name: "TextContent", fn: () => generateIdByTextContent(element) }
    ];

    for (const strategy of strategies) {
        const id = strategy.fn();
        // Check if the generated ID is valid and unique within the document/current scan.
        if (id && isIdUnique(id, element)) {
            if (DEBUG_ELEMENT_IDENTIFICATION) {
                console.log(`[DebugID] Element: %o, Strategy: ${strategy.name}, ID: \"${id}\"`, element);
            }
            currentScanUsedIds.add(id); // Add to used IDs for the current scan
            return id;
        }
    }

    // Fallback strategy: generate a less stable but unique ID using a timestamp and random string.
    // This is a last resort if other strategies fail.
    let fallbackIdCount = 0;
    let fallbackId;
    do {
        fallbackId = `element_${Date.now()}_${Math.random().toString(36).substr(2, 9)}_${fallbackIdCount++}`;
    } while (currentScanUsedIds.has(fallbackId) || document.querySelector(`[data-element-id=\"${fallbackId}\"]`));
    
    if (DEBUG_ELEMENT_IDENTIFICATION) {
        console.log(`[DebugID] Element: %o, Strategy: Fallback, ID: \"${fallbackId}\"`, element);
    }
    console.warn("Falling back to timestamp-based ID for element:", element, "Generated ID:", fallbackId);
    currentScanUsedIds.add(fallbackId);
    return fallbackId;
}

/**
 * Tries to generate an ID based on common unique HTML attributes.
 * Prioritizes 'id', then 'name', 'data-testid', 'aria-label'.
 * @param {HTMLElement} element - The DOM element.
 * @returns {string|null} The generated ID or null if no suitable attribute is found.
 */
function generateIdByUniqueAttributes(element) {
    const uniqueAttrs = ['id', 'name', 'data-testid', 'aria-label'];
    for (const attr of uniqueAttrs) {
        const value = element.getAttribute(attr);
        if (value && value.trim()) {
            // Sanitize value by replacing spaces and special characters to make it a valid ID part.
            const sanitizedValue = value.trim().replace(/[^a-zA-Z0-9_-]/g, '_');
            const id = `attr_${attr}_${sanitizedValue}`;
            // The isIdUnique check in generateStableElementId will handle overall uniqueness.
            return id;
        }
    }
    return null;
}

/**
 * Generates an ID based on the element's structural position in the DOM tree (tag name and index among siblings).
 * Example: struct_div[0]_p[2]_span[1]
 * @param {HTMLElement} element - The DOM element.
 * @returns {string|null} The generated ID or null if path cannot be constructed.
 */
function generateIdByStructuralPosition(element) {
    const path = [];
    let current = element;
    while (current && current.parentElement && current !== document.body) {
        const siblings = Array.from(current.parentNode.children);
        // Filter for siblings with the same tag name to get a more stable index.
        const sameTagSiblings = siblings.filter(sibling => sibling.tagName === current.tagName);
        const index = sameTagSiblings.indexOf(current);
        const tagName = current.tagName.toLowerCase();
        path.unshift(`${tagName}[${index}]`);
        current = current.parentNode;
    }
    return path.length > 0 ? `struct_${path.join('_')}` : null;
}

/**
 * Generates an XPath for the element.
 * Prefers using an existing 'id' if available for robustness.
 * @param {HTMLElement} element - The DOM element.
 * @returns {string} The generated XPath string, prefixed with "xpath_".
 */
function generateIdByXPath(element) {
    if (element.id) {
        // Using a direct ID-based XPath is the most robust.
        return `xpath_id(\"${element.id}\")`; // Standard XPath function for ID
    }

    let path = '';
    let node = element;
    while (node && node.nodeType === Node.ELEMENT_NODE && node !== document.documentElement) {
        const tagName = node.tagName.toLowerCase();
        let segment = tagName;
        const siblings = Array.from(node.parentNode.children).filter(e => e.tagName === node.tagName);
        if (siblings.length > 1) {
            const index = siblings.indexOf(node) + 1; // XPath indices are 1-based.
            segment += `[${index}]`;
        }
        path = `/${segment}${path}`;
        node = node.parentNode;
    }
    // Construct the final XPath, relative to the document root.
    const fullXPath = path ? `/${document.documentElement.tagName.toLowerCase()}${path}` : '';
    return `xpath_${fullXPath}`;
}

/**
 * Generates an ID based on a snippet of the element's text content.
 * Limits the text length and sanitizes it.
 * @param {HTMLElement} element - The DOM element.
 * @returns {string|null} The generated ID or null if no suitable text content.
 */
function generateIdByTextContent(element) {
    // Try to get text from common sources, prioritizing input values or ARIA labels.
    const textSources = [
        element.value,
        element.getAttribute('aria-label'),
        element.textContent,
        element.innerText,
        element.title,
        element.alt
    ];
    
    let text = '';
    for (const source of textSources) {
        if (source && typeof source === 'string' && source.trim()) {
            text = source.trim();
            break;
        }
    }

    if (text && text.length > 0 && text.length < 60) { // Adjusted length constraints
        // Sanitize text: keep alphanumeric, replace others with underscore, trim, and limit length.
        const sanitizedText = text.replace(/[^a-zA-Z0-9]/g, '_').replace(/__+/g, '_').substring(0, 40);
        return `text_${sanitizedText}`;
    }
    return null;
}

/**
 * Checks if a generated ID is unique in the document.
 * It considers IDs already used in the current scan and existing data-element-id attributes.
 * @param {string} id - The ID to check for uniqueness.
 * @param {HTMLElement} currentElement - The element for which the ID is being generated (to exclude itself if already marked).
 * @returns {boolean} True if the ID is unique, false otherwise.
 */
function isIdUnique(id, currentElement) {
    if (currentScanUsedIds.has(id)) {
        if (DEBUG_ELEMENT_IDENTIFICATION) console.log(`[DebugIDUniqueness] ID \"${id}\" already in currentScanUsedIds.`);
        return false;
    }
    // Check if any *other* element in the DOM already uses this ID as data-element-id
    const existingElementWithId = document.querySelector(`[data-element-id=\"${id}\"]`);
    if (existingElementWithId && existingElementWithId !== currentElement) {
        if (DEBUG_ELEMENT_IDENTIFICATION) console.log(`[DebugIDUniqueness] ID \"${id}\" already used by another element: %o`, existingElementWithId);
        return false;
    }
    return true;
}


// --- Actionable Elements Detection ---

/**
 * Detects all actionable elements on the page.
 * For each actionable element, it generates a stable ID and collects relevant metadata.
 * @returns {Array<Object>} An array of objects, each representing an actionable element.
 */
function detectActionableElements() {
    console.log("Starting detection of actionable elements...");
    currentScanUsedIds.clear(); // Clear IDs from previous scan
    const actionableElements = [];
    // Query all elements. Filtering will happen in isElementActionable.
    const allElements = document.querySelectorAll('*');
    if (DEBUG_ACTIONABILITY_CHECK) console.log(`Total elements found: ${allElements.length}`);

    for (const element of allElements) {
        if (isElementActionable(element)) {
            const elementId = generateStableElementId(element);
            // Store the generated ID on the element itself for easier resolution later.
            element.setAttribute('data-element-id', elementId);

            const elementData = {
                id: elementId,
                type: getElementType(element),
                tag: element.tagName.toLowerCase(),
                text_content: getElementTextContent(element),
                attributes: getRelevantAttributes(element),
                is_visible: isElementVisible(element), // Visibility check
                available_operations: getAvailableOperations(element)
            };
            actionableElements.push(elementData);
             if (DEBUG_ACTIONABILITY_CHECK) console.log(`[Actionable] Element: %o, Data: %o`, element, elementData);
        }
    }
    console.log(`Finished detection. Found ${actionableElements.length} actionable elements.`);
    return actionableElements;
}

/**
 * Determines if an element is actionable based on various criteria.
 * Criteria include visibility, interactivity (tag, role, event handlers), and content richness.
 * @param {HTMLElement} element - The DOM element to check.
 * @returns {boolean} True if the element is considered actionable, false otherwise.
 */
function isElementActionable(element) {
    if (!isElementVisible(element)) { // Basic visibility check first
        if (DEBUG_ACTIONABILITY_CHECK) console.log(`[NonActionable] Element not visible: %o`, element);
        return false;
    }

    const tagName = element.tagName.toLowerCase();
    const role = element.getAttribute('role');

    // Check for interactive tags
    const interactiveTags = ['a', 'button', 'input', 'select', 'textarea', 'label', 'details', 'summary', 'option'];
    if (interactiveTags.includes(tagName)) {
        if (DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Interactive tag "${tagName}": %o`, element);
        return true;
    }

    // Check for interactive ARIA roles
    const interactiveRoles = ['button', 'link', 'textbox', 'checkbox', 'radio', 'combobox', 'menuitem', 'tab', 'slider', 'spinbutton', 'treeitem'];
    if (role && interactiveRoles.includes(role)) {
         if (DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Interactive role "${role}": %o`, element);
        return true;
    }
    
    // Check for elements with explicit tabindex making them focusable
    if (element.hasAttribute('tabindex') && parseInt(element.getAttribute('tabindex'), 10) >= 0) {
        if (DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Focusable via tabindex: %o`, element);
        return true;
    }

    // Check for click handlers (more heuristic)
    // Note: This is not foolproof as handlers can be attached in many ways.
    const eventChecks = ['onclick', 'onmousedown', 'onmouseup', 'ontouchend'];
    if (eventChecks.some(event => element.hasAttribute(event) || (typeof element[event] === 'function'))) {
        if (DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Has direct event handler: %o`, element);
        return true;
    }
    
    // Check for content-rich, non-interactive elements that might be targets for text extraction or visibility checks
    const contentRichTags = ['p', 'span', 'div', 'li', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article', 'section'];
    if (contentRichTags.includes(tagName)) {
        const textContent = (element.textContent || "").trim();
        if (textContent.length >= 5 && textContent.length < 500) { // Reasonable amount of text
             if (DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Content-rich tag "${tagName}" with text: %o`, element);
            return true; // Consider it actionable for potential text scraping or context
        }
    }
    
    // Check for images with alt text (important for accessibility and context)
    if (tagName === 'img' && element.getAttribute('alt')) {
        if (DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Image with alt text: %o`, element);
        return true;
    }

    if (DEBUG_ACTIONABILITY_CHECK && isElementVisible(element)) console.log(`[NonActionable] Element passed visibility but no other criteria: %o`, element);
    return false;
}

/**
 * Determines the 'type' of an element based on its tag, attributes (type, role).
 * @param {HTMLElement} element - The DOM element.
 * @returns {string} A string representing the element type (e.g., 'link', 'button', 'text_input').
 */
function getElementType(element) {
    const tag = element.tagName.toLowerCase();
    const typeAttr = element.getAttribute('type')?.toLowerCase();
    const role = element.getAttribute('role')?.toLowerCase();

    if (tag === 'input') {
        return typeAttr || 'text'; // Default to 'text' for inputs if type is missing
    }
    if (role) return role; // ARIA role can be very descriptive

    const tagToTypeMap = {
        'a': 'link',
        'button': 'button',
        'select': 'dropdown', // or 'select'
        'textarea': 'textarea',
        'img': 'image',
        'form': 'form',
        'label': 'label',
        'h1': 'heading1', 'h2': 'heading2', 'h3': 'heading3', 'h4': 'heading4', 'h5': 'heading5', 'h6': 'heading6',
        'p': 'paragraph',
        'ul': 'unordered_list', 'ol': 'ordered_list', 'li': 'list_item',
        'table': 'table', 'tr': 'table_row', 'td': 'table_cell', 'th': 'table_header_cell',
        'div': 'div_container', // Generic container
        'span': 'text_span',   // Generic inline text container
    };
    return tagToTypeMap[tag] || tag; // Fallback to the tag name itself
}

/**
 * Gets relevant text content from an element.
 * Prioritizes value, placeholder, ARIA labels, alt text, then general textContent.
 * Limits text length to prevent overly long content.
 * @param {HTMLElement} element - The DOM element.
 * @returns {string} The extracted text content, truncated if necessary.
 */
function getElementTextContent(element) {
    let text = '';
    const tagName = element.tagName.toLowerCase();

    if (tagName === 'input' || tagName === 'textarea') {
        text = element.value || element.getAttribute('placeholder') || '';
    } else if (tagName === 'img') {
        text = element.getAttribute('alt') || element.getAttribute('title') || '';
    } else if (tagName === 'select') {
        // For select, get the text of the selected option
        const selectedOption = element.options[element.selectedIndex];
        text = selectedOption ? selectedOption.textContent.trim() : '';
    }
    
    // Fallback or supplement with ARIA label or general text content
    if (!text.trim()) {
        text = element.getAttribute('aria-label') || element.textContent || element.innerText || '';
    }
    
    text = text.trim().replace(/\\s+/g, ' '); // Normalize whitespace

    // Limit text length to a reasonable maximum
    const MAX_TEXT_LENGTH = 250;
    return text.length > MAX_TEXT_LENGTH ? text.substring(0, MAX_TEXT_LENGTH) + '...' : text;
}

/**
 * Collects relevant attributes from an element.
 * Focuses on attributes useful for identification and understanding element state.
 * @param {HTMLElement} element - The DOM element.
 * @returns {Object} An object where keys are attribute names and values are attribute values.
 */
function getRelevantAttributes(element) {
    // A curated list of attributes that are generally most informative.
    const relevantAttrs = [
        'id', 'class', 'name', 'type', 'role', 'aria-label', 'aria-labelledby', 'aria-describedby',
        'title', 'href', 'src', 'alt', 'placeholder', 'value', 'for', 'tabindex',
        'disabled', 'readonly', 'checked', 'selected', 'aria-disabled', 'aria-hidden', 'aria-expanded', 'aria-pressed'
    ];
    const attributes = {};
    for (const attr of relevantAttrs) {
        const value = element.getAttribute(attr);
        if (value !== null) { // Include attribute if it exists, even if empty string
            attributes[attr] = value;
        }
    }
    // Add custom data attributes if any, as they are often used for testing or custom behaviors.
    for (let i = 0; i < element.attributes.length; i++) {
        const attr = element.attributes[i];
        if (attr.name.startsWith('data-')) {
            attributes[attr.name] = attr.value;
        }
    }
    return attributes;
}

/**
 * Checks if an element is currently visible in the viewport.
 * Considers CSS properties like display, visibility, opacity, and element dimensions.
 * @param {HTMLElement} element - The DOM element to check.
 * @returns {boolean} True if the element is visible, false otherwise.
 */
function isElementVisible(element) {
    if (!element || !element.getBoundingClientRect) return false; // Element might not be valid or attached

    const style = window.getComputedStyle(element);
    if (style.display === 'none') return false;
    if (style.visibility === 'hidden') return false;
    if (parseFloat(style.opacity) < 0.1) return false; // Effectively invisible

    // Check dimensions - an element with zero width/height is not visible
    // Also consider elements that might be positioned off-screen
    const rect = element.getBoundingClientRect();
    if (rect.width <= 1 || rect.height <= 1) { // Allow for 1px borders/lines
        // Further check if it's genuinely content or just a collapsed placeholder
        if (!element.children.length && !(element.textContent || "").trim() && !(element.tagName.toLowerCase() === 'hr')) {
             return false;
        }
    }
    
    // Check if the element is within the viewport boundaries
    // (This part is tricky because an element can be scrollable into view)
    // For now, focusing on CSS properties and basic dimensions.
    // A more advanced check could involve intersection observers or complex geometry.

    // Check if element is obscured by an overlay (basic check)
    // Note: This is a simplified check and might not catch all overlay scenarios.
    // let point = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
    // if (point !== element && !element.contains(point)) {
    //     return false; // Another element is on top
    // }
    
    return true;
}

/**
 * Determines the available operations for an element based on its type and properties.
 * E.g., an input field might allow 'input_text', 'clear', 'click'. A link allows 'click', 'navigate'.
 * @param {HTMLElement} element - The DOM element.
 * @returns {Array<string>} An array of strings, each representing an available operation.
 */
function getAvailableOperations(element) {
    const operations = [];
    const tag = element.tagName.toLowerCase();
    const type = element.getAttribute('type')?.toLowerCase();
    const elementType = getElementType(element); // Use our derived type

    // Click is generally available for most visible, actionable elements
    if (isElementVisible(element)) { // Re-check visibility for safety
        operations.push('click');
    }

    // Input-related operations
    if (tag === 'input' || tag === 'textarea') {
        if (!element.disabled && !element.readOnly) {
            if (type === 'checkbox' || type === 'radio' || elementType === 'checkbox' || elementType === 'radio') {
                operations.push('check', 'uncheck'); // More specific than just 'click' for checkboxes/radios
            } else if (type !== 'submit' && type !== 'button' && type !== 'reset' && type !== 'image') {
                operations.push('input_text', 'clear');
            }
        }
    }

    // Select/Dropdown operations
    if (tag === 'select' && !element.disabled) {
        operations.push('select_option');
    }

    // Navigation for links
    if (tag === 'a' && element.getAttribute('href')) {
        operations.push('navigate');
    }

    // Scroll operations (element itself or document)
    if (element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth) {
        operations.push('scroll_element'); // Scroll the element itself
    }
    operations.push('scroll_window'); // Always offer window scroll

    // Hover is generally available
    operations.push('hover');
    
    // Focus/Blur
    operations.push('focus', 'blur');

    // Get text, attributes
    operations.push('get_text', 'get_attributes');

    return [...new Set(operations)]; // Return unique operations
}


// --- State Handling ---

/**
 * Handles the 'get_state' message from the background script.
 * Collects page URL, title, viewport info, scroll position, and detailed actionable element data.
 * @param {string} requestId - The ID of the request, for correlating responses.
 * @returns {Promise<Object>} A promise that resolves with the page state object.
 */
async function handleGetState(requestId) {
    console.log(`handleGetState called for requestId: ${requestId}`);
    try {
        const actionableElements = detectActionableElements(); // This is the core new part

        const pageState = {
            // requestId: requestId, // requestId is now added by the caller in onMessage
            type: "state_response", // Consistent response type
            status: "success",
            state: { // Nest actual state data under a 'state' key
                url: window.location.href,
                title: document.title,
                viewport: {
                    width: window.innerWidth,
                    height: window.innerHeight,
                    pixel_ratio: window.devicePixelRatio || 1.0
                },
                scroll_position: {
                    x: window.scrollX,
                    y: window.scrollY,
                    max_x: document.documentElement.scrollWidth - window.innerWidth,
                    max_y: document.documentElement.scrollHeight - window.innerHeight
                },
                document_dimensions: {
                    width: document.documentElement.scrollWidth,
                    height: document.documentElement.scrollHeight
                },
                actionable_elements: actionableElements,
                page_metrics: {
                    total_elements_on_page: document.querySelectorAll('*').length,
                    actionable_elements_count: actionableElements.length,
                    visible_actionable_elements_count: actionableElements.filter(el => el.is_visible).length,
                    dom_load_time: window.performance && window.performance.timing ? (window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart) : -1,
                    page_load_time: window.performance && window.performance.timing ? (window.performance.timing.loadEventEnd - window.performance.timing.navigationStart) : -1,
                },
                timestamp: new Date().toISOString()
            }
        };
        console.log(`State extracted successfully for requestId: ${requestId}. ${actionableElements.length} actionable elements found.`);
        return pageState;
    } catch (error) {
        console.error(`Error extracting page state for requestId ${requestId}:`, error);
        // Structure the error response consistently
        return {
            // requestId: requestId,
            type: "state_response",
            status: "error",
            error: `Error extracting page state: ${error.message}`,
            details: error.stack // Optional: include stack for debugging
        };
    }
}

// --- Action Execution System ---

/**
 * Resolves an element by its string ID.
 * First tries querying by 'data-element-id', then attempts to use ID strategy prefixes.
 * @param {string} elementId - The string ID of the element.
 * @returns {HTMLElement|null} The resolved DOM element or null if not found.
 * @throws {Error} If elementId is not provided.
 */
function resolveElementById(elementId) {
    if (!elementId || typeof elementId !== 'string') {
        console.error('resolveElementById: elementId is required and must be a string. Received:', elementId);
        throw new Error('Element ID is required and must be a string.');
    }
    if (DEBUG_ELEMENT_IDENTIFICATION) console.log(`Resolving element by ID: "${elementId}"`);

    // Primary method: Query by the 'data-element-id' attribute we set.
    let element = document.querySelector(`[data-element-id="${elementId}"]`);
    if (element) {
        if (DEBUG_ELEMENT_IDENTIFICATION) console.log(`Element found by data-element-id: %o`, element);
        return element;
    }

    // Fallback strategies based on ID prefix, if data-element-id fails (e.g., element was re-rendered without our attribute)
    if (DEBUG_ELEMENT_IDENTIFICATION) console.log(`Element not found by data-element-id. Trying prefix strategies for ID: "${elementId}"`);
    
    if (elementId.startsWith('attr_id_')) { // Specifically for 'id' attribute
        const idValue = elementId.substring('attr_id_'.length);
        element = document.getElementById(idValue);
         if (DEBUG_ELEMENT_IDENTIFICATION && element) console.log(`Element found by getElementById for attr_id_: %o`, element);
    } else if (elementId.startsWith('xpath_')) {
        const xpath = elementId.substring('xpath_'.length);
        try {
            element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (DEBUG_ELEMENT_IDENTIFICATION && element) console.log(`Element found by XPath: %o`, element);
        } catch (e) {
            console.error(`Error evaluating XPath "${xpath}":`, e);
            element = null;
        }
    } else if (elementId.startsWith('struct_')) {
        element = resolveStructuralPath(elementId);
        if (DEBUG_ELEMENT_IDENTIFICATION && element) console.log(`Element found by structural path: %o`, element);
    } else if (elementId.startsWith('text_')) {
        // This is less reliable as text can change or be non-unique.
        // Consider if this fallback is too risky or should be more constrained.
        element = resolveByTextContent(elementId.substring("text_".length));
         if (DEBUG_ELEMENT_IDENTIFICATION && element) console.log(`Element found by text content: %o`, element);
    }
    
    if (!element && DEBUG_ELEMENT_IDENTIFICATION) {
        console.warn(`Element with ID "${elementId}" could not be resolved by any strategy.`);
    }
    return element;
}

/**
 * Helper to resolve an element based on a structural path ID.
 * @param {string} elementId - The structural ID (e.g., "struct_div[0]_p[1]").
 * @returns {HTMLElement|null} The resolved element or null.
 */
function resolveStructuralPath(elementId) {
    const pathString = elementId.substring("struct_".length);
    const segments = pathString.split('_');
    let currentElement = document.body;

    for (const segment of segments) {
        const match = segment.match(/^([a-z0-9]+)\[(\d+)\]$/i); // Tag name and index
        if (!match || !currentElement) return null;

        const [, tagName, indexStr] = match;
        const index = parseInt(indexStr, 10);
        
        const childrenWithTag = Array.from(currentElement.children).filter(
            child => child.tagName.toLowerCase() === tagName
        );

        if (index < 0 || index >= childrenWithTag.length) return null; // Index out of bounds
        currentElement = childrenWithTag[index];
    }
    // Ensure the final resolved element is not the body itself unless it was the only segment
    return (currentElement === document.body && segments.length > 0) ? null : currentElement;
}

/**
 * Helper to resolve an element based on a text content ID.
 * This is generally less reliable due to potential text non-uniqueness or changes.
 * @param {string} elementId - The text-based ID (e.g., "text_Submit_Button").
 * @returns {HTMLElement|null} The resolved element or null.
 */
function resolveByTextContent(elementId) {
    const textKey = elementId.replace(/_/g, ' '); // Restore spaces
    const elements = Array.from(document.querySelectorAll('*')); // Search all elements
    
    // Prioritize exact matches, then case-insensitive, then contains.
    // Also prefer elements where this text is more unique or prominent.
    for (const el of elements) {
        const elTextContent = (el.textContent || "").trim();
        const elValue = (el.value || "").trim();
        const elAriaLabel = (el.getAttribute('aria-label') || "").trim();

        if (elTextContent === textKey || elValue === textKey || elAriaLabel === textKey) return el;
    }
    // Fallback to case-insensitive contains (could be broader)
    const lowerTextKey = textKey.toLowerCase();
    for (const el of elements) {
         if (isElementVisible(el)) { // Only consider visible elements for text search
            const elTextContentLower = (el.textContent || "").trim().toLowerCase();
            const elValueLower = (el.value || "").trim().toLowerCase();
            const elAriaLabelLower = (el.getAttribute('aria-label') || "").trim().toLowerCase();
            if (elTextContentLower.includes(lowerTextKey) || elValueLower.includes(lowerTextKey) || elAriaLabelLower.includes(lowerTextKey)) {
                 // This could return many elements. Consider returning the first visible one or one with more specific tags.
                return el;
            }
        }
    }
    return null;
}

/**
 * Handles the 'execute_action' message.
 * Resolves the target element using its string ID and executes the specified action.
 * @param {Object} payload - The action payload containing 'action' (string) and 'params' (object).
 *                           'params' must include 'element_id'.
 * @param {string} requestId - The ID of the request for response correlation.
 * @returns {Promise<Object>} A promise that resolves with the action result (success/failure, messages).
 */
async function handleExecuteAction(payload, requestId) {
    console.log(`handleExecuteAction called for requestId: ${requestId}, Payload:`, payload);
    const { action, params } = payload;

    if (!params || !params.element_id) {
        if (action !== 'scroll_window' && action !== 'navigate_to_url') { // These actions might not need element_id
            console.error("Action execution failed: element_id is missing in params.", params);
            return { status: "error", error: `Element ID is required for action '${action}'.` };
        }
    }
    
    try {
        let element = null;
        // Some actions operate on the window or don't need a specific element
        if (action !== 'scroll_window' && action !== 'navigate_to_url' && params.element_id) {
            element = resolveElementById(params.element_id);
            if (!element) {
                return { status: "error", error: `Element with ID '${params.element_id}' not found or no longer exists.` };
            }
             // Ensure element is visible and interactable before acting (unless action is like 'get_text')
            if (!isElementVisible(element) && !['get_text', 'get_attributes', 'scroll_element'].includes(action)) {
                 console.warn(`Action '${action}' on non-visible element ID '${params.element_id}'. Proceeding cautiously.`);
                 // return { status: "error", error: `Element with ID '${params.element_id}' is not visible.` };
            }
        }

        let result;
        // Generalized action names (removed "_by_index" convention)
        switch (action) {
            case 'click':
                result = await executeClick(element, params); // Made async for potential waits
                break;
            case 'input_text':
                result = executeInputText(element, params);
                break;
            case 'clear':
                result = executeClear(element, params);
                break;
            case 'select_option':
                result = executeSelectOption(element, params);
                break;
            case 'scroll_element': // For scrolling a specific element
                result = executeScroll(element, params);
                break;
            case 'scroll_window': // For scrolling the main window
                result = executeScroll(window, params); // Pass window as target
                break;
            case 'hover':
                result = executeHover(element, params);
                break;
            case 'check':
            case 'uncheck':
                result = executeCheckbox(element, params, action === 'check');
                break;
            case 'navigate': // Assumes element is a link, action navigates by clicking it
                result = executeNavigateByClick(element, params);
                break;
            case 'navigate_to_url': // New action for direct navigation
                result = executeNavigateToUrl(params);
                break;
            case 'focus':
                result = executeFocus(element, params);
                break;
            case 'blur':
                result = executeBlur(element, params);
                break;
            case 'get_text':
                result = executeGetText(element, params);
                break;
            case 'get_attributes':
                result = executeGetAttributes(element, params);
                break;
            // TODO: Add cases for 'upload_file' if needed (complex, involves file inputs)
            default:
                return { status: "error", error: `Unknown action: ${action}` };
        }
        return { status: "success", result: result }; // Consistent success response structure
    } catch (error) {
        console.error(`Error executing action '${action}' for requestId ${requestId}:`, error);
        return { status: "error", error: error.message, details: error.stack };
    }
}


// --- Individual Action Handlers ---
// These functions now accept the resolved DOM element directly.

async function executeClick(element, params) {
    if (!element || typeof element.click !== 'function') {
        return { success: false, error: 'Element is not clickable or not found.' };
    }
    try {
        // Scroll into view if not fully visible, helps with elements obscured or off-screen.
        element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
        
        // Wait a brief moment for scroll to complete and element to be interactable.
        // This is a common trick to improve reliability of clicks after scrolling.
        await new Promise(resolve => setTimeout(resolve, 150)); 

        element.focus(); // Focus before clicking can help in some cases
        await new Promise(resolve => setTimeout(resolve, 50)); 

        element.click();
        console.log(`Clicked element:`, element, `Params:`, params);
        return { success: true, message: `Clicked element (Tag: ${element.tagName}, ID: ${element.getAttribute('data-element-id')})` };
    } catch (error) {
        console.error('Failed to click element:', element, 'Error:', error);
        return { success: false, error: `Failed to click element: ${error.message}` };
    }
}

function executeInputText(element, params) {
    if (!element || typeof element.focus !== 'function' || typeof element.select === "function" && element.disabled || element.readOnly) {
        return { success: false, error: 'Element is not an interactable input/textarea or not found.' };
    }
    try {
        const { text, append = false } = params;
        if (typeof text !== 'string') {
            return { success: false, error: 'Text parameter must be a string.' };
        }
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        element.focus();
        
        if (append) {
            element.value += text;
        } else {
            // Some applications react better if existing text is selected and then replaced
            if (typeof element.select === "function") element.select(); 
            element.value = text;
        }
        
        // Trigger common events to simulate user input behavior for reactive frameworks.
        element.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
        element.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
        console.log(`Input text "${text}" into element:`, element);
        return { success: true, message: `Input text: "${text}" into element (Tag: ${element.tagName})` };
    } catch (error) {
        console.error('Failed to input text:', error);
        return { success: false, error: `Failed to input text: ${error.message}` };
    }
}

function executeClear(element, params) {
     if (!element || typeof element.focus !== 'function' || typeof element.value === 'undefined' || element.disabled || element.readOnly) {
        return { success: false, error: 'Element cannot be cleared (not an input/textarea, or disabled/readonly).' };
    }
    try {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        element.focus();
        element.value = '';
        element.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
        element.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
        console.log('Cleared element content:', element);
        return { success: true, message: 'Cleared element content.' };
    } catch (error) {
        console.error('Failed to clear element:', error);
        return { success: false, error: `Failed to clear element: ${error.message}` };
    }
}

function executeSelectOption(element, params) {
    if (!element || element.tagName.toLowerCase() !== 'select' || element.disabled) {
        return { success: false, error: 'Element is not a non-disabled select dropdown or not found.' };
    }
    try {
        const { option_value, option_text } = params; // Allow selecting by value or text
        if (!option_value && !option_text) {
            return { success: false, error: 'Either option_value or option_text parameter is required for select_option.' };
        }

        let targetOptionFound = false;
        for (let i = 0; i < element.options.length; i++) {
            const opt = element.options[i];
            if ((option_value && opt.value === option_value) || (option_text && opt.text.trim() === option_text.trim())) {
                element.selectedIndex = i;
                targetOptionFound = true;
                break;
            }
        }

        if (!targetOptionFound) {
            return { success: false, error: `Option matching "${option_value || option_text}" not found.` };
        }
        
        element.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
        console.log(`Selected option "${option_value || option_text}" in element:`, element);
        return { success: true, message: `Selected option: "${element.options[element.selectedIndex].text}"` };
    } catch (error) {
        console.error('Failed to select option:', error);
        return { success: false, error: `Failed to select option: ${error.message}` };
    }
}

/**
 * Scrolls an element or the window.
 * @param {HTMLElement|Window} scrollTarget - The element to scroll, or window object.
 * @param {Object} params - Scroll parameters (direction, amount).
 */
function executeScroll(scrollTarget, params) {
    try {
        // Default to scrolling down by a moderate amount if not specified
        const { direction = 'down', amount = 300, behavior = 'smooth' } = params;
        let scrollOptions = { behavior };

        if (direction === 'to_coordinates' && params.x !== undefined && params.y !== undefined) {
            scrollOptions.left = parseInt(params.x, 10);
            scrollOptions.top = parseInt(params.y, 10);
        } else {
            const scrollAmount = parseInt(amount, 10) || 300;
            switch (direction) {
                case 'down': scrollOptions.top = scrollAmount; break;
                case 'up': scrollOptions.top = -scrollAmount; break;
                case 'left': scrollOptions.left = -scrollAmount; break;
                case 'right': scrollOptions.left = scrollAmount; break;
                case 'top_of_page': scrollOptions.top = 0; scrollOptions.left = 0; break; // For window
                case 'bottom_of_page': // For window
                    if (scrollTarget === window) scrollOptions.top = document.body.scrollHeight;
                    else scrollOptions.top = scrollTarget.scrollHeight; // For element
                    break;
                case 'element_into_view': // Special case if scrollTarget is an element
                     if (scrollTarget !== window) {
                        scrollTarget.scrollIntoView({ behavior, block: params.block || 'center', inline: params.inline || 'nearest' });
                        return { success: true, message: `Scrolled element into view.`};
                    } else {
                        return { success: false, error: `Cannot use 'element_into_view' with window scroll.`};
                    }
                default: return { success: false, error: `Invalid scroll direction: ${direction}` };
            }
        }
        
        if (scrollTarget === window) {
            window.scrollBy(scrollOptions);
        } else {
            scrollTarget.scrollBy(scrollOptions);
        }
        
        console.log(`Scrolled ${scrollTarget === window ? 'window' : 'element'} with options:`, scrollOptions);
        return { success: true, message: `Scrolled ${scrollTarget === window ? 'window' : 'element'} ${direction || ''} ${amount || ''}px.` };
    } catch (error) {
        console.error('Failed to scroll:', error);
        return { success: false, error: `Failed to scroll: ${error.message}` };
    }
}

function executeHover(element, params) {
     if (!element || typeof element.dispatchEvent !== 'function') {
        return { success: false, error: 'Element is not valid or cannot dispatch events.' };
    }
    try {
        // Create and dispatch 'mouseover' and 'mouseenter' events for comprehensive hover simulation.
        const mouseOverEvent = new MouseEvent('mouseover', { bubbles: true, cancelable: true, view: window });
        const mouseEnterEvent = new MouseEvent('mouseenter', { bubbles: true, cancelable: true, view: window });
        element.dispatchEvent(mouseOverEvent);
        element.dispatchEvent(mouseEnterEvent);
        console.log('Hovered over element:', element);
        return { success: true, message: 'Hovered over element.' };
    } catch (error) {
        console.error('Failed to hover over element:', error);
        return { success: false, error: `Failed to hover: ${error.message}` };
    }
}

function executeCheckbox(element, params, shouldCheck) {
    if (!element || element.tagName.toLowerCase() !== 'input' || (element.type !== 'checkbox' && element.type !== 'radio') || element.disabled) {
        return { success: false, error: 'Element is not a non-disabled checkbox/radio or not found.' };
    }
    try {
        if (element.checked === shouldCheck) {
            return { success: true, message: `Element is already ${shouldCheck ? 'checked' : 'unchecked'}.` };
        }
        element.checked = shouldCheck;
        // Clicking might be more robust for some frameworks than just setting .checked
        element.click(); 
        // Dispatch change event as click() might not always do it consistently for programmatic changes
        element.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
        console.log(`${shouldCheck ? 'Checked' : 'Unchecked'} element:`, element);
        return { success: true, message: `${shouldCheck ? 'Checked' : 'Unchecked'} element.` };
    } catch (error) {
        console.error(`Failed to ${shouldCheck ? 'check' : 'uncheck'} element:`, error);
        return { success: false, error: `Failed to ${shouldCheck ? 'check' : 'uncheck'} element: ${error.message}` };
    }
}

/**
 * Navigates by clicking an element (typically an <a> tag).
 */
function executeNavigateByClick(element, params) {
    if (!element || typeof element.click !== 'function') {
        return { success: false, error: 'Element is not clickable for navigation or not found.' };
    }
    try {
        const href = element.getAttribute('href');
        // For links, it's often better to just click them.
        element.click();
        console.log(`Navigating by clicking element (href: ${href || 'N/A'}):`, element);
        return { success: true, message: `Attempted navigation by clicking element. Target: ${href || 'JavaScript action'}` };
    } catch (error) {
        console.error('Failed to navigate by click:', error);
        return { success: false, error: `Failed to navigate by click: ${error.message}` };
    }
}

/**
 * Navigates the current tab to a specified URL.
 */
function executeNavigateToUrl(params) {
    const { url } = params;
    if (!url || typeof url !== 'string') {
        return { success: false, error: 'URL parameter is required and must be a string for navigate_to_url.' };
    }
    try {
        window.location.href = url;
        console.log(`Navigating to URL: ${url}`);
        // Note: This will cause the content script to potentially reload.
        // The response might not be received by the sender if the page changes too quickly.
        // Consider if any message needs to be sent *before* changing location.
        return { success: true, message: `Navigation initiated to: ${url}` };
    } catch (error) {
        console.error('Failed to navigate to URL:', error);
        return { success: false, error: `Failed to navigate to URL: ${error.message}` };
    }
}


function executeFocus(element, params) {
    if (!element || typeof element.focus !== 'function') {
        return { success: false, error: 'Element is not focusable or not found.' };
    }
    try {
        element.focus();
        console.log('Focused element:', element);
        return { success: true, message: 'Element focused.' };
    } catch (error) {
        console.error('Failed to focus element:', error);
        return { success: false, error: `Failed to focus element: ${error.message}` };
    }
}

function executeBlur(element, params) {
    if (!element || typeof element.blur !== 'function') {
        return { success: false, error: 'Element is not blurrable or not found.' };
    }
    try {
        element.blur();
        console.log('Blurred element:', element);
        return { success: true, message: 'Element blurred.' };
    } catch (error) {
        console.error('Failed to blur element:', error);
        return { success: false, error: `Failed to blur element: ${error.message}` };
    }
}

function executeGetText(element, params) {
    if (!element) {
        return { success: false, error: 'Element not found for get_text.' };
    }
    try {
        const text = getElementTextContent(element); // Use our helper for consistent text extraction
        console.log('Retrieved text from element:', element, 'Text:', text);
        return { success: true, message: 'Text retrieved.', data: text };
    } catch (error) {
        console.error('Failed to get text from element:', error);
        return { success: false, error: `Failed to get text: ${error.message}` };
    }
}

function executeGetAttributes(element, params) {
     if (!element) {
        return { success: false, error: 'Element not found for get_attributes.' };
    }
    try {
        const attributes = getRelevantAttributes(element); // Use our helper
        console.log('Retrieved attributes from element:', element, 'Attributes:', attributes);
        return { success: true, message: 'Attributes retrieved.', data: attributes };
    } catch (error) {
        console.error('Failed to get attributes from element:', error);
        return { success: false, error: `Failed to get attributes: ${error.message}` };
    }
}



// --- Initialization and Signalling Readiness ---

/**
 * Sends a message to the background script indicating that the content script is loaded and ready.
 * This is crucial for the two-way handshake to prevent errors when the background script
 * tries to message a content script that hasn't fully initialized its listeners.
 */
async function signalReadyToBackground() {
    // This function seems to be a leftover or an alternative implementation attempt.
    // The PERPLEXITY_OUTPUT.md details a `signalContentScriptReady` function, which has been implemented above.
    // To avoid conflicts and align with the plan, this function will be commented out or removed.
    /*
    console.log("content.js: Attempting to send content_script_ready message (from signalReadyToBackground).");
    try {
        const response = await chrome.runtime.sendMessage({ type: "content_script_ready" });
        // console.log("content.js: Background acked content_script_ready:", response);
    } catch (error) {
        if (error.message.includes("Receiving end does not exist")) {
            console.warn("content.js: Background script not ready yet for content_script_ready signal. This might be okay if background initializes slower.");
        } else {
            console.error('content.js: Error sending content_script_ready (from signalReadyToBackground):', error.message);
        }
    }
    */
}

// ADDED CODE based on PERPLEXITY_OUTPUT.md
// Start initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeContentScript);
} else {
    initializeContentScript();
}

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    console.log('Content script cleaning up...');
    // Resetting ready state. If the script is re-injected on a new page, it will re-initialize.
    isContentScriptReady = false; 
    // It's also good practice to remove the listener if the script instance is truly being destroyed
    // and not just for a page navigation where it might be re-used or re-injected.
    // However, typical content script lifecycle means it's unloaded with the page.
    // if (messageListener && chrome.runtime.onMessage.hasListener(messageListener)) {
    //     chrome.runtime.onMessage.removeListener(messageListener);
    //     console.log('Message listener removed during cleanup.');
    //     messageListener = null;
    // }
});
// END ADDED CODE

console.log("Content script initialized and message listener added. Ready signal will be sent.");
// Ensure this log appears. If not, the script might be crashing before this point.
