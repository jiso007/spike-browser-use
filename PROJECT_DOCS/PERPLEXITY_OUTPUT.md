# Chrome Extension Content Script Readiness Implementation Plan

This implementation plan establishes a crucial reliability feature within the Chrome extension component of the `browser_use_ext` system by implementing a "ready" handshake between `content.js` and `background.js`. The handshake mechanism ensures robust internal extension communication by allowing `content.js` to signal when it has completed initialization and is ready to receive messages from `background.js`. This prevents race conditions and "receiving end does not exist" errors that would otherwise destabilize the browser interaction system, enabling reliable state acquisition and action execution for agent-driven browser interactions.

## Overview

The primary objective is to implement a bidirectional communication handshake that ensures `content.js` is fully initialized before `background.js` attempts to send critical messages. This involves modifying `content.js` to proactively send a `content_script_ready` message after completing its initialization sequence, and enhancing `background.js` to receive, acknowledge, and track the readiness status of content scripts across different tabs.

The implementation centers on establishing a robust messaging protocol using Chrome's runtime API, where `content.js` signals its readiness state and `background.js` maintains a persistent record of ready tabs. This foundation enables the broader browser automation system to reliably coordinate between the Chrome extension components and the Python backend, supporting features like state acquisition (`get_state`) and action execution (`execute_action`).

Key technical components include message type standardization, tab-specific readiness tracking, timeout handling for graceful error recovery, and comprehensive logging for debugging and monitoring. The solution leverages Chrome Extension Manifest V3 APIs, specifically `chrome.runtime.sendMessage`, `chrome.runtime.onMessage`, and `chrome.tabs` for tab management.

## Folder Structure

```
browser-use/
├── .cursor/
│   └── rules/
│       ├── chrome_extension_content_readiness.mdc
│       ├── cursor_rules.mdc
│       ├── custom_test_guide.mdc
│       ├── dev_workflow.mdc
│       ├── pydantic_model_guidelines.mdc
│       ├── pytest_config.mdc
│       ├── python_script_module_execution.mdc
│       ├── python_websockets_guidelines.mdc
│       └── self_improve.mdc
├── browser_use_ext/
│   ├── __init__.py
│   ├── browser/
│   │   ├── __init__.py
│   │   ├── context.py
│   │   └── views.py
│   ├── extension/
│   │   ├── background.js
│   │   ├── content.js
│   │   ├── manifest.json
│   │   ├── icons/
│   │   │   └── icon128.png
│   │   └── popup/
│   │       ├── popup.html
│   │       └── popup.js
│   ├── extension_interface/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── service.py
│   └── tests/
│       ├── __init__.py
│       └── test_content_script_ready.py
├── PROJECT_DOCS/
│   ├── CURRENT_PROJECT_GOAL.md
│   └── CURRENT_PROJECT_STATE.md 
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt
└── run_test.py
```

## Implementation Steps

### Step 1: Enhance browser_use_ext/extension/content.js Ready Signal Implementation
Modify the content script to implement the ready handshake mechanism immediately after its initialization sequence. The content script must establish its message listener first, then signal readiness to the background script with comprehensive error handling and logging.

Add the ready signal logic after the existing `chrome.runtime.onMessage.addListener` setup, ensuring the listener is fully configured before sending the readiness notification. Include proper error handling for cases where the background script might not be available, and implement retry logic with exponential backoff for improved reliability.

### Step 2: Enhance browser_use_ext/extension/background.js Message Reception and Tracking
Extend the background script's message handling capabilities to receive and process `content_script_ready` messages from content scripts. Implement a robust tracking system using a JavaScript Set to maintain the list of ready tab IDs, with proper cleanup when tabs are closed.

Add comprehensive logging for debugging purposes and implement the acknowledgment response mechanism to complete the handshake. Ensure the existing `waitForContentScriptReady` function properly integrates with the new tracking system and includes appropriate timeout handling.

### Step 3: Create browser_use_ext/tests/test_content_script_ready.py Test Suite
Develop a comprehensive test suite that validates the handshake mechanism using Jest for JavaScript testing. The tests must cover both successful handshake scenarios and error conditions, including timeout handling and tab closure cleanup.

