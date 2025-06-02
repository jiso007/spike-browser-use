// browser-use-ext/extension/background.js
// Establishes and manages WebSocket connection with the Python backend.
// Handles messages from content scripts and the Python backend.
// Manages browser tab interactions.

const WS_URL = "ws://localhost:8765"; // Fixed: Now matches Python server port
let websocket = null;
let activeTabId = null;
let reconnectInterval = 5000; // 5 seconds
let eventQueue = []; // Queue for events to be sent when the WebSocket is open
const contentScriptsReady = new Set(); // Stores tabIds where content script is ready
const CONTENT_SCRIPT_READY_TIMEOUT = 15000; // Increased to 15 seconds

/**
 * Initializes the WebSocket connection.
 * Sets up event handlers for open, message, error, and close events.
 */
function connectWebSocket() {
    console.log("Attempting to connect to WebSocket at", WS_URL);
    websocket = new WebSocket(WS_URL);

    websocket.onopen = async () => {
        console.log("WebSocket connection established.");
        // Inform popup about connection status if applicable
        if (chrome.runtime.sendMessage) {
            chrome.runtime.sendMessage({ type: "WS_STATUS", status: "Connected" }).catch((_e) => console.warn("Popup not listening for WS_STATUS (onopen)", _e)); // Log prefixed unused error
        }
        
        // ADDED: Small delay to allow Python server to fully settle after accepting connection
        console.log("Background.js: WebSocket opened. Waiting 200ms before sending initial tab query.");
        await new Promise(resolve => setTimeout(resolve, 200)); 
        console.log("Background.js: Delay complete. Proceeding with initial tab query.");

        // Send initial active tab info once connected
        queryActiveTab(true); // Send context on initial connection
        
        // After sending initial query, attempt to send any queued events
        sendQueuedEvents();
    };

    websocket.onmessage = (event) => {
        console.log("Message received from server:", event.data);
        try {
            const message = JSON.parse(event.data);
            handleServerMessage(message);
        } catch (_error) {
            console.error("Error parsing message from server:", _error);
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
 * Sends generic data (responses or events) to the Python WebSocket server.
 * @param {object} dataToSend - The data to send.
 */
function sendDataToServer(dataToSend) {
    // The Python server expects messages with 'id' and 'type' at the top level.
    // If dataToSend already has 'id' and 'type', use it as is.
    // Otherwise, wrap it if it's meant to be the 'data' part of an 'extension_event'.
    let messageToSend;
    if (dataToSend.type && Object.prototype.hasOwnProperty.call(dataToSend, 'id')) {
        messageToSend = dataToSend; // Assume it's already a correctly structured message
    } else {
        console.warn("Sending data that might not have a server-correlating ID:", dataToSend);
        messageToSend = dataToSend; // Send as is, review server side if ID is strictly needed for all types
    }

    const messageString = JSON.stringify(messageToSend);

    if (websocket && websocket.readyState === WebSocket.OPEN) {
        try {
            console.log("Attempting to send to server:", messageString);
            websocket.send(messageString);
            console.log("Data sent to server successfully.");
            console.log("Background.js: DEBUG - websocket.bufferedAmount after send:", websocket.bufferedAmount);
             // After sending, attempt to send any queued messages
             sendQueuedEvents();
        } catch (error) {
            console.error("Error serializing data for server:", error, dataToSend);
        }
    } else {
        console.warn("WebSocket not connected. Queueing data for server.", dataToSend);
        eventQueue.push(messageString); // Queue the stringified message
        console.log(`Background.js: Event queued. Queue size: ${eventQueue.length}`);
    }
}

// ADDED: Function to send queued events
function sendQueuedEvents() {
    if (websocket && websocket.readyState === WebSocket.OPEN && eventQueue.length > 0) {
        console.log(`Background.js: WebSocket open and queue not empty. Attempting to send ${eventQueue.length} queued events.`);
        while (eventQueue.length > 0) {
            const messageString = eventQueue.shift(); // Get the oldest message
            try {
                console.log("Background.js: Sending queued event:", messageString);
                websocket.send(messageString);
                console.log("Background.js: Queued event sent successfully.");
            } catch (error) {
                console.error("Background.js: Error sending queued event:", error, messageString);
                // If sending a queued event fails, stop and put it back at the front
                eventQueue.unshift(messageString); 
                console.warn("Background.js: Failed to send queued event. Putting it back in queue and stopping queue processing.");
                break; // Stop processing the queue on the first error
            }
        }
        console.log(`Background.js: Finished sending queued events. Remaining queue size: ${eventQueue.length}`);
    }
}

// NEW: Listen for messages from content scripts and popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('🎯 BACKGROUND.JS: Message received:', message, 'from sender:', sender);
  console.log('🎯 BACKGROUND.JS: Message type:', message?.type);
  console.log('🎯 BACKGROUND.JS: Sender tab ID:', sender?.tab?.id);
  console.log('🎯 BACKGROUND.JS: Sender tab URL:', sender?.tab?.url);

  if (sender.tab && message.type === "content_script_ready") {
    console.log(`🎉 BACKGROUND.JS: *** RECEIVED content_script_ready from tabId: ${sender.tab.id} ***`);
    console.log(`🎉 BACKGROUND.JS: Tab URL: ${sender.tab.url}`);
    console.log(`🎉 BACKGROUND.JS: WebSocket state: ${websocket?.readyState} (1=OPEN)`);
    contentScriptsReady.add(sender.tab.id);
    
    // SEND CONTENT SCRIPT READY EVENT TO PYTHON SERVER
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      const readyEvent = {
        type: "extension_event",
        id: Date.now(),
        data: {
          event_name: "content_script_ready",
          tabId: sender.tab.id
        }
      };
      websocket.send(JSON.stringify(readyEvent));
      console.log(`🚀 BACKGROUND.JS: *** SENT content_script_ready event to Python WebSocket server for tab ${sender.tab.id} ***`);
      
      // Also send debug info for troubleshooting
      const debugMsg = {
        type: "extension_event",
        id: Date.now() + 1,
        data: {
          event_name: "debug_content_script_ready",
          tabId: sender.tab.id,
          readyTabsCount: contentScriptsReady.size,
          allReadyTabs: Array.from(contentScriptsReady)
        }
      };
      websocket.send(JSON.stringify(debugMsg));
      console.log(`background.js: Sent debug info to Python server for tab ${sender.tab.id}`);
    }
    
    return true; // For async response
  }

  // ADDED: Debug utility to get currently ready tabs
  else if (message.type === "debug_get_ready_tabs") {
    const readyTabsArray = Array.from(contentScriptsReady);
    console.log("Background: Debug: Currently ready tabs:", readyTabsArray);
    sendResponse({ status: "ok", readyTabs: readyTabsArray });
    return false; // Synchronous response for this debug utility.
  }

  // Handle popup status request
  else if (message.type === "GET_POPUP_STATUS") {
    console.log("Background: Received GET_POPUP_STATUS from popup");
    const status = websocket && websocket.readyState === WebSocket.OPEN ? "Connected" : "Disconnected";
    sendResponse({ status: status });
    return false; // Synchronous response
  }

  // Handle task submission from popup
  else if (message.type === "SUBMIT_TASK") {
    console.log("Background: Received SUBMIT_TASK from popup", message);
    
    if (!websocket || websocket.readyState !== WebSocket.OPEN) {
      console.error("Background: WebSocket not connected, cannot submit task");
      sendResponse({ success: false, error: "WebSocket not connected to Python server" });
      return false;
    }

    // Set the active tab based on the context from the popup
    if (message.context && message.context.tabId) {
      activeTabId = message.context.tabId;
      console.log(`Background: Set active tab to ${activeTabId} based on task submission context`);
    }

    // Forward the task to the Python server
    const taskMessage = {
      type: "extension_event",
      id: Date.now(),
      data: {
        event_name: "user_task_submitted",
        task: message.task,
        context: message.context,
        tabId: message.context?.tabId || activeTabId
      }
    };

    try {
      websocket.send(JSON.stringify(taskMessage));
      console.log(`Background: Sent user task to Python server:`, taskMessage);
      sendResponse({ success: true });
    } catch (error) {
      console.error("Background: Error sending task to Python server:", error);
      sendResponse({ success: false, error: "Failed to send task to server: " + error.message });
    }

    return false; // Synchronous response
  }

  // Fallback for messages not handled by the `if` above.
  else {
    console.warn(`⚠️ BACKGROUND.JS: Unhandled runtime message type '${message?.type}' from sender:`, sender);
    console.warn(`⚠️ BACKGROUND.JS: Full message object:`, message);
    if (sender?.tab) {
      console.warn(`⚠️ BACKGROUND.JS: Message from tab ${sender.tab.id} (${sender.tab.url}) was not handled`);
    }
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
chrome.tabs.onActivated.addListener(async (activeInfo) => {
    console.log('background.js: Tab activated:', activeInfo.tabId);
    // You might want to store the active tab ID if needed
    // Removed unused and undefined function call: _set_active_tab_id(activeInfo.tabId);
    // Inform the server that the active tab has changed
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        try {
            await websocket.send(JSON.stringify({
                type: "active_tab_changed",
                tabId: activeInfo.tabId,
                windowId: activeInfo.windowId
            }));
            console.log(`background.js: Sent 'active_tab_changed' for tabId: ${activeInfo.tabId}`);
        } catch (error) {
            console.error('background.js: Failed to send active_tab_changed message:', error);
        }
    }
});

// Handles tab updates (e.g., page load status)
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && (tab.url.startsWith('http://') || tab.url.startsWith('https://'))) {
    console.log(`background.js: Tab ${tabId} status is complete.`);

    // If content script is already marked ready, send the event
    if (contentScriptsReady.has(tabId)) {
      console.log(`Tab ${tabId} is ready. Sending page_fully_loaded_and_ready event.`);
      sendPageFullyLoadedAndReadyEventToPython(tabId, tab.url, tab.title, "tab_updated_complete");
    } else {
      console.log(`Tab ${tabId} is not ready. Page ${tab.url} will need to send its signal.`);
    }

    // Ensure the update is for the main frame and the tab is completely loaded
    if (changeInfo.status === 'complete' && tab.url && !tab.url.startsWith('chrome://')) {
      console.log(`Tab ${tabId} update complete: ${tab.url}. Active tab is ${activeTabId}.`);
      
      sendPageFullyLoadedAndReadyEventToPython(tabId, tab.url, tab.title, "tab_updated_complete");

      if (tabId === activeTabId) {
        console.log(`Active tab ${activeTabId} just completed loading ${tab.url}.`);
        // Don't clear content script ready status here - let the content script manage its own lifecycle
        // The content script will send a ready signal when it's actually ready
        console.log(`TabId ${tabId} page load complete. Content script should signal when ready.`);
      }
    }

    // Proactive update for when tab is just activated (might not be fully loaded yet)
    // if (changeInfo.status === 'loading' && tab.active) { // This might be too noisy or premature
    // activeTabId = tabId;
    // sendTabContextUpdate("tab_activated_loading", tab);
    // }
  }
});

