// browser-use-ext/extension/content.modular.js
// Modular version of content.js that can be tested with Jest

// Check if we're in a browser or Node.js environment
const isBrowser = typeof chrome !== 'undefined' && chrome.runtime;

// Check if we're in a test environment
const isTestEnvironment = typeof process !== 'undefined' && process.env.NODE_ENV === 'test';

// Module state
const state = {
    currentScanUsedIds: new Set(),
    messageListener: null,
    DEBUG_ELEMENT_IDENTIFICATION: false,
    DEBUG_ACTIONABILITY_CHECK: false
};

// Export console log for testing
if (!isBrowser && typeof global !== 'undefined') {
    global.console = global.console || {
        log: () => {},
        error: () => {},
        warn: () => {}
    };
}

// Content Script Ready Signal
function signalReadyToBackground() {
    console.log("CONTENT.JS: Attempting to send content_script_ready message.");
    if (isBrowser && chrome.runtime.sendMessage) {
        chrome.runtime.sendMessage({ type: "content_script_ready" }, _response => {
            if (chrome.runtime.lastError) {
                console.error('CONTENT.JS: Error sending content_script_ready:', chrome.runtime.lastError.message);
            } else {
                console.log("CONTENT.JS: Successfully sent content_script_ready.");
            }
        });
    } else {
        console.log("CONTENT.JS: Not in browser environment, skipping ready signal");
    }
}

// Element ID generation strategies
function generateStableElementId(element) {
    const strategies = [
        { name: "UniqueAttributes", fn: () => generateIdByUniqueAttributes(element) },
        { name: "StructuralPosition", fn: () => generateIdByStructuralPosition(element) },
        { name: "XPath", fn: () => generateIdByXPath(element) },
        { name: "TextContent", fn: () => generateIdByTextContent(element) }
    ];

    for (const strategy of strategies) {
        const id = strategy.fn();
        if (id && isIdUnique(id, element)) {
            if (state.DEBUG_ELEMENT_IDENTIFICATION) {
                console.log(`[DebugID] Element: %o, Strategy: ${strategy.name}, ID: "${id}"`, element);
            }
            state.currentScanUsedIds.add(id);
            return id;
        }
    }

    // Fallback strategy
    let fallbackIdCount = 0;
    let fallbackId;
    do {
        fallbackId = `element_${Date.now()}_${Math.random().toString(36).substr(2, 9)}_${fallbackIdCount++}`;
    } while (state.currentScanUsedIds.has(fallbackId) || (isBrowser && document.querySelector(`[data-element-id="${fallbackId}"]`)));
    
    if (state.DEBUG_ELEMENT_IDENTIFICATION) {
        console.log(`[DebugID] Element: %o, Strategy: Fallback, ID: "${fallbackId}"`, element);
    }
    console.warn("Falling back to timestamp-based ID for element:", element, "Generated ID:", fallbackId);
    state.currentScanUsedIds.add(fallbackId);
    return fallbackId;
}

function generateIdByUniqueAttributes(element) {
    const uniqueAttrs = ['id', 'name', 'data-testid', 'aria-label'];
    for (const attr of uniqueAttrs) {
        const value = element.getAttribute(attr);
        if (value && value.trim()) {
            const sanitizedValue = value.trim().replace(/[^a-zA-Z0-9_-]/g, '_');
            const id = `attr_${attr}_${sanitizedValue}`;
            return id;
        }
    }
    return null;
}

function generateIdByStructuralPosition(element) {
    const path = [];
    let current = element;
    const documentBody = isBrowser ? document.body : null;
    
    while (current && current.parentElement && current !== documentBody) {
        const siblings = Array.from(current.parentNode.children);
        const sameTagSiblings = siblings.filter(sibling => sibling.tagName === current.tagName);
        const index = sameTagSiblings.indexOf(current);
        const tagName = current.tagName.toLowerCase();
        path.unshift(`${tagName}[${index}]`);
        current = current.parentNode;
    }
    return path.length > 0 ? `struct_${path.join('_')}` : null;
}

function generateIdByXPath(element) {
    if (element.id) {
        return `xpath_id("${element.id}")`;
    }

    let path = '';
    let node = element;
    const documentElement = isBrowser ? document.documentElement : { tagName: 'HTML' };
    
    while (node && node.nodeType === 1 && node !== documentElement) {
        const tagName = node.tagName.toLowerCase();
        let segment = tagName;
        const siblings = Array.from(node.parentNode.children).filter(e => e.tagName === node.tagName);
        if (siblings.length > 1) {
            const index = siblings.indexOf(node) + 1;
            segment += `[${index}]`;
        }
        path = `/${segment}${path}`;
        node = node.parentNode;
    }
    const fullXPath = path ? `/${documentElement.tagName.toLowerCase()}${path}` : '';
    return `xpath_${fullXPath}`;
}

