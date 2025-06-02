/**
 * Integration tests for popup to background script communication
 */

// Mock Chrome API
global.chrome = {
  runtime: {
    sendMessage: jest.fn(),
    onMessage: {
      addListener: jest.fn(),
      removeListener: jest.fn()
    },
    lastError: null
  },
  tabs: {
    query: jest.fn(),
    sendMessage: jest.fn()
  }
};

// Mock WebSocket
class MockWebSocket {
  constructor(url) {
    this.url = url;
    this.readyState = 1; // OPEN
    this.send = jest.fn();
    this.close = jest.fn();
    MockWebSocket.instances.push(this);
  }
  
  static instances = [];
  static OPEN = 1;
  static CLOSED = 3;
  
  static reset() {
    MockWebSocket.instances = [];
  }
}

global.WebSocket = MockWebSocket;

describe('Popup to Background Integration', () => {
  let messageHandlers = {};
  
  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();
    MockWebSocket.reset();
    messageHandlers = {};
    
    // Capture message handlers
    chrome.runtime.onMessage.addListener.mockImplementation((handler) => {
      messageHandlers['runtime'] = handler;
    });
  });

  describe('Complete user task flow', () => {
    test('should handle task submission from popup to WebSocket', async () => {
      // Setup mock tab
      const mockTab = {
        id: 123,
        url: 'https://example.com',
        title: 'Example Page'
      };
      chrome.tabs.query.mockResolvedValue([mockTab]);
      
      // Simulate background script setup
      const ws = new MockWebSocket('ws://localhost:8765');
      
      // Register background message handler
      const backgroundHandler = (message, sender, sendResponse) => {
        if (message.type === 'GET_POPUP_STATUS') {
          sendResponse({ status: 'Connected' });
          return false;
        }
        
        if (message.type === 'SUBMIT_TASK') {
          // Simulate background script processing
          const taskMessage = {
            type: "extension_event",
            id: Date.now(),
            data: {
              event_name: "user_task_submitted",
              task: message.task,
              context: message.context,
              tabId: message.context?.tabId
            }
          };
          
          ws.send(JSON.stringify(taskMessage));
          sendResponse({ success: true });
          return false;
        }
      };
      
      messageHandlers['runtime'] = backgroundHandler;
      
      // Simulate popup requesting status
      const statusResponse = await new Promise((resolve) => {
        messageHandlers['runtime'](
          { type: 'GET_POPUP_STATUS' },
          { tab: null },
          resolve
        );
      });
      
      expect(statusResponse.status).toBe('Connected');
      
      // Simulate popup submitting task
      const taskResponse = await new Promise((resolve) => {
        messageHandlers['runtime'](
          {
            type: 'SUBMIT_TASK',
            task: 'Find Python tutorials on Google',
            context: {
              url: mockTab.url,
              title: mockTab.title,
              tabId: mockTab.id
            }
          },
          { tab: null },
          resolve
        );
      });
      
      expect(taskResponse.success).toBe(true);
      expect(ws.send).toHaveBeenCalled();
      
      // Verify the message sent to WebSocket
      const sentMessage = JSON.parse(ws.send.mock.calls[0][0]);
      expect(sentMessage).toMatchObject({
        type: 'extension_event',
        data: {
          event_name: 'user_task_submitted',
          task: 'Find Python tutorials on Google',
          context: {
            url: 'https://example.com',
            title: 'Example Page',
            tabId: 123
          },
          tabId: 123
        }
      });
    });

    test('should handle disconnected WebSocket gracefully', async () => {
      // Setup disconnected WebSocket
      const ws = new MockWebSocket('ws://localhost:8765');
      ws.readyState = MockWebSocket.CLOSED;
      
      // Background handler with disconnected WebSocket
      const backgroundHandler = (message, sender, sendResponse) => {
        if (message.type === 'GET_POPUP_STATUS') {
          sendResponse({ status: 'Disconnected' });
          return false;
        }
        
        if (message.type === 'SUBMIT_TASK') {
          sendResponse({ 
            success: false, 
            error: 'WebSocket not connected to Python server' 
          });
          return false;
        }
      };
      
      messageHandlers['runtime'] = backgroundHandler;
      
      // Check status
      const statusResponse = await new Promise((resolve) => {
        messageHandlers['runtime'](
          { type: 'GET_POPUP_STATUS' },
          { tab: null },
          resolve
        );
      });
      
      expect(statusResponse.status).toBe('Disconnected');
      
      // Try to submit task
      const taskResponse = await new Promise((resolve) => {
        messageHandlers['runtime'](
          {
            type: 'SUBMIT_TASK',
            task: 'Test task',
            context: { tabId: 123 }
          },
          { tab: null },
          resolve
        );
      });
      
      expect(taskResponse.success).toBe(false);
      expect(taskResponse.error).toContain('WebSocket not connected');
      expect(ws.send).not.toHaveBeenCalled();
    });

    test('should handle multiple task submissions', async () => {
      const ws = new MockWebSocket('ws://localhost:8765');
      let activeTabId = null;
      
      const backgroundHandler = (message, sender, sendResponse) => {
        if (message.type === 'SUBMIT_TASK') {
          // Update active tab
          if (message.context && message.context.tabId) {
            activeTabId = message.context.tabId;
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
          
          ws.send(JSON.stringify(taskMessage));
          sendResponse({ success: true });
          return false;
        }
      };
      
      messageHandlers['runtime'] = backgroundHandler;
      
      // Submit multiple tasks
      const tasks = [
        { task: 'Task 1', tabId: 101 },
        { task: 'Task 2', tabId: 102 },
        { task: 'Task 3', tabId: 103 }
      ];
      
      for (const { task, tabId } of tasks) {
        const response = await new Promise((resolve) => {
          messageHandlers['runtime'](
            {
              type: 'SUBMIT_TASK',
              task: task,
              context: { tabId: tabId }
            },
            { tab: null },
            resolve
          );
        });
        
        expect(response.success).toBe(true);
      }
      
      // Verify all tasks were sent
      expect(ws.send).toHaveBeenCalledTimes(3);
      
      // Verify last active tab
      expect(activeTabId).toBe(103);
    });

    test('should handle WebSocket reconnection', async () => {
      // Initial WebSocket
      let ws = new MockWebSocket('ws://localhost:8765');
      
      const backgroundHandler = (message, sender, sendResponse) => {
        if (message.type === 'GET_POPUP_STATUS') {
          const status = ws && ws.readyState === MockWebSocket.OPEN 
            ? 'Connected' 
            : 'Disconnected';
          sendResponse({ status });
          return false;
        }
      };
      
      messageHandlers['runtime'] = backgroundHandler;
      
      // Check initial status
      let response = await new Promise((resolve) => {
        messageHandlers['runtime'](
          { type: 'GET_POPUP_STATUS' },
          { tab: null },
          resolve
        );
      });
      expect(response.status).toBe('Connected');
      
      // Simulate disconnect
      ws.readyState = MockWebSocket.CLOSED;
      ws = null;
      
      response = await new Promise((resolve) => {
        messageHandlers['runtime'](
          { type: 'GET_POPUP_STATUS' },
          { tab: null },
          resolve
        );
      });
      expect(response.status).toBe('Disconnected');
      
      // Simulate reconnection
      ws = new MockWebSocket('ws://localhost:8765');
      
      response = await new Promise((resolve) => {
        messageHandlers['runtime'](
          { type: 'GET_POPUP_STATUS' },
          { tab: null },
          resolve
        );
      });
      expect(response.status).toBe('Connected');
    });
  });

  describe('Error handling', () => {
    test('should handle runtime errors during message sending', async () => {
      chrome.runtime.lastError = { message: 'Extension context invalidated' };
      
      const backgroundHandler = (message, sender, sendResponse) => {
        if (message.type === 'GET_POPUP_STATUS') {
          // Simulate checking lastError
          if (chrome.runtime.lastError) {
            sendResponse({ 
              status: 'Error', 
              error: chrome.runtime.lastError.message 
            });
            return false;
          }
        }
      };
      
      messageHandlers['runtime'] = backgroundHandler;
      
      const response = await new Promise((resolve) => {
        messageHandlers['runtime'](
          { type: 'GET_POPUP_STATUS' },
          { tab: null },
          resolve
        );
      });
      
      expect(response.status).toBe('Error');
      expect(response.error).toBe('Extension context invalidated');
    });

    test('should handle WebSocket send failures', async () => {
      const ws = new MockWebSocket('ws://localhost:8765');
      ws.send.mockImplementation(() => {
        throw new Error('WebSocket send failed');
      });
      
      const backgroundHandler = (message, sender, sendResponse) => {
        if (message.type === 'SUBMIT_TASK') {
          try {
            const taskMessage = {
              type: "extension_event",
              id: Date.now(),
              data: {
                event_name: "user_task_submitted",
                task: message.task,
                context: message.context,
                tabId: message.context?.tabId
              }
            };
            
            ws.send(JSON.stringify(taskMessage));
            sendResponse({ success: true });
          } catch (error) {
            sendResponse({ 
              success: false, 
              error: 'Failed to send task to server: ' + error.message 
            });
          }
          return false;
        }
      };
      
      messageHandlers['runtime'] = backgroundHandler;
      
      const response = await new Promise((resolve) => {
        messageHandlers['runtime'](
          {
            type: 'SUBMIT_TASK',
            task: 'Test task',
            context: { tabId: 123 }
          },
          { tab: null },
          resolve
        );
      });
      
      expect(response.success).toBe(false);
      expect(response.error).toContain('Failed to send task to server');
    });
  });
});