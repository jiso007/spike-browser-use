// browser_use_ext/tests/unit/javascript/test_action_execution_unit.js
// Unit tests for the updated action execution system in content.js

/* eslint-env jest */

// --- Mock DOM and Helper Functions (similar to other test files) ---
let mockDocument;
let resolveElementById;
// Mock specific action execution functions that handleExecuteAction will call
let executeClick, executeInputText, executeClear, executeSelectOption, executeScroll, executeHover, executeCheckbox, executeNavigate;

// The function we are primarily testing
let handleExecuteAction;

// Declare spies at a higher scope so they can be defined in setup and used in tests
let DYNAMIC_HREF_SETTER_SPY;

// Helper to create mock elements, simplified
function createMockElement(tagName, attributes = {}, textContent = '', children = []) {
    const element = {
        tagName: tagName.toUpperCase(),
        _attributes: { ...attributes },
        textContent: textContent,
        style: { display: 'block', visibility: 'visible', opacity: '1' },
        children: [],
        parentNode: null,
        href: attributes.href || null,
        type: attributes.type || null,
        value: attributes.value || '',
        id: attributes.id || '',
        checked: attributes.checked || false,
        disabled: attributes.disabled || false,
        readOnly: attributes.readOnly || false,
        options: attributes.options || [], // For select elements
        selectedIndex: attributes.selectedIndex !== undefined ? attributes.selectedIndex : -1,
        // Mock methods
        getAttribute: jest.fn(attr => element._attributes[attr] !== undefined ? element._attributes[attr] : null),
        setAttribute: jest.fn((attr, value) => {
            element._attributes[attr] = value;
            if (attr === 'id') element.id = value;
            if (attr === 'value') element.value = value;
        }),
        hasAttribute: jest.fn(attr => element._attributes[attr] !== undefined),
        appendChild: jest.fn(child => {
            child.parentNode = element;
            element.children.push(child);
        }),
        dispatchEvent: jest.fn(),
        focus: jest.fn(),
        click: jest.fn(() => { // Simulate navigation for links
            if (element.tagName === 'A' && element.href) {
                // console.log(`Mock navigating to ${element.href}`);
            }
        }),
        scrollIntoView: jest.fn(),
        scrollBy: jest.fn(),
        nodeType: 1, // Node.ELEMENT_NODE
    };
    if (tagName === 'select') {
        // Populate select options if provided
        (attributes.optionsData || []).forEach(optData => {
            const option = createMockElement('option', { value: optData.value }, optData.text);
            element.options.push(option);
        });
        if (element.options.length > 0 && element.selectedIndex === -1) {
            // element.selectedIndex = 0; // Default select first if not specified
        }
    }
    children.forEach(child => element.appendChild(child));
    return element;
}

