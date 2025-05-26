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

// ADDED CODE based on PERPLEXITY_OUTPUT.md
// Handle content script ready signals
function handleContentScriptReady(request, sender, sendResponse) {
    const tabId = sender.tab?.id;
    
    if (!tabId) {
        console.error('Content script ready signal missing tab ID from sender');
        sendResponse({ error: 'Missing tab ID in sender object', status: "error_missing_tab_id" });
        return; // Explicitly return for clarity, sendResponse is sync here
    }
    
    console.log(`Background: 'content_script_ready' signal received from tab ${tabId}`);
    contentScriptsReady.add(tabId);
    
    // Send acknowledgment
    sendResponse({ 
        acknowledged: true, 
        tabId: tabId,
        status: "acknowledged_content_script_ready", // Added status for clarity
        timestamp: Date.now()
    });
    
    console.log(`Background: Tab ${tabId} marked as ready. Ready tabs:`, Array.from(contentScriptsReady));
}
// END ADDED CODE

// Listener for messages from content scripts or other extension parts (e.g., popup)
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    // Log all incoming messages for debugging
    // console.log('Background.js: Received runtime message:', request, 'from sender:', sender);

    if (sender.tab && request.type === "content_script_ready") {
        // This specific log is in the chrome_extension_content_readiness.mdc rule
        console.log(`background.js: Received 'content_script_ready' from tabId: ${sender.tab.id}`);
        // Delegate to the new handler
        handleContentScriptReady(request, sender, sendResponse);
        // sendResponse is called synchronously within handleContentScriptReady
        // For content_script_ready, the response is synchronous. Return false.
        return false; 
    }
    // IMPORTANT: If this listener is intended to handle more message types (e.g., from popup),
    // ensure they are handled here. If other listeners exist, ensure this one returns `true`
    // appropriately for messages it handles asynchronously, and `false` or nothing for
    // messages it doesn't handle (or handles synchronously) to allow other listeners to run.

    // Example of how other messages could be routed (currently, only content_script_ready is explicitly handled here)
    // switch (request.type) {
    //     case 'content_script_ready':
    //         handleContentScriptReady(request, sender, sendResponse);
    //         return false; // Synchronous for this specific message type
    //     case 'get_state_from_content': // Example: if content script sends data directly
    //         handleGetStateRequest(request, sender, sendResponse); // Hypothetical handler
    //         return true; // Async
    //     case 'execute_action_from_content': // Example
    //         handleExecuteActionRequest(request, sender, sendResponse); // Hypothetical handler
    //         return true; // Async
    //     default:
    //         console.warn('Background.js: Received unhandled runtime message type:', request.type);
    //         // sendResponse({ error: 'Unknown message type in background.js' });
    //         // Return false or undefined if not handling, to allow other listeners a chance.
    //         return false;
    // }

    // The `chrome_extension_content_readiness` rule shows `return true; // For async response` 
    // in the generic onMessage listener. This is crucial IF there are async operations *directly* in this listener.
    // Since `handleContentScriptReady` calls `sendResponse` synchronously, for that path, `false` is correct.
    // If this listener expands, this return behavior needs careful management.
    // For now, focusing only on content_script_ready, and assuming it's the main purpose of this listener block.
    // If other messages are expected, this logic needs to be more robust.
    // Let's stick to the provided PERPLEXITY output for now for other messages, which seems to use a different handler for server messages.

    // The PERPLEXITY_OUTPUT.md `background.js` has a different onMessage listener structure:
    /*
    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
        console.log('Background received message:', request.type, 'from tab:', sender.tab?.id);
        
        switch (request.type) {
            case 'content_script_ready':
                handleContentScriptReady(request, sender, sendResponse);
                return false; // Synchronous response
                
            case 'get_state': // This implies content.js might send 'get_state' directly to background
                handleGetStateRequest(request, sender, sendResponse); // Assumes a direct request from content to background
                return true; // Asynchronous response
                
            case 'execute_action': // This implies content.js might send 'execute_action' directly to background
                handleExecuteActionRequest(request, sender, sendResponse); // Assumes a direct request from content to background
                return true; // Asynchronous response
                
            default:
                console.warn('Unknown message type received by background.js runtime message listener:', request.type);
                sendResponse({ error: 'Unknown message type in background.js runtime listener' });
                return false;
        }
    });
    */
    // For now, only explicitly handling 'content_script_ready' in this listener as per the task.
    // Other messages like 'get_state' and 'execute_action' are primarily initiated by the Python server via WebSocket
    // and then sent to content.js, not the other way around for these core commands.
    // The POPUP script might send other messages, which this listener should also handle if needed.

    // ADDED: Debug utility to get currently ready tabs
    else if (request.type === "debug_get_ready_tabs") {
        const readyTabsArray = Array.from(contentScriptsReady);
        console.log("Background: Debug: Currently ready tabs:", readyTabsArray);
        sendResponse({ status: "ok", readyTabs: readyTabsArray });
        return false; // Synchronous response for this debug utility.
    }

    // Fallback for messages not handled by the `if` above.
    // If this is the *only* runtime message listener, unhandled messages might need an error response.
    // If there are other listeners, `return false` (or `undefined`) is usually correct to allow them to process.
    if (request.type !== "content_script_ready") {
        console.warn(`Background.js: Unhandled runtime message type '${request.type}' from sender:`, sender);
        // Optionally send a response if no other listeners are expected to handle it.
        // sendResponse({ error: `Unhandled message type: ${request.type}` });
    }
    // Returning false to indicate synchronous response or that the message was not handled here,
    // allowing other listeners (if any) to process it. If this is the only listener, this is fine.
    return false;
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
    // console.log(`background.js: waitForContentScriptReady called for tabId: ${tabId}, timeout: ${timeoutMs}ms`); // From rule
    const startTime = Date.now();
    // console.log(`Background.js: waitForContentScriptReady called for tabId: ${tabId}, timeout: ${timeoutMs}ms`); // Duplicated log from rule
    while (Date.now() - startTime < timeoutMs) {
        if (contentScriptsReady.has(tabId)) {
            console.log(`background.js: Content script for tabId: ${tabId} is ready.`);
            return true;
        }
        console.log(`background.js: Polling for content script ready for tabId: ${tabId}. Still waiting...`); // From rule, ensure it is active
        await new Promise(resolve => setTimeout(resolve, 250)); // Poll frequently - as per rule
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

// ADDED: Cleanup when tabs are closed (from PERPLEXITY_OUTPUT.md and rule)
chrome.tabs.onRemoved.addListener(function(tabId, removeInfo) {
    console.log(`Background: Tab ${tabId} closed, cleaning up ready state. RemoveInfo:`, removeInfo);
    if (contentScriptsReady.has(tabId)) {
        contentScriptsReady.delete(tabId);
        console.log(`Background: Removed tabId ${tabId} from contentScriptsReady set.`);
    }
    console.log('Background: Ready tabs after cleanup:', Array.from(contentScriptsReady));
});

console.log('Background script (background.js) initialized and event listeners added.'); // General init log 