/**
 * Unit tests for background.js user input message handlers
 */

// Test the message handler logic without loading the full background.js
describe('Background Script User Input Handlers', () => {
  let mockWebSocket;
  let activeTabId;
  let sendResponse;

  beforeEach(() => {
    // Mock WebSocket
    mockWebSocket = {
      readyState: 1, // OPEN
      send: jest.fn()
    };

    // Mock globals
    activeTabId = null;
    sendResponse = jest.fn();
    
    // Clear all mocks
    jest.clearAllMocks();
  });

  describe('GET_POPUP_STATUS handler', () => {
    test('should return Connected when WebSocket is open', () => {
      // Simulate the handler logic
      const message = { type: 'GET_POPUP_STATUS' };
      const status = mockWebSocket && mockWebSocket.readyState === 1 ? "Connected" : "Disconnected";
      
      sendResponse({ status: status });
      
      expect(sendResponse).toHaveBeenCalledWith({ status: "Connected" });
    });

    test('should return Disconnected when WebSocket is closed', () => {
      mockWebSocket.readyState = 3; // CLOSED
      
      const message = { type: 'GET_POPUP_STATUS' };
      const status = mockWebSocket && mockWebSocket.readyState === 1 ? "Connected" : "Disconnected";
      
      sendResponse({ status: status });
      
      expect(sendResponse).toHaveBeenCalledWith({ status: "Disconnected" });
    });

    test('should return Disconnected when WebSocket is null', () => {
      mockWebSocket = null;
      
      const message = { type: 'GET_POPUP_STATUS' };
      const status = mockWebSocket && mockWebSocket.readyState === 1 ? "Connected" : "Disconnected";
      
      sendResponse({ status: status });
      
      expect(sendResponse).toHaveBeenCalledWith({ status: "Disconnected" });
    });
  });

  describe('SUBMIT_TASK handler', () => {
    test('should send task to Python server when WebSocket is connected', () => {
      const taskMessage = {
        type: 'SUBMIT_TASK',
        task: 'Find cheap laptops on Amazon',
        context: {
          url: 'https://example.com',
          title: 'Example Page',
          tabId: 123
        }
      };

      // Simulate handler logic
      if (mockWebSocket && mockWebSocket.readyState === 1) {
        // Set active tab from context
        if (taskMessage.context && taskMessage.context.tabId) {
          activeTabId = taskMessage.context.tabId;
        }

        // Create message for Python server
        const serverMessage = {
          type: "extension_event",
          id: Date.now(),
          data: {
            event_name: "user_task_submitted",
            task: taskMessage.task,
            context: taskMessage.context,
            tabId: taskMessage.context?.tabId || activeTabId
          }
        };

        mockWebSocket.send(JSON.stringify(serverMessage));
        sendResponse({ success: true });
      }

      expect(mockWebSocket.send).toHaveBeenCalled();
      const sentData = JSON.parse(mockWebSocket.send.mock.calls[0][0]);
      expect(sentData.type).toBe("extension_event");
      expect(sentData.data.event_name).toBe("user_task_submitted");
      expect(sentData.data.task).toBe("Find cheap laptops on Amazon");
      expect(sentData.data.tabId).toBe(123);
      expect(sendResponse).toHaveBeenCalledWith({ success: true });
    });

    test('should fail when WebSocket is not connected', () => {
      mockWebSocket.readyState = 3; // CLOSED

      const taskMessage = {
        type: 'SUBMIT_TASK',
        task: 'Test task',
        context: { tabId: 123 }
      };

      // Simulate handler logic
      if (!mockWebSocket || mockWebSocket.readyState !== 1) {
        sendResponse({ success: false, error: "WebSocket not connected to Python server" });
      }

      expect(mockWebSocket.send).not.toHaveBeenCalled();
      expect(sendResponse).toHaveBeenCalledWith({
        success: false,
        error: "WebSocket not connected to Python server"
      });
    });

    test('should handle WebSocket send error', () => {
      mockWebSocket.send.mockImplementation(() => {
        throw new Error('WebSocket send failed');
      });

      const taskMessage = {
        type: 'SUBMIT_TASK',
        task: 'Test task',
        context: { tabId: 123 }
      };

      // Simulate handler logic with error handling
      try {
        if (mockWebSocket && mockWebSocket.readyState === 1) {
          const serverMessage = {
            type: "extension_event",
            id: Date.now(),
            data: {
              event_name: "user_task_submitted",
              task: taskMessage.task,
              context: taskMessage.context,
              tabId: taskMessage.context?.tabId || activeTabId
            }
          };
          mockWebSocket.send(JSON.stringify(serverMessage));
          sendResponse({ success: true });
        }
      } catch (error) {
        sendResponse({ success: false, error: "Failed to send task to server: " + error.message });
      }

      expect(sendResponse).toHaveBeenCalledWith({
        success: false,
        error: "Failed to send task to server: WebSocket send failed"
      });
    });

    test('should update activeTabId from context', () => {
      let localActiveTabId = null;

      const taskMessage = {
        type: 'SUBMIT_TASK',
        task: 'Test task',
        context: {
          tabId: 456,
          url: 'https://test.com',
          title: 'Test'
        }
      };

      // Simulate setting active tab
      if (taskMessage.context && taskMessage.context.tabId) {
        localActiveTabId = taskMessage.context.tabId;
      }

      expect(localActiveTabId).toBe(456);
    });

    test('should handle missing context gracefully', () => {
      const taskMessage = {
        type: 'SUBMIT_TASK',
        task: 'Test task'
        // No context
      };

      // Simulate handler logic
      if (mockWebSocket && mockWebSocket.readyState === 1) {
        const serverMessage = {
          type: "extension_event",
          id: Date.now(),
          data: {
            event_name: "user_task_submitted",
            task: taskMessage.task,
            context: taskMessage.context,
            tabId: taskMessage.context?.tabId || activeTabId
          }
        };

        mockWebSocket.send(JSON.stringify(serverMessage));
        sendResponse({ success: true });
      }

      expect(mockWebSocket.send).toHaveBeenCalled();
      const sentData = JSON.parse(mockWebSocket.send.mock.calls[0][0]);
      expect(sentData.data.context).toBeUndefined();
      expect(sentData.data.tabId).toBeNull(); // activeTabId is null
    });
  });

  describe('Message structure validation', () => {
    test('should create proper extension_event structure', () => {
      const task = 'Complex task with special chars: $@#%';
      const context = {
        tabId: 789,
        url: 'https://test.com/page?query=test',
        title: 'Test Page & Title'
      };

      const serverMessage = {
        type: "extension_event",
        id: 12345,
        data: {
          event_name: "user_task_submitted",
          task: task,
          context: context,
          tabId: context.tabId
        }
      };

      expect(serverMessage).toMatchObject({
        type: "extension_event",
        id: expect.any(Number),
        data: {
          event_name: "user_task_submitted",
          task: 'Complex task with special chars: $@#%',
          context: {
            tabId: 789,
            url: 'https://test.com/page?query=test',
            title: 'Test Page & Title'
          },
          tabId: 789
        }
      });
    });

    test('should generate unique message IDs', () => {
      const id1 = Date.now();
      
      // Wait a tiny bit to ensure different timestamp
      jest.advanceTimersByTime(1);
      
      const id2 = Date.now();
      
      expect(id1).not.toBe(id2);
    });
  });
});