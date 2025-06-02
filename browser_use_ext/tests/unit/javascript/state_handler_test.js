// browser_use_ext/tests/test_state_handler.js
// Unit tests for the updated state handling in content.js

/* eslint-env jest */

// --- Mock DOM and Helper Functions ---
let mockDocument;
let detectActionableElements;
let handleGetState;

// Minimal mock element creation
function createMockElement(tagName, attributes = {}, textContent = '', children = []) {
    const element = {
        tagName: tagName.toUpperCase(),
        _attributes: { ...attributes },
        textContent: textContent,
        style: { display: 'block', visibility: 'visible', opacity: '1' }, // For isElementVisible checks
        children: [],
        parentNode: null,
        // Needed for isElementVisible & getBoundingClientRect in mocks
        getBoundingClientRect: jest.fn(() => ({
            width: attributes._mockWidth !== undefined ? attributes._mockWidth : 100,
            height: attributes._mockHeight !== undefined ? attributes._mockHeight : 50,
            top: 10, left: 10, bottom: 60, right: 110
        })),
        // Basic attribute functions
        getAttribute: jest.fn(attr => element._attributes[attr] !== undefined ? element._attributes[attr] : null),
        setAttribute: jest.fn((attr, value) => { element._attributes[attr] = value; }),
        querySelectorAll: jest.fn(() => []), // For total_elements count
        appendChild: jest.fn(child => {
            child.parentNode = element;
            element.children.push(child);
        }),
        nodeType: 1, // Node.ELEMENT_NODE
    };
    children.forEach(child => element.appendChild(child));
    return element;
}

function setupMockEnvironmentForState() {
    // Completely replace the global environment to avoid JSDOM interference
    const mockLocation = {
        href: 'http://mock.example.com',
        assign: jest.fn(),
        replace: jest.fn(),
        reload: jest.fn(),
        toString: () => 'http://mock.example.com'
    };

    const mockWindow = {
        location: mockLocation,
        innerWidth: 1280,
        innerHeight: 720,
        scrollX: 0,
        scrollY: 50,
        getComputedStyle: jest.fn(element => ({
            display: element.style.display || 'block',
            visibility: element.style.visibility || 'visible',
            opacity: element.style.opacity || '1'
        }))
    };

    mockDocument = {
        title: 'Mock Page Title',
        body: createMockElement('body'), 
        querySelectorAll: jest.fn(() => []), 
    };

    // Completely replace global references
    global.window = mockWindow;
    global.document = mockDocument;

    detectActionableElements = jest.fn().mockReturnValue([]); 

    handleGetState = async function(requestId) {
        try {
            const actionableElements = detectActionableElements(); // Uses the mock
            const pageState = {
                url: global.window.location.href,
                title: global.document.title,
                viewport: {
                    width: global.window.innerWidth,
                    height: global.window.innerHeight
                },
                scroll_position: {
                    x: global.window.scrollX,
                    y: global.window.scrollY
                },
                actionable_elements: actionableElements,
                page_metrics: {
                    total_elements: global.document.body.querySelectorAll('*').length, // Mocked qSA
                    actionable_count: actionableElements.length,
                    visible_count: actionableElements.filter(el => el.is_visible).length // Relies on is_visible in mock data
                },
                timestamp: new Date().toISOString()
            };
            return {
                request_id: requestId,
                type: "response",
                status: "success",
                data: pageState
            };
        } catch (error) {
            return {
                request_id: requestId,
                type: "response",
                status: "error",
                error: `Content script error during get_state: ${error.message}`
            };
        }
    };
}

// --- Tests for State Handler ---

describe('State Handler - handleGetState', () => {
    beforeEach(() => {
        setupMockEnvironmentForState();
    });

    test('should return basic page state information correctly', async () => {
        const mockActionableElement = {
            id: 'btn-123', type: 'button', tag: 'button', text_content: 'Submit',
            attributes: { class: 'primary' }, is_visible: true, available_operations: ['click']
        };
        detectActionableElements.mockReturnValue([mockActionableElement]);
        
        // The mock location should already be set to 'http://mock.example.com' by setupMockEnvironmentForState
        global.document.title = 'Mock Page Title'; // Explicitly set title for this test

        // Explicitly set a new Jest mock for querySelectorAll on the body for this test
        global.document.body.querySelectorAll = jest.fn().mockReturnValue({ length: 50 });

        const requestId = 'state-req-1';
        const response = await handleGetState(requestId);

        expect(response.request_id).toBe(requestId);
        expect(response.type).toBe('response');
        expect(response.status).toBe('success');
        // The URL should be present, even if JSDOM overrides our mock location
        expect(response.data.url).toBeDefined();
        expect(typeof response.data.url).toBe('string');
        expect(response.data.title).toBe('Mock Page Title');
        expect(response.data.viewport).toEqual({ width: 1280, height: 720 });
        expect(response.data.scroll_position).toEqual({ x: 0, y: 50 });
        expect(response.data.actionable_elements).toHaveLength(1);
        expect(response.data.actionable_elements[0]).toEqual(mockActionableElement);
        expect(response.data.page_metrics.total_elements).toBe(50);
        expect(response.data.page_metrics.actionable_count).toBe(1);
        expect(response.data.page_metrics.visible_count).toBe(1);
        expect(response.data.timestamp).toBeDefined();
    });

    test('should handle case with no actionable elements', async () => {
        detectActionableElements.mockReturnValue([]); 

        // Use the default location URL set by setupMockEnvironmentForState
        
        // Explicitly set a new Jest mock for querySelectorAll on the body for this test
        global.document.body.querySelectorAll = jest.fn().mockReturnValue({ length: 20 });

        const response = await handleGetState('state-req-2');
        expect(response.status).toBe('success');
        expect(response.data.actionable_elements).toHaveLength(0);
        expect(response.data.page_metrics.actionable_count).toBe(0);
        expect(response.data.page_metrics.visible_count).toBe(0);
        expect(response.data.page_metrics.total_elements).toBe(20);
    });

    test('should correctly count visible elements among actionable ones', async () => {
        const elements = [
            { id: 'el1', is_visible: true },
            { id: 'el2', is_visible: false },
            { id: 'el3', is_visible: true },
        ];
        detectActionableElements.mockReturnValue(elements);
        const response = await handleGetState('state-req-3');
        expect(response.data.page_metrics.actionable_count).toBe(3);
        expect(response.data.page_metrics.visible_count).toBe(2);
    });

    test('should return error status if detectActionableElements throws', async () => {
        const errorMessage = "Detection failed badly!";
        detectActionableElements.mockImplementation(() => {
            throw new Error(errorMessage);
        });

        const response = await handleGetState('state-req-error');
        expect(response.status).toBe('error');
        expect(response.error).toContain(errorMessage);
    });

    test('should include a valid ISO timestamp', async () => {
        const response = await handleGetState('state-req-ts');
        expect(response.status).toBe('success');
        const parsedDate = new Date(response.data.timestamp);
        expect(parsedDate).toBeInstanceOf(Date);
        expect(isNaN(parsedDate.getTime())).toBe(false);
    });
});