function setupMockEnvironment() {
    mockDocument = {
        querySelector: jest.fn(),
        getElementById: jest.fn(),
        evaluate: jest.fn().mockReturnValue({ singleNodeValue: null }), // XPath mock
        body: createMockElement('body'),
        documentElement: createMockElement('html'),
    };
    global.document = mockDocument;

    DYNAMIC_HREF_SETTER_SPY = jest.fn();
    let currentHref = 'http://localhost/';

    const mockHistory = { back: jest.fn() };

    // Work with existing JSDOM window instead of creating a new one
    if (!global.window) {
        global.window = {};
    }

    // Define/override properties on the existing global.window object
    global.window.scrollBy = jest.fn();
    global.window.history = mockHistory;
    global.window.getComputedStyle = jest.fn(element => element.style || {});
    global.window.innerWidth = 1024;
    global.window.innerHeight = 768;
    
    // Mock window.location completely since JSDOM's location is not configurable
    const mockLocation = {
        href: currentHref,
        assign: jest.fn((url) => {
            mockLocation.href = url;
            currentHref = url;
            DYNAMIC_HREF_SETTER_SPY(url);
        }),
        replace: jest.fn((url) => {
            mockLocation.href = url;
            currentHref = url;
        }),
        reload: jest.fn(),
        toString: () => currentHref
    };
    
    // Use Object.defineProperty to make a custom getter/setter for href
    Object.defineProperty(mockLocation, 'href', {
        get() {
            return currentHref;
        },
        set(url) {
            currentHref = url;
            DYNAMIC_HREF_SETTER_SPY(url);
        },
        configurable: true
    });
    
    // Replace window.location with our mock
    delete global.window.location;
    global.window.location = mockLocation;

    global.Node = { ELEMENT_NODE: 1 };
    global.XPathResult = { FIRST_ORDERED_NODE_TYPE: 9 };
    global.HTMLInputElement = function () { };
    global.HTMLTextAreaElement = function () { };
    global.HTMLSelectElement = function () { };
    global.HTMLAnchorElement = function () { };
    global.HTMLElement = function () { };

    // Mock the individual action execution functions
    executeClick = jest.fn().mockResolvedValue({ success: true, message: 'Clicked' });
    executeInputText = jest.fn().mockReturnValue({ success: true, message: 'Input text' });
    executeClear = jest.fn().mockReturnValue({ success: true, message: 'Cleared' });
    executeSelectOption = jest.fn().mockReturnValue({ success: true, message: 'Selected option' });
    executeScroll = jest.fn().mockReturnValue({ success: true, message: 'Scrolled' });
    executeHover = jest.fn().mockReturnValue({ success: true, message: 'Hovered' });
    executeCheckbox = jest.fn().mockReturnValue({ success: true, message: 'Checkbox action' });
    executeNavigate = jest.fn().mockReturnValue({ success: true, message: 'Navigated' });

    // Mock resolveElementById
    // This will be the primary way tests provide elements to handleExecuteAction
    resolveElementById = jest.fn();

    // Function under test (logic copied from content.js)
    // It will call the mocked execute<Action> functions and mocked resolveElementById
    handleExecuteAction = async function (actionName, params, requestId) {
        let resultData = {};
        let status = "success";
        let error = null;
        try {
            let element = null;
            const elementSpecificActions = ['click', 'input_text', 'clear', 'select_option', 'scroll_element', 'hover', 'check', 'uncheck', 'get_attributes', 'read_text', 'read_value'];
            if (elementSpecificActions.includes(actionName)) {
                if (!params || !params.element_id) throw new Error(`Action '${actionName}' requires an 'element_id' parameter.`);
                element = resolveElementById(params.element_id); // Uses the mock
                if (!element) throw new Error(`Element with ID '${params.element_id}' not found.`);
            }

            switch (actionName) {
                case 'click': resultData = await executeClick(element, params); break;
                case 'input_text': resultData = executeInputText(element, params); break;
                case 'clear': resultData = executeClear(element, params); break;
                case 'select_option': resultData = executeSelectOption(element, params); break;
                case 'scroll_element': resultData = executeScroll(element, params); break;
                case 'scroll_window': resultData = executeScroll(global.window, params); break;
                case 'hover': resultData = executeHover(element, params); break;
                case 'check': case 'uncheck': resultData = executeCheckbox(element, params, actionName === 'check'); break;
                case 'navigate':
                    if (element && element.tagName === 'A') resultData = executeNavigate(element, params);
                    else if (params && params.url) {
                        global.window.location.href = params.url;
                        resultData = { success: true, message: `Navigating to URL: ${params.url}` };
                    }
                    else throw new Error("Navigate action requires a target <a> element or a URL in params.");
                    break;
                case 'go_to_url':
                    if (!params || !params.url) throw new Error("go_to_url action requires a 'url' parameter.");
                    global.window.location.href = params.url;
                    resultData = { success: true, message: `Navigated to ${params.url}` };
                    break;
                case 'go_back':
                    global.window.history.back();
                    resultData = { success: true, message: "Navigated back." };
                    break;
                case 'get_attributes': resultData.attributes = { mock_attr: element.getAttribute('mock_attr') || 'mock_value' }; break;
                case 'read_text': resultData.text_content = element.textContent || 'mock text'; break;
                case 'read_value':
                    resultData.value = element.value; // Use element.value directly
                    if (element.type === 'checkbox' || element.type === 'radio') {
                        resultData.checked = element.checked;
                    }
                    break;
                default: throw new Error(`Unknown or unsupported action: ${actionName}`);
            }
            if (resultData && resultData.success === false) {
                status = "error"; error = resultData.error || "Action failed.";
            }
        } catch (e) {
            status = "error"; error = e.message;
        }
        return { request_id: requestId, type: "response", status: status, data: resultData, error: error };
    };
}

// --- Tests for Action Execution ---

