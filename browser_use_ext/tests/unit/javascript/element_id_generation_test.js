// browser_use_ext/tests/test_element_id_generation.js
// Unit tests for the element ID generation system in content.js

// Mocking browser environment for tests (simplified)
// In a real setup, you would use a testing library like Jest with JSDOM.
/* eslint-env jest */

// --- Mock DOM and Helper Functions ---
let mockDocument;
let isIdUnique; // Will be a Jest mock function

// Declare variables for functions from content.js; they will be defined in beforeEach
let generateIdByUniqueAttributes;
let generateIdByStructuralPosition;
let generateIdByXPath;
let generateIdByTextContent;
let generateStableElementId;
let currentScanUsedIds; // Declared here, will be initialized in setup

function setupMockDocumentForTests() {
    mockDocument = {
        querySelectorAll: jest.fn(selector => {
            if (selector.startsWith('[data-element-id=')) {
                // Robust regex to extract ID from attribute selector
                const match = selector.match(/data-element-id="([^"]+)"/);
                if (!match || !match[1]) return []; // No valid ID found in selector
                const id = match[1];
                const found = [];
                function findInData(elements) {
                    for (const el of elements) {
                        if (el.getAttribute('data-element-id') === id) found.push(el);
                        if (el.children) findInData(el.children);
                    }
                }
                if (mockDocument.body && mockDocument.body.children) findInData(mockDocument.body.children);
                return found;
            }
            return [];
        }),
        getElementById: jest.fn(id => {
            let found = null;
            function findInBody(elements) {
                for (const el of elements) {
                    if (el.id === id) found = el;
                    if (el.children && !found) findInBody(el.children);
                }
            }
            if (mockDocument.body && mockDocument.body.children) findInBody(mockDocument.body.children);
            return found;
        }),
        evaluate: jest.fn((xpath, contextNode) => { 
            if (xpath.includes("@id='test-id'")) { 
                 const el = createElement('div', {id: 'test-id'});
                 return { singleNodeValue: el };
            }
            return { singleNodeValue: null };
        }),
        body: null, 
        documentElement: null,
    };
    global.document = mockDocument;
    global.Node = { ELEMENT_NODE: 1, TEXT_NODE: 3 };
    global.XPathResult = { FIRST_ORDERED_NODE_TYPE: 9 };
    currentScanUsedIds = new Set(); // Initialize here

    // More realistic isIdUnique for testing
    global.isIdUnique = jest.fn((idToTest, currentElement) => {
        const elementsWithId = global.document.querySelectorAll(`[data-element-id="${idToTest}"]`);
        if (!elementsWithId || elementsWithId.length === 0) return true;
        if (elementsWithId.length === 1 && elementsWithId[0] === currentElement) return true;
        return false;
    });
}

function createElement(tagName, attributes = {}, textContent = '') {
    const element = {
        tagName: tagName.toUpperCase(),
        _attributes: { ...attributes }, 
        children: [],
        parentNode: null,
        textContent: textContent,
        value: attributes.value || '', 
        id: attributes.id || '', 
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
        nodeType: Node.ELEMENT_NODE,
    };
    element.children.forEach(c => c.parentNode = element);
    return element;
}

// --- Tests for Element ID Generation ---