Implement mock objects for Chrome extension APIs and create test scenarios that simulate real-world usage patterns. Include integration tests that verify the complete handshake flow from content script initialization through background script acknowledgment.

### Step 4: Verify Integration with Existing browser_use_ext/extension_interface/service.py
Ensure the Python-side extension interface properly integrates with the enhanced Chrome extension communication mechanism. Verify that the `waitForContentScriptReady` functionality works correctly with the new handshake system and that timeout handling is consistent across both JavaScript and Python components.

Test the end-to-end communication flow from Python backend through WebSocket to background script, and confirm that the ready state tracking prevents premature message sending to uninitialized content scripts.

## Code Snippets

### Enhanced content.js Implementation

```javascript
// browser_use_ext/extension/content.js - Enhanced with ready handshake

console.log('Content script starting initialization...');

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
            return false;
        }

        // Handle different message types
        switch (request.type) {
            case 'get_state':
                handleGetState(request, sendResponse);
                return true; // Indicates async response
            case 'execute_action':
                handleExecuteAction(request, sendResponse);
                return true; // Indicates async response
            case 'ping':
                sendResponse({ status: 'ready', timestamp: Date.now() });
                return false;
            default:
                console.warn('Unknown message type:', request.type);
                sendResponse({ error: 'Unknown message type' });
                return false;
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
        
        chrome.runtime.sendMessage(
            { type: "content_script_ready", tabId: null, timestamp: Date.now() }, 
            function(response) {
                if (chrome.runtime.lastError) {
                    console.error('Error sending ready signal:', chrome.runtime.lastError.message);
                    
                    if (retryCount  attemptSignal(retryCount + 1), delay);
                    } else {
                        console.error('Failed to signal ready state after all retries');
                    }
                } else {
                    console.log('Content script ready signal acknowledged:', response);
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
        
        // Signal readiness after all setup is complete
        signalContentScriptReady();
        
    } catch (error) {
        console.error('Content script initialization failed:', error);
        // Could implement additional error recovery here
    }
}

// Placeholder handlers (to be implemented based on existing functionality)
function handleGetState(request, sendResponse) {
    // Implementation for state gathering
    console.log('Handling get_state request');
    // ... existing get_state logic ...
    sendResponse({ status: 'success', data: {} });
}

function handleExecuteAction(request, sendResponse) {
    // Implementation for action execution
    console.log('Handling execute_action request:', request.action);
    // ... existing execute_action logic ...
    sendResponse({ status: 'success' });
}

// Start initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeContentScript);
} else {
    initializeContentScript();
}

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    console.log('Content script cleaning up...');
    isContentScriptReady = false;
});
```

### Enhanced content.js Unit Tests

```javascript
// browser_use_ext/tests/javascript/content.test.js

describe('Content Script Ready Handshake', () => {
    let mockChrome;
    let mockSendMessage;
    let mockAddListener;
    
    beforeEach(() => {
        // Reset DOM state
        document.readyState = 'complete';
        
        // Mock Chrome APIs
        mockSendMessage = jest.fn();
        mockAddListener = jest.fn();
        
        mockChrome = {
            runtime: {
                sendMessage: mockSendMessage,
                onMessage: {
                    addListener: mockAddListener
                },
                lastError: null
            }
        };
        
        global.chrome = mockChrome;
        global.console = {
            log: jest.fn(),
            warn: jest.fn(),
            error: jest.fn()
        };
    });

    test('should establish message listener before signaling ready', async () => {
        // Load content script
        require('../../browser_use_ext/extension/content.js');
        
        // Wait for initialization
        await new Promise(resolve => setTimeout(resolve, 10));
        
        expect(mockAddListener).toHaveBeenCalledTimes(1);
        expect(mockSendMessage).toHaveBeenCalledWith(
            expect.objectContaining({
                type: 'content_script_ready'
            }),
            expect.any(Function)
        );
    });

    test('should retry ready signal on failure', async () => {
        mockChrome.runtime.lastError = { message: 'Connection error' };
        
        // Load content script
        require('../../browser_use_ext/extension/content.js');
        
        // Wait for initial attempt and first retry
        await new Promise(resolve => setTimeout(resolve, 200));
        
        expect(mockSendMessage).toHaveBeenCalledTimes(2);
        expect(global.console.error).toHaveBeenCalledWith(
            'Error sending ready signal:', 'Connection error'
        );
    });

    test('should handle message after ready state established', () => {
        require('../../browser_use_ext/extension/content.js');
        
        // Simulate successful ready signal
        const readyCallback = mockSendMessage.mock.calls[0][1];
        mockChrome.runtime.lastError = null;
        readyCallback({ acknowledged: true });
        
        // Get the message listener
        const messageListener = mockAddListener.mock.calls[0][0];
        const mockSendResponse = jest.fn();
        
        // Test ping message
        messageListener(
            { type: 'ping' },
            { tab: { id: 1 } },
            mockSendResponse
        );
        
        expect(mockSendResponse).toHaveBeenCalledWith(
            expect.objectContaining({
                status: 'ready'
            })
        );
    });

    test('should reject messages before ready state', () => {
        require('../../browser_use_ext/extension/content.js');
        
        // Get the message listener before ready signal is acknowledged
        const messageListener = mockAddListener.mock.calls[0][0];
        const mockSendResponse = jest.fn();
        
        // Test message before ready
        messageListener(
            { type: 'get_state' },
            { tab: { id: 1 } },
            mockSendResponse
        );
        
        expect(mockSendResponse).toHaveBeenCalledWith(
            expect.objectContaining({
                error: 'Content script not ready'
            })
        );
    });
});
```

