// browser-use-ext/extension/background.js
// Establishes and manages WebSocket connection with the Python backend.
// Handles messages from content scripts and the Python backend.
// Manages browser tab interactions.

const WS_URL = "ws://localhost:8765";
let websocket = null;
let activeTabId = null;
let reconnectInterval = 5000; // 5 seconds
const contentScriptsReady = new Set(); // Stores tabIds where content script is ready
const CONTENT_SCRIPT_READY_TIMEOUT = 3000; // 3 seconds to wait for content script ready signal

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
                const includeScreenshot = serverParams && serverParams.includeScreenshot === true;

                if (activeTabId) {
                    console.log(`Attempting to get state for tab ${activeTabId}. Checking if content script is ready.`);

                    // Wait for the content script to be ready in the target tab
                    const isReady = await waitForContentScriptReady(activeTabId, CONTENT_SCRIPT_READY_TIMEOUT);

                    if (!isReady) {
                        console.warn(`Content script in tab ${activeTabId} did not signal ready within timeout for get_state (ID: ${requestId}).`);
                        throw new Error(`Content script in tab ${activeTabId} not ready after ${CONTENT_SCRIPT_READY_TIMEOUT}ms`);
                    }
                    
                    console.log(`Content script for tab ${activeTabId} is ready. Forwarding 'get_state' (ID: ${requestId}).`);
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

                // Screenshot logic now centralized here, but Python currently expects null.
                let screenshotData = null; // Default to null as Python expects

                if (includeScreenshot && activeTabId) {
                    console.warn(`Python requested includeScreenshot=true, but current implementation forces screenshot to null for Python.`);
                    // try {
                    //     console.log(`Attempting to capture screenshot for tab ${activeTabId} (request ID: ${requestId}) because includeScreenshot was true.`);
                    //     screenshotData = await chrome.tabs.captureVisibleTab(null, { format: "png" }); 
                    //     console.log("Screenshot captured successfully.");
                    // } catch (error) {
                    //     console.error(`Error capturing screenshot for tab ${activeTabId} (request ID: ${requestId}):`, error);
                    //     // Keep screenshotData as null
                    // }
                } else {
                    console.log(`Screenshot not requested (includeScreenshot: ${includeScreenshot}) or no active tab for screenshot.`);
                }

                const finalDataPayload = {
                    success: true, ...pageSpecificData, tabs: formattedTabs, screenshot: screenshotData // Ensure this is consistently null for now
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
        return false; 
    }
    // ADDED: Listener for content_script_ready
    else if (sender.tab && message.type === "content_script_ready") {
        console.log(`Content script in tab ${sender.tab.id} reported ready.`);
        contentScriptsReady.add(sender.tab.id);
        // Optionally, acknowledge back to content script
        sendResponse({ status: "acknowledged", tabId: sender.tab.id });
        // Clean up tabId from the set if the tab is closed (see onRemoved listener)
        return true; // Acknowledging async response
    }
    // Handle messages from the POPUP
    else if (message.source === "POPUP_ACTION") {
        if (message.action === "GET_POPUP_STATUS") {
            console.log("Popup requested status.");
            queryActiveTab(false); // Update activeTabId without sending context
            sendResponse({
                websocketStatus: websocket ? websocket.readyState : WebSocket.CLOSED,
                activeTabId: activeTabId
            });
        } else {
            console.warn("Unknown popup action:", message.action);
            sendResponse({ error: "Unknown popup action" });
        }
        return true; // Indicate async response for popup messages
    }
    // Add other specific message handlers here if needed, e.g., from popup for other actions

    console.warn("Message type not explicitly handled in onMessage listener or response already sent:", message.type, "Sender:", sender.id);
    // Return false if not handling the message or not intending to send an async response from this top-level listener.
    // Specific handlers might return true if they use sendResponse asynchronously.
    return false;
});

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
    console.log("Tab activated:", activeInfo);
    activeTabId = activeInfo.tabId;
    // Fetch tab details as onActivated only gives tabId and windowId
    chrome.tabs.get(activeInfo.tabId, (tab) => {
        if (chrome.runtime.lastError) {
            console.error("Error getting tab details in onActivated:", chrome.runtime.lastError.message);
            return;
        }
        if (tab) {
            console.log("Active tab details:", tab);
            // Only send update if websocket is ready and tab is fully loaded
            // The onUpdated listener will handle sending page_fully_loaded_and_ready when status is 'complete'
            // This can send a simpler "tab_activated" event if needed.
            // sendTabContextUpdate("tab_activated", tab);

            // If the newly activated tab is already loaded, we might want to send the event here too.
            // This is a bit redundant if onUpdated also fires, but covers cases where activation happens
            // to an already loaded tab without an 'onUpdated' event with status 'complete'.
            if (tab.status === 'complete' && tab.url && (tab.url.startsWith('http://') || tab.url.startsWith('https://'))) {
                if (websocket && websocket.readyState === WebSocket.OPEN) {
                    const eventData = {
                        type: "extension_event",
                        id: Date.now() + 1, // Slightly different ID for debugging
                        data: {
                            event_name: "page_fully_loaded_and_ready", // Sending same event name
                            reason: "tab_activated_and_complete", // Add a reason for debugging
                            tabId: tab.id,
                            url: tab.url,
                            title: tab.title
                        }
                    };
                    sendDataToServer(eventData);
                    console.info(`Sent 'page_fully_loaded_and_ready' (onActivated) for tab ${tab.id} to Python server.`);
                }
            }
        }
    });
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    console.log("Tab updated:", tabId, "ChangeInfo:", changeInfo, "Tab:", tab);
    // Ensure the update is for the main frame and the tab is completely loaded
    if (changeInfo.status === 'complete' && tab.url && (tab.url.startsWith('http://') || tab.url.startsWith('https://'))) {
        console.log(`Tab ${tabId} finished loading: ${tab.url}`);
        activeTabId = tabId; // Update activeTabId if the completed tab is now active or just becomes the focus.

        // ADDED: Send 'page_fully_loaded_and_ready' event to Python server
        if (websocket && websocket.readyState === WebSocket.OPEN) {
            const eventData = {
                type: "extension_event",
                // Python server doesn't use an ID for events like this, but good practice to have a type.
                // If a specific ID were needed for correlation on Python side for this event, it would be generated here.
                id: Date.now(), // Simple unique ID for this event instance, if server needs it later.
                data: {
                    event_name: "page_fully_loaded_and_ready",
                    tabId: tabId,
                    url: tab.url,
                    title: tab.title
                }
            };
            sendDataToServer(eventData);
            console.info(`Sent 'page_fully_loaded_and_ready' event for tab ${tabId} to Python server.`);
        } else {
            console.warn("WebSocket not open, cannot send 'page_fully_loaded_and_ready' event.");
        }

        // Existing logic to send proactive context update to Python server can remain or be adjusted
        // For now, let's keep it to see if it conflicts or complements.
        // sendTabContextUpdate("tab_updated_complete", tab);
    }

    // Proactive update for when tab is just activated (might not be fully loaded yet)
    if (changeInfo.status === 'loading' && tab.active) {
        activeTabId = tabId;
        // sendTabContextUpdate("tab_activated_loading", tab);
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
    // ADDED: Clean up from contentScriptsReady set
    if (contentScriptsReady.has(tabId)) {
        contentScriptsReady.delete(tabId);
        console.log(`Removed tab ${tabId} from contentScriptsReady set.`);
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

// ADDED: Helper function to wait for content script readiness
async function waitForContentScriptReady(tabId, timeoutMs) {
    if (contentScriptsReady.has(tabId)) {
        return true;
    }
    console.log(`Waiting for content script to be ready in tab ${tabId}...`);
    const startTime = Date.now();
    while (Date.now() - startTime < timeoutMs) {
        if (contentScriptsReady.has(tabId)) {
            console.log(`Content script for tab ${tabId} became ready.`);
            return true;
        }
        // Check if tab still exists
        try {
            await chrome.tabs.get(tabId);
        } catch (e) {
            console.warn(`Tab ${tabId} closed or does not exist while waiting for content script ready.`);
            contentScriptsReady.delete(tabId); // Clean up if tab is gone
            return false; 
        }
        await new Promise(resolve => setTimeout(resolve, 100)); // Poll every 100ms
    }
    console.warn(`Timeout waiting for content script in tab ${tabId} after ${timeoutMs}ms.`);
    return false;
}

connectWebSocket();
// connectWebSocket(); // MODIFIED: Removed duplicate call 