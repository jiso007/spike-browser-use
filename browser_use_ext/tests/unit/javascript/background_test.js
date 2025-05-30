// browser_use_ext/tests/javascript/background.test.js

// Mock the entire chrome API globally for all tests in this file
// This helps ensure a clean state for each test and avoids unintended side effects.
global.chrome = {
    runtime: {
        onMessage: {
            addListener: jest.fn(),
            removeListener: jest.fn(),
            hasListener: jest.fn(() => true),
        },
        sendMessage: jest.fn((messageOrCallback, callback) => {
            // Handle the case where only a callback is passed (background.modular.js passes only message)
            let message = messageOrCallback;
            if (typeof messageOrCallback === 'function') {
                callback = messageOrCallback;
                message = {};
            }
            
            // If testing scenarios where background sends to content script, mock this response
            // For example, for page_fully_loaded_and_ready
            if (message && message.type === "page_fully_loaded_and_ready") {
                if (typeof callback === 'function') {
                    setTimeout(() => callback({ status: "content_script_acked_load_ready" }), 0);
                }
                return Promise.resolve({ status: "content_script_acked_load_ready_promise" });
            }
            // Generic ack for other messages
            if (typeof callback === 'function') {
                setTimeout(() => callback({ status: "mock_generic_ack" }), 0);
            }
            return Promise.resolve({ status: "mock_generic_ack_promise" });
        }),
        lastError: null,
    },
    tabs: {
        onActivated: {
            addListener: jest.fn(),
            removeListener: jest.fn(),
        },
        onUpdated: {
            addListener: jest.fn(),
            removeListener: jest.fn(),
        },
        onRemoved: {
            addListener: jest.fn(),
            removeListener: jest.fn(),
        },
        query: jest.fn(async (queryInfo) => {
            // Return mock tab data based on queryInfo
            if (queryInfo.active && queryInfo.currentWindow) {
                return [{ id: 123, url: 'https://example.com', status: 'complete', windowId: 1 }];
            }
            return [{ id: 123, url: 'https://example.com', status: 'complete', windowId: 1 }];
        }),
        get: jest.fn(async (tabId) => {
            // Return mock tab data
            return { id: tabId, url: 'https://example.com', status: 'complete', windowId: 1, title: "Mock Tab" };
        }),
        sendMessage: jest.fn(async (tabId, message, options) => {
            // Mock response from content script if needed for the test
            if (message.type === 'get_state_from_content') {
                return { success: true, data: { url: 'https://example.com', title: 'Mock State' } };
            }
            return { status: "mock_content_script_ack" };
        }),
        // Add other tab functions if used by background.js
    },
    storage: {
        local: {
            get: jest.fn(async (keys) => {
                // Simulate fetching from local storage
                return { wsUrl: 'ws://localhost:8765' }; 
            }),
            set: jest.fn(async (items) => { /* Simulate setting to local storage */ }),
        },
    },
    action: { // For chrome.action API (formerly browserAction/pageAction)
        setBadgeText: jest.fn(),
        setBadgeBackgroundColor: jest.fn(),
        setIcon: jest.fn(),
        // ... other action API mocks
    },
    webNavigation: { // If used for page load events etc.
        onCommitted: {
            addListener: jest.fn()
        },
        onCompleted: {
            addListener: jest.fn()
        }
    }
};

global.WebSocket = jest.fn(() => ({
    onopen: jest.fn(),
    onmessage: jest.fn(),
    onerror: jest.fn(),
    onclose: jest.fn(),
    send: jest.fn(),
    close: jest.fn(),
    readyState: WebSocket.OPEN, // Simulate open state by default for some tests
}));

global.console = {
    log: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
    info: jest.fn(), 
    debug: jest.fn(),
};

// Assuming background.js initializes itself or exposes functions for testing.
// For instance, if background.js has an init function or directly adds listeners.
// We might need to manually call parts of it or simulate its execution flow.

