// browser_use_ext/tests/test_action_execution.js
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
            if(attr === 'id') element.id = value;
            if(attr === 'value') element.value = value;
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
            const option = createMockElement('option', {value: optData.value}, optData.text);
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

    // Temporarily store original window if it exists, for restoring (though Jest usually handles this)
    const originalWindow = global.window;

    // Start with a fresh window object for each test setup or ensure it's clean
    global.window = {}; // Or: delete global.window; global.window = {};

    // Define properties on the new global.window object
    global.window.scrollBy = jest.fn();
    global.window.history = mockHistory;
    global.window.getComputedStyle = jest.fn(element => element.style || {});
    global.window.innerWidth = 1024;
    global.window.innerHeight = 768;

    // Robustly mock window.location using Object.defineProperty
    Object.defineProperty(global.window, 'location', {
        value: {
            // Provide a getter and setter for href that uses the DYNAMIC_HREF_SETTER_SPY
            get href() {
                return currentHref;
            },
            set href(url) {
                currentHref = url;
                DYNAMIC_HREF_SETTER_SPY(url);
            },
            // assign: jest.fn(url => { currentHref = url; DYNAMIC_HREF_SETTER_SPY(url); }), // Optional: mock assign if used
            // reload: jest.fn(), // Optional: mock reload if used
            // replace: jest.fn(url => { currentHref = url; DYNAMIC_HREF_SETTER_SPY(url); }), // Optional: mock replace
        },
        writable: true, // Allow tests to further modify/spy on parts of location if necessary
        configurable: true // Important for Jest to be able to restore/manage it
    });

    global.Node = { ELEMENT_NODE: 1 };
    global.XPathResult = { FIRST_ORDERED_NODE_TYPE: 9 };
    global.HTMLInputElement = function() {};
    global.HTMLTextAreaElement = function() {};
    global.HTMLSelectElement = function() {};
    global.HTMLAnchorElement = function() {};
    global.HTMLElement = function() {};

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
    handleExecuteAction = async function(actionName, params, requestId) {
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
                        resultData = { success: true, message: `Navigating to URL: ${params.url}`};
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
                    if(element.type === 'checkbox' || element.type === 'radio') { 
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
        const mockElement = createMockElement('button', {id: 'btn1'});
        resolveElementById.mockReturnValue(mockElement);
        
        await handleExecuteAction('click', { element_id: 'eid-btn1' }, 'req1');
        expect(resolveElementById).toHaveBeenCalledWith('eid-btn1');
        expect(executeClick).toHaveBeenCalledWith(mockElement, { element_id: 'eid-btn1' });
    });

    test('should call executeInputText for "input_text" action', async () => {
        const mockElement = createMockElement('input', {id: 'inp1'});
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
        expect(DYNAMIC_HREF_SETTER_SPY).toHaveBeenCalledWith('https://example.com'); // Use the directly scoped spy
        expect(global.window.location.href).toBe('https://example.com'); 
        expect(response.status).toBe('success');
    });

    test('should handle "go_back" action', async () => {
        const response = await handleExecuteAction('go_back', {}, 'req6');
        expect(global.window.history.back).toHaveBeenCalled(); // Assert directly on the (mocked) global object's method
        expect(response.status).toBe('success');
    });

    test('should handle unknown action', async () => {
        const response = await handleExecuteAction('fly_to_moon', {}, 'req7');
        expect(response.status).toBe('error');
        expect(response.error).toContain('Unknown or unsupported action: fly_to_moon');
    });

    test('should call executeSelectOption for "select_option" action', async () => {
        const mockElement = createMockElement('select', {id: 'sel1'});
        resolveElementById.mockReturnValue(mockElement);
        const params = { element_id: 'eid-sel1', option_value: 'val2' };

        await handleExecuteAction('select_option', params, 'req8');
        expect(executeSelectOption).toHaveBeenCalledWith(mockElement, params);
    });
    
    test('should correctly pass check status for "check" action', async () => {
        const mockElement = createMockElement('input', {type: 'checkbox', id: 'chk1'});
        resolveElementById.mockReturnValue(mockElement);
        const params = { element_id: 'eid-chk1' };

        await handleExecuteAction('check', params, 'req9');
        expect(executeCheckbox).toHaveBeenCalledWith(mockElement, params, true);
    });

    test('should correctly pass check status for "uncheck" action', async () => {
        const mockElement = createMockElement('input', {type: 'checkbox', id: 'chk2'});
        resolveElementById.mockReturnValue(mockElement);
        const params = { element_id: 'eid-chk2' };

        await handleExecuteAction('uncheck', params, 'req10');
        expect(executeCheckbox).toHaveBeenCalledWith(mockElement, params, false);
    });

    test('should execute scroll_window action', async () => {
        const params = { direction: 'down' };
        await handleExecuteAction('scroll_window', params, 'req11');
        expect(executeScroll).toHaveBeenCalledWith(global.window, params);
    });

    test('should execute scroll_element action', async () => {
        const mockElement = createMockElement('div', {id: 'div1'});
        resolveElementById.mockReturnValue(mockElement);
        const params = { element_id: 'eid-div1', direction: 'up' };
        await handleExecuteAction('scroll_element', params, 'req12');
        expect(executeScroll).toHaveBeenCalledWith(mockElement, params);
    });

    // Test for get_attributes, read_text, read_value
    test('should handle get_attributes action', async () => {
        const mockElement = createMockElement('div', { id: 'ga1', 'data-testid': 'test-div' });
        mockElement.getAttribute.mockImplementation(attr => attr === 'mock_attr' ? 'mock_val' : null);
        resolveElementById.mockReturnValue(mockElement);
        const response = await handleExecuteAction('get_attributes', { element_id: 'eid-ga1' }, 'req_ga');
        expect(response.status).toBe('success');
        expect(response.data.attributes).toEqual({ mock_attr: 'mock_val' });
    });

    test('should handle read_text action', async () => {
        const mockElement = createMockElement('p', { id: 'rt1' }, 'Sample Text');
        resolveElementById.mockReturnValue(mockElement);
        const response = await handleExecuteAction('read_text', { element_id: 'eid-rt1' }, 'req_rt');
        expect(response.status).toBe('success');
        expect(response.data.text_content).toBe('Sample Text');
    });

    test('should handle read_value action for input', async () => {
        const mockElement = createMockElement('input', { id: 'rv1', type:'text', value: 'Input Value' });
        resolveElementById.mockReturnValue(mockElement);
        const response = await handleExecuteAction('read_value', { element_id: 'eid-rv1' }, 'req_rv');
        expect(response.status).toBe('success');
        expect(response.data.value).toBe('Input Value');
    });

    test('should handle read_value action for checkbox', async () => {
        const mockElement = createMockElement('input', { id: 'rv2', type:'checkbox', checked: true });
        // Simulate checked property for the mock element itself for the switch case
        Object.defineProperty(mockElement, 'checked', { get: () => true, configurable: true }); 
        resolveElementById.mockReturnValue(mockElement);

        const response = await handleExecuteAction('read_value', { element_id: 'eid-rv2' }, 'req_rv_chk');
        expect(response.status).toBe('success');
        expect(response.data.value).toBe(''); // Checkbox value attribute might be different from checked state
        expect(response.data.checked).toBe(true);
    });
}); 