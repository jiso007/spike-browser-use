// browser-use-ext/extension/background.js
// Establishes and manages WebSocket connection with the Python backend.
// Handles messages from content scripts and the Python backend.
// Manages browser tab interactions.

const WS_URL = "ws://localhost:8765";
let websocket = null;
let activeTabId = null;
let reconnectInterval = 5000; // 5 seconds

/**
 * Initializes the WebSocket connection.
 * Sets up event handlers for open, message, error, and close events.
 */
function connectWebSocket() {
    console.log("Attempting to connect to WebSocket at", WS_URL);
    websocket = new WebSocket(WS_URL);

    websocket.onopen = () => {
        console.log("WebSocket connection established.");
        // Inform popup about connection status if applicable
        if (chrome.runtime.sendMessage) {
            chrome.runtime.sendMessage({ type: "WS_STATUS", status: "Connected" }).catch(e => console.log("Popup not listening for WS_STATUS"));
        }
    };

    websocket.onmessage = (event) => {
        console.log("Message received from server:", event.data);
        try {
            const message = JSON.parse(event.data);
            handleServerMessage(message);
        } catch (error) {
            console.error("Error parsing message from server:", error);
        }
    };

    websocket.onerror = (error) => {
        console.error("WebSocket error:", error);
        // The onclose event will handle reconnection logic
    };

    websocket.onclose = () => {
        console.log("WebSocket connection closed. Attempting to reconnect in", reconnectInterval / 1000, "seconds.");
        websocket = null; // Ensure the old websocket is cleaned up
        if (chrome.runtime.sendMessage) {
            chrome.runtime.sendMessage({ type: "WS_STATUS", status: "Disconnected" }).catch(e => console.log("Popup not listening for WS_STATUS"));
        }
        setTimeout(connectWebSocket, reconnectInterval);
    };
}

/**
 * Handles messages received from the Python WebSocket server.
 * @param {object} message - The parsed message object from the server.
 */
function handleServerMessage(message) {
    console.log("Handling server message:", message);
    // Route message to content script of the active tab if it's a known action
    if (message.type === "request" && message.action) {
        if (activeTabId) {
            chrome.tabs.sendMessage(activeTabId, {
                type: message.action, // e.g., "get_state", "execute_action"
                payload: message.params,
                requestId: message.request_id // Forward the request_id
            }).then(response => {
                console.log(`Response from content script for ${message.action}:`, response);
                // Check if response is valid before sending
                if (response !== undefined) {
                     sendResponseToServer(response);
                } else {
                    console.warn(`Undefined response from content script for action: ${message.action}. This may happen if the tab is not ready or an error occurred.`);
                    // Optionally, send an error response back to the server
                    sendResponseToServer({
                        request_id: message.request_id,
                        status: "error",
                        error: `Content script for action '${message.action}' returned undefined. Tab ID: ${activeTabId}`
                    });
                }
            }).catch(error => {
                console.error("Error sending message to content script or receiving response:", error);
                sendResponseToServer({
                    request_id: message.request_id,
                    status: "error",
                    error: `Failed to communicate with content script for action '${message.action}': ${error.message}`
                });
            });
        } else {
            console.warn("No active tab to send message to for action:", message.action);
            sendResponseToServer({
                request_id: message.request_id,
                status: "error",
                error: "No active tab identified to process the request."
            });
        }
    }
}

/**
 * Sends a response message back to the Python WebSocket server.
 * @param {object} responseData - The data to send as a response.
 */
function sendResponseToServer(responseData) {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        try {
            const messageString = JSON.stringify(responseData);
            console.log("Sending response to server:", messageString);
            websocket.send(messageString);
        } catch (error) {
            console.error("Error serializing response data for server:", error, responseData);
        }
    } else {
        console.error("WebSocket not connected. Cannot send response to server.", responseData);
    }
}

// Listener for messages from content scripts or popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Message received in background script:", message, "from sender:", sender);

    // Handle messages from content.js (typically responses to server requests)
    if (sender.tab && message.type === "response") {
        console.log("Forwarding response from content script to server:", message.data);
        sendResponseToServer(message.data);
        return false; // Indicate that sendResponse will not be called asynchronously here by this direct handler
    }

    // Handle screenshot requests specifically, as these are handled by background
    if (message.type === "request_screenshot") {
        handleScreenshotRequest(message.requestId, sender.tab ? sender.tab.id : null, sendResponse);
        return true; // Indicate that sendResponse will be called asynchronously
    }
    
    // Handle popup status request
    if (message.type === "GET_POPUP_STATUS") {
        sendResponse({ status: websocket && websocket.readyState === WebSocket.OPEN ? "Connected" : "Disconnected" });
        return false;
    }

    // Other direct messages to background (e.g., from popup, though not exemplified yet)
    // ...

    // Default: if the message is not handled, return false or nothing.
    // For clarity, explicitly return false if not intending to use sendResponse asynchronously.
    return false;
});

/**
 * Handles requests for screenshots from content scripts.
 * Captures the visible tab and sends the data URL back.
 * @param {string} requestId - The original request ID to include in the response.
 * @param {number} tabId - The ID of the tab to capture.
 * @param {function} sendResponse - Function to send response back to content script.
 */
async function handleScreenshotRequest(requestId, tabId, sendResponse) {
    if (!tabId) {
        console.error("Screenshot request failed: No tab ID provided.");
        sendResponse({
            request_id: requestId, // Ensure requestId from original message is used
            type: "response", // This is a response to content.js, not directly to server
            status: "error",
            error: "No tab ID for screenshot."
        });
        return;
    }
    try {
        const dataUrl = await chrome.tabs.captureVisibleTab(tabId, { format: "png" });
        console.log("Screenshot captured for tab:", tabId);
        // This response goes to content.js, which will then package it for the server
        sendResponse({
            request_id: requestId, // Ensure requestId from original message is used
            type: "response", // This is a response to content.js
            status: "success",
            data: { screenshot: dataUrl } // data that content.js expects
        });
    } catch (error) {
        console.error("Error capturing screenshot:", error);
        sendResponse({
            request_id: requestId, // Ensure requestId from original message is used
            type: "response", // This is a response to content.js
            status: "error",
            error: `Screenshot capture failed: ${error.message}`
        });
    }
}


// Tab management and active tab tracking
/**
 * Updates the activeTabId when the active tab changes.
 */
chrome.tabs.onActivated.addListener(activeInfo => {
    console.log("Active tab changed. New active tab ID:", activeInfo.tabId);
    activeTabId = activeInfo.tabId;
    // Optionally, notify the server or content script about the tab change if needed.
});

/**
 * Updates activeTabId if the currently active tab is closed.
 * Queries for a new active tab.
 */
chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
    console.log("Tab removed:", tabId);
    if (activeTabId === tabId) {
        console.log("Active tab was closed. Querying for new active tab.");
        queryActiveTab(); // Try to find a new active tab
    }
});

/**
 * Queries for the currently active tab and updates activeTabId.
 * This is useful on startup and when the active tab might have changed (e.g., closed).
 */
function queryActiveTab() {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length > 0) {
            activeTabId = tabs[0].id;
            console.log("Initial active tab ID set to:", activeTabId);
        } else {
            activeTabId = null; // No active tab found
            console.log("No active tab found.");
        }
    });
}

// Initial setup
console.log("Background script started.");
connectWebSocket(); // Start WebSocket connection
queryActiveTab();   // Determine the initially active tab 