// --- Example: Import or simulate loading of background.js components ---
// This part is tricky and depends on background.js structure.
// If background.js is a non-module script that runs on load:
//   You might need to use `require('../../extension/background.js');`
//   And then test the side effects on the mocked chrome APIs.
// If background.js functions are exported (better):
//   const { handleContentScriptReady, handleTabActivation, ... } = require('../../extension/background.js');

// For demonstration, let's assume we can access the listeners background.js would have added.
// In a real scenario, you'd require background.js and it would call chrome.runtime.onMessage.addListener, etc.
// Then you can capture the callback passed to addListener.

let contentScriptsReady = new Set(); // Simulate this state from background.js
let activeTabId = null;
const WS_URL_DEFAULT = "ws://localhost:8765";
let wsUrl = WS_URL_DEFAULT;
let socket = null; // Mock WebSocket object
let messageQueue = [];
let connected = false;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;
const RECONNECT_DELAY_MS = 100; // Shorter for tests
const CONTENT_SCRIPT_READY_TIMEOUT = 1000; // Shorter for tests

// --- Helper to get the callback passed to chrome.runtime.onMessage.addListener ---
function getRuntimeOnMessageCallback() {
    if (chrome.runtime.onMessage.addListener.mock.calls.length > 0) {
        return chrome.runtime.onMessage.addListener.mock.calls[0][0];
    }
    throw new Error("chrome.runtime.onMessage.addListener was not called by background.js simulation");
}

// --- Helper to get onActivated callback ---
function getTabOnActivatedCallback() {
    if (chrome.tabs.onActivated.addListener.mock.calls.length > 0) {
        return chrome.tabs.onActivated.addListener.mock.calls[0][0];
    }
    throw new Error("chrome.tabs.onActivated.addListener was not called");
}

// --- Mock WebSocket globally or for specific tests ---
// Add WebSocket constants
global.WebSocket = jest.fn(url => {
    const wsMock = {
        url: url,
        readyState: 0, // WebSocket.CONNECTING
        send: jest.fn(data => {
            // console.log("[Mock WebSocket] send:", data);
            // If testing message queue, add to it
            // messageQueue.push(data);
        }),
        close: jest.fn(() => {
            wsMock.readyState = 3; // WebSocket.CLOSED
            if (wsMock.onclose) wsMock.onclose({ code: 1000, reason: "Normal closure" });
        }),
        onopen: null,
        onmessage: null,
        onerror: null,
        onclose: null,
    };
    // Simulate connection opening
    setTimeout(() => {
        wsMock.readyState = 1; // WebSocket.OPEN
        if (wsMock.onopen) wsMock.onopen();
    }, 0);
    socket = wsMock; // Assign to global mock socket for inspection
    return wsMock;
});
// Mock WebSocket constants
global.WebSocket.CONNECTING = 0;
global.WebSocket.OPEN = 1;
global.WebSocket.CLOSING = 2;
global.WebSocket.CLOSED = 3;