/**
 * Smart active tab management - prioritizes based on user interaction, content script readiness, and recency.
 * @param {boolean} [sendContext=false] - Whether to send context update for the new active tab.
 */
function queryActiveTab(sendContext = false) {
    chrome.tabs.query({}, (allTabs) => {
        if (chrome.runtime.lastError) {
            console.error("Error querying all tabs:", chrome.runtime.lastError.message);
            activeTabId = null;
            return;
        }

        // Group tabs by window and find active tabs
        const activeTabs = allTabs.filter(tab => tab.active);
        console.log(`Background.js: Found ${activeTabs.length} active tabs across ${new Set(allTabs.map(t => t.windowId)).size} windows`);

        if (activeTabs.length === 0) {
            console.log("Background.js: No active tabs found");
            activeTabId = null;
            return;
        }

        // Smart tab selection logic
        const bestTab = selectBestActiveTab(activeTabs);
        if (bestTab) {
            updateActiveTab(bestTab.tab, sendContext, bestTab.reason);
        } else {
            console.log("Background.js: No suitable active tab found");
            activeTabId = null;
        }
    });
}

/**
 * Selects the best active tab based on smart prioritization
 * @param {Array} activeTabs - Array of active tab objects
 * @returns {Object|null} - {tab: TabObject, reason: string} or null
 */
