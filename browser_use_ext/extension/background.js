// browser-use-ext/extension/background.js
// Establishes and manages WebSocket connection with the Python backend.
// Handles messages from content scripts and the Python backend.
// Manages browser tab interactions.

const WS_URL = "ws://localhost:8765";
let websocket = null;
let activeTabId = null;
let reconnectInterval = 5000; // 5 seconds
const contentScriptsReady = new Set(); // Stores tabIds where content script is ready
const CONTENT_SCRIPT_READY_TIMEOUT = 10000; // Increased to 10 seconds

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

                // MODIFIED: Determine targetTabId from serverParams first, then fallback to activeTabId if not provided
                // The Python server should now always send a tabId for get_state calls triggered by events.
                let targetTabIdForState = serverParams.tabId; // Python sends this as "tabId"

                if (!targetTabIdForState && activeTabId) {
                    console.warn(`'get_state' (ID: ${requestId}) called without an explicit tabId from server, using current activeTabId: ${activeTabId}`);
                    targetTabIdForState = activeTabId;
                } else if (!targetTabIdForState && !activeTabId) {
                    console.warn(`'get_state' (ID: ${requestId}) called without an explicit tabId and no global activeTabId. Page-specific data will be default.`);
                    // No targetTabIdForState, pageSpecificData will remain default
                }

                if (targetTabIdForState) {
                    console.log(`Attempting to get state for target tab ${targetTabIdForState}. Checking if content script is ready. Request ID: ${requestId}`);

                    const isReady = await waitForContentScriptReady(targetTabIdForState, CONTENT_SCRIPT_READY_TIMEOUT);

                    if (!isReady) {
                        console.warn(`Content script in tab ${targetTabIdForState} did not signal ready within timeout for get_state (ID: ${requestId}).`);
                        throw new Error(`Content script in tab ${targetTabIdForState} not ready after ${CONTENT_SCRIPT_READY_TIMEOUT}ms`);
                    }
                    
                    console.log(`Content script for tab ${targetTabIdForState} is ready. Forwarding 'get_state' (ID: ${requestId}).`);
                    const contentResponse = await chrome.tabs.sendMessage(targetTabIdForState, {
                        type: "get_state", 
                        requestId: requestId
                    });

                    if (contentResponse && contentResponse.status === "success" && contentResponse.data) {
                        console.log(`Received state from content script for ID ${requestId} (Tab: ${targetTabIdForState}):`, contentResponse.data);
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
                        const errorMsg = contentResponse ? contentResponse.error : `No response or error from content script for get_state on tab ${targetTabIdForState}.`;
                        console.warn(errorMsg, `(ID: ${requestId})`);
                        // Do not throw here, allow collection of general tab data
                    }
                } // End if (targetTabIdForState)

                const allTabsRaw = await chrome.tabs.query({});
                const formattedTabs = allTabsRaw.map(t => ({
                    tabId: t.id, url: t.url || "", title: t.title || "", isActive: t.active
                }));

                // Screenshot logic now centralized here, but Python currently expects null.
                let screenshotData = null; // Default to null as Python expects

                if (includeScreenshot && targetTabIdForState) {
                    console.warn(`Python requested includeScreenshot=true, but current implementation forces screenshot to null for Python.`);
                    // try {
                    //     console.log(`Attempting to capture screenshot for tab ${targetTabIdForState} (request ID: ${requestId}) because includeScreenshot was true.`);
                    //     screenshotData = await chrome.tabs.captureVisibleTab(null, { format: "png" }); 
                    //     console.log("Screenshot captured successfully.");
                    // } catch (error) {
                    //     console.error(`Error capturing screenshot for tab ${targetTabIdForState} (request ID: ${requestId}):`, error);
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

            console.log(`Forwarding action '${subActionName}' (ID: ${requestId}) to tab ${activeTabId} as type 'execute_action'`);
            // Ensure content script is ready before sending execute_action
            const isReady = await waitForContentScriptReady(activeTabId, CONTENT_SCRIPT_READY_TIMEOUT);
            if (!isReady) {
                console.error(`Content script in tab ${activeTabId} not ready for execute_action (ID: ${requestId}).`);
                sendDataToServer({
                    type: "response",
                    id: requestId,
                    data: { success: false, error: `Content script in tab ${activeTabId} not ready after ${CONTENT_SCRIPT_READY_TIMEOUT}ms` }
                });
                return;
            }

            chrome.tabs.sendMessage(activeTabId, {
                type: "execute_action",       // CORRECTED: Send 'execute_action' as the type
                payload: {                  // CORRECTED: Nest subActionName and subActionParams in payload
                    action: subActionName,
                    params: subActionParams
                },
                requestId: requestId
            }).then(response => {
                console.log(`Response from content script for action '${subActionName}' (ID: ${requestId}):`, response);
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
                    console.warn(`Undefined or malformed response from content script for action: '${subActionName}' (ID: ${requestId}). Tab ID: ${activeTabId}`);
                    sendDataToServer({ type: "response", id: requestId, data: { success: false, error: `Content script for action '${subActionName}' returned malformed response. Tab ID: ${activeTabId}` }});
                }
            }).catch(error => {
                console.error(`Error sending/receiving for action '${subActionName}' (ID: ${requestId}):`, error);
                sendDataToServer({ type: "response", id: requestId, data: { success: false, error: `Failed to communicate with content script for action '${subActionName}': ${error.message}` }});
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

// Listener for messages from content scripts or other extension parts (e.g., popup)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // Handle readiness signal from content script
    if (sender.tab && message.type === "content_script_ready") {
        console.log(`background.js: Received 'content_script_ready' from tabId: ${sender.tab.id}`);
        contentScriptsReady.add(sender.tab.id);
        sendResponse({ status: "acknowledged_content_script_ready", tabId: sender.tab.id });

        // NEW: Check if this tab is also complete and then send page_fully_loaded_and_ready
        // This helps if onUpdated fired before content_script_ready was processed.
        chrome.tabs.get(sender.tab.id, (tabDetails) => {
            if (chrome.runtime.lastError) {
                console.error(`Error getting tab details for ${sender.tab.id} after content_script_ready:`, chrome.runtime.lastError.message);
                return;
            }
            if (tabDetails && tabDetails.status === 'complete' && tabDetails.url && !tabDetails.url.startsWith('chrome://')) {
                console.log(`Content script for tab ${sender.tab.id} is ready, and tab status is complete. Sending page_fully_loaded_and_ready from onMessage handler.`);
                sendPageFullyLoadedAndReadyEventToPython(sender.tab.id, tabDetails.url, tabDetails.title, "cs_ready_and_tab_complete");
            } else {
                console.log(`Content script for tab ${sender.tab.id} is ready, but tab not yet complete (Status: ${tabDetails?.status}). Waiting for onUpdated.`);
            }
        });

        return true; // For async response
    }

    // Handle messages from content scripts intended for the server (e.g., responses to actions)
    // This assumes content script sends messages with a specific structure for server forwarding
    if (message.type === "forward_to_server") { // Example: Content script wants to send something to Python
        console.log("Forwarding message from content script to server:", message.payload);
        // Ensure the message payload from content script is structured as expected by sendDataToServer
        // or directly by the Python server if sendDataToServer just wraps it.
        sendDataToServer(message.payload); 
        sendResponse({status: "Message forwarded to server"});
        return true;
    }

    // Handle other message types from popup or other parts of the extension if necessary
    if (message.type === "GET_WS_STATUS") {
        sendResponse({ status: websocket && websocket.readyState === WebSocket.OPEN ? "Connected" : "Disconnected" });
        return true;
    }

    // If not handled, log and potentially return false or nothing
    console.log("Background.js received unhandled message type or from unexpected sender:", message, sender);
    // sendResponse({status: "unknown_message_type"}); // Optionally respond for unhandled types
    return false; // If not sending an async response or if not handled
});