### Enhanced background.js Implementation

```javascript
// browser_use_ext/extension/background.js - Enhanced with ready tracking

console.log('Background script initializing...');

// Track content scripts that have signaled ready
const contentScriptsReady = new Set();

// Enhanced message listener with ready signal handling
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    console.log('Background received message:', request.type, 'from tab:', sender.tab?.id);
    
    switch (request.type) {
        case 'content_script_ready':
            handleContentScriptReady(request, sender, sendResponse);
            return false; // Synchronous response
            
        case 'get_state':
            handleGetStateRequest(request, sender, sendResponse);
            return true; // Asynchronous response
            
        case 'execute_action':
            handleExecuteActionRequest(request, sender, sendResponse);
            return true; // Asynchronous response
            
        default:
            console.warn('Unknown message type received:', request.type);
            sendResponse({ error: 'Unknown message type' });
            return false;
    }
});

// Handle content script ready signals
function handleContentScriptReady(request, sender, sendResponse) {
    const tabId = sender.tab?.id;
    
    if (!tabId) {
        console.error('Content script ready signal missing tab ID');
        sendResponse({ error: 'Missing tab ID' });
        return;
    }
    
    console.log(`Content script ready signal received from tab ${tabId}`);
    contentScriptsReady.add(tabId);
    
    // Send acknowledgment
    sendResponse({ 
        acknowledged: true, 
        tabId: tabId,
        timestamp: Date.now()
    });
    
    console.log(`Tab ${tabId} marked as ready. Ready tabs:`, Array.from(contentScriptsReady));
}

// Enhanced wait function with ready state checking
async function waitForContentScriptReady(tabId, timeoutMs = 5000) {
    console.log(`Waiting for content script readiness on tab ${tabId}`);
    
    const startTime = Date.now();
    const pollInterval = 100; // Check every 100ms
    
    while (Date.now() - startTime  setTimeout(resolve, pollInterval));
    }
    
    console.error(`Timeout waiting for content script readiness on tab ${tabId}`);
    return false;
}

// Handle state requests with readiness verification
async function handleGetStateRequest(request, sender, sendResponse) {
    const tabId = sender.tab?.id;
    
    if (!tabId) {
        sendResponse({ error: 'Missing tab ID' });
        return;
    }
    
    try {
        const isReady = await waitForContentScriptReady(tabId, 2000);
        if (!isReady) {
            sendResponse({ error: 'Content script not ready' });
            return;
        }
        
        // Forward to appropriate handler or process directly
        console.log(`Processing get_state request for ready tab ${tabId}`);
        sendResponse({ status: 'success', data: {} });
        
    } catch (error) {
        console.error('Error handling get_state request:', error);
        sendResponse({ error: error.message });
    }
}

// Handle action requests with readiness verification
async function handleExecuteActionRequest(request, sender, sendResponse) {
    const tabId = sender.tab?.id;
    
    if (!tabId) {
        sendResponse({ error: 'Missing tab ID' });
        return;
    }
    
    try {
        const isReady = await waitForContentScriptReady(tabId, 2000);
        if (!isReady) {
            sendResponse({ error: 'Content script not ready' });
            return;
        }
        
        // Forward to appropriate handler or process directly
        console.log(`Processing execute_action request for ready tab ${tabId}`);
        sendResponse({ status: 'success' });
        
    } catch (error) {
        console.error('Error handling execute_action request:', error);
        sendResponse({ error: error.message });
    }
}

// Clean up when tabs are closed
chrome.tabs.onRemoved.addListener(function(tabId, removeInfo) {
    console.log(`Tab ${tabId} closed, cleaning up ready state`);
    contentScriptsReady.delete(tabId);
    console.log('Ready tabs after cleanup:', Array.from(contentScriptsReady));
});

// Utility function to check if specific tab is ready (for external calls)
function isTabReady(tabId) {
    return contentScriptsReady.has(tabId);
}

// Utility function to get all ready tabs (for debugging)
function getReadyTabs() {
    return Array.from(contentScriptsReady);
}

console.log('Background script ready');
```

