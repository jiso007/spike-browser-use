// browser_use_ext/tests/javascript/background.test.js

// Mock chrome APIs (using jest-chrome or manual mocks)
global.chrome = {
    runtime: {
        onMessage: {
            addListener: jest.fn(),
            removeListener: jest.fn(),
            hasListener: jest.fn(() => true),
        },
        sendMessage: jest.fn((tabId, message, callback) => {
            // If testing scenarios where background sends to content script, mock this response
            // For example, for page_fully_loaded_and_ready
            if (message.type === "page_fully_loaded_and_ready") {
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
global.WebSocket = jest.fn(url => {
    const wsMock = {
        url: url,
        readyState: WebSocket.CONNECTING, // Initial state
        send: jest.fn(data => {
            // console.log("[Mock WebSocket] send:", data);
            // If testing message queue, add to it
            // messageQueue.push(data);
        }),
        close: jest.fn(() => {
            wsMock.readyState = WebSocket.CLOSED;
            if (wsMock.onclose) wsMock.onclose({ code: 1000, reason: "Normal closure" });
        }),
        onopen: null,
        onmessage: null,
        onerror: null,
        onclose: null,
    };
    // Simulate connection opening
    setTimeout(() => {
        wsMock.readyState = WebSocket.OPEN;
        if (wsMock.onopen) wsMock.onopen();
    }, 0);
    socket = wsMock; // Assign to global mock socket for inspection
    return wsMock;
});

ddescribe('Background Script Logic', () => {

    beforeEach(() => {
        // Reset all mocks and simulated state
        jest.clearAllMocks();
        contentScriptsReady.clear();
        activeTabId = null;
        wsUrl = WS_URL_DEFAULT;
        socket = null;
        messageQueue = [];
        connected = false;
        reconnectAttempts = 0;
        chrome.runtime.lastError = null;

        // --- Simulate loading background.js ---
        // Option 1: If background.js is a script that executes immediately.
        // This is tricky as it might run only once per Jest worker.
        // You may need to use jest.resetModules() and re-require if it should re-init.
        // jest.resetModules();
        // require('../../extension/background.js'); 

        // Option 2: If background.js has an init function, call it here.
        // initBackgroundScript(); 

        // For these tests, we will assume the listeners ARE ALREADY ATTACHED by background.js
        // and we will retrieve and invoke them directly.
        // This requires background.js to have actually called chrome.runtime.onMessage.addListener etc.
        // If it does so at the top level, you might need `require('../../extension/background.js')` once at the top of this file.
    });

    describe('Content Script Ready Handling', () => {
        // Test the logic within chrome.runtime.onMessage when type is "content_script_ready"
        test('should add tabId to contentScriptsReady on content_script_ready message', () => {
            // Manually simulate the background.js setup if not running the whole script
            const onMessageCallback = (message, sender, sendResponse) => {
                if (sender.tab && message.type === "content_script_ready") {
                    // console.log(`background.js: Received 'content_script_ready' from tabId: ${sender.tab.id}`);
                    contentScriptsReady.add(sender.tab.id);
                    sendResponse({ status: "acknowledged_content_script_ready", tabId: sender.tab.id });
                    return true; // For async response
                }
            };
            chrome.runtime.onMessage.addListener(onMessageCallback); // Simulate background adding its listener
            const capturedCallback = getRuntimeOnMessageCallback();

            const mockSender = { tab: { id: 101, url: 'https://test.com' } };
            const mockSendResponse = jest.fn();
            
            const result = capturedCallback({ type: "content_script_ready" }, mockSender, mockSendResponse);
            
            expect(contentScriptsReady.has(101)).toBe(true);
            expect(mockSendResponse).toHaveBeenCalledWith({ status: "acknowledged_content_script_ready", tabId: 101 });
            expect(result).toBe(true); // Important for async sendResponse
        });

        test('should remove tabId from contentScriptsReady on tabs.onRemoved', () => {
            // Simulate background.js adding its listener
            const onRemovedCallback = (tabId) => {
                if (contentScriptsReady.has(tabId)) {
                    contentScriptsReady.delete(tabId);
                    // console.log(`background.js: Removed tabId ${tabId} from contentScriptsReady set.`);
                }
            };
            chrome.tabs.onRemoved.addListener(onRemovedCallback);
            const capturedCallback = chrome.tabs.onRemoved.addListener.mock.calls[0][0];

            contentScriptsReady.add(202);
            expect(contentScriptsReady.has(202)).toBe(true);

            capturedCallback(202); // Simulate tab removal event
            expect(contentScriptsReady.has(202)).toBe(false);
        });
    });

    describe('waitForContentScriptReady', () => {
        // Test the waitForContentScriptReady helper function directly
        // This function needs to be exposed by background.js for this test style
        // Or, you test the functions that *use* it.
        async function waitForContentScriptReady(tabId, timeoutMs) { // Copied from rule for testability
            const startTime = Date.now();
            while (Date.now() - startTime < timeoutMs) {
                if (contentScriptsReady.has(tabId)) return true;
                await new Promise(resolve => setTimeout(resolve, 50)); // Poll
            }
            return false;
        }

        test('should return true if content script is already ready', async () => {
            contentScriptsReady.add(303);
            const isReady = await waitForContentScriptReady(303, 100);
            expect(isReady).toBe(true);
        });

        test('should return true if content script becomes ready within timeout', async () => {
            setTimeout(() => contentScriptsReady.add(304), 60);
            const isReady = await waitForContentScriptReady(304, 200);
            expect(isReady).toBe(true);
        });

        test('should return false if content script does not become ready within timeout', async () => {
            const isReady = await waitForContentScriptReady(305, 100);
            expect(isReady).toBe(false);
        });
    });

    describe('Tab Activation Logic (Simplified Example)', () => {
        // Test what happens on chrome.tabs.onActivated
        // This is a simplified test assuming the handler structure from your provided log/code
        test('onActivated should attempt to send page_fully_loaded_and_ready if tab is complete and ready', async () => {
            const onActivatedHandler = async (activeInfo) => {
                activeTabId = activeInfo.tabId;
                const tab = await chrome.tabs.get(activeInfo.tabId);
                if (tab && tab.status === 'complete' && tab.url && (tab.url.startsWith('http'))) {
                    // Simulate waitForContentScriptReady behavior directly
                    if (contentScriptsReady.has(tab.id)) {
                        // console.log(`Tab ${tab.id} is complete and content script ready. Sending page_fully_loaded_and_ready.`);
                        await chrome.tabs.sendMessage(tab.id, { type: "page_fully_loaded_and_ready" });
                    } else {
                        // console.log(`Tab ${tab.id} is complete but content script NOT YET ready. Waiting...`);
                        // In real code, might call waitForContentScriptReady here.
                    }
                }
            };
            chrome.tabs.onActivated.addListener(onActivatedHandler); // Simulate background.js attaching listener
            const capturedCallback = getTabOnActivatedCallback();
            
            contentScriptsReady.add(404); // Mark as ready
            chrome.tabs.get.mockResolvedValueOnce({ id: 404, url: 'https://test.com', status: 'complete'});

            await capturedCallback({ tabId: 404, windowId: 1 });

            expect(chrome.tabs.get).toHaveBeenCalledWith(404);
            expect(chrome.tabs.sendMessage).toHaveBeenCalledWith(404, { type: "page_fully_loaded_and_ready" });
        });

        test('onActivated should NOT send if content script not ready', async () => {
             const onActivatedHandler = async (activeInfo) => { /* as above */ }; // simplified definition
             chrome.tabs.onActivated.addListener(onActivatedHandler); 
             const capturedCallback = getTabOnActivatedCallback();

            contentScriptsReady.delete(405); // Ensure not ready
            chrome.tabs.get.mockResolvedValueOnce({ id: 405, url: 'https://test.com', status: 'complete'});

            await capturedCallback({ tabId: 405, windowId: 1 });

            expect(chrome.tabs.get).toHaveBeenCalledWith(405);
            expect(chrome.tabs.sendMessage).not.toHaveBeenCalledWith(405, { type: "page_fully_loaded_and_ready" });
        });
    });

    describe('WebSocket Connection Logic (connectToServer)', () => {
        // This will test the WebSocket connection and message handling logic.
        // Assumes a function like `connectToServer` exists in background.js
        // or that the connection logic is triggered in a testable way.

        // Simplified connectToServer function for testing purposes
        // In real background.js, this would be more complex with retries, etc.
        async function connectToServer() {
            // console.log(`Attempting to connect to WebSocket server at ${wsUrl}...`);
            return new Promise((resolve, reject) => {
                const ws = new WebSocket(wsUrl);
                ws.onopen = () => {
                    // console.log("WebSocket connection established.");
                    connected = true;
                    reconnectAttempts = 0;
                    // processMessageQueue(); // If there's a message queue
                    resolve(ws);
                };
                ws.onerror = (error) => {
                    // console.error("WebSocket error:", error);
                    reject(error);
                };
                ws.onclose = (event) => {
                    // console.log(`WebSocket connection closed. Code: ${event.code}, Reason: ${event.reason}`);
                    connected = false;
                    // Attempt to reconnect if needed
                };
                ws.onmessage = (event) => {
                    // This is where background.js would handle messages from the Python server
                    // console.log("Received from Python server:", event.data);
                    // Example: if (event.data === "ping") socket.send("pong");
                };
            });
        }

        test('should establish WebSocket connection on connectToServer', async () => {
            await connectToServer();
            expect(WebSocket).toHaveBeenCalledWith(WS_URL_DEFAULT);
            expect(socket).not.toBeNull();
            expect(socket.readyState).toBe(WebSocket.OPEN);
            expect(connected).toBe(true);
        });

        test('WebSocket onmessage should be set up to handle server messages', async () => {
            await connectToServer();
            expect(socket.onmessage).toEqual(expect.any(Function));
            
            // Simulate a message from the server
            const serverMessage = { data: JSON.stringify({ id: 1, type: "server_event", data: "hello" }) };
            socket.onmessage(serverMessage);
            // Add assertions here based on how background.js processes server messages
            // e.g., expect(chrome.tabs.sendMessage).toHaveBeenCalledWith(...)
        });

        test('should attempt to send a message via WebSocket', async () => {
            await connectToServer(); // Establish connection
            const messagePayload = { type: "greeting", content: "hello server" };
            
            // Simulate background.js sending a message
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify(messagePayload));
            }
            
            expect(socket.send).toHaveBeenCalledWith(JSON.stringify(messagePayload));
        });
    });
});

// Notes for running these tests:
// 1. Similar Jest + jest-chrome setup as content.test.js.
// 2. Refactor background.js to make its core logic (event handlers, WebSocket management)
//    testable, possibly by encapsulating them in functions that can be imported and called.
// 3. Testing service workers (background scripts) can be complex due to their lifecycle.
//    Jest provides a good environment for unit testing the logic in isolation from the actual browser runtime. 