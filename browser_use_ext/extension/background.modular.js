// browser-use-ext/extension/background.modular.js
// Modular version of background.js that can be tested with Jest

// Default configuration
const DEFAULT_CONFIG = {
    WS_URL: "ws://localhost:8766",
    reconnectInterval: 5000,
    CONTENT_SCRIPT_READY_TIMEOUT: 15000
};

// Module state
const state = {
    websocket: null,
    activeTabId: null,
    eventQueue: [],
    contentScriptsReady: new Set(),
    config: { ...DEFAULT_CONFIG }
};

// Check if we're in a browser or Node.js environment
const isBrowser = typeof chrome !== 'undefined' && chrome.runtime;

// Check if we're in a test environment
const isTestEnvironment = typeof process !== 'undefined' && process.env.NODE_ENV === 'test';

/**
 * Initializes the WebSocket connection.
 * Sets up event handlers for open, message, error, and close events.
 */
function connectWebSocket() {
    console.log("Attempting to connect to WebSocket at", state.config.WS_URL);
    
    // In test environment, WebSocket might be mocked
    const WebSocketConstructor = typeof WebSocket !== 'undefined' ? WebSocket : global.WebSocket;
    state.websocket = new WebSocketConstructor(state.config.WS_URL);

    state.websocket.onopen = async () => {
        console.log("WebSocket connection established.");
        
        // Only send Chrome messages if in browser environment
        if (isBrowser && chrome.runtime.sendMessage) {
            chrome.runtime.sendMessage({ type: "WS_STATUS", status: "Connected" }).catch((_e) => 
                console.warn("Popup not listening for WS_STATUS (onopen)", _e)
            );
        }
        
        console.log("Background.js: WebSocket opened. Waiting 200ms before sending initial tab query.");
        await new Promise(resolve => setTimeout(resolve, 200)); 
        console.log("Background.js: Delay complete. Proceeding with initial tab query.");

        queryActiveTab(true);
        sendQueuedEvents();
    };

    state.websocket.onmessage = (event) => {
        console.log("Message received from server:", event.data);
        try {
            const message = JSON.parse(event.data);
            handleServerMessage(message);
        } catch (_error) {
            console.error("Error parsing message from server:", _error);
        }
    };

    state.websocket.onerror = (error) => {
        console.error("WebSocket error:", error);
        if (isBrowser && chrome.runtime.sendMessage) {
            chrome.runtime.sendMessage({ type: "WS_STATUS", status: "Error" }).catch(() => {});
        }
    };

    state.websocket.onclose = () => {
        console.log("WebSocket connection closed. Reconnecting in", state.config.reconnectInterval, "ms");
        if (isBrowser && chrome.runtime.sendMessage) {
            chrome.runtime.sendMessage({ type: "WS_STATUS", status: "Disconnected" }).catch(() => {});
        }
        setTimeout(() => connectWebSocket(), state.config.reconnectInterval);
    };
}

/**
 * Sends a message through the WebSocket connection.
 * Queues the message if the connection is not open.
 */
function sendWebSocketMessage(message) {
    if (state.websocket && state.websocket.readyState === (WebSocket.OPEN || 1)) {
        state.websocket.send(JSON.stringify(message));
        console.log("Sent message to server:", message);
    } else {
        console.log("WebSocket not ready. Queuing message:", message);
        state.eventQueue.push(message);
    }
}

/**
 * Sends any queued events when the WebSocket connection is established.
 */
function sendQueuedEvents() {
    if (state.eventQueue.length > 0) {
        console.log(`Sending ${state.eventQueue.length} queued events.`);
        while (state.eventQueue.length > 0) {
            const event = state.eventQueue.shift();
            sendWebSocketMessage(event);
        }
    }
}

/**
 * Queries the active tab and optionally sends its information to the server.
 */
