# Chrome Extension Content Script Refactoring Implementation Plan

This implementation plan provides a complete refactoring strategy for `browser_use_ext/extension/content.js` to align browser state representation and action execution with modern element identification patterns. The refactoring transitions from index-based element targeting to stable string-based element IDs while maintaining robust DOM interaction capabilities.

## Overview

The primary objective is to refactor the Chrome extension's content script to implement a modern element identification and action execution system. This involves two main transformations: converting the state generation mechanism to produce `actionable_elements` with stable string IDs, and updating the action execution system to use these string IDs instead of numeric indices. The refactoring ensures better reliability, maintainability, and alignment with contemporary web automation practices.

## Folder Structure

```
.cursor/rules/chrome_extension_content_readiness.mdc
.cursor/rules/cursor_rules.mdc
.cursor/rules/custom_test_guide.mdc
.cursor/rules/dev_workflow.mdc
.cursor/rules/pydantic_model_guidelines.mdc
.cursor/rules/pytest_config.mdc
.cursor/rules/python_script_module_execution.mdc
.cursor/rules/python_websockets_guidelines.mdc
.cursor/rules/self_improve.mdc
.env.example
.gitattributes
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/config.yml
.github/ISSUE_TEMPLATE/docs_issue.yml
.github/ISSUE_TEMPLATE/feature_request.yml
.github/workflows/cloud_evals.yml
.github/workflows/lint.yml
.github/workflows/package.yaml
.github/workflows/publish.yml
.github/workflows/test.yaml
.gitignore
.pre-commit-config.yaml
.python-version
.windsurfrules
browser_use_ext/__init__.py
browser_use_ext/agent/__init__.py
browser_use_ext/agent/memory/__init__.py
browser_use_ext/agent/memory/service.py
browser_use_ext/agent/message_manager/__init__.py
browser_use_ext/agent/message_manager/service.py
browser_use_ext/agent/prompts.py
browser_use_ext/agent/views.py
browser_use_ext/browser/__init__.py
browser_use_ext/browser/browser.py
browser_use_ext/browser/context.py
browser_use_ext/browser/views.py
browser_use_ext/controller/__init__.py
browser_use_ext/controller/registry/__init__.py
browser_use_ext/controller/registry/views.py
browser_use_ext/controller/service.py
browser_use_ext/dom/__init__.py
browser_use_ext/dom/views.py
browser_use_ext/extension_interface/__init__.py
browser_use_ext/extension_interface/models.py
browser_use_ext/extension_interface/service.py
browser_use_ext/extension/background.js
browser_use_ext/extension/content.js
browser_use_ext/extension/popup.html
browser_use_ext/extension/popup.js
browser_use_ext/README.md
browser_use_ext/tests/__init__.py
browser_use_ext/tests/conftest.py
browser_use_ext/tests/test_agent_prompts.py
browser_use_ext/tests/test_browser_context.py
browser_use_ext/tests/test_browser.py
browser_use_ext/tests/test_controller_service.py
browser_use_ext/tests/test_extension_interface.py
browser_use_ext/tests/test_message_manager.py
browser_use/__init__.py
browser_use/agent/gif.py
browser_use/agent/memory/__init__.py
browser_use/agent/memory/service.py
browser_use/agent/memory/views.py
browser_use/agent/message_manager/service.py
browser_use/agent/message_manager/utils.py
browser_use/agent/message_manager/views.py
browser_use/agent/playwright_script_generator.py
browser_use/agent/playwright_script_helpers.py
browser_use/agent/prompts.py
browser_use/agent/service.py
browser_use/agent/system_prompt.md
browser_use/agent/views.py
browser_use/browser/browser.py
browser_use/browser/chrome.py
browser_use/browser/context.py
browser_use/browser/dolphin_service.py
browser_use/browser/utils/screen_resolution.py
browser_use/browser/views.py
browser_use/controller/registry/service.py
browser_use/controller/registry/views.py
browser_use/controller/service.py
browser_use/controller/views.py
browser_use/dom/buildDomTree.js
browser_use/dom/clickable_element_processor/service.py
browser_use/dom/history_tree_processor/service.py
browser_use/dom/history_tree_processor/view.py
browser_use/dom/service.py
browser_use/dom/views.py
browser_use/exceptions.py
browser_use/logging_config.py
browser_use/README.md
browser_use/telemetry/service.py
browser_use/telemetry/views.py
browser_use/utils.py
check_config_access.py
codebeaver.yml
docs/cloud/implementation.mdx
docs/cloud/quickstart.mdx
docs/customize/agent-settings.mdx
docs/customize/browser-settings.mdx
docs/customize/custom-functions.mdx
docs/customize/hooks.mdx
docs/customize/output-format.mdx
docs/customize/real-browser.mdx
docs/customize/sensitive-data.mdx
docs/customize/supported-models.mdx
docs/customize/system-prompt.mdx
docs/development.mdx
docs/development/contribution-guide.mdx
docs/development/evaluations.mdx
docs/development/local-setup.mdx
docs/development/n8n-integration.mdx
docs/development/observability.mdx
docs/development/roadmap.mdx
docs/development/telemetry.mdx
docs/favicon.svg
docs/introduction.mdx
docs/logo/dark.svg
docs/logo/light.svg
docs/quickstart.mdx
docs/README.md
eval/claude-3.5.py
eval/claude-3.6.py
eval/claude-3.7.py
eval/deepseek-r1.py
eval/deepseek.py
eval/gemini-1.5-flash.py
eval/gemini-2.0-flash.py
eval/gemini-2.5-preview.py
eval/gpt-4.1.py
eval/gpt-4o-no-boundingbox.py
eval/gpt-4o-no-vision.py
eval/gpt-4o-viewport-0.py
eval/gpt-4o.py
eval/gpt-o4-mini.py
eval/grok.py
eval/service.py
examples/browser/real_browser.py
examples/browser/stealth.py
examples/browser/using_cdp.py
examples/custom-functions/action_filters.py
examples/custom-functions/advanced_search.py
examples/custom-functions/clipboard.py
examples/custom-functions/custom_hooks_before_after_step.py
examples/custom-functions/file_upload.py
examples/custom-functions/group_ungroup.py
examples/custom-functions/hover_element.py
examples/custom-functions/notification.py
examples/custom-functions/onepassword_2fa.py
examples/custom-functions/save_to_file_hugging_face.py
examples/features/click_fallback_options.py
examples/features/cross_origin_iframes.py
examples/features/custom_output.py
examples/features/custom_system_prompt.py
examples/features/custom_user_agent.py
examples/features/download_file.py
examples/features/drag_drop.py
examples/features/follow_up_tasks.py
examples/features/initial_actions.py
examples/features/multi-tab_handling.py
examples/features/multiple_agents_same_browser.py
examples/features/outsource_state.py
examples/features/parallel_agents.py
examples/features/pause_resume.py
examples/features/planner.py
examples/features/vision_enabled.py
examples/n8n/advanced_usage.json
examples/n8n/browser_use_node.ipynb
examples/n8n/local_server.py
examples/n8n/minimal.json
examples/pydantic_models.py
examples/quickstart.py
examples/README.md
examples/telemetry/custom_events.py
examples/telemetry/disable_telemetry.py
examples/telemetry/inspect_event_stream.py
examples/telemetry/using_callbacks.py
extension-showcase/screenshot.png
images/architecture.png
images/archvie.png
images/browser-use-overview.png
images/browser-use.gif
images/cloud/function_calling.png
images/cloud/zapier.png
images/icon_128.png
images/icon_16.png
images/icon_32.png
images/icon_48.png
images/logo.png
images/n8n-workflow.png
images/playwright-trace.png
images/thumbnail.png
images/trace.zip
images/web-arena.png
LICENSE
logger-config.yaml
main.py
manifest.json
poetry.lock
PROJECT_DOCS/CURRENT_PROJECT.md
PROJECT_DOCS/CURRENT_PROJECT_GOAL.md
PROJECT_DOCS/CURRENT_PROJECT_STATE.md
PROJECT_DOCS/CURRENT_PROJECT_TASK.md
pyproject.toml
python_logging_quickstart.ipynb
README.md
repomix-output.md
requirements.txt
run_test.py
scripts/create_tags.sh
scripts/generate_docs.py
scripts/generate_schema.py
scripts/prepare_archive.sh
scripts/publish_alpha.sh
scripts/setup_git_hooks.sh
scripts/update_version.py
SECURITY.md
setup.py
```

