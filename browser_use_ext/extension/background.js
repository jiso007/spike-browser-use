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
async function handleServerMessage(message) {
    console.log("Handling server message:", message);

    // Python sends: { id: number, type: string (e.g., "get_state", "execute_action"), data: object (params for action) }
    if (message.id !== undefined && typeof message.type === 'string') {
        const requestId = message.id;
        const serverActionType = message.type; // This is "get_state" or "execute_action"
        const serverParams = message.data || {};   // Parameters sent from Python

        // Initial check for activeTabId, similar to before but simplified
        if (!activeTabId && serverActionType !== "get_state" && serverActionType !== "get_state_without_active_tab") {
            console.warn(`No active tab for action '${serverActionType}' (ID: ${requestId})`);
            sendDataToServer({
                type: "response",
                id: requestId,
                data: { success: false, error: "No active tab identified." }
            });
            return;
        }
        if (!activeTabId && serverActionType === "get_state"){
            console.warn(`'get_state' called but no activeTabId. Proceeding to fetch all tabs, but page-specific data will be from a default/empty state.`);
            // Allows get_state to proceed even without activeTabId for initial state capture (mostly tabs list)
        }

        if (serverActionType === "get_state") {
            try {
                let pageSpecificData = {
                    url: "about:blank", title: "",
                    html_content: "<html><head></head><body></body></html>",
                    tree: { type: "document", children: [{ type: "element", name: "html", attributes: {}, children: [ {type: "element", name: "head", attributes: {}, children: []}, {type: "element", name: "body", attributes: {}, children: []} ]}]},
                    selector_map: {},
                    pixels_above: 0, pixels_below: 0,
                };

                if (activeTabId) {
                    console.log(`Forwarding 'get_state' (ID: ${requestId}) to content script in tab ${activeTabId}`);
                    const contentResponse = await chrome.tabs.sendMessage(activeTabId, {
                        type: "get_state", // Message type for content.js
                        payload: serverParams, // Python's params (e.g., {"includeScreenshot": ...})
                        requestId: requestId
                    });

                    if (contentResponse && contentResponse.status === "success" && contentResponse.data) {
                        console.log(`Received state from content script for ID ${requestId}:`, contentResponse.data);
                        pageSpecificData.url = contentResponse.data.url || pageSpecificData.url;
                        pageSpecificData.title = contentResponse.data.title || pageSpecificData.title;
                        pageSpecificData.html_content = contentResponse.data.html_content || pageSpecificData.html_content;
                        pageSpecificData.tree = contentResponse.data.tree || pageSpecificData.tree;
                        pageSpecificData.selector_map = contentResponse.data.selector_map || pageSpecificData.selector_map;
                        pageSpecificData.pixels_above = contentResponse.data.scroll_y !== undefined ? contentResponse.data.scroll_y : 0;
                        pageSpecificData.pixels_below = contentResponse.data.page_content_height !== undefined && contentResponse.data.scroll_y !== undefined && contentResponse.data.viewport_height !== undefined ?
                                                       Math.max(0, contentResponse.data.page_content_height - (contentResponse.data.scroll_y + contentResponse.data.viewport_height))
                                                       : 0;
                    } else {
                        const errorMsg = contentResponse ? contentResponse.error : "No response or error from content script for get_state.";
                        console.warn(errorMsg, `(ID: ${requestId})`);
                    }
                } // End if (activeTabId)

                const allTabsRaw = await chrome.tabs.query({});
                const formattedTabs = allTabsRaw.map(t => ({
                    tabId: t.id, url: t.url || "", title: t.title || "", isActive: t.active
                }));

                const finalDataPayload = {
                    success: true, ...pageSpecificData, tabs: formattedTabs, screenshot: null
                };
                sendDataToServer({ type: "response", id: requestId, data: finalDataPayload });

            } catch (error) {
                console.error(`Error processing 'get_state' in background.js (ID: ${requestId}):`, error);
                sendDataToServer({ type: "response", id: requestId, data: { success: false, error: `Background script error during 'get_state': ${error.message}` }});
            }
        } else if (serverActionType === "execute_action") {
            // For execute_action, serverParams is {action: "sub_action_name", params: {sub_action_params}}
            const subActionName = serverParams.action;
            const subActionParams = serverParams.params;

            if (!activeTabId) { // Should have been caught earlier, but double check for execute_action
                 console.warn("No active tab for execute_action:", subActionName, `(ID: ${requestId})`);
                 sendDataToServer({type: "response", id: requestId, data: { success: false, error: "No active tab to process action."}});
                 return;
            }
            if (!subActionName) {
                console.error(`'execute_action' request (ID: ${requestId}) from server is missing the nested 'action' field in its data.`);
                sendDataToServer({ type: "response", id: requestId, data: { success: false, error: "Malformed execute_action from server: missing nested action." }});
                return;
            }

            console.log(`Forwarding sub-action '${subActionName}' (ID: ${requestId}) to tab ${activeTabId}`);
            chrome.tabs.sendMessage(activeTabId, {
                type: subActionName,       // This is the actual action for content.js (e.g., "click_element_by_index")
                payload: subActionParams,  // These are the params for the sub-action
                requestId: requestId
            }).then(response => {
                console.log(`Response from content script for sub-action '${subActionName}' (ID: ${requestId}):`, response);
                if (response && response.type === "response") {
                    sendDataToServer({
                        type: "response",
                        id: response.request_id || requestId,
                        data: { 
                            success: response.status === "success",
                            error: response.status === "error" ? response.error : null,
                            ...(response.data || {})
                        }
                    });
                } else {
                    console.warn(`Undefined or malformed response from content script for sub-action: '${subActionName}' (ID: ${requestId}). Tab ID: ${activeTabId}`);
                    sendDataToServer({ type: "response", id: requestId, data: { success: false, error: `Content script for sub-action '${subActionName}' returned malformed response. Tab ID: ${activeTabId}` }});
                }
            }).catch(error => {
                console.error(`Error sending/receiving for sub-action '${subActionName}' (ID: ${requestId}):`, error);
                sendDataToServer({ type: "response", id: requestId, data: { success: false, error: `Failed to communicate with content script for sub-action '${subActionName}': ${error.message}` }});
            });
        } else {
            console.warn(`Received unhandled server action type '${serverActionType}' (ID: ${requestId}):`, message);
            sendDataToServer({ type: "response", id: requestId, data: { success: false, error: `Unknown server action type: ${serverActionType}` }});
        }
    } else {
        console.warn("Received message from server that is not a recognized action request or is malformed (missing id/type):", message);
        // Optionally send an error back if the message structure is completely off and an ID is parseable
        if (message && message.id !== undefined) {
            sendDataToServer({ type: "response", id: message.id, data: { success: false, error: "Malformed request from server." }});
        }
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

    // Handle messages from content.js (typically responses to server requests that were relayed by background.js)
    if (sender.tab && message.type === "response_to_server") {
        console.log("Forwarding response from content script to server:", message.payload);
        sendDataToServer({
            type: "response",
            id: message.payload.id, // This should be the original Python request ID
            data: message.payload.data // This is the actual data payload from content.js
        });
        // This specific path for "response_to_server" is not using sendResponse back to the original sender (content.js),
        // it's forwarding to Python. So, not returning true here is okay.
        return false; 
    }
    // MODIFIED: Added handler for "request_screenshot" from content.js
    else if (message.type === "request_screenshot") {
        if (sender.tab && sender.tab.id) {
            handleScreenshotRequest(message.requestId, sender.tab.id, sendResponse);
        } else {
            // Fallback if sender.tab.id is not available (should not happen if sent from content script)
            console.warn("Screenshot requested without a valid sender tab ID. Attempting with activeTabId if available.");
            if (activeTabId) {
                handleScreenshotRequest(message.requestId, activeTabId, sendResponse);
            } else {
                console.error("Cannot fulfill screenshot request: no valid tab ID.");
                sendResponse({
                    request_id: message.requestId,
                    type: "response",
                    status: "error",
                    error: "Background script could not determine tab ID for screenshot."
                });
            }
        }
        return true; // Crucial: Indicates that sendResponse will be called asynchronously by handleScreenshotRequest
    } 
    // else if (message.type === "WS_STATUS_REQUEST") { // Example for popup requests
    //    sendResponse({ status: websocket && websocket.readyState === WebSocket.OPEN ? "Connected" : "Disconnected" });
    //    return false; // Synchronous response
    // }

    // If the message isn't handled by any of the above, 
    // and sendResponse isn't called, the channel might close for the sender if they expect a response.
    // For messages not expecting a response, or for which `return true` was not used, this is fine.
    console.log("Message type not explicitly handled in onMessage listener or response already sent:", message.type);
    // Default to not keeping the channel open if not handled explicitly for async response.
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
// connectWebSocket(); // MODIFIED: Removed duplicate call 