describe('Background Script Ready Handshake & Core Logic', () => {
    let messageListenerCallback; // To store the function passed to chrome.runtime.onMessage.addListener
    let tabRemovedListenerCallback; // To store the function passed to chrome.tabs.onRemoved.addListener
    let backgroundModule; // To access exported functions if any (like waitForContentScriptReady)

    beforeEach(() => {
        // Reset all mocks and module state before each test
        jest.clearAllMocks();
        jest.resetModules(); // This is key to re-require and re-initialize background.js

        // Reset console mocks
        global.console.log.mockClear();
        global.console.error.mockClear();
        global.console.warn.mockClear();

        // Mock tabs.query to prevent issues
        global.chrome.tabs.query.mockImplementation((queryInfo, callback) => {
            if (callback) {
                callback([]);
            }
            return Promise.resolve([]);
        });

        // Load the modular background script
        backgroundModule = require('../../../extension/background.modular.js');
        
        // Initialize listeners (in browser environment this happens automatically)
        backgroundModule.initializeListeners();
        
        // Capture the listener callbacks after initialization
        if (global.chrome.runtime.onMessage.addListener.mock.calls.length > 0) {
            messageListenerCallback = global.chrome.runtime.onMessage.addListener.mock.calls[0][0];
        }
        if (global.chrome.tabs.onRemoved.addListener.mock.calls.length > 0) {
            tabRemovedListenerCallback = global.chrome.tabs.onRemoved.addListener.mock.calls[0][0];
        }
    });

    test('should register runtime message and tab removal listeners on init', () => {
        // The modular version may call addListener multiple times in initialization
        expect(global.chrome.runtime.onMessage.addListener.mock.calls.length).toBeGreaterThanOrEqual(1);
        expect(global.chrome.tabs.onRemoved.addListener.mock.calls.length).toBeGreaterThanOrEqual(1);
    });

    describe('Content Script Ready Handling', () => {
        test('should handle content_script_ready signal and acknowledge', () => {
            const mockSendResponse = jest.fn();
            const sender = { tab: { id: 123 } };
            const request = { type: 'content_script_ready', timestamp: Date.now() };

            // Simulate a message from content script
            const result = messageListenerCallback(request, sender, mockSendResponse);

            // Check that the tab was added to the ready set
            expect(backgroundModule.state.contentScriptsReady.has(123)).toBe(true);
            
            // Check the response
            expect(result).toBe(false); // Synchronous response
            expect(mockSendResponse).toHaveBeenCalledWith({
                status: "acknowledged",
                tabId: 123
            });
            
            // Check console logs
            expect(global.console.log).toHaveBeenCalledWith(
                expect.stringContaining('Content script ready for tab 123')
            );
        });

        test('should not add tab if tab ID is missing in ready signal', () => {
            const mockSendResponse = jest.fn();
            const sender = { /* tab missing */ }; 
            const request = { type: 'content_script_ready' };

            messageListenerCallback(request, sender, mockSendResponse);

            // The modular version doesn't send an error response for missing tab ID
            expect(mockSendResponse).not.toHaveBeenCalled();
            // Check that no tab was added to the ready set
            expect(backgroundModule.state.contentScriptsReady.size).toBe(0);
        });

        test('should track multiple ready tabs correctly', () => {
            const mockSendResponse = jest.fn();
            
            // Add first tab
            messageListenerCallback({ type: 'content_script_ready' }, { tab: { id: 1 } }, mockSendResponse);
            expect(backgroundModule.state.contentScriptsReady.has(1)).toBe(true);
            expect(backgroundModule.state.contentScriptsReady.size).toBe(1);
            
            // Add second tab
            messageListenerCallback({ type: 'content_script_ready' }, { tab: { id: 2 } }, mockSendResponse);
            expect(backgroundModule.state.contentScriptsReady.has(2)).toBe(true);
            expect(backgroundModule.state.contentScriptsReady.size).toBe(2);
            
            // Verify both tabs are tracked
            expect(Array.from(backgroundModule.state.contentScriptsReady)).toEqual([1, 2]);
        });
    });

    describe('Tab Removal Handling', () => {
        test('should clean up ready state when a tracked tab is removed', () => {
            const mockSendResponse = jest.fn();
            
            // Mark tab 123 as ready
            messageListenerCallback({ type: 'content_script_ready' }, { tab: { id: 123 } }, mockSendResponse);
            expect(backgroundModule.state.contentScriptsReady.has(123)).toBe(true);

            // Simulate tab removal
            tabRemovedListenerCallback(123);

            // Verify the tab was removed from the ready set
            expect(backgroundModule.state.contentScriptsReady.has(123)).toBe(false);
            expect(backgroundModule.state.contentScriptsReady.size).toBe(0);
            
            // Check console logs
            expect(global.console.log).toHaveBeenCalledWith(
                expect.stringContaining('Tab 123 removed. Cleared from ready set.')
            );
        });

        test('should not error if a non-tracked tab is removed', () => {
            // Ensure the set is empty initially
            expect(backgroundModule.state.contentScriptsReady.size).toBe(0);
            
            // Try to remove a tab that was never added
            tabRemovedListenerCallback(999);
            
            // The set should still be empty
            expect(backgroundModule.state.contentScriptsReady.size).toBe(0);
            
            // Since the tab wasn't in the set, no removal log should be shown
            expect(global.console.log).not.toHaveBeenCalledWith(
                expect.stringContaining('Tab 999 removed. Cleared from ready set.')
            );
        });
    });

    describe('waitForContentScriptReady Functionality', () => {
        // To test waitForContentScriptReady, it needs to be accessible.
        // If it's not exported from background.js, these tests would need to be adapted
        // or it would need to be exported for testing purposes.
        // Assuming backgroundModule.waitForContentScriptReady is available:

        // Test relies on background.js structure where waitForContentScriptReady is global or exported.
        // If it's not, this describe block needs to be rethought.
        // For now, we proceed as if it's available as in PERPLEXITY_OUTPUT test structure for `backgroundModule`
        // This implies `waitForContentScriptReady` should be a global function in background.js or exported.
        // The provided background.js in PERPLEXITY_OUTPUT has it as a global function.

        beforeAll(() => {
            jest.useFakeTimers(); // Use fake timers for controlling setTimeout in polling
        });

        afterAll(() => {
            jest.useRealTimers(); // Restore real timers
        });

        test('should resolve true immediately if tab is already ready', async () => {
            // Mark tab as ready
            messageListenerCallback({ type: 'content_script_ready' }, { tab: { id: 777 } }, jest.fn());
            expect(backgroundModule.state.contentScriptsReady.has(777)).toBe(true);

            const isReadyPromise = backgroundModule.waitForContentScriptReady(777, 1000);
            jest.runAllTimers(); // Resolve any setTimeout
            const isReady = await isReadyPromise;
            
            expect(isReady).toBe(true);
            expect(global.console.log).toHaveBeenCalledWith(
                'Content script already ready for tab 777'
            );
        });

        test('should resolve true after polling if tab becomes ready', async () => {
            const tabId = 888;
            const readyPromise = backgroundModule.waitForContentScriptReady(tabId, 1000);

            // Simulate tab becoming ready after some polling attempts
            setTimeout(() => {
                messageListenerCallback({ type: 'content_script_ready' }, { tab: { id: tabId } }, jest.fn());
            }, 300); // Becomes ready after ~1 poll (250ms interval)

            jest.advanceTimersByTime(100); // First poll: not ready
            
            jest.advanceTimersByTime(200); // Advance to 300ms total
            // The ready signal (messageListenerCallback) is called now.
            
            jest.advanceTimersByTime(100); // Next poll: should be ready

            const isReady = await readyPromise;
            expect(isReady).toBe(true);
            expect(global.console.log).toHaveBeenCalledWith(
                `Content script is now ready for tab ${tabId}`
            );
        });

        test('should timeout and resolve false if tab does not become ready', async () => {
            const tabId = 999;
            const readyPromise = backgroundModule.waitForContentScriptReady(tabId, 500); // Short timeout

            jest.advanceTimersByTime(600); // Advance time past the timeout

            const isReady = await readyPromise;
            expect(isReady).toBe(false);
            expect(global.console.error).toHaveBeenCalledWith(
                `Timeout: Content script not ready for tab ${tabId} after 500ms`
            );
        });
    });

    // Add more describe blocks for other functionalities like WebSocket interactions,
    // handleServerMessage logic, tab event handling (onUpdated, onActivated) etc.,
    // based on the full functionality of your background.js.
});

// Notes for running these tests:
// 1. Similar Jest + jest-chrome setup as content.test.js.
// 2. Refactor background.js to make its core logic (event handlers, WebSocket management)
//    testable, possibly by encapsulating them in functions that can be imported and called.
// 3. Testing service workers (background scripts) can be complex due to their lifecycle.
//    Jest provides a good environment for unit testing the logic in isolation from the actual browser runtime. 