function queryActiveTab(sendContext = false) {
    if (!isBrowser) {
        console.log("Not in browser environment, skipping tab query");
        return;
    }

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length > 0) {
            const tab = tabs[0];
            state.activeTabId = tab.id;
            console.log(`Active tab: ID=${tab.id}, URL=${tab.url}`);
            
            if (sendContext && tab.id && tab.url) {
                const event = {
                    type: "extension_event",
                    data: {
                        event_name: "tab_activated_on_query",
                        tabId: tab.id,
                        url: tab.url,
                        title: tab.title || "No title",
                        timestamp: new Date().toISOString()
                    }
                };
                sendWebSocketMessage(event);
            }
        }
    });
}

/**
 * Handles messages received from the WebSocket server.
 */
function handleServerMessage(message) {
    console.log("Handling server message:", message.type || "Unknown type");
    
    switch (message.type) {
        case "get_state":
            handleGetState(message);
            break;
        case "execute_action":
            handleExecuteAction(message);
            break;
        default:
            console.warn("Unknown message type from server:", message.type);
    }
}

/**
 * Waits for the content script in a specific tab to be ready.
 * Returns true if ready, false if timeout.
 */
async function waitForContentScriptReady(tabId, timeoutMs = state.config.CONTENT_SCRIPT_READY_TIMEOUT) {
    if (state.contentScriptsReady.has(tabId)) {
        console.log(`Content script already ready for tab ${tabId}`);
        return true;
    }

    console.log(`Waiting for content script to be ready in tab ${tabId}...`);
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeoutMs) {
        if (state.contentScriptsReady.has(tabId)) {
            console.log(`Content script is now ready for tab ${tabId}`);
            return true;
        }
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    console.error(`Timeout: Content script not ready for tab ${tabId} after ${timeoutMs}ms`);
    return false;
}

/**
 * Handles the get_state request from the server.
 */
async function handleGetState(message) {
    console.log("handleGetState called with message:", message);
    
    if (!isBrowser) {
        console.log("Not in browser environment, sending mock response");
        sendWebSocketMessage({
            id: message.id,
            type: "response",
            data: { success: false, error: "Not in browser environment" }
        });
        return;
    }

    // Implementation continues...
    // (rest of the function implementation)
}

/**
 * Handles the execute_action request from the server.
 */
async function handleExecuteAction(message) {
    console.log("handleExecuteAction called with message:", message);
    
    if (!isBrowser) {
        console.log("Not in browser environment, sending mock response");
        sendWebSocketMessage({
            id: message.id,
            type: "response",
            data: { success: false, error: "Not in browser environment" }
        });
        return;
    }

    // Implementation continues...
}

// Initialize listeners only in browser environment
function initializeListeners() {
    if (!isBrowser) {
        console.log("Not in browser environment, skipping listener initialization");
        return;
    }

    // Message listener for content scripts
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        console.log("Background received message:", request.type, "from:", sender.tab?.id || "popup/extension");
        
        if (request.type === "content_script_ready" && sender.tab?.id) {
            const tabId = sender.tab.id;
            state.contentScriptsReady.add(tabId);
            console.log(`Content script ready for tab ${tabId}. Total ready: ${state.contentScriptsReady.size}`);
            sendResponse({ status: "acknowledged", tabId: tabId });
        }
        
        return false;
    });

    // Tab removal listener
    chrome.tabs.onRemoved.addListener((tabId) => {
        if (state.contentScriptsReady.has(tabId)) {
            state.contentScriptsReady.delete(tabId);
            console.log(`Tab ${tabId} removed. Cleared from ready set.`);
        }
    });
}

// Module exports for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        state,
        connectWebSocket,
        sendWebSocketMessage,
        sendQueuedEvents,
        queryActiveTab,
        handleServerMessage,
        waitForContentScriptReady,
        handleGetState,
        handleExecuteAction,
        initializeListeners,
        DEFAULT_CONFIG
    };
}

// Initialize in browser environment (but not in tests)
if (isBrowser && !isTestEnvironment) {
    initializeListeners();
    connectWebSocket();
}