describe('Action Execution - handleExecuteAction', () => {
    beforeEach(() => {
        setupMockEnvironment();
        // Explicitly ensure global.window.history.back is a fresh Jest mock for each test
        // This might seem redundant if setupMockEnvironment already does jest.fn(),
        // but it guarantees it here if there's any subtlety in execution order or object references.
        global.window.history.back = jest.fn();

        DYNAMIC_HREF_SETTER_SPY.mockClear();
        global.window.history.back.mockClear(); // Now this should work on the guaranteed mock.
    });

    test('should call executeClick for "click" action', async () => {
        const mockElement = createMockElement('button', { id: 'btn1' });
        resolveElementById.mockReturnValue(mockElement);

        await handleExecuteAction('click', { element_id: 'eid-btn1' }, 'req1');
        expect(resolveElementById).toHaveBeenCalledWith('eid-btn1');
        expect(executeClick).toHaveBeenCalledWith(mockElement, { element_id: 'eid-btn1' });
    });

    test('should call executeInputText for "input_text" action', async () => {
        const mockElement = createMockElement('input', { id: 'inp1' });
        resolveElementById.mockReturnValue(mockElement);
        const params = { element_id: 'eid-inp1', text: 'hello' };

        await handleExecuteAction('input_text', params, 'req2');
        expect(executeInputText).toHaveBeenCalledWith(mockElement, params);
    });

    test('should return error if element_id is missing for element-specific action', async () => {
        const response = await handleExecuteAction('click', { text: 'oops' }, 'req3'); // Missing element_id
        expect(response.status).toBe('error');
        expect(response.error).toContain("requires an 'element_id' parameter");
    });

    test('should return error if resolveElementById returns null', async () => {
        resolveElementById.mockReturnValue(null);
        const response = await handleExecuteAction('click', { element_id: 'nonexistent' }, 'req4');
        expect(response.status).toBe('error');
        expect(response.error).toContain("Element with ID 'nonexistent' not found");
    });

    test('should handle "go_to_url" action', async () => {
        const params = { url: 'https://example.com' };
        const response = await handleExecuteAction('go_to_url', params, 'req5');
        expect(response.status).toBe('success');
        expect(response.data.message).toBe(`Navigated to https://example.com`);
    });

    test('should handle "go_back" action', async () => {
        const response = await handleExecuteAction('go_back', {}, 'req6');
        expect(response.status).toBe('success');
        expect(response.data.message).toBe("Navigated back.");
    });

    test('should handle "scroll_element" action', async () => {
        const mockElement = createMockElement('div', {id: 'scrollable'});
        resolveElementById.mockReturnValue(mockElement);
        const params = { element_id: 'eid-scrollable' };
        
        await handleExecuteAction('scroll_element', params, 'req7');
        expect(resolveElementById).toHaveBeenCalledWith('eid-scrollable');
        expect(executeScroll).toHaveBeenCalledWith(mockElement, params);
    });

    test('should handle "scroll_window" action', async () => {
        const params = { scroll_amount: { x: 100, y: 200 } };
        const response = await handleExecuteAction('scroll_window', params, 'req8');
        expect(response.status).toBe('success');
        expect(response.data.message).toBe('Scrolled');
    });

    test('should handle "hover" action', async () => {
        const mockElement = createMockElement('div', {id: 'hoverable'});
        resolveElementById.mockReturnValue(mockElement);
        const params = { element_id: 'eid-hoverable' };
        
        await handleExecuteAction('hover', params, 'req9');
        expect(resolveElementById).toHaveBeenCalledWith('eid-hoverable');
        expect(executeHover).toHaveBeenCalledWith(mockElement, params);
    });

    test('should handle "check" action', async () => {
        const mockElement = createMockElement('input', {id: 'checkbox', type: 'checkbox'});
        resolveElementById.mockReturnValue(mockElement);
        const params = { element_id: 'eid-checkbox' };
        
        await handleExecuteAction('check', params, 'req10');
        expect(resolveElementById).toHaveBeenCalledWith('eid-checkbox');
        expect(executeCheckbox).toHaveBeenCalledWith(mockElement, params, true);
    });

    test('should handle "uncheck" action', async () => {
        const mockElement = createMockElement('input', {id: 'checkbox', type: 'checkbox'});
        resolveElementById.mockReturnValue(mockElement);
        const params = { element_id: 'eid-checkbox' };
        
        await handleExecuteAction('uncheck', params, 'req11');
        expect(resolveElementById).toHaveBeenCalledWith('eid-checkbox');
        expect(executeCheckbox).toHaveBeenCalledWith(mockElement, params, false);
    });

    test('should handle "get_attributes" action', async () => {
        const mockElement = createMockElement('div', {id: 'testElement', mock_attr: 'testValue'});
        resolveElementById.mockReturnValue(mockElement);
        const params = { element_id: 'eid-testElement' };
        
        const response = await handleExecuteAction('get_attributes', params, 'req12');
        expect(resolveElementById).toHaveBeenCalledWith('eid-testElement');
        expect(response.status).toBe('success');
        expect(response.data.attributes).toEqual({ mock_attr: 'testValue' });
    });
});

 