## Implementation Steps

### Step 1: Create Enhanced Element Identification System
- Modify the `buildDomTreeWithMappings` function in `browser_use_ext/extension/content.js` to generate stable element IDs
- Implement a robust XPath generation algorithm that creates unique, stable identifiers for actionable elements
- Add element visibility detection and interactive element classification logic
- Create utility functions for determining available operations based on element type and properties

### Step 2: Refactor State Generation Logic
- Update the `handleGetState` function in `browser_use_ext/extension/content.js` to return `actionable_elements` instead of `selectorMap`
- Implement element filtering logic to identify truly actionable elements (visible, interactive, content-rich)
- Add metadata collection for each element including type, tag, text content, attributes, and visibility status
- Ensure the new state structure aligns with the specifications in `PROJECT_DOCS/CURRENT_PROJECT_GOAL.md`

### Step 3: Modernize Action Execution Framework
- Refactor the `handleExecuteAction` function in `browser_use_ext/extension/content.js` to accept `element_id` parameters
- Implement element resolution logic that can convert string-based element IDs back to DOM elements
- Update all action handler functions (`click_element_by_index`, `input_text`, etc.) to use the new element identification system
- Generalize action names to remove index-based naming conventions

### Step 4: Update Message Interface
- Modify message handling in `browser_use_ext/extension/content.js` to support the new element ID-based action parameters
- Ensure compatibility with `browser_use_ext/extension/background.js` for message forwarding
- Update action parameter validation to work with string-based element identifiers
- Maintain backward compatibility during the transition period