function selectBestActiveTab(activeTabs) {
    const tabScores = activeTabs.map(tab => {
        const score = calculateTabScore(tab);
        console.log(`Background.js: Tab ${tab.id} (${tab.url}) - Score: ${score.total} (${score.breakdown})`);
        return { tab, score: score.total, breakdown: score.breakdown };
    });

    // Sort by score (highest first)
    tabScores.sort((a, b) => b.score - a.score);
    
    const winner = tabScores[0];
    if (winner && winner.score > 0) {
        return { tab: winner.tab, reason: `smart_selection_${winner.breakdown}` };
    }
    
    return null;
}

/**
 * Calculates a priority score for a tab based on multiple factors
 * @param {Object} tab - Chrome tab object
 * @returns {Object} - {total: number, breakdown: string}
 */
function calculateTabScore(tab) {
    let score = 0;
    const factors = [];

    // Factor 1: Content script readiness (highest priority)
    if (contentScriptsReady.has(tab.id)) {
        score += 100;
        factors.push("ready");
    } else {
        // No content script = much lower priority
        // But for blank tabs, be more lenient since they can't have content scripts
        if (tab.url === "about:blank" || tab.url === "chrome://newtab/" || !tab.url) {
            score += 5;  // Small positive score for blank tabs
            factors.push("blank_tab");
        } else {
            score -= 50;
            factors.push("not_ready");
        }
    }

    // Factor 2: Current active tab in this browser gets bonus
    if (activeTabId === tab.id) {
        score += 30;
        factors.push("current");
    }

    // Factor 3: URL quality indicators
    const urlScore = calculateUrlScore(tab.url);
    score += urlScore.score;
    if (urlScore.reason) factors.push(urlScore.reason);

    // Factor 4: Recency - tabs that were recently activated
    // (This would need tab activation tracking, simplified for now)
    
    // Factor 5: Browser window characteristics
    // Prefer windows with fewer tabs (likely test scenarios)
    // This will be calculated in the context of window tabs when needed

    return {
        total: score,
        breakdown: factors.join("_")
    };
}

