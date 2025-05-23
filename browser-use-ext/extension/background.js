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
            chrome.runtime.sendMessage({ type: "WS_STATUS", status: "Connected" }).catch(e => console.warn("Popup not listening for WS_STATUS (onopen)"));
        }
        // Send initial active tab info once connected
        queryActiveTab(true); // Send context on initial connection
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
            chrome.runtime.sendMessage({ type: "WS_STATUS", status: "Disconnected" }).catch(e => console.warn("Popup not listening for WS_STATUS (onclose)"));
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
    if (message.type === "request" && message.data && message.data.action) {
        if (activeTabId) {
            // Ensure requestId is consistently named, Python side uses 'id' in BaseMessage
            const requestId = message.id; 
            console.log(`Forwarding action '${message.data.action}' (ID: ${requestId}) to tab ${activeTabId}`);
            chrome.tabs.sendMessage(activeTabId, {
                type: message.data.action, // e.g., "get_state", "execute_action"
                payload: message.data.params, // Assuming params are within data object
                requestId: requestId 
            }).then(response => {
                console.log(`Response from content script for action '${message.data.action}' (ID: ${requestId}):`, response);
                if (response !== undefined) {
                     // Ensure the response includes the original requestId
                     sendDataToServer({ type: "response", id: requestId, data: response });
                } else {
                    console.warn(`Undefined response from content script for action: '${message.data.action}' (ID: ${requestId}). Tab ID: ${activeTabId}`);
                    sendDataToServer({
                        type: "response",
                        id: requestId,
                        data: {
                            success: false,
                            error: `Content script for action '${message.data.action}' returned undefined. Tab ID: ${activeTabId}`
                        }
                    });
                }
            }).catch(error => {
                const requestId = message.id;
                console.error(`Error sending message to content script or receiving response for action '${message.data.action}' (ID: ${requestId}):`, error);
                sendDataToServer({
                    type: "response",
                    id: requestId,
                    data: {
                         success: false,
                         error: `Failed to communicate with content script for action '${message.data.action}': ${error.message}`
                    }
                });
            });
        } else {
            const requestId = message.id;
            console.warn("No active tab to send message to for action:", message.data.action, `(ID: ${requestId})`);
            sendDataToServer({
                type: "response",
                id: requestId,
                data: {
                    success: false,
                    error: "No active tab identified to process the request."
                }
            });
        }
    } else {
        console.warn("Received message from server that is not a recognized action request:", message);
    }
}

/**
 * Sends generic data (responses or events) to the Python WebSocket server.
 * @param {object} dataToSend - The data to send.
 */
function sendDataToServer(dataToSend) {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        try {
            // The Python server expects messages with 'id' and 'type' at the top level.
            // If dataToSend already has 'id' and 'type', use it as is.
            // Otherwise, wrap it if it's meant to be the 'data' part of an 'extension_event'.
            let messageToSend;
            if (dataToSend.type && dataToSend.hasOwnProperty('id')) {
                messageToSend = dataToSend; // Assume it's already a correctly structured message
            } else {
                console.warn("Sending data that might not have a server-correlating ID:", dataToSend);
                messageToSend = dataToSend; // Send as is, review server side if ID is strictly needed for all types
            }

            const messageString = JSON.stringify(messageToSend);
            console.log("Attempting to send to server:", messageString);
            websocket.send(messageString);
            console.log("Data sent to server successfully.");
        } catch (error) {
            console.error("Error serializing data for server:", error, dataToSend);
        }
    } else {
        console.error("WebSocket not connected. Cannot send data to server.", dataToSend);
    }
}