### Step 5: Implement Error Handling and Fallbacks
- Add robust error handling for element resolution failures
- Implement fallback mechanisms when string-based element IDs cannot be resolved
- Create logging and debugging utilities for troubleshooting element identification issues
- Add validation to ensure element IDs are properly formatted and resolvable

## Code Snippets

### Enhanced Element ID Generation

```javascript
// Enhanced element identification system
function generateStableElementId(element) {
    // Try multiple strategies for generating stable IDs
    const strategies = [
        () => generateIdByUniqueAttributes(element),
        () => generateIdByStructuralPosition(element),
        () => generateIdByXPath(element),
        () => generateIdByTextContent(element)
    ];
    
    for (const strategy of strategies) {
        const id = strategy();
        if (id && isIdUnique(id)) {
            return id;
        }
    }
    
    // Fallback to timestamp-based ID (not ideal for stability)
    return `element_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function generateIdByUniqueAttributes(element) {
    const uniqueAttrs = ['id', 'name', 'data-testid', 'aria-label'];
    
    for (const attr of uniqueAttrs) {
        const value = element.getAttribute(attr);
        if (value && value.trim()) {
            const id = `attr_${attr}_${value}`;
            if (isIdUnique(id)) {
                return id;
            }
        }
    }
    return null;
}

function generateIdByStructuralPosition(element) {
    const path = [];
    let current = element;
    
    while (current && current !== document.body) {
        const siblings = Array.from(current.parentNode?.children || []);
        const index = siblings.indexOf(current);
        const tagName = current.tagName.toLowerCase();
        path.unshift(`${tagName}[${index}]`);
        current = current.parentNode;
    }
    
    return path.length > 0 ? `struct_${path.join('_')}` : null;
}

function generateIdByXPath(element) {
    let path = '';
    let node = element;
    
    while (node && node.nodeType === Node.ELEMENT_NODE && node !== document.documentElement) {
        const tagName = node.tagName.toLowerCase();
        const siblings = Array.from(node.parentNode.children).filter(e => e.tagName === node.tagName);
        const index = siblings.indexOf(node) + 1;
        
        if (siblings.length > 1) {
            path = `/${tagName}[${index}]${path}`;
        } else {
            path = `/${tagName}${path}`;
        }
        
        node = node.parentNode;
    }
    
    return `xpath_${path}`;
}