/**
 * Calculates URL-based scoring for tab prioritization
 * @param {string} url - Tab URL
 * @returns {Object} - {score: number, reason: string}
 */
function calculateUrlScore(url) {
    if (!url) return { score: 0, reason: "no_url" };

    // High priority URLs (testing/development)
    const highPriorityUrls = [
        "example.com",
        "wikipedia.org", 
        "httpbin.org",
        "jsonplaceholder",
        "127.0.0.1",
        "localhost"
    ];

    // Medium priority URLs (neutral)
    const neutralUrls = [
        "github.com",
        "stackoverflow.com"
    ];

    // Low priority URLs (likely personal browsing)
    const lowPriorityUrls = [
        "tradingview.com",
        "youtube.com",
        "facebook.com",
        "twitter.com",
        "instagram.com",
        "tiktok.com",
        "netflix.com"
    ];

    // Special cases
    if (url === "about:blank" || url === "data:,") {
        return { score: 10, reason: "blank_page" };
    }

    // Check high priority
    for (const pattern of highPriorityUrls) {
        if (url.includes(pattern)) {
            return { score: 20, reason: "high_priority_url" };
        }
    }

    // Check low priority (negative score)
    for (const pattern of lowPriorityUrls) {
        if (url.includes(pattern)) {
            return { score: -20, reason: "low_priority_url" };
        }
    }

    // Check neutral
    for (const pattern of neutralUrls) {
        if (url.includes(pattern)) {
            return { score: 5, reason: "neutral_url" };
        }
    }

    // Default case
    return { score: 0, reason: "unknown_url" };
}


/**
 * Updates the active tab with smart override protection
 */
function updateActiveTab(newActiveTab, sendContext, source) {
    const isFirstTime = activeTabId === null;
    const isSameTab = activeTabId === newActiveTab.id;
    
    if (isFirstTime || isSameTab || sendContext) {
        // Always allow: first time, same tab, or explicit context request
        console.log(`Background.js: Setting active tab ${newActiveTab.id} (${newActiveTab.url}) - Source: ${source}`);
        activeTabId = newActiveTab.id;
        if (sendContext) {
            sendTabContextUpdate("tab_activated_on_query", newActiveTab);
        }
        return;
    }
    
    // For tab changes, check if the new tab is actually better
    // ADDED: Extra protection - never let low-priority URLs override high-priority ones
    const newUrlScore = calculateUrlScore(newActiveTab.url);
    if (newUrlScore.score < -15) {
        console.log(`Background.js: BLOCKING tab ${newActiveTab.id} (${newActiveTab.url}) - very low priority URL (${newUrlScore.score})`);
        return; // Block very low priority URLs completely
    }
    
    if (shouldReplaceActiveTab(activeTabId, newActiveTab)) {
        console.log(`Background.js: Replacing active tab ${activeTabId} with ${newActiveTab.id} (${newActiveTab.url}) - Source: ${source}`);
        activeTabId = newActiveTab.id;
        if (sendContext) {
            sendTabContextUpdate("tab_activated_on_query", newActiveTab);
        }
    } else {
        console.log(`Background.js: Keeping current active tab ${activeTabId}, rejecting ${newActiveTab.id} (${newActiveTab.url}) - Source: ${source}`);
    }
}

/**
 * Determines if we should replace the current active tab with a new one
 * @param {number} currentTabId - Current active tab ID
 * @param {Object} newTab - New tab object to potentially switch to
 * @returns {boolean} - True if we should switch
 */