describe('Element ID Generation - generateStableElementId', () => {
    beforeEach(() => {
        setupMockDocumentForTests();

        // Define the functions from content.js within this scope for each test
        // This assigns to the variables declared at the top of the script
        generateIdByUniqueAttributes = function(element) { 
            const uniqueAttrs = ['id', 'name', 'data-testid', 'aria-label'];
            for (const attr of uniqueAttrs) {
                const value = element.getAttribute(attr);
                if (value && value.trim()) { return `attr_${attr}_${value.replace(/\s+/g, '_')}`; }
            }
            return null;
        };

        generateIdByStructuralPosition = function(element) {
            const path = [];
            let current = element;

            // Traverse upwards, adding segments until we reach a child of body/documentElement or the element has no valid parent.
            while (current && current.parentNode && 
                   current.parentNode.nodeType === Node.ELEMENT_NODE &&
                   current.parentNode !== global.document.body && 
                   current.parentNode !== global.document.documentElement) {

                let siblings = [];
                if (current.parentNode.children && typeof current.parentNode.children.length === 'number') {
                    siblings = Array.from(current.parentNode.children).filter(s => s.nodeType === Node.ELEMENT_NODE);
                }
                
                const index = siblings.indexOf(current);
                const tagName = current.tagName.toLowerCase();
                path.unshift(`${tagName}[${index >= 0 ? index : 0}]`);
                current = current.parentNode;
            }

            // After the loop, 'current' is either:
            // 1. The original element (if it was a direct child of body/html or had no valid parent for the loop).
            // 2. The highest ancestor element that is still a child of body/html.
            // We need to add this 'current' element's segment to the path if its parent is body or html.
            if (current && current.parentNode && 
                (current.parentNode === global.document.body || current.parentNode === global.document.documentElement) &&
                 current.parentNode.nodeType === Node.ELEMENT_NODE ) {
                
                 let parentChildren = [];
                 if (current.parentNode.children && typeof current.parentNode.children.length === 'number') {
                    parentChildren = Array.from(current.parentNode.children).filter(s => s.nodeType === Node.ELEMENT_NODE);
                 }
                 const index = parentChildren.indexOf(current);
                 const tagName = current.tagName.toLowerCase();
                 path.unshift(`${tagName}[${index >= 0 ? index : 0}]`);
            } else if (current && path.length === 0 && current.parentNode && current.parentNode.nodeType === Node.ELEMENT_NODE) {
                // This case is for elements that are direct children of some other element not body/HTML,
                // and the while loop didn't run. This shouldn't typically happen if the element is deeply nested 
                // unless the initial element itself is the one whose parent is not body/html.
                // This is a fallback to ensure at least one segment if the element itself is the starting point of the path.
                let parentChildren = [];
                 if (current.parentNode.children && typeof current.parentNode.children.length === 'number') {
                    parentChildren = Array.from(current.parentNode.children).filter(s => s.nodeType === Node.ELEMENT_NODE);
                 }
                 const index = parentChildren.indexOf(current);
                 const tagName = current.tagName.toLowerCase();
                 path.unshift(`${tagName}[${index >= 0 ? index : 0}]`);
            }

            return path.length > 0 ? `struct_${path.join('_')}` : null;
        };

        generateIdByXPath = function(element) {
            if (element.id) return `xpath_id("${element.id}")`; // Perplexity style
            let currentPath = '';
            let node = element;
            while (node && node.nodeType === Node.ELEMENT_NODE) {
                const tagName = node.tagName.toLowerCase();
                let segment = tagName;
                if (node.parentNode && node.parentNode.nodeType === Node.ELEMENT_NODE) {
                    const siblings = Array.from(node.parentNode.children)
                                        .filter(e => e.nodeType === Node.ELEMENT_NODE && e.tagName === node.tagName);
                    if (siblings.length > 1) {
                        const index = siblings.indexOf(node) + 1;
                        segment += `[${index}]`;
                    }
                }
                currentPath = `/${segment}${currentPath}`;
                if (node === global.document.documentElement) break;
                node = node.parentNode;
            }
            return `xpath_${currentPath}`; // This should now be a standard XPath
        };

        generateIdByTextContent = function(element) {
            // Prioritize value, then textContent, then aria-label
            const text = (element.value || element.textContent || element.getAttribute('aria-label') || '').trim();
            if (text && text.length > 0 && text.length < 50) { return `text_${text.replace(/[^a-zA-Z0-9_]/g, '_').substring(0,30)}`; }
            return null;
        };

        generateStableElementId = function(element) {
            const strategies = [
                () => generateIdByUniqueAttributes(element),
                () => generateIdByStructuralPosition(element),
                () => generateIdByXPath(element),
                () => generateIdByTextContent(element)
            ];
            for (const strategy of strategies) {
                const id = strategy();
                // Use the globally mocked isIdUnique (which is a jest.fn())
                if (id && global.isIdUnique(id, element)) { return id; } 
            }
            return `element_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        };
    });

    test('should prioritize ID from unique attributes (id)', () => {
        const mockElement = createElement('button', { id: 'submit-btn' });
        const id = generateIdByUniqueAttributes(mockElement);
        expect(id).toBe('attr_id_submit-btn');
    });

    test('should prioritize ID from unique attributes (name)', () => {
        const mockElement = createElement('input', { name: 'username' });
        const id = generateIdByUniqueAttributes(mockElement);
        expect(id).toBe('attr_name_username');
    });

    test('should generate a fallback ID if all strategies fail or produce non-unique IDs', () => {
        const mockElement = createElement('div');
        global.isIdUnique = jest.fn(() => false); // All strategies yield non-unique IDs
        const id = generateStableElementId(mockElement);
        expect(id).toMatch(/^element_\d+_\w{9}$/);
    });

    test('generateIdByUniqueAttributes handles data-testid', () => {
        const mockElement = createElement('div', { 'data-testid': 'my-component' });
        const id = generateIdByUniqueAttributes(mockElement);
        expect(id).toBe('attr_data-testid_my-component');
    });

    test('generateIdByUniqueAttributes handles aria-label', () => {
        const mockElement = createElement('button', { 'aria-label': 'Close button' });
        const id = generateIdByUniqueAttributes(mockElement);
        expect(id).toBe('attr_aria-label_Close_button');
    });

    test('generateIdByUniqueAttributes returns null if no unique attributes', () => {
        const mockElement = createElement('div', { class: 'some-class' });
        const id = generateIdByUniqueAttributes(mockElement);
        expect(id).toBeNull();
    });
});