// Clean up contentScriptsReady set when a tab is removed
chrome.tabs.onRemoved.addListener(tabId => {
    if (contentScriptsReady.has(tabId)) {
        contentScriptsReady.delete(tabId);
        console.log(`background.js: Removed tabId ${tabId} from contentScriptsReady set due to tab removal.`);
    }
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
            // MODIFIED: Check both tab.status and contentScriptsReady
            if (tab.status === 'complete' && tab.url && (tab.url.startsWith('http://') || tab.url.startsWith('https://'))) {
                if (contentScriptsReady.has(tab.id)) {
                    console.log(`background.js: Tab ${tab.id} activated, is complete, and content script is ready. Sending page_fully_loaded_and_ready.`);
                    if (websocket && websocket.readyState === WebSocket.OPEN) {
                        // Using the helper function for consistency
                        sendPageFullyLoadedAndReadyEventToPython(tab.id, tab.url, tab.title, "tab_activated_and_cs_ready_and_tab_complete");
                    } else {
                         console.warn(`WebSocket not open, cannot send 'page_fully_loaded_and_ready' (Reason: tab_activated_and_cs_ready_and_tab_complete) for tab ${tab.id}.`);
                    }
                } else {
                    console.log(`background.js: Tab ${tab.id} activated and is complete, but content script NOT YET ready. Waiting for content_script_ready message or onUpdated.`);
                    // The onMessage listener for "content_script_ready" will handle sending the event if tab is also complete.
                    // The onUpdated listener will also handle sending if content script becomes ready later.
                }
            } else {
                 console.log(`background.js: Tab ${tab.id} activated, but not yet complete (Status: ${tab.status}) or content script not ready, or not a http(s) URL. Will rely on onUpdated or onMessage for 'page_fully_loaded_and_ready'.`);
            }
        }
    });
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    console.log("Tab updated:", tabId, "ChangeInfo:", changeInfo, "Tab:", tab);
    // Ensure the update is for the main frame and the tab is completely loaded
    if (changeInfo.status === 'complete' && tab.url && (tab.url.startsWith('http://') || tab.url.startsWith('https://'))) {
        console.log(`Tab ${tabId} finished loading: ${tab.url}`);
        // activeTabId = tabId; // Update activeTabId - This is handled by onActivated mostly

        // MODIFIED: Only send page_fully_loaded_and_ready if content script is also ready.
        if (contentScriptsReady.has(tabId)) {
            console.log(`background.js: Tab ${tabId} is complete and content script already reported ready. Sending page_fully_loaded_and_ready to Python.`);
            sendPageFullyLoadedAndReadyEventToPython(tabId, tab.url, tab.title, "tab_updated_and_content_script_was_ready");
        } else {
            console.log(`background.js: Tab ${tabId} is complete, but content script has NOT YET reported ready. Waiting for content_script_ready signal.`);
            // We will now rely on the content_script_ready handler to send the event once it fires for this tab.
        }
    }

    // Proactive update for when tab is just activated (might not be fully loaded yet)
    // if (changeInfo.status === 'loading' && tab.active) { // This might be too noisy or premature
    // activeTabId = tabId;
    // sendTabContextUpdate("tab_activated_loading", tab);
    // }
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
    const startTime = Date.now();
    console.log(`background.js: waitForContentScriptReady called for tabId: ${tabId}, timeout: ${timeoutMs}ms`);
    while (Date.now() - startTime < timeoutMs) {
        if (contentScriptsReady.has(tabId)) {
            console.log(`background.js: Content script for tabId: ${tabId} is ready.`);
            return true;
        }
        console.log(`background.js: Polling for content script ready for tabId: ${tabId}. Still waiting...`);
        await new Promise(resolve => setTimeout(resolve, 250)); // Poll every 250ms
    }
    console.error(`background.js: Timeout waiting for content script in tab ${tabId} to signal ready after ${timeoutMs}ms.`);
    return false;
}

/**
 * Helper function to send the 'page_fully_loaded_and_ready' event to the Python server.
 * @param {number} tabId
 * @param {string} url
 * @param {string} title
 * @param {string} reason - For logging/debugging, why this event is being sent.
 */
function sendPageFullyLoadedAndReadyEventToPython(tabId, url, title, reason) {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        const eventData = {
            type: "extension_event",
            id: Date.now(), 
            data: {
                event_name: "page_fully_loaded_and_ready",
                reason: reason, // Added reason for better debugging
                tabId: tabId,
                url: url,
                title: title
            }
        };
        sendDataToServer(eventData);
        console.info(`Sent 'page_fully_loaded_and_ready' (Reason: ${reason}) for tab ${tabId} to Python server.`);
    } else {
        console.warn(`WebSocket not open, cannot send 'page_fully_loaded_and_ready' (Reason: ${reason}) event for tab ${tabId}.`);
    }
}

connectWebSocket();
// connectWebSocket(); // MODIFIED: Removed duplicate call 
console.log("background.js: Script loaded, listeners initialized."); 