function shouldReplaceActiveTab(currentTabId, newTab) {
    // If current tab is not ready but new tab is, switch
    const currentReady = contentScriptsReady.has(currentTabId);
    const newReady = contentScriptsReady.has(newTab.id);
    
    if (!currentReady && newReady) {
        console.log(`Background.js: Switching because new tab ${newTab.id} is ready but current ${currentTabId} is not`);
        return true;
    }
    
    // If current tab is ready but new tab is not, don't switch
    if (currentReady && !newReady) {
        console.log(`Background.js: Not switching because current tab ${currentTabId} is ready but new ${newTab.id} is not`);
        return false;
    }
    
    // If both ready or both not ready, compare by URL priority
    const newUrlScore = calculateUrlScore(newTab.url);
    
    // For now, use a simple approach: if current tab is ready, don't switch unless new tab is much better
    // This prevents good tabs from being overridden by random browser tabs
    if (currentReady) {
        console.log(`Background.js: Current tab ${currentTabId} is ready, being very conservative about switching`);
        // Only switch if new tab has very high priority URL
        if (newUrlScore.score > 15) {
            console.log(`Background.js: New tab ${newTab.id} has very high priority (${newUrlScore.score}), allowing switch`);
            return true;
        } else {
            console.log(`Background.js: New tab ${newTab.id} priority too low (${newUrlScore.score}), keeping current ready tab`);
            return false;
        }
    }
    
    // If current tab is not ready, be more permissive but still check URL quality
    if (newUrlScore.score < -10) {
        console.log(`Background.js: New tab ${newTab.id} has very low priority (${newUrlScore.score}), rejecting`);
        return false;
    }
    
    console.log(`Background.js: Current tab not ready, new tab acceptable (${newUrlScore.score}), allowing switch`);
    return true;
}

// Initial setup
console.log("Background script started.");

// Function to wait for content script readiness (robust version from rule)
async function waitForContentScriptReady(tabId, timeoutMs) {
    const startTime = Date.now();
    console.log(`Background.js: waitForContentScriptReady CALLED for tabId: ${tabId}, timeout: ${timeoutMs}ms. Current ready set: ${JSON.stringify(Array.from(contentScriptsReady))}`);
    while (Date.now() - startTime < timeoutMs) {
        if (contentScriptsReady.has(tabId)) {
            console.log(`Background.js: Content script for tabId: ${tabId} IS READY.`);
            return true;
        }
        // console.log(`Background.js: Polling for content script ready for tabId: ${tabId}. Still waiting...`);
        await new Promise(resolve => setTimeout(resolve, 250)); // Poll frequently
    }
    console.error(`Background.js: TIMEOUT waiting for content script in tab ${tabId} to signal ready after ${timeoutMs}ms.`);
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
                title: title // Ensure title is used in log
            }
        };
        sendDataToServer(eventData);
        console.info(`Sent 'page_fully_loaded_and_ready' (Reason: ${reason}) for tab ${tabId}, URL: ${url}, Title: ${title} to Python server.`);
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