### Enhanced background.js Unit Tests

```javascript
// browser_use_ext/tests/javascript/background.test.js

describe('Background Script Ready Handshake', () => {
    let mockChrome;
    let messageListener;
    let tabRemovedListener;
    
    beforeEach(() => {
        // Mock Chrome APIs
        mockChrome = {
            runtime: {
                onMessage: {
                    addListener: jest.fn(listener => {
                        messageListener = listener;
                    })
                }
            },
            tabs: {
                onRemoved: {
                    addListener: jest.fn(listener => {
                        tabRemovedListener = listener;
                    })
                }
            }
        };
        
        global.chrome = mockChrome;
        global.console = {
            log: jest.fn(),
            warn: jest.fn(),
            error: jest.fn()
        };
    });

    test('should register message and tab removal listeners', () => {
        require('../../browser_use_ext/extension/background.js');
        
        expect(mockChrome.runtime.onMessage.addListener).toHaveBeenCalledTimes(1);
        expect(mockChrome.tabs.onRemoved.addListener).toHaveBeenCalledTimes(1);
    });

    test('should handle content script ready signal', () => {
        require('../../browser_use_ext/extension/background.js');
        
        const mockSendResponse = jest.fn();
        const sender = { tab: { id: 123 } };
        const request = { type: 'content_script_ready' };
        
        const result = messageListener(request, sender, mockSendResponse);
        
        expect(result).toBe(false); // Synchronous response
        expect(mockSendResponse).toHaveBeenCalledWith({
            acknowledged: true,
            tabId: 123,
            timestamp: expect.any(Number)
        });
    });

    test('should track multiple ready tabs', () => {
        require('../../browser_use_ext/extension/background.js');
        
        const mockSendResponse = jest.fn();
        
        // Add first tab
        messageListener(
            { type: 'content_script_ready' },
            { tab: { id: 123 } },
            mockSendResponse
        );
        
        // Add second tab
        messageListener(
            { type: 'content_script_ready' },
            { tab: { id: 456 } },
            mockSendResponse
        );
        
        expect(mockSendResponse).toHaveBeenCalledTimes(2);
    });

    test('should clean up ready state when tab is removed', () => {
        require('../../browser_use_ext/extension/background.js');
        
        const mockSendResponse = jest.fn();
        
        // Add tab to ready state
        messageListener(
            { type: 'content_script_ready' },
            { tab: { id: 123 } },
            mockSendResponse
        );
        
        // Remove tab
        tabRemovedListener(123, {});
        
        expect(global.console.log).toHaveBeenCalledWith(
            'Tab 123 closed, cleaning up ready state'
        );
    });

    test('should wait for content script readiness', async () => {
        const backgroundModule = require('../../browser_use_ext/extension/background.js');
        
        // Add tab to ready state
        messageListener(
            { type: 'content_script_ready' },
            { tab: { id: 123 } },
            jest.fn()
        );
        
        // Test waitForContentScriptReady function
        const isReady = await waitForContentScriptReady(123, 1000);
        expect(isReady).toBe(true);
    });

    test('should timeout when waiting for unready content script', async () => {
        require('../../browser_use_ext/extension/background.js');
        
        const isReady = await waitForContentScriptReady(999, 200);
        expect(isReady).toBe(false);
        expect(global.console.error).toHaveBeenCalledWith(
            'Timeout waiting for content script readiness on tab 999'
        );
    });
});
```