function generateIdByTextContent(element) {
    const text = element.textContent?.trim();
    if (text && text.length > 0 && text.length  {
    let mockElement;
    
    beforeEach(() => {
        document.body.innerHTML = '';
        mockElement = document.createElement('div');
        document.body.appendChild(mockElement);
    });
    
    afterEach(() => {
        document.body.innerHTML = '';
    });
    
    test('should generate ID from unique attributes when available', () => {
        mockElement.setAttribute('id', 'unique-button');
        const id = generateStableElementId(mockElement);
        expect(id).toBe('attr_id_unique-button');
    });
    
    test('should generate structural position ID when unique attributes unavailable', () => {
        const parent = document.createElement('section');
        const child = document.createElement('button');
        parent.appendChild(child);
        document.body.appendChild(parent);
        
        const id = generateStableElementId(child);
        expect(id).toMatch(/^struct_section\[\d+\]_button\[\d+\]$/);
    });
    
    test('should generate XPath-based ID for complex elements', () => {
        const nav = document.createElement('nav');
        const ul = document.createElement('ul');
        const li = document.createElement('li');
        nav.appendChild(ul);
        ul.appendChild(li);
        document.body.appendChild(nav);
        
        const id = generateStableElementId(li);
        expect(id).toBe('xpath_/nav/ul/li');
    });
    
    test('should generate text-based ID for elements with unique text content', () => {
        mockElement.textContent = 'Submit Form';
        const id = generateStableElementId(mockElement);
        expect(id).toBe('text_Submit_Form');
    });
    
    test('should handle elements with no identifying features gracefully', () => {
        const id = generateStableElementId(mockElement);
        expect(id).toMatch(/^element_\d+_[a-z0-9]+$/);
    });
    
    test('should ensure generated IDs are unique within document', () => {
        const element1 = document.createElement('div');
        const element2 = document.createElement('div');
        element1.setAttribute('class', 'test');
        element2.setAttribute('class', 'test');
        document.body.appendChild(element1);
        document.body.appendChild(element2);
        
        const id1 = generateStableElementId(element1);
        const id2 = generateStableElementId(element2);
        expect(id1).not.toBe(id2);
    });
});
```

### Actionable Elements Detection

```javascript
// Enhanced actionable elements detection
function detectActionableElements() {
    const actionableElements = [];
    const allElements = document.querySelectorAll('*');
    
    for (const element of allElements) {
        if (isElementActionable(element)) {
            const elementData = {
                id: generateStableElementId(element),
                type: getElementType(element),
                tag: element.tagName.toLowerCase(),
                text_content: getElementTextContent(element),
                attributes: getRelevantAttributes(element),
                is_visible: isElementVisible(element),
                available_operations: getAvailableOperations(element)
            };
            
            actionableElements.push(elementData);
            // Mark element with generated ID for future reference
            element.setAttribute('data-element-id', elementData.id);
        }
    }
    
    return actionableElements;
}

function isElementActionable(element) {
    // Check if element is interactive
    const interactiveTags = ['a', 'button', 'input', 'select', 'textarea', 'label'];
    const interactiveRoles = ['button', 'link', 'textbox', 'checkbox', 'radio', 'combobox'];
    
    if (interactiveTags.includes(element.tagName.toLowerCase())) {
        return true;
    }
    
    const role = element.getAttribute('role');
    if (role && interactiveRoles.includes(role)) {
        return true;
    }
    
    // Check for click handlers
    if (element.onclick || element.hasAttribute('onclick')) {
        return true;
    }
    
    // Check for elements with tabindex (potentially focusable)
    if (element.hasAttribute('tabindex') && element.getAttribute('tabindex') !== '-1') {
        return true;
    }
    
    // Check for content-rich elements (for text extraction)
    const contentTags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div'];
    if (contentTags.includes(element.tagName.toLowerCase()) && element.textContent.trim().length > 10) {
        return true;
    }
    
    return false;
}

function getElementType(element) {
    const tag = element.tagName.toLowerCase();
    const type = element.getAttribute('type');
    const role = element.getAttribute('role');
    
    if (tag === 'input') {
        return type || 'text';
    }
    
    if (role) {
        return role;
    }
    
    const typeMap = {
        'a': 'link',
        'button': 'button',
        'select': 'dropdown',
        'textarea': 'textarea',
        'img': 'image',
        'form': 'form'
    };
    
    return typeMap[tag] || 'element';
}

function getElementTextContent(element) {
    let text = element.textContent?.trim() || '';
    
    // For input elements, get value or placeholder
    if (element.tagName.toLowerCase() === 'input') {
        text = element.value || element.getAttribute('placeholder') || '';
    }
    
    // For images, get alt text
    if (element.tagName.toLowerCase() === 'img') {
        text = element.getAttribute('alt') || element.getAttribute('title') || '';
    }
    
    // Limit text length to prevent overly long content
    return text.length > 200 ? text.substring(0, 200) + '...' : text;
}

function getRelevantAttributes(element) {
    const relevantAttrs = ['id', 'class', 'name', 'type', 'role', 'aria-label', 'title', 'href', 'src', 'alt'];
    const attributes = {};
    
    for (const attr of relevantAttrs) {
        const value = element.getAttribute(attr);
        if (value !== null) {
            attributes[attr] = value;
        }
    }
    
    return attributes;
}

function isElementVisible(element) {
    const style = window.getComputedStyle(element);
    
    return style.display !== 'none' && 
           style.visibility !== 'hidden' && 
           style.opacity !== '0' &&
           element.offsetWidth > 0 && 
           element.offsetHeight > 0;
}

function getAvailableOperations(element) {
    const operations = [];
    const tag = element.tagName.toLowerCase();
    const type = element.getAttribute('type');
    
    // All visible elements can potentially be clicked
    if (isElementVisible(element)) {
        operations.push('click');
    }
    
    // Input operations
    if (tag === 'input' || tag === 'textarea') {
        if (type !== 'checkbox' && type !== 'radio' && type !== 'submit' && type !== 'button') {
            operations.push('input_text', 'clear');
        }
        if (type === 'checkbox' || type === 'radio') {
            operations.push('check', 'uncheck');
        }
    }
    
    // Selection operations
    if (tag === 'select') {
        operations.push('select_option');
    }
    
    // Navigation operations
    if (tag === 'a' && element.getAttribute('href')) {
        operations.push('navigate');
    }
    
    // Scroll operations for scrollable elements
    if (element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth) {
        operations.push('scroll');
    }
    
    // Hover operations for interactive elements
    if (operations.length > 0) {
        operations.push('hover');
    }
    
    return operations;
}
```

### Actionable Elements Detection Unit Tests

```javascript
// detectActionableElements.test.js
describe('detectActionableElements', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
    });
    
    test('should detect button elements as actionable', () => {
        const button = document.createElement('button');
        button.textContent = 'Click me';
        document.body.appendChild(button);
        
        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].tag).toBe('button');
        expect(elements[0].type).toBe('button');
        expect(elements[0].available_operations).toContain('click');
    });
    
    test('should detect input elements with appropriate operations', () => {
        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Enter text';
        document.body.appendChild(input);
        
        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].type).toBe('text');
        expect(elements[0].available_operations).toContain('input_text');
        expect(elements[0].available_operations).toContain('clear');
    });
    
    test('should detect links with navigation operations', () => {
        const link = document.createElement('a');
        link.href = 'https://example.com';
        link.textContent = 'Visit Example';
        document.body.appendChild(link);
        
        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].type).toBe('link');
        expect(elements[0].available_operations).toContain('navigate');
        expect(elements[0].attributes.href).toBe('https://example.com');
    });
    
    test('should filter out hidden elements', () => {
        const visibleButton = document.createElement('button');
        visibleButton.textContent = 'Visible';
        
        const hiddenButton = document.createElement('button');
        hiddenButton.textContent = 'Hidden';
        hiddenButton.style.display = 'none';
        
        document.body.appendChild(visibleButton);
        document.body.appendChild(hiddenButton);
        
        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].text_content).toBe('Visible');
    });
    
    test('should detect content-rich elements', () => {
        const heading = document.createElement('h1');
        heading.textContent = 'This is a significant heading with enough content';
        document.body.appendChild(heading);
        
        const elements = detectActionableElements();
        expect(elements).toHaveLength(1);
        expect(elements[0].tag).toBe('h1');
        expect(elements[0].text_content).toContain('significant heading');
    });
    
    test('should assign unique IDs to each element', () => {
        const button1 = document.createElement('button');
        const button2 = document.createElement('button');
        button1.textContent = 'Button 1';
        button2.textContent = 'Button 2';
        document.body.appendChild(button1);
        document.body.appendChild(button2);
        
        const elements = detectActionableElements();
        expect(elements).toHaveLength(2);
        expect(elements[0].id).not.toBe(elements[1].id);
        expect(button1.getAttribute('data-element-id')).toBe(elements[0].id);
        expect(button2.getAttribute('data-element-id')).toBe(elements[1].id);
    });
});
```

### Enhanced Action Execution System

```javascript
// Enhanced action execution with element ID resolution
function handleExecuteAction(request) {
    const { action, params } = request;
    
    try {
        // Resolve element using the new string-based ID system
        const element = resolveElementById(params.element_id);
        if (!element) {
            return {
                success: false,
                error: `Element with ID '${params.element_id}' not found or no longer exists`
            };
        }
        
        // Execute action using modernized action names
        switch (action) {
            case 'click':
                return executeClick(element, params);
            case 'input_text':
                return executeInputText(element, params);
            case 'clear':
                return executeClear(element, params);
            case 'select_option':
                return executeSelectOption(element, params);
            case 'scroll':
                return executeScroll(element, params);
            case 'hover':
                return executeHover(element, params);
            case 'check':
            case 'uncheck':
                return executeCheckbox(element, params, action === 'check');
            case 'navigate':
                return executeNavigate(element, params);
            default:
                return {
                    success: false,
                    error: `Unknown action: ${action}`
                };
        }
    } catch (error) {
        console.error('Error executing action:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

function resolveElementById(elementId) {
    if (!elementId) {
        throw new Error('Element ID is required');
    }
    
    // First try to find element by our custom data attribute
    let element = document.querySelector(`[data-element-id="${elementId}"]`);
    if (element) {
        return element;
    }
    
    // If not found, try to resolve by ID strategy
    if (elementId.startsWith('attr_id_')) {
        const id = elementId.replace('attr_id_', '');
        element = document.getElementById(id);
    } else if (elementId.startsWith('xpath_')) {
        const xpath = elementId.replace('xpath_', '');
        element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    } else if (elementId.startsWith('struct_')) {
        element = resolveStructuralPath(elementId);
    } else if (elementId.startsWith('text_')) {
        element = resolveByTextContent(elementId);
    }
    
    return element;
}

function resolveStructuralPath(elementId) {
    const path = elementId.replace('struct_', '').split('_');
    let current = document.body;
    
    for (const segment of path) {
        const match = segment.match(/^(\w+)\[(\d+)\]$/);
        if (!match) break;
        
        const [, tagName, index] = match;
        const children = Array.from(current.children).filter(
            child => child.tagName.toLowerCase() === tagName
        );
        
        if (children[parseInt(index)]) {
            current = children[parseInt(index)];
        } else {
            return null;
        }
    }
    
    return current !== document.body ? current : null;
}

function resolveByTextContent(elementId) {
    const textKey = elementId.replace('text_', '').replace(/_/g, ' ');
    const elements = Array.from(document.querySelectorAll('*'));
    
    return elements.find(element => {
        const text = element.textContent?.trim().toLowerCase();
        return text && text.includes(textKey.toLowerCase());
    });
}

function executeClick(element, params) {
    try {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Wait a brief moment for scroll to complete
        setTimeout(() => {
            element.click();
        }, 100);
        
        return { success: true, message: `Clicked element ${element.tagName}` };
    } catch (error) {
        return { success: false, error: `Failed to click element: ${error.message}` };
    }
}

function executeInputText(element, params) {
    try {
        const { text } = params;
        if (typeof text !== 'string') {
            return { success: false, error: 'Text parameter must be a string' };
        }
        
        element.focus();
        element.value = text;
        
        // Trigger input and change events
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
        
        return { success: true, message: `Input text: "${text}"` };
    } catch (error) {
        return { success: false, error: `Failed to input text: ${error.message}` };
    }
}

function executeClear(element, params) {
    try {
        element.focus();
        element.value = '';
        
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
        
        return { success: true, message: 'Cleared element content' };
    } catch (error) {
        return { success: false, error: `Failed to clear element: ${error.message}` };
    }
}

function executeSelectOption(element, params) {
    try {
        const { option } = params;
        if (!option) {
            return { success: false, error: 'Option parameter is required' };
        }
        
        // Try to find option by text content or value
        const options = Array.from(element.options);
        const targetOption = options.find(opt => 
            opt.textContent.trim() === option || opt.value === option
        );
        
        if (!targetOption) {
            return { success: false, error: `Option "${option}" not found` };
        }
        
        element.value = targetOption.value;
        element.dispatchEvent(new Event('change', { bubbles: true }));
        
        return { success: true, message: `Selected option: ${option}` };
    } catch (error) {
        return { success: false, error: `Failed to select option: ${error.message}` };
    }
}

function executeScroll(element, params) {
    try {
        const { direction = 'down', amount = 300 } = params;
        
        const scrollOptions = {
            behavior: 'smooth'
        };
        
        switch (direction) {
            case 'down':
                element.scrollBy({ top: amount, ...scrollOptions });
                break;
            case 'up':
                element.scrollBy({ top: -amount, ...scrollOptions });
                break;
            case 'left':
                element.scrollBy({ left: -amount, ...scrollOptions });
                break;
            case 'right':
                element.scrollBy({ left: amount, ...scrollOptions });
                break;
            default:
                return { success: false, error: `Invalid scroll direction: ${direction}` };
        }
        
        return { success: true, message: `Scrolled ${direction} by ${amount}px` };
    } catch (error) {
        return { success: false, error: `Failed to scroll: ${error.message}` };
    }
}

function executeHover(element, params) {
    try {
        const hoverEvent = new MouseEvent('mouseover', {
            bubbles: true,
            cancelable: true,
            view: window
        });
        
        element.dispatchEvent(hoverEvent);
        return { success: true, message: 'Hovered over element' };
    } catch (error) {
        return { success: false, error: `Failed to hover: ${error.message}` };
    }
}

function executeCheckbox(element, params, shouldCheck) {
    try {
        if (element.checked === shouldCheck) {
            return { 
                success: true, 
                message: `Element is already ${shouldCheck ? 'checked' : 'unchecked'}` 
            };
        }
        
        element.checked = shouldCheck;
        element.dispatchEvent(new Event('change', { bubbles: true }));
        
        return { 
            success: true, 
            message: `${shouldCheck ? 'Checked' : 'Unchecked'} element` 
        };
    } catch (error) {
        return { 
            success: false, 
            error: `Failed to ${shouldCheck ? 'check' : 'uncheck'} element: ${error.message}` 
        };
    }
}

function executeNavigate(element, params) {
    try {
        const href = element.getAttribute('href');
        if (!href) {
            return { success: false, error: 'Element has no href attribute' };
        }
        
        element.click();
        return { success: true, message: `Navigating to: ${href}` };
    } catch (error) {
        return { success: false, error: `Failed to navigate: ${error.message}` };
    }
}
```

### Action Execution Unit Tests

```javascript
// handleExecuteAction.test.js
describe('handleExecuteAction', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
    });
    
    test('should execute click action successfully', () => {
        const button = document.createElement('button');
        button.setAttribute('data-element-id', 'test-button');
        button.textContent = 'Test Button';
        document.body.appendChild(button);
        
        const request = {
            action: 'click',
            params: { element_id: 'test-button' }
        };
        
        const result = handleExecuteAction(request);
        expect(result.success).toBe(true);
        expect(result.message).toContain('Clicked element BUTTON');
    });
    
    test('should execute input_text action successfully', () => {
        const input = document.createElement('input');
        input.type = 'text';
        input.setAttribute('data-element-id', 'test-input');
        document.body.appendChild(input);
        
        const request = {
            action: 'input_text',
            params: { 
                element_id: 'test-input',
                text: 'Hello World'
            }
        };
        
        const result = handleExecuteAction(request);
        expect(result.success).toBe(true);
        expect(input.value).toBe('Hello World');
    });
    
    test('should handle element not found gracefully', () => {
        const request = {
            action: 'click',
            params: { element_id: 'nonexistent-element' }
        };
        
        const result = handleExecuteAction(request);
        expect(result.success).toBe(false);
        expect(result.error).toContain('not found');
    });
    
    test('should execute select_option action successfully', () => {
        const select = document.createElement('select');
        const option1 = document.createElement('option');
        const option2 = document.createElement('option');
        
        option1.value = 'value1';
        option1.textContent = 'Option 1';
        option2.value = 'value2';
        option2.textContent = 'Option 2';
        
        select.appendChild(option1);
        select.appendChild(option2);
        select.setAttribute('data-element-id', 'test-select');
        document.body.appendChild(select);
        
        const request = {
            action: 'select_option',
            params: { 
                element_id: 'test-select',
                option: 'Option 2'
            }
        };
        
        const result = handleExecuteAction(request);
        expect(result.success).toBe(true);
        expect(select.value).toBe('value2');
    });
    
    test('should execute checkbox actions successfully', () => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.setAttribute('data-element-id', 'test-checkbox');
        document.body.appendChild(checkbox);
        
        // Test check
        let request = {
            action: 'check',
            params: { element_id: 'test-checkbox' }
        };
        
        let result = handleExecuteAction(request);
        expect(result.success).toBe(true);
        expect(checkbox.checked).toBe(true);
        
        // Test uncheck
        request = {
            action: 'uncheck',
            params: { element_id: 'test-checkbox' }
        };
        
        result = handleExecuteAction(request);
        expect(result.success).toBe(true);
        expect(checkbox.checked).toBe(false);
    });
    
    test('should handle unknown actions gracefully', () => {
        const button = document.createElement('button');
        button.setAttribute('data-element-id', 'test-button');
        document.body.appendChild(button);
        
        const request = {
            action: 'unknown_action',
            params: { element_id: 'test-button' }
        };
        
        const result = handleExecuteAction(request);
        expect(result.success).toBe(false);
        expect(result.error).toContain('Unknown action');
    });
});
```

### Updated State Handler

```javascript
// Updated handleGetState function
function handleGetState() {
    try {
        const actionableElements = detectActionableElements();
        
        const pageState = {
            url: window.location.href,
            title: document.title,
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            scroll_position: {
                x: window.scrollX,
                y: window.scrollY
            },
            actionable_elements: actionableElements,
            page_metrics: {
                total_elements: document.querySelectorAll('*').length,
                actionable_count: actionableElements.length,
                visible_count: actionableElements.filter(el => el.is_visible).length
            },
            timestamp: new Date().toISOString()
        };
        
        // Send state back to background script
        chrome.runtime.sendMessage({
            type: 'state_response',
            state: pageState
        });
        
        console.log(`State extracted: ${actionableElements.length} actionable elements found`);
        return pageState;
        
    } catch (error) {
        console.error('Error extracting page state:', error);
        chrome.runtime.sendMessage({
            type: 'state_error',
            error: error.message
        });
        throw error;
    }
}
```

### State Handler Unit Tests

```javascript
// handleGetState.test.js
describe('handleGetState', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
        // Mock chrome.runtime.sendMessage
        global.chrome = {
            runtime: {
                sendMessage: jest.fn()
            }
        };
    });
    
    afterEach(() => {
        delete global.chrome;
    });
    
    test('should extract basic page state correctly', () => {
        document.title = 'Test Page';
        
        const button = document.createElement('button');
        button.textContent = 'Test Button';
        document.body.appendChild(button);
        
        const state = handleGetState();
        
        expect(state.title).toBe('Test Page');
        expect(state.url).toBe('about:blank');
        expect(state.actionable_elements).toHaveLength(1);
        expect(state.actionable_elements[0].tag).toBe('button');
        expect(state.page_metrics.actionable_count).toBe(1);
    });
    
    test('should include viewport and scroll information', () => {
        // Mock window dimensions
        Object.defineProperty(window, 'innerWidth', { value: 1024 });
        Object.defineProperty(window, 'innerHeight', { value: 768 });
        Object.defineProperty(window, 'scrollX', { value: 100 });
        Object.defineProperty(window, 'scrollY', { value: 200 });
        
        const state = handleGetState();
        
        expect(state.viewport.width).toBe(1024);
        expect(state.viewport.height).toBe(768);
        expect(state.scroll_position.x).toBe(100);
        expect(state.scroll_position.y).toBe(200);
    });
    
    test('should handle empty pages gracefully', () => {
        const state = handleGetState();
        
        expect(state.actionable_elements).toHaveLength(0);
        expect(state.page_metrics.actionable_count).toBe(0);
        expect(state.page_metrics.visible_count).toBe(0);
    });
    
    test('should send state via chrome.runtime.sendMessage', () => {
        handleGetState();
        
        expect(chrome.runtime.sendMessage).toHaveBeenCalledWith(
            expect.objectContaining({
                type: 'state_response',
                state: expect.any(Object)
            })
        );
    });
    
    test('should handle errors and send error message', () => {
        // Force an error by making document.querySelectorAll throw
        const originalQuerySelectorAll = document.querySelectorAll;
        document.querySelectorAll = jest.fn(() => {
            throw new Error('Test error');
        });
        
        expect(() => handleGetState()).toThrow('Test error');
        
        expect(chrome.runtime.sendMessage).toHaveBeenCalledWith(
            expect.objectContaining({
                type: 'state_error',
                error: 'Test error'
            })
        );
        
        // Restore original function
        document.querySelectorAll = originalQuerySelectorAll;
    });
    
    test('should include timestamp in state', () => {
        const state = handleGetState();
        
        expect(state.timestamp).toBeDefined();
        expect(new Date(state.timestamp)).toBeInstanceOf(Date);
    });
});
```

## error-tasks.md

**Cursor AI is required to check off each of the following tasks as they are completed. This is the single source of truth.**

- [ ] Replace the existing `buildDomTreeWithMappings` function in `browser_use_ext/extension/content.js` with the new `detectActionableElements` function
- [ ] Update the `handleGetState` function in `browser_use_ext/extension/content.js` to use the new actionable elements structure instead of selectorMap
- [ ] Implement the `generateStableElementId` function in `browser_use_ext/extension/content.js` with all four ID generation strategies
- [ ] Add the `resolveElementById` function to `browser_use_ext/extension/content.js` for converting string IDs back to DOM elements
- [ ] Refactor the `handleExecuteAction` function in `browser_use_ext/extension/content.js` to use element_id parameters instead of highlight_index
- [ ] Update all individual action handler functions (`click_element_by_index`, `input_text`, etc.) in `browser_use_ext/extension/content.js` to work with the new element resolution system
- [ ] Rename action handler functions to use generalized names (remove "_by_index" suffixes) in `browser_use_ext/extension/content.js`
- [ ] Add comprehensive error handling for element resolution failures in `browser_use_ext/extension/content.js`
- [ ] Implement element visibility detection (`isElementVisible` function) in `browser_use_ext/extension/content.js`
- [ ] Add available operations detection (`getAvailableOperations` function) in `browser_use_ext/extension/content.js`
- [ ] Create unit test file `browser_use_ext/tests/test_element_id_generation.js` for the element ID generation system
- [ ] Create unit test file `browser_use_ext/tests/test_actionable_elements.js` for the actionable elements detection
- [ ] Create unit test file `browser_use_ext/tests/test_action_execution.js` for the updated action execution system
- [ ] Create unit test file `browser_use_ext/tests/test_state_handler.js` for the updated state handling
- [ ] Update message handling in `browser_use_ext/extension/content.js` to support the new element_id parameter structure
- [ ] Verify compatibility between `browser_use_ext/extension/content.js` and `browser_use_ext/extension/background.js` for message forwarding
- [ ] Add element ID uniqueness validation functions in `browser_use_ext/extension/content.js`
- [ ] Implement fallback mechanisms for when element IDs cannot be resolved in `browser_use_ext/extension/content.js`
- [ ] Add logging and debugging utilities for element identification troubleshooting in `browser_use_ext/extension/content.js`
- [ ] Test the complete refactored system with a sample webpage to ensure all functionality works correctly

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/63074468/37431bd6-ace5-4db3-a3c6-5180e6480c85/paste.txt
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/63074468/82fc60d2-1c0a-44e7-b2e0-ba27a06933ce/repomix-output.md
[3] https://github.com/rexgarland/markdown-plan
[4] https://whatfix.com/blog/software-implementation/
[5] https://www.implementationpractice.org/wp-content/uploads/2021/05/NIRN-CIP-Implementation-Plan-Template-and-Examples-fillable-v1.pdf
[6] https://technologyadvice.com/blog/information-technology/software-implementation-timeline/
[7] https://docs.runmyprocess.com/Developer_Guide_DigitalSuite/Appendix/Process_Utilities/Markdown_Template/
[8] https://www.techsmith.com/blog/software-rollout/
[9] https://www.atlassian.com/software/confluence/templates/project-plan
[10] https://github.com/mgsloan/8760-hours-template
[11] https://the.fibery.io/@public/User_Guide/Guide/Markdown-Templates-53
[12] https://marketplace.visualstudio.com/items?itemName=maziac.markdown-planner

---
Answer from Perplexity: pplx.ai/share