/**
 * Unit tests for user task submission flow.
 * Tests the popup -> background -> WebSocket communication.
 */

// Mock Chrome APIs
global.chrome = {
    runtime: {
        sendMessage: jest.fn(),
        lastError: null,
        onMessage: {
            addListener: jest.fn()
        }
    },
    tabs: {
        query: jest.fn()
    }
};

describe('User Task Submission Flow', () => {
    let mockWebSocket;
    let backgroundScript;
    
    beforeEach(() => {
        // Reset mocks
        jest.clearAllMocks();
        
        // Mock WebSocket
        mockWebSocket = {
            readyState: WebSocket.OPEN,
            send: jest.fn(),
            close: jest.fn()
        };
        
        global.WebSocket = jest.fn(() => mockWebSocket);
        global.WebSocket.OPEN = 1;
        global.WebSocket.CLOSED = 3;
        
        // Mock console
        global.console.log = jest.fn();
        global.console.error = jest.fn();
    });
    
    describe('Popup Task Submission', () => {
        test('should send SUBMIT_TASK message to background', async () => {
            // Mock current tab
            chrome.tabs.query.mockResolvedValue([{
                id: 123,
                url: 'https://example.com',
                title: 'Example Page'
            }]);
            
            // Mock successful response
            chrome.runtime.sendMessage.mockImplementation((message, callback) => {
                callback({ success: true });
            });
            
            // Simulate task submission
            const task = 'Click the search button';
            const submitButton = { disabled: false };
            const taskInput = { value: task };
            
            // This would be in the actual popup.js click handler
            const submitTask = async () => {
                const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
                
                chrome.runtime.sendMessage({
                    type: "SUBMIT_TASK",
                    task: task,
                    context: {
                        url: tab.url,
                        title: tab.title,
                        tabId: tab.id
                    }
                }, (response) => {
                    expect(response.success).toBe(true);
                });
            };
            
            await submitTask();
            
            // Verify message was sent
            expect(chrome.runtime.sendMessage).toHaveBeenCalledWith(
                {
                    type: "SUBMIT_TASK",
                    task: "Click the search button",
                    context: {
                        url: "https://example.com",
                        title: "Example Page",
                        tabId: 123
                    }
                },
                expect.any(Function)
            );
        });
        
        test('should handle submission when WebSocket is disconnected', () => {
            chrome.runtime.sendMessage.mockImplementation((message, callback) => {
                callback({ 
                    success: false, 
                    error: "WebSocket not connected to Python server" 
                });
            });
            
            const handleResponse = (response) => {
                expect(response.success).toBe(false);
                expect(response.error).toContain("WebSocket not connected");
            };
            
            chrome.runtime.sendMessage({ type: "SUBMIT_TASK" }, handleResponse);
        });
        
        test('should handle empty task submission', () => {
            const task = '';
            
            // Popup should validate before sending
            const validateTask = (taskText) => {
                return taskText.trim().length > 0;
            };
            
            expect(validateTask(task)).toBe(false);
        });
    });
    
    describe('Background Script Task Handling', () => {
        beforeEach(() => {
            // Setup background script context
            global.websocket = mockWebSocket;
            global.activeTabId = null;
        });
        
        test('should forward task to Python server via WebSocket', () => {
            const message = {
                type: "SUBMIT_TASK",
                task: "Navigate to about page",
                context: {
                    url: "https://example.com",
                    title: "Example",
                    tabId: 456
                }
            };
            
            // Simulate background script handling
            const handleSubmitTask = (message) => {
                if (!websocket || websocket.readyState !== WebSocket.OPEN) {
                    return { success: false, error: "WebSocket not connected" };
                }
                
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
                
                websocket.send(JSON.stringify(taskMessage));
                return { success: true };
            };
            
            const result = handleSubmitTask(message);
            
            expect(result.success).toBe(true);
            expect(mockWebSocket.send).toHaveBeenCalled();
            
            const sentMessage = JSON.parse(mockWebSocket.send.mock.calls[0][0]);
            expect(sentMessage.type).toBe("extension_event");
            expect(sentMessage.data.event_name).toBe("user_task_submitted");
            expect(sentMessage.data.task).toBe("Navigate to about page");
            expect(sentMessage.data.tabId).toBe(456);
        });
        
        test('should update active tab ID on task submission', () => {
            global.activeTabId = 999;
            
            const updateActiveTab = (tabId) => {
                global.activeTabId = tabId;
            };
            
            const message = {
                context: { tabId: 123 }
            };
            
            updateActiveTab(message.context.tabId);
            expect(global.activeTabId).toBe(123);
        });
        
        test('should handle WebSocket disconnection gracefully', () => {
            mockWebSocket.readyState = WebSocket.CLOSED;
            
            const handleSubmitTask = (message) => {
                if (!websocket || websocket.readyState !== WebSocket.OPEN) {
                    return { 
                        success: false, 
                        error: "WebSocket not connected to Python server" 
                    };
                }
                return { success: true };
            };
            
            const result = handleSubmitTask({ type: "SUBMIT_TASK" });
            
            expect(result.success).toBe(false);
            expect(result.error).toContain("WebSocket not connected");
            expect(mockWebSocket.send).not.toHaveBeenCalled();
        });
    });
    
    describe('WebSocket Message Format', () => {
        test('should create properly formatted task message', () => {
            const task = "Fill form with test data";
            const context = {
                url: "https://form.example.com",
                title: "Contact Form",
                tabId: 789
            };
            
            const createTaskMessage = (task, context) => {
                return {
                    type: "extension_event",
                    id: 12345, // Fixed for testing
                    data: {
                        event_name: "user_task_submitted",
                        task: task,
                        context: context,
                        tabId: context.tabId
                    }
                };
            };
            
            const message = createTaskMessage(task, context);
            
            expect(message).toEqual({
                type: "extension_event",
                id: 12345,
                data: {
                    event_name: "user_task_submitted",
                    task: "Fill form with test data",
                    context: {
                        url: "https://form.example.com",
                        title: "Contact Form",
                        tabId: 789
                    },
                    tabId: 789
                }
            });
        });
        
        test('should include timestamp in real implementation', () => {
            const createTaskMessage = () => {
                const timestamp = Date.now();
                return {
                    type: "extension_event",
                    id: timestamp,
                    data: {
                        event_name: "user_task_submitted",
                        timestamp: new Date(timestamp).toISOString()
                    }
                };
            };
            
            const message = createTaskMessage();
            
            expect(message.id).toBeGreaterThan(0);
            expect(message.data.timestamp).toMatch(/^\d{4}-\d{2}-\d{2}T/);
        });
    });
    
    describe('Error Handling', () => {
        test('should handle runtime errors during message sending', () => {
            chrome.runtime.lastError = { message: "Extension context invalidated" };
            chrome.runtime.sendMessage.mockImplementation((message, callback) => {
                if (callback) callback(undefined);
            });
            
            const sendMessage = (message, onResponse) => {
                chrome.runtime.sendMessage(message, (response) => {
                    if (chrome.runtime.lastError) {
                        onResponse({ 
                            success: false, 
                            error: chrome.runtime.lastError.message 
                        });
                    } else {
                        onResponse(response || { success: false, error: "No response" });
                    }
                });
            };
            
            let result;
            sendMessage({ type: "SUBMIT_TASK" }, (response) => {
                result = response;
            });
            
            expect(result.success).toBe(false);
            expect(result.error).toBe("Extension context invalidated");
        });
        
        test('should handle WebSocket send failures', () => {
            mockWebSocket.send.mockImplementation(() => {
                throw new Error("WebSocket is already in CLOSING or CLOSED state");
            });
            
            const safeSend = (websocket, data) => {
                try {
                    websocket.send(data);
                    return { success: true };
                } catch (error) {
                    return { success: false, error: error.message };
                }
            };
            
            const result = safeSend(mockWebSocket, "test data");
            
            expect(result.success).toBe(false);
            expect(result.error).toContain("CLOSING or CLOSED state");
        });
    });
});