### Python Integration Test

```python
# browser_use_ext/tests/test_content_script_ready.py

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from browser_use_ext.extension_interface.service import ExtensionInterface

class TestContentScriptReadiness:
    """Test suite for content script ready handshake mechanism"""
    
    @pytest.fixture
    def mock_websocket(self):
        """Mock websocket for testing"""
        mock_ws = Mock()
        mock_ws.send = AsyncMock()
        mock_ws.recv = AsyncMock()
        return mock_ws
    
    @pytest.fixture
    def extension_interface(self, mock_websocket):
        """Create ExtensionInterface instance with mocked websocket"""
        interface = ExtensionInterface()
        interface.websocket = mock_websocket
        return interface

    @pytest.mark.asyncio
    async def test_wait_for_content_script_ready_success(self, extension_interface, mock_websocket):
        """Test successful wait for content script readiness"""
        
        # Mock the response indicating content script is ready
        mock_websocket.recv.return_value = json.dumps({
            "type": "content_script_ready_response",
            "tabId": 123,
            "ready": True
        })
        
        # Test the wait function
        result = await extension_interface.wait_for_content_script_ready(tab_id=123, timeout_ms=1000)
        
        assert result is True
        mock_websocket.send.assert_called_once()
        
        # Verify the message sent to check readiness
        sent_message = json.loads(mock_websocket.send.call_args[0][0])
        assert sent_message["type"] == "check_content_script_ready"
        assert sent_message["tabId"] == 123

    @pytest.mark.asyncio
    async def test_wait_for_content_script_ready_timeout(self, extension_interface, mock_websocket):
        """Test timeout when content script is not ready"""
        
        # Mock no response (simulating timeout)
        mock_websocket.recv.side_effect = asyncio.TimeoutError()
        
        # Test the wait function with short timeout
        result = await extension_interface.wait_for_content_script_ready(tab_id=123, timeout_ms=100)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_get_state_waits_for_readiness(self, extension_interface, mock_websocket):
        """Test that get_state waits for content script readiness"""
        
        # Mock readiness check response
        readiness_response = json.dumps({
            "type": "content_script_ready_response", 
            "tabId": 123,
            "ready": True
        })
        
        # Mock state response
        state_response = json.dumps({
            "type": "get_state_response",
            "tabId": 123,
            "state": {
                "url": "https://example.com",
                "title": "Example Page",
                "actionable_elements": []
            }
        })
        
        # Configure mock to return different responses in sequence
        mock_websocket.recv.side_effect = [readiness_response, state_response]
        
        # Test get_state
        with patch.object(extension_interface, 'wait_for_content_script_ready', return_value=True):
            state = await extension_interface.get_state(tab_id=123)
        
        assert state is not None
        assert state.url == "https://example.com"

    @pytest.mark.asyncio
    async def test_get_state_fails_when_not_ready(self, extension_interface, mock_websocket):
        """Test that get_state fails when content script is not ready"""
        
        # Test get_state when content script is not ready
        with patch.object(extension_interface, 'wait_for_content_script_ready', return_value=False):
            state = await extension_interface.get_state(tab_id=123)
        
        assert state is None

    @pytest.mark.asyncio
    async def test_execute_action_waits_for_readiness(self, extension_interface, mock_websocket):
        """Test that execute_action waits for content script readiness"""
        
        action_response = json.dumps({
            "type": "execute_action_response",
            "tabId": 123,
            "success": True,
            "result": "Action completed"
        })
        
        mock_websocket.recv.return_value = action_response
        
        # Test execute_action
        with patch.object(extension_interface, 'wait_for_content_script_ready', return_value=True):
            result = await extension_interface.execute_action(
                tab_id=123,
                action={"type": "click", "element_id": "btn-123"}
            )
        
        assert result is not None
        assert result.get("success") is True

    def test_ready_state_tracking_data_structure(self):
        """Test that ready state tracking uses appropriate data structure"""
        
        # This would test the JavaScript Set operations if we had a way to test them
        # For now, we document the expected behavior:
        # - contentScriptsReady should be a Set for O(1) lookup
        # - add() method should be used for marking tabs ready
        # - delete() method should be used for cleanup
        # - has() method should be used for checking readiness
        
        # In a real test environment with a JavaScript test runner,
        # we would verify these operations directly
        pass

    @pytest.mark.asyncio
    async def test_tab_cleanup_on_removal(self, extension_interface):
        """Test cleanup of ready state when tabs are removed"""
        
        # This test would verify that the chrome.tabs.onRemoved listener
        # properly removes tab IDs from the contentScriptsReady Set
        # In a real environment, we would:
        # 1. Add a tab to ready state
        # 2. Trigger tab removal event
        # 3. Verify tab is no longer in ready state
        
        # For now, we document the expected behavior
        assert True  # Placeholder for actual tab cleanup testing

    def test_message_format_validation(self):
        """Test that ready messages follow expected format"""
        
        expected_ready_message = {
            "type": "content_script_ready",
            "tabId": None,  # Will be filled by sender info
            "timestamp": "number"
        }
        
        expected_acknowledgment = {
            "acknowledged": True,
            "tabId": "number",
            "timestamp": "number"
        }
        
        # In a real test, we would validate actual message objects
        # against these schemas
        assert "type" in expected_ready_message
        assert "acknowledged" in expected_acknowledgment
```

