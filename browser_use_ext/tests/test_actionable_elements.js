// browser_use_ext/tests/test_actionable_elements.js
// Unit tests for actionable element detection in content.js

const { TextEncoder, TextDecoder } = require('util');
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

/* eslint-env jest */
const { JSDOM } = require('jsdom');

// --- Mock DOM and Helper Functions (subset from test_element_id_generation.js) ---
let currentDocument;
let currentWindow;
let generateStableElementId;
let getElementType;
let getElementTextContent;
let getRelevantAttributes;
let isElementVisible;
let getAvailableOperations;
let isElementActionable; // The main function to test here, plus its dependencies
let detectActionableElements;

function setupSimpleMockDocument() {
    const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
    currentDocument = dom.window.document;
    currentWindow = dom.window;

    Object.defineProperty(currentWindow, 'getComputedStyle', {
        value: jest.fn(element => {
            // Provide a basic mock for style properties
            const style = {
                display: element.style.display || 'block',
                visibility: element.style.visibility || 'visible',
                opacity: element.style.opacity !== undefined ? element.style.opacity.toString() : '1',
                // Ensure JSDOM's default getBoundingClientRect is available on the element
                // or mock it if element doesn't have it naturally.
            };
            // If testing specific computed values not directly on element.style,
            // they would need to be added here or element.style needs to be pre-populated.
            return style; 
        })
    });
    Object.defineProperty(currentWindow, 'innerWidth', { value: 1024, configurable: true });
    Object.defineProperty(currentWindow, 'innerHeight', { value: 768, configurable: true });
    Object.defineProperty(currentWindow, 'scrollX', { value: 0, configurable: true });
    Object.defineProperty(currentWindow, 'scrollY', { value: 0, configurable: true });

    global.document = currentDocument; // Make JSDOM document global for tests
    global.window = currentWindow;     // Make JSDOM window global
    global.Node = currentWindow.Node;         // Use JSDOM Node
    global.HTMLElement = currentWindow.HTMLElement; // Use JSDOM HTMLElement
}

// createMockElement might still be useful for elements not interacting with getComputedStyle,
// or simplify it further if all elements become real JSDOM elements.
function createRealElement(tagName, attributes = {}, textContent = '') {
    const element = global.document.createElement(tagName); 
    let hasMockWidth = false;
    let hasMockHeight = false;
    let isDisplayNone = false;

    for (const key in attributes) {
        if (key === 'style' && typeof attributes.style === 'object') {
            for (const styleKey in attributes.style) {
                element.style[styleKey] = attributes.style[styleKey];
                if (styleKey === 'display' && attributes.style[styleKey] === 'none') {
                    isDisplayNone = true;
                }
            }
        } else if (key === '_mockWidth') { 
            Object.defineProperty(element, 'offsetWidth', { value: attributes[key], configurable: true, writable: true });
            hasMockWidth = true;
        } else if (key === '_mockHeight') { 
            Object.defineProperty(element, 'offsetHeight', { value: attributes[key], configurable: true, writable: true });
            hasMockHeight = true;
        } else {
            element.setAttribute(key, attributes[key]);
        }
    }

    if (isDisplayNone) {
        // If display: none, offsetWidth/Height should be 0
        if (!hasMockWidth) Object.defineProperty(element, 'offsetWidth', { value: 0, configurable: true, writable: true });
        if (!hasMockHeight) Object.defineProperty(element, 'offsetHeight', { value: 0, configurable: true, writable: true });
        hasMockWidth = true; // Mark as handled
        hasMockHeight = true; // Mark as handled
    }

    if (!hasMockWidth) {
        // JSDOM might not reflect style.width to offsetWidth well, so we mock it if not display:none
        Object.defineProperty(element, 'offsetWidth', { 
            value: parseInt(element.style.width, 10) || (attributes.style && attributes.style.width === '0px' ? 0 : 10), 
            configurable: true, writable: true 
        });
    }
    if (!hasMockHeight) {
        Object.defineProperty(element, 'offsetHeight', { 
            value: parseInt(element.style.height, 10) || (attributes.style && attributes.style.height === '0px' ? 0 : 10), 
            configurable: true, writable: true 
        });
    }

    if (textContent) element.textContent = textContent;
    
    const originalGetBoundingClientRect = element.getBoundingClientRect.bind(element);
    element.getBoundingClientRect = () => {
        // const currentRect = originalGetBoundingClientRect(); // JSDOM's can be unreliable for non-rendered

        let finalWidth = element.offsetWidth; // Use the (potentially mocked) offsetWidth
        let finalHeight = element.offsetHeight; // Use the (potentially mocked) offsetHeight

        if (isDisplayNone) {
            finalWidth = 0;
            finalHeight = 0;
        }
        
        // For JSDOM, top/left are often 0. If the element is meant to be visible (non-zero size), give it some position.
        const finalTop = (finalWidth > 0 || finalHeight > 0) ? 10 : 0;
        const finalLeft = (finalWidth > 0 || finalHeight > 0) ? 10 : 0;

        return {
            top: finalTop,
            left: finalLeft,
            width: finalWidth,
            height: finalHeight,
            bottom: finalTop + finalHeight,
            right: finalLeft + finalWidth,
        };
    };

    return element;
}