// --- MODIFIED: handleServerMessage to use pingContentScript for get_state ---

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
                    console.log(`Background.js: DEBUG get_state (Request ID: ${requestId}) - TargetTabID for state: ${targetTabIdForState}. About to call waitForContentScriptReady. Current contentScriptsReady set: ${JSON.stringify(Array.from(contentScriptsReady))}`);
                    const isReady = await waitForContentScriptReady(targetTabIdForState, CONTENT_SCRIPT_READY_TIMEOUT);
                    console.log(`Background.js: DEBUG get_state (Request ID: ${requestId}) - waitForContentScriptReady returned: ${isReady} for tab ${targetTabIdForState}.`);

                    if (!isReady) {
                        console.warn(`Content script in tab ${targetTabIdForState} did not signal ready within timeout for get_state (ID: ${requestId}).`);
                        throw new Error(`Content script in tab ${targetTabIdForState} not ready after ${CONTENT_SCRIPT_READY_TIMEOUT}ms`);
                    }
                    
                    console.log(`Content script for tab ${targetTabIdForState} is ready. Forwarding 'get_state' (ID: ${requestId}).`);
                    // ADDED: Small delay to allow content script message listener to be fully ready
                    console.log(`Background.js: Adding 300ms delay before sending get_state to content.js (ID: ${requestId}).`);
                    await new Promise(resolve => setTimeout(resolve, 300)); // Add a small delay
                    console.log(`Background.js: Delay complete. Sending get_state message now (ID: ${requestId}).`);

                    try {
                        console.log(`🚀 Background.js: About to send get_state message to tab ${targetTabIdForState} (ID: ${requestId})`);
                        
                        // First, check if the tab exists and has content scripts
                        const tab = await chrome.tabs.get(targetTabIdForState);
                        console.log(`🔍 Background.js: Tab info for ${targetTabIdForState}:`, {
                            url: tab.url, 
                            title: tab.title, 
                            status: tab.status,
                            active: tab.active
                        });
                        
                        // FIXED: Send message specifically to the main frame (frameId: 0) to avoid about:blank iframes
                        console.log(`🚀 Background.js: Sending get_state to main frame (frameId: 0) of tab ${targetTabIdForState}...`);
                        
                        const contentResponse = await chrome.tabs.sendMessage(targetTabIdForState, {
                            type: "get_state", 
                            requestId: requestId
                        }, {
                            frameId: 0  // Explicitly target the main frame only
                        });
                        
                        console.log(`✅ Background.js: *** SUCCESSFULLY SENT get_state to MAIN FRAME (frameId: 0) of tab ${targetTabIdForState} ***`);
                        console.log(`📥 Background.js: *** RECEIVED RESPONSE from content script ***:`, contentResponse);

                        // ADDED: Detailed logging of contentResponse before checking structure
                        console.log(`Background.js: DEBUG get_state (ID: ${requestId}) - Received contentResponse:`, contentResponse);
                        console.log(`Background.js: DEBUG get_state (ID: ${requestId}) - contentResponse.type:`, contentResponse?.type);
                        console.log(`Background.js: DEBUG get_state (ID: ${requestId}) - contentResponse.status:`, contentResponse?.status);
                        console.log(`Background.js: DEBUG get_state (ID: ${requestId}) - contentResponse.data:`, contentResponse?.data);
                        console.log(`Background.js: DEBUG get_state (ID: ${requestId}) - contentResponse.data.state:`, contentResponse?.data?.state);
                        
                        if (contentResponse && contentResponse.type === "state_response" && contentResponse.status === "success" && contentResponse.state) {
                            console.log(`Received state from content script for ID ${requestId} (Tab: ${targetTabIdForState}):`, contentResponse.state);
                            // Access nested state object
                            pageSpecificData.url = contentResponse.state.url || pageSpecificData.url;
                            pageSpecificData.title = contentResponse.state.title || pageSpecificData.title;
                            // The rest of these fields might need review based on the new content.js structure if not directly under .state
                            // Assuming tree, selector_map, scroll_y, page_content_height, viewport_height are now under .state as per handleGetState in content.js
                            pageSpecificData.html_content = contentResponse.state.html_content || pageSpecificData.html_content;
                            pageSpecificData.tree = contentResponse.state.tree || pageSpecificData.tree;
                            pageSpecificData.selector_map = contentResponse.state.selector_map || pageSpecificData.selector_map;
                            
                            // Update pixels_above/below based on new state structure
                            pageSpecificData.pixels_above = contentResponse.state.scroll_position?.y !== undefined ? contentResponse.state.scroll_position.y : 0;
                            pageSpecificData.pixels_below = (contentResponse.state.document_dimensions?.height !== undefined && 
                                                           contentResponse.state.scroll_position?.y !== undefined && 
                                                           contentResponse.state.viewport?.height !== undefined) ?
                                                           Math.max(0, contentResponse.state.document_dimensions.height - (contentResponse.state.scroll_position.y + contentResponse.state.viewport.height))
                                                           : 0;

                            // ADDED: Store actionable_elements directly from the content script response
                             pageSpecificData.actionable_elements = contentResponse.state.actionable_elements;

                             // ADDED: Store viewport and document dimensions
                            pageSpecificData.viewport = contentResponse.state.viewport;
                            pageSpecificData.document_dimensions = contentResponse.state.document_dimensions;
                            pageSpecificData.page_metrics = contentResponse.state.page_metrics;
                            pageSpecificData.timestamp = contentResponse.state.timestamp;

                        } else if (contentResponse && contentResponse.type === "state_response" && contentResponse.status === "error") {
                            // Handle error case explicitly from content script
                            const errorMsg = contentResponse.error || `Content script returned error status for get_state on tab ${targetTabIdForState}.`;
                            console.warn(`Content script error for get_state (ID: ${requestId}, Tab: ${targetTabIdForState}): ${errorMsg}`);
                            // Do not throw here, allow collection of general tab data if any
                        } else {
                            // Handle no response or malformed response case
                            const errorMsg = contentResponse ? `Malformed response from content script for get_state on tab ${targetTabIdForState}. Response:` + JSON.stringify(contentResponse) : `No response from content script for get_state on tab ${targetTabIdForState}.`;
                             console.warn(errorMsg, `(ID: ${requestId})`);
                            // Do not throw here, allow collection of general tab data if any
                        }
                    } catch (e) {
                        if (e.message && e.message.includes("Could not establish connection")) {
                            console.warn(`Background.js: Initial sendMessage for get_state (ID: ${requestId}, Tab: ${targetTabIdForState}) failed with connection error. Retrying once... Error: ${e.message}`);
                            await new Promise(resolve => setTimeout(resolve, 500)); // Wait 500ms before retry
                            try {
                                const retryResponse = await chrome.tabs.sendMessage(targetTabIdForState, {
                                    type: "get_state", 
                                    requestId: requestId
                                }, {
                                    frameId: 0  // Also target main frame on retry
                                });
                                if (retryResponse && retryResponse.type === "state_response" && retryResponse.status === "success" && retryResponse.state) {
                                    console.log(`Successfully received state on retry for ID ${requestId} (Tab: ${targetTabIdForState}):`, retryResponse.state);
                                    pageSpecificData.url = retryResponse.state.url || pageSpecificData.url;
                                    pageSpecificData.title = retryResponse.state.title || pageSpecificData.title;
                                    pageSpecificData.html_content = retryResponse.state.html_content || pageSpecificData.html_content;
                                    pageSpecificData.tree = retryResponse.state.tree || pageSpecificData.tree;
                                    pageSpecificData.selector_map = retryResponse.state.selector_map || pageSpecificData.selector_map;
                                    pageSpecificData.pixels_above = retryResponse.state.scroll_position?.y !== undefined ? retryResponse.state.scroll_position.y : 0;
                                    pageSpecificData.pixels_below = (retryResponse.state.document_dimensions?.height !== undefined && 
                                                                   retryResponse.state.scroll_position?.y !== undefined && 
                                                                   retryResponse.state.viewport?.height !== undefined) ?
                                                                   Math.max(0, retryResponse.state.document_dimensions.height - (retryResponse.state.scroll_position.y + retryResponse.state.viewport.height))
                                                                   : 0;
                                    pageSpecificData.actionable_elements = retryResponse.state.actionable_elements;
                                    pageSpecificData.viewport = retryResponse.state.viewport;
                                    pageSpecificData.document_dimensions = retryResponse.state.document_dimensions;
                                    pageSpecificData.page_metrics = retryResponse.state.page_metrics;
                                    pageSpecificData.timestamp = retryResponse.state.timestamp;
                                } else if (retryResponse && retryResponse.type === "state_response" && retryResponse.status === "error") {
                                     const errorMsg = retryResponse.error || `Content script returned error status on retry for get_state on tab ${targetTabIdForState}.`;
                                     console.error(`Retry for get_state (ID: ${requestId}, Tab: ${targetTabIdForState}) returned error: ${errorMsg}`);
                                    throw new Error(`Failed to get state from content script on tab ${targetTabIdForState} after retry: ${errorMsg}`);
                                } else {
                                    const errorMsg = retryResponse ? `Malformed response from content script on retry for get_state on tab ${targetTabIdForState}. Response:` + JSON.stringify(retryResponse) : `No response from content script on retry for get_state on tab ${targetTabIdForState}.`;
                                    console.error(`Retry for get_state (ID: ${requestId}, Tab: ${targetTabIdForState}) also failed or returned malformed response: ${errorMsg}`);
                                    throw new Error(`Failed to get state from content script on tab ${targetTabIdForState} after retry: ${errorMsg}`);
                                }
                            } catch (retryError) {
                                console.error(`Background.js: Retry sendMessage for get_state (ID: ${requestId}, Tab: ${targetTabIdForState}) also failed. Error: ${retryError.message}`);
                                throw retryError; // Rethrow the error from the retry attempt
                            }
                        } else {
                            // Original error was not a connection error, or was a different error during retry
                            console.error(`Background.js: Error during initial get_state sendMessage or retry error (ID: ${requestId}, Tab: ${targetTabIdForState}). Error: ${e.message}`);
                            throw e; 
                        }
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
            // For execute_action, serverParams is the content of message.data from Python
            // Python sends: message.data = {action_name: "navigate", params: {"url": "https://example.com"}}
            // So, serverParams IS message.data from Python.
            const subActionName = serverParams.action_name; 
            const subActionParams = serverParams.params;

            if (!activeTabId) { 
                 console.warn("No active tab for execute_action:", subActionName, `(ID: ${requestId})`);
                 sendDataToServer({type: "response", id: requestId, data: { success: false, error: "No active tab to process action."}});
                 return;
            }
            if (!subActionName) {
                console.error(`'execute_action' request (ID: ${requestId}) from server is missing the nested 'action_name' field in its data.`);
                sendDataToServer({ type: "response", id: requestId, data: { success: false, error: "Malformed execute_action from server: missing nested action_name." }});
                return;
            }

            console.log(`Forwarding action '${subActionName}' (ID: ${requestId}) to tab ${activeTabId} as type 'execute_action'`);
            
            // Special handling for navigate action on blank tabs
            if (subActionName === "navigate") {
                // Check if this is a blank tab
                const tab = await chrome.tabs.get(activeTabId);
                if (tab.url === "about:blank" || tab.url === "chrome://newtab/" || !tab.url) {
                    console.log(`Direct navigation for blank tab ${activeTabId} to ${subActionParams.url}`);
                    // Navigate directly using Chrome API instead of content script
                    try {
                        await chrome.tabs.update(activeTabId, { url: subActionParams.url });
                        console.log(`Navigation initiated for blank tab ${activeTabId} to ${subActionParams.url}`);
                        
                        sendDataToServer({
                            type: "response",
                            id: requestId,
                            data: { success: true, message: `Navigated blank tab ${activeTabId} to ${subActionParams.url}` }
                        });
                        return;
                    } catch (error) {
                        console.error(`Failed to navigate blank tab: ${error.message}`);
                        sendDataToServer({
                            type: "response",
                            id: requestId,
                            data: { success: false, error: `Failed to navigate blank tab: ${error.message}` }
                        });
                        return;
                    }
                }
            }
            
            // Wait for content script to be ready (important for non-navigate actions, and for navigate to ensure the current page's content script receives the command)
            const isReady = await waitForContentScriptReady(activeTabId, CONTENT_SCRIPT_READY_TIMEOUT);
            if (!isReady) {
                console.error(`Content script in tab ${activeTabId} not ready for execute_action (ID: ${requestId}). Action: ${subActionName}`);
                sendDataToServer({
                    type: "response",
                    id: requestId,
                    data: { success: false, error: `Content script in tab ${activeTabId} not ready after ${CONTENT_SCRIPT_READY_TIMEOUT}ms for action '${subActionName}'` }
                });
                return;
            }

            const messagePayloadToContent = {
                type: "execute_action",       
                payload: {                  
                    action: subActionName,
                    params: subActionParams
                },
                requestId: requestId
            };
            
            console.log(`Background.js: About to send 'execute_action' to content.js. TabID: ${activeTabId}, RequestID: ${requestId}, ActionName: ${subActionName}, ActionParams:`, JSON.stringify(subActionParams));

            if (subActionName === "navigate") {
                // For "navigate", send the message and immediately respond success to Python.
                // The content script will not send a response back for navigation.
                try {
                    await chrome.tabs.sendMessage(activeTabId, messagePayloadToContent);
                    console.log(`Background.js: 'navigate' command sent to content script for tab ${activeTabId}, (ID: ${requestId}).`);
                    sendDataToServer({
                        type: "response",
                        id: requestId,
                        data: { 
                            success: true, 
                            message: `Navigate command for '${subActionParams.url}' sent to tab ${activeTabId}.`
                        }
                    });
                } catch (error) {
                    // This catch is for errors during the sendMessage itself (e.g., if tab closed instantly)
                    console.error(`Error sending 'navigate' command to content script (ID: ${requestId}, Tab: ${activeTabId}):`, error);
                    sendDataToServer({
                        type: "response",
                        id: requestId,
                        data: { success: false, error: `Failed to send navigate command to content script: ${error.message}` }
                    });
                }
            } else {
                // For other actions, expect a response from the content script.
                chrome.tabs.sendMessage(activeTabId, messagePayloadToContent)
                .then(response => {
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
            }
        } else if (serverActionType === "extension_event") {
            // Handle extension events like page_fully_loaded_and_ready
            const eventName = serverParams.event_name;
            console.log(`Background.js: Received extension_event: ${eventName} (ID: ${requestId})`);
            if (eventName === "page_fully_loaded_and_ready") {
                const { tabId, url, title, reason } = serverParams.data;
                if (tabId) {
                     console.log(`Background.js: Page fully loaded and ready event for tab ${tabId}, URL: ${url} (Reason: ${reason}).`);
                     // Update the active tab ID if this event is for the currently tracked active tab
                    if (activeTabId === tabId) {
                        console.log(`Background.js: Page fully loaded and ready event matches activeTabId ${tabId}. Updating internal state.`);
                        // Invalidate content script readiness for this tab as the page has reloaded
                         if (contentScriptsReady.has(tabId)) {
                            contentScriptsReady.delete(tabId);
                            console.log(`Background.js: TabId ${tabId} removed from contentScriptsReady due to navigation.`);
                        }
                        // We might also want to update the stored tab details (url, title) here
                        
                        // --- ADDED DELAY AFTER PAGE READY EVENT ---
                        console.log("Background.js: Adding a 750ms delay after page_fully_loaded_and_ready to allow content script to stabilize before next server command.");
                        await new Promise(resolve => setTimeout(resolve, 750)); // Adjust delay as needed
                        // --- END ADDED DELAY ---

                    }
                }
            }
            // Do NOT send a response for extension events unless specifically required.
            // These are typically signals *from* the extension *to* the server.
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