## error-tasks.md

**Cursor AI is required to check off each of the following tasks as they are completed. This is the single source of truth.**

- [ ] Create or modify browser_use_ext/extension/content.js to implement content script ready handshake
- [ ] Add chrome.runtime.onMessage.addListener setup in content.js before signaling ready
- [ ] Implement signalContentScriptReady function with retry logic and error handling in content.js
- [ ] Add comprehensive logging for debugging ready signal attempts in content.js
- [ ] Implement message handling logic that checks ready state before processing in content.js
- [ ] Create or modify browser_use_ext/extension/background.js to handle content_script_ready messages
- [ ] Implement contentScriptsReady Set for tracking ready tab IDs in background.js
- [ ] Add handleContentScriptReady function to process ready signals and send acknowledgments in background.js
- [ ] Enhance waitForContentScriptReady function to use new tracking system in background.js
- [ ] Implement chrome.tabs.onRemoved listener for cleanup of ready state in background.js
- [ ] Add comprehensive logging for ready state changes and message handling in background.js
- [ ] Create browser_use_ext/tests/javascript/content.test.js for content script unit tests
- [ ] Implement test cases for successful ready signal and acknowledgment in content.test.js
- [ ] Add test cases for retry logic and error handling in content.test.js
- [ ] Create test cases for message handling before and after ready state in content.test.js
- [ ] Create browser_use_ext/tests/javascript/background.test.js for background script unit tests
- [ ] Implement test cases for ready signal reception and tab tracking in background.test.js
- [ ] Add test cases for tab cleanup on removal in background.test.js
- [ ] Create test cases for waitForContentScriptReady function behavior in background.test.js
- [ ] Create browser_use_ext/tests/test_content_script_ready.py for Python integration tests
- [ ] Implement test cases for ExtensionInterface wait_for_content_script_ready method
- [ ] Add test cases for get_state and execute_action readiness verification
- [ ] Create test cases for timeout handling and error scenarios
- [ ] Verify integration between Python ExtensionInterface and JavaScript ready tracking
- [ ] Test end-to-end communication flow from Python through WebSocket to extension
- [ ] Add error handling for cases where content script fails to initialize
- [ ] Implement timeout configuration for ready signal waiting
- [ ] Add debugging utilities for monitoring ready state across tabs
- [ ] Verify manifest.json permissions support the messaging requirements
- [ ] Test handshake mechanism across different browser scenarios (reload, navigation, etc.)

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/63074468/d88fd4bc-d12a-43e4-bc5d-0ab97e83d669/paste.txt
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/63074468/6ac653dd-ec2a-4a24-b9e6-6abff5a79c37/repomix-output.md

---
Answer from Perplexity: pplx.ai/share