// --- Tests for Actionable Element Detection ---

describe('Actionable Element Detection - detectActionableElements', () => {
    beforeEach(() => {
        setupSimpleMockDocument(); // Sets up global.document and global.window with JSDOM

        global.isIdUnique = jest.fn().mockReturnValue(true);

        generateStableElementId = jest.fn(element => {
            if (element.getAttribute('id')) return `attr_id_${element.getAttribute('id')}`;
            return `mock_id_${element.tagName}_${Math.random().toString(16).slice(2)}`;
        });

        getElementType = jest.fn(element => {
            const tag = element.tagName.toLowerCase();
            if (tag === 'input') return element.type || 'text';
            if (tag === 'a') return 'link';
            return tag;
        });

        getElementTextContent = jest.fn(element => (element.textContent || element.value || '').trim());

        getRelevantAttributes = jest.fn(element => {
            const attrs = {};
            if (element.id) attrs.id = element.id;
            if (element.getAttribute('class')) attrs.class = element.getAttribute('class');
            return attrs;
        });

        // Updated isElementVisible mock
        isElementVisible = jest.fn(element => {
            if (!element || !global.window || !global.document) return false;
            
            const style = global.window.getComputedStyle(element);
            if (!style) return false;

            if (style.display === 'none') return false;
            if (style.visibility === 'hidden') return false;
            if (style.opacity === '0' || parseFloat(style.opacity) === 0) return false; // Check string '0' too

            // Use direct offsetWidth/offsetHeight from the element, which createRealElement now tries to set realistically
            if (element.offsetWidth <= 0 || element.offsetHeight <= 0) {
                 // Allow SVG elements to have 0x0 dimensions but still be "visible" if not display:none etc.
                if (!element.tagName || element.tagName.toLowerCase() !== 'svg') {
                    return false;
                }
            }
            
            // getBoundingClientRect check can be an additional check, but offsetWidth/Height are primary for "rendered" size
            // const rect = element.getBoundingClientRect();
            // if (rect.width <= 0 || rect.height <= 0) {
            //    if (!element.tagName || element.tagName.toLowerCase() !== 'svg') return false;
            // }

            return true; 
        });
        
        getAvailableOperations = jest.fn(element => {
            const ops = ['click'];
            if (element.tagName === 'INPUT') ops.push('input_text');
            return ops;
        });

        isElementActionable = function(element) {
            if (!isElementVisible(element)) return false;
            const tagName = element.tagName.toLowerCase();
            const interactiveTags = ['a', 'button', 'input', 'select', 'textarea', 'label'];
            const interactiveRoles = ['button', 'link', 'textbox', 'checkbox', 'radio', 'combobox', 'menuitem', 'tab', 'slider'];
            if (interactiveTags.includes(tagName)) {
                if (tagName === 'input' && element.type === 'hidden') return false;
                return true;
            }
            const role = element.getAttribute('role');
            if (role && interactiveRoles.includes(role)) return true;
            if (element.onclick || element.hasAttribute('onclick') || element.hasAttribute('ng-click') || element.hasAttribute('vue-click')) return true;
            if (element.hasAttribute('tabindex') && parseInt(element.getAttribute('tabindex'), 10) >= 0) return true;
            const contentTags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div', 'li', 'td', 'th'];
            if (contentTags.includes(tagName) && (element.textContent || '').trim().length > 10) return true;
            return false;
        };

        detectActionableElements = function() {
            const actionableElements = [];
            const allElements = global.document.querySelectorAll('*'); 
            for (const element of allElements) {
                if (isElementActionable(element)) { 
                    const elementId = generateStableElementId(element);
                    const elementData = {
                        id: elementId,
                        type: getElementType(element),
                        tag: element.tagName.toLowerCase(),
                        text_content: getElementTextContent(element),
                        attributes: getRelevantAttributes(element),
                        is_visible: isElementVisible(element), // This will now always use the true-returning mock
                        available_operations: getAvailableOperations(element)
                    };
                    actionableElements.push(elementData);
                    element.setAttribute('data-element-id', elementId);
                }
            }
            return actionableElements;
        };
    });

    afterEach(() => {
        // Clean up JSDOM window and document globals if necessary, or rely on Jest's environment reset
        global.document = undefined;
        global.window = undefined;
        global.Node = undefined;
        global.HTMLElement = undefined;
    });

    test('should detect button elements as actionable', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const button = createRealElement('button', {}, 'Click me');
        global.document.body.appendChild(button);
        
        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].tag).toBe('button');
        expect(elements[0].type).toBe('button');
        expect(elements[0].available_operations).toContain('click');
    });

    test('should detect input elements with appropriate operations', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const input = createRealElement('input', { type: 'text', placeholder: 'Enter text' });
        global.document.body.appendChild(input);

        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].type).toBe('text');
        expect(elements[0].available_operations).toContain('input_text');
    });

    test('should detect links with navigation operations', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const link = createRealElement('a', { href: 'https://example.com' }, 'Visit Example');
        global.document.body.appendChild(link);

        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].type).toBe('link');
        // Ensure getRelevantAttributes is called and returns href
        getRelevantAttributes.mockReturnValueOnce({ href: 'https://example.com' });
        expect(detectActionableElements()[0].attributes.href).toBe('https://example.com');
    });

    test('should filter out hidden elements (display: none)', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const visibleButton = createRealElement('button', {}, 'Visible');
        const hiddenButton = createRealElement('button', { style: { display: 'none' } }, 'Hidden');
        global.document.body.appendChild(visibleButton);
        global.document.body.appendChild(hiddenButton);
        
        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].text_content).toBe('Visible');
    });

    test('should filter out hidden elements (zero width/height)', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const normalButton = createRealElement('button', { _mockWidth: 100, _mockHeight: 50 }, 'Normal');
        const zeroSizeButton = createRealElement('button', { _mockWidth: 0, _mockHeight: 0 }, 'Zero Size');
        global.document.body.appendChild(normalButton);
        global.document.body.appendChild(zeroSizeButton);

        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].text_content).toBe('Normal');
    });

    test('should detect content-rich elements (e.g., h1)', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const heading = createRealElement('h1', {}, 'This is a significant heading with enough content');
        global.document.body.appendChild(heading);
        
        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].tag).toBe('h1');
        expect(elements[0].text_content).toContain('significant heading');
    });

    test('should assign unique IDs to each element and set data-element-id attribute', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const button1 = createRealElement('button', { id: 'btn1' }, 'Button 1');
        const button2 = createRealElement('button', { id: 'btn2' }, 'Button 2');
        global.document.body.appendChild(button1);
        global.document.body.appendChild(button2);
        
        const elements = detectActionableElements();
        expect(elements).toHaveLength(2);
        expect(elements[0].id).not.toBe(elements[1].id);
        expect(elements[0].id).toBe('attr_id_btn1');
        expect(elements[1].id).toBe('attr_id_btn2');
        expect(button1.getAttribute('data-element-id')).toBe(elements[0].id);
        expect(button2.getAttribute('data-element-id')).toBe(elements[1].id);
    });

    test('isElementActionable should return true for an input with type submit', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const submitInput = createRealElement('input', { type: 'submit' });
        global.document.body.appendChild(submitInput); // Must be in document for getComputedStyle
        expect(isElementActionable(submitInput)).toBe(true);
    });

    test('isElementActionable should return false for an input with type hidden', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const hiddenInput = createRealElement('input', { type: 'hidden' });
        global.document.body.appendChild(hiddenInput);
        expect(isElementActionable(hiddenInput)).toBe(false);
    });

    test('isElementActionable should return true for element with ARIA role button', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const ariaButton = createRealElement('div', { role: 'button' }, 'ARIA Button');
        global.document.body.appendChild(ariaButton);
        expect(isElementActionable(ariaButton)).toBe(true);
    });

    test('isElementActionable should return true for element with onclick attribute', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const onclickDiv = createRealElement('div', {}, 'Clickable Div');
        onclickDiv.onclick = () => {}; // Assign a function to make it truthy
        global.document.body.appendChild(onclickDiv);
        expect(isElementActionable(onclickDiv)).toBe(true);
    });

    test('isElementActionable should return false for a div with short text and no interactive attributes', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const simpleDiv = createRealElement('div', {}, 'Hi');
        global.document.body.appendChild(simpleDiv);
        expect(isElementActionable(simpleDiv)).toBe(false);
    });

    test('isElementActionable should return true for a div with long text', () => {
        global.document.body.innerHTML = ''; // Clear body for this specific test
        const textyDiv = createRealElement('div', {}, 'This is a div with sufficiently long text content.');
        global.document.body.appendChild(textyDiv);
        expect(isElementActionable(textyDiv)).toBe(true);
    });
}); 