// Listener for messages from content scripts or popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Message received in background script:", message, "from sender:", sender);

    // Handle messages from content.js (typically responses to server requests)
    if (sender.tab && message.type === "response_to_server") {
        console.log("Forwarding response from content script to server:", message.payload);
        sendDataToServer({
            type: "response",
            id: message.payload.id,
            data: message.payload.data
        });
        return false; 
    }

    // Handle screenshot requests specifically, as these are handled by background
    if (message.type === "request_screenshot") {
        handleScreenshotRequest(message.requestId, sender.tab ? sender.tab.id : null, sendResponse);
        return true; 
    }
    
    if (message.type === "GET_POPUP_STATUS") {
        sendResponse({ status: websocket && websocket.readyState === WebSocket.OPEN ? "Connected" : "Disconnected" });
        return false;
    }
    
    // Handle proactive context update requests from content scripts
    if (message.type === "PROACTIVE_CONTEXT_UPDATE") {
        console.log("Received proactive context update from content script:", message.context);
        sendDataToServer({
            type: "extension_event",
            id: 0,
            data: {
                event_name: "context_changed_proactive",
                context: message.context
            }
        });
        return false;
    }

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
            type: "response", 
            status: "error",
            error: "No tab ID for screenshot."
        });
        return;
    }
    try {
        const dataUrl = await chrome.tabs.captureVisibleTab(tabId, { format: "png" });
        console.log("Screenshot captured for tab:", tabId);
        sendResponse({
            type: "response", 
            status: "success",
            data: { screenshot: dataUrl } 
        });
    } catch (error) {
        console.error("Error capturing screenshot:", error);
        sendResponse({
            type: "response", 
            status: "error",
            error: `Screenshot capture failed: ${error.message}`
        });
    }
}

/**
 * Sends a simple context update to the server.
 * @param {string} eventName - The name of the event (e.g., "tab_activated", "tab_updated").
 * @param {object} tab - The Chrome tab object.
 */
function sendTabContextUpdate(eventName, tab) {
    if (!tab) {
        console.warn(`Cannot send ${eventName} update, tab object is missing.`);
        return;
    }
    console.log(`Preparing to send ${eventName} for tab ID ${tab.id}, URL: ${tab.url}`);

    const context = {
        event_name: eventName,
        tabId: tab.id,
        url: tab.url,
        title: tab.title,
        active: tab.active,
        windowId: tab.windowId
    };

    sendDataToServer({
        type: "extension_event", 
        id: 0,
        data: context 
    });
}

// Tab management and active tab tracking
chrome.tabs.onActivated.addListener(activeInfo => {
    console.log("chrome.tabs.onActivated fired. New active tab ID:", activeInfo.tabId);
    activeTabId = activeInfo.tabId;
    chrome.tabs.get(activeInfo.tabId, (tab) => {
        if (chrome.runtime.lastError) {
            console.error("Error getting tab details in onActivated:", chrome.runtime.lastError.message);
            return;
        }
        if (tab) {
            sendTabContextUpdate("tab_activated", tab);
        }
    });
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    console.log("chrome.tabs.onUpdated fired. Tab ID:", tabId, "ChangeInfo:", changeInfo);
    if (changeInfo.status === 'complete' && tab.url && tab.url !== "chrome://newtab/") {
        console.log("Tab update complete and URL present:", tab.url);
        activeTabId = tabId;
        sendTabContextUpdate("tab_updated_complete", tab);
    } else if (changeInfo.url) {
        console.log("Tab URL changed to:", changeInfo.url);
        activeTabId = tabId;
        chrome.tabs.get(tabId, (updatedTab) => {
            if (chrome.runtime.lastError) {
                console.error("Error getting tab details in onUpdated (url change):", chrome.runtime.lastError.message);
                return;
            }
            if (updatedTab) {
                sendTabContextUpdate("tab_url_changed", updatedTab);
            }
        });
    }
});

chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
    console.log("Tab removed:", tabId);
    const eventContext = {
        event_name: "tab_removed",
        tabId: tabId,
        windowId: removeInfo.windowId,
        isWindowClosing: removeInfo.isWindowClosing
    };
    sendDataToServer({ type: "extension_event", id: 0, data: eventContext });

    if (activeTabId === tabId) {
        console.log("Active tab was closed. Querying for new active tab.");
        queryActiveTab(true);
    }
});

/**
 * Queries for the currently active tab and updates activeTabId.
 * Optionally sends context update if a new active tab is found.
 * @param {boolean} [sendContext=false] - Whether to send context update for the new active tab.
 */
function queryActiveTab(sendContext = false) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (chrome.runtime.lastError) {
            console.error("Error querying active tab:", chrome.runtime.lastError.message);
            activeTabId = null;
            return;
        }
        if (tabs.length > 0) {
            const newActiveTab = tabs[0];
            if (activeTabId !== newActiveTab.id || sendContext) {
                console.log("Querying active tab. Found:", newActiveTab.id, newActiveTab.url);
                activeTabId = newActiveTab.id;
                if (sendContext) {
                    sendTabContextUpdate("tab_activated_on_query", newActiveTab);
                }
            }
        } else {
            console.log("No active tab found during query.");
            activeTabId = null; 
        }
    });
}

// Initial setup
console.log("Background script started.");
connectWebSocket(); 