function generateIdByTextContent(element) {
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

    if (text && text.length > 0 && text.length < 60) {
        const sanitizedText = text.replace(/[^a-zA-Z0-9]/g, '_').replace(/__+/g, '_').substring(0, 40);
        return `text_${sanitizedText}`;
    }
    return null;
}

function isIdUnique(id, currentElement) {
    if (state.currentScanUsedIds.has(id)) {
        if (state.DEBUG_ELEMENT_IDENTIFICATION) console.log(`[DebugIDUniqueness] ID "${id}" already in currentScanUsedIds.`);
        return false;
    }
    
    if (isBrowser) {
        const existingElementWithId = document.querySelector(`[data-element-id="${id}"]`);
        if (existingElementWithId && existingElementWithId !== currentElement) {
            if (state.DEBUG_ELEMENT_IDENTIFICATION) console.log(`[DebugIDUniqueness] ID "${id}" already used by another element: %o`, existingElementWithId);
            return false;
        }
    }
    
    return true;
}

// Actionable element detection
function isElementVisible(element) {
    if (!element || !element.getBoundingClientRect) return false;

    if (isBrowser) {
        const style = window.getComputedStyle(element);
        if (style.display === 'none') return false;
        if (style.visibility === 'hidden') return false;
        if (parseFloat(style.opacity) < 0.1) return false;
    }

    const rect = element.getBoundingClientRect();
    if (rect.width <= 1 || rect.height <= 1) {
        if (!element.children.length && !(element.textContent || "").trim() && !(element.tagName.toLowerCase() === 'hr')) {
            return false;
        }
    }
    
    return true;
}

function isElementActionable(element) {
    if (!isElementVisible(element)) {
        if (state.DEBUG_ACTIONABILITY_CHECK) console.log(`[NonActionable] Element not visible: %o`, element);
        return false;
    }

    const tagName = element.tagName.toLowerCase();
    const role = element.getAttribute('role');

    const interactiveTags = ['a', 'button', 'input', 'select', 'textarea', 'label', 'details', 'summary', 'option'];
    if (interactiveTags.includes(tagName)) {
        if (state.DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Interactive tag "${tagName}": %o`, element);
        return true;
    }

    const interactiveRoles = ['button', 'link', 'textbox', 'checkbox', 'radio', 'combobox', 'menuitem', 'tab', 'slider', 'spinbutton', 'treeitem'];
    if (role && interactiveRoles.includes(role)) {
         if (state.DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Interactive role "${role}": %o`, element);
        return true;
    }
    
    if (element.hasAttribute('tabindex') && parseInt(element.getAttribute('tabindex'), 10) >= 0) {
        if (state.DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Focusable via tabindex: %o`, element);
        return true;
    }

    const eventChecks = ['onclick', 'onmousedown', 'onmouseup', 'ontouchend'];
    if (eventChecks.some(event => element.hasAttribute(event) || (typeof element[event] === 'function'))) {
        if (state.DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Has direct event handler: %o`, element);
        return true;
    }
    
    const contentRichTags = ['p', 'span', 'div', 'li', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article', 'section'];
    if (contentRichTags.includes(tagName)) {
        const textContent = (element.textContent || "").trim();
        if (textContent.length >= 5 && textContent.length < 500) {
             if (state.DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Content-rich tag "${tagName}" with text: %o`, element);
            return true;
        }
    }
    
    if (tagName === 'img' && element.getAttribute('alt')) {
        if (state.DEBUG_ACTIONABILITY_CHECK) console.log(`[ActionableReason] Image with alt text: %o`, element);
        return true;
    }

    if (state.DEBUG_ACTIONABILITY_CHECK && isElementVisible(element)) console.log(`[NonActionable] Element passed visibility but no other criteria: %o`, element);
    return false;
}

function getElementType(element) {
    const tag = element.tagName.toLowerCase();
    const typeAttr = element.getAttribute('type')?.toLowerCase();
    const role = element.getAttribute('role')?.toLowerCase();

    if (tag === 'input') {
        return typeAttr || 'text';
    }
    if (role) return role;

    const tagToTypeMap = {
        'a': 'link',
        'button': 'button',
        'select': 'dropdown',
        'textarea': 'textarea',
        'img': 'image',
        'form': 'form',
        'label': 'label',
        'h1': 'heading1', 'h2': 'heading2', 'h3': 'heading3', 'h4': 'heading4', 'h5': 'heading5', 'h6': 'heading6',
        'p': 'paragraph',
        'ul': 'unordered_list', 'ol': 'ordered_list', 'li': 'list_item',
        'table': 'table', 'tr': 'table_row', 'td': 'table_cell', 'th': 'table_header_cell',
        'div': 'div_container',
        'span': 'text_span',
    };
    return tagToTypeMap[tag] || tag;
}

function getElementTextContent(element) {
    let text = '';
    const tagName = element.tagName.toLowerCase();

    if (tagName === 'input' || tagName === 'textarea') {
        text = element.value || element.getAttribute('placeholder') || '';
    } else if (tagName === 'img') {
        text = element.getAttribute('alt') || element.getAttribute('title') || '';
    } else if (tagName === 'select') {
        const selectedOption = element.options[element.selectedIndex];
        text = selectedOption ? selectedOption.textContent.trim() : '';
    }
    
    if (!text.trim()) {
        text = element.getAttribute('aria-label') || element.textContent || element.innerText || '';
    }
    
    text = text.trim().replace(/\\s+/g, ' ');

    const MAX_TEXT_LENGTH = 250;
    return text.length > MAX_TEXT_LENGTH ? text.substring(0, MAX_TEXT_LENGTH) + '...' : text;
}

function getRelevantAttributes(element) {
    const relevantAttrs = [
        'id', 'class', 'name', 'type', 'role', 'aria-label', 'aria-labelledby', 'aria-describedby',
        'title', 'href', 'src', 'alt', 'placeholder', 'value', 'for', 'tabindex',
        'disabled', 'readonly', 'checked', 'selected', 'aria-disabled', 'aria-hidden', 'aria-expanded', 'aria-pressed'
    ];
    const attributes = {};
    for (const attr of relevantAttrs) {
        const value = element.getAttribute(attr);
        if (value !== null) {
            attributes[attr] = value;
        }
    }
    
    for (let i = 0; i < element.attributes.length; i++) {
        const attr = element.attributes[i];
        if (attr.name.startsWith('data-')) {
            attributes[attr.name] = attr.value;
        }
    }
    return attributes;
}

function getAvailableOperations(element) {
    const operations = [];
    const tag = element.tagName.toLowerCase();
    const type = element.getAttribute('type')?.toLowerCase();
    const elementType = getElementType(element);

    if (isElementVisible(element)) {
        operations.push('click');
    }

    if (tag === 'input' || tag === 'textarea') {
        if (!element.disabled && !element.readOnly) {
            if (type === 'checkbox' || type === 'radio' || elementType === 'checkbox' || elementType === 'radio') {
                operations.push('check', 'uncheck');
            } else if (type !== 'submit' && type !== 'button' && type !== 'reset' && type !== 'image') {
                operations.push('input_text', 'clear');
            }
        }
    }

    if (tag === 'select' && !element.disabled) {
        operations.push('select_option');
    }

    if (tag === 'a' && element.getAttribute('href')) {
        operations.push('navigate');
    }

    if (element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth) {
        operations.push('scroll_element');
    }
    operations.push('scroll_window');

    operations.push('hover');
    operations.push('focus', 'blur');
    operations.push('get_text', 'get_attributes');

    return [...new Set(operations)];
}

function detectActionableElements() {
    console.log("Starting detection of actionable elements...");
    state.currentScanUsedIds.clear();
    const actionableElements = [];
    
    if (!isBrowser) {
        console.log("Not in browser environment, returning empty actionable elements");
        return actionableElements;
    }
    
    const allElements = document.querySelectorAll('*');
    if (state.DEBUG_ACTIONABILITY_CHECK) console.log(`Total elements found: ${allElements.length}`);

    for (const element of allElements) {
        if (isElementActionable(element)) {
            const elementId = generateStableElementId(element);
            element.setAttribute('data-element-id', elementId);

            const elementData = {
                id: elementId,
                type: getElementType(element),
                tag: element.tagName.toLowerCase(),
                text_content: getElementTextContent(element),
                attributes: getRelevantAttributes(element),
                is_visible: isElementVisible(element),
                available_operations: getAvailableOperations(element)
            };
            actionableElements.push(elementData);
             if (state.DEBUG_ACTIONABILITY_CHECK) console.log(`[Actionable] Element: %o, Data: %o`, element, elementData);
        }
    }
    console.log(`Finished detection. Found ${actionableElements.length} actionable elements.`);
    return actionableElements;
}

// State handling
async function handleGetState(requestId) {
    console.log(`CONTENT.JS: handleGetState ENTERED for requestId: ${requestId}`);
    try {
        // Use the exported function to allow overriding in tests
        const actionableElements = (typeof module !== 'undefined' && module.exports && module.exports.detectActionableElements) 
            ? module.exports.detectActionableElements() 
            : detectActionableElements();

        const pageState = {
            type: "state_response",
            status: "success",
            state: {
                url: isBrowser ? window.location.href : 'http://test.example.com',
                title: isBrowser ? document.title : 'Test Page',
                viewport: {
                    width: isBrowser ? window.innerWidth : 1920,
                    height: isBrowser ? window.innerHeight : 1080,
                    pixel_ratio: isBrowser ? window.devicePixelRatio || 1.0 : 1.0
                },
                scroll_position: {
                    x: isBrowser ? window.scrollX : 0,
                    y: isBrowser ? window.scrollY : 0,
                    max_x: isBrowser ? document.documentElement.scrollWidth - window.innerWidth : 0,
                    max_y: isBrowser ? document.documentElement.scrollHeight - window.innerHeight : 0,
                },
                document_dimensions: {
                    width: isBrowser ? document.documentElement.scrollWidth : 1920,
                    height: isBrowser ? document.documentElement.scrollHeight : 1080
                },
                actionable_elements: actionableElements,
                page_metrics: {
                    total_elements_on_page: isBrowser ? document.querySelectorAll('*').length : 0,
                    actionable_elements_count: actionableElements.length,
                    visible_actionable_elements_count: actionableElements.filter(el => el.is_visible).length,
                    dom_load_time: -1,
                    page_load_time: -1,
                },
                timestamp: new Date().toISOString()
            }
        };
        console.log(`CONTENT.JS: State extracted successfully for requestId: ${requestId}. ${actionableElements.length} actionable elements found.`);
        return pageState;
    } catch (error) {
        console.error(`CONTENT.JS: Error extracting page state for requestId ${requestId}:`, error);
        return {
            type: "state_response",
            status: "error",
            error: `Error extracting page state: ${error.message}`,
            details: error.stack
        };
    }
}

// Message listener setup
function setupMessageListener() {
    if (state.messageListener) {
        console.warn('CONTENT.JS: Message listener already established');
        return;
    }

    state.messageListener = function(request, sender, sendResponse) {
        switch (request.type) {
            case 'get_state':
                handleGetState(request.requestId)
                    .then(response => {
                        console.log("CONTENT.JS: State data collected by handleGetState for ID", request.requestId, ":", response);
                        sendResponse({ request_id: request.requestId, ...response });
                    })
                    .catch(_error => {
                        console.error("CONTENT.JS: Error in handleGetState:", _error);
                        sendResponse({
                            request_id: request.requestId, type: "response",
                            status: "error", error: `Failed to get state: ${_error.message}`
                        });
                    });
                return true;
                
            case 'execute_action':
                console.log("CONTENT.JS: execute_action not implemented in modular version");
                sendResponse({
                    request_id: request.requestId, type: "response",
                    status: "error", error: "execute_action not implemented in modular version"
                });
                return false;
                
            case 'ping':
                console.log("CONTENT.JS: Received PING. Request ID:", request.requestId);
                sendResponse({ type: 'pong', requestId: request.requestId });
                return false;
                
            default:
                console.warn('CONTENT.JS: Unknown message type:', request.type);
                sendResponse({ error: 'Unknown message type' });
                return false;
        }
    };
    
    if (isBrowser) {
        console.log("CONTENT.JS: About to add runtime.onMessage.addListener.");
        chrome.runtime.onMessage.addListener(state.messageListener);
        console.log('CONTENT.JS: Message listener established.');
    } else {
        console.log('CONTENT.JS: Not in browser environment, message listener not added.');
    }
}

// Initialization
function initializeContentScript() {
    console.log('CONTENT.JS: Initializing content script...');
    try {
        // Use the exported function to allow overriding in tests
        const messageListenerFn = (typeof module !== 'undefined' && module.exports && module.exports.setupMessageListener) 
            ? module.exports.setupMessageListener 
            : setupMessageListener;
        messageListenerFn();
        signalReadyToBackground();
        console.log("CONTENT.JS: Core initialization complete. Ready signal sent.");
    } catch (error) {
        console.error('CONTENT.JS: Content script core initialization failed:', error);
    }
}

// Module exports for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        state,
        signalReadyToBackground,
        generateStableElementId,
        generateIdByUniqueAttributes,
        generateIdByStructuralPosition,
        generateIdByXPath,
        generateIdByTextContent,
        isIdUnique,
        isElementVisible,
        isElementActionable,
        getElementType,
        getElementTextContent,
        getRelevantAttributes,
        getAvailableOperations,
        detectActionableElements,
        handleGetState,
        setupMessageListener,
        initializeContentScript
    };
}

// Initialize in browser environment (but not in tests)
if (isBrowser && !isTestEnvironment) {
    console.log("CONTENT.JS TOP LEVEL EXECUTION - Script Start");
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeContentScript);
    } else {
        initializeContentScript();
    }

    window.addEventListener('beforeunload', function() {
        console.log('Content script cleaning up...');
    });
    
    console.log("Content script initialized and message listener added. Ready signal will be sent.");
}