/**
 * Unit tests for background.js user input functionality
 */

// Mock WebSocket
class MockWebSocket {
  constructor(url) {
    this.url = url;
    this.readyState = WebSocket.OPEN;
    this.send = jest.fn();
    this.close = jest.fn();
  }
}

global.WebSocket = MockWebSocket;
global.WebSocket.OPEN = 1;
global.WebSocket.CLOSED = 3;

// Mock Chrome API
global.chrome = {
  runtime: {
    onMessage: {
      addListener: jest.fn()
    },
    sendMessage: jest.fn(),
    lastError: null
  },
  tabs: {
    query: jest.fn(),
    get: jest.fn(),
    update: jest.fn(),
    sendMessage: jest.fn(),
    onActivated: {
      addListener: jest.fn()
    },
    onUpdated: {
      addListener: jest.fn()
    },
    onRemoved: {
      addListener: jest.fn()
    }
  }
};

describe('Background Script User Input Tests', () => {
  let messageHandler;
  let mockWebSocket;
  let activeTabId;
  let contentScriptsReady;

  beforeEach(() => {
    jest.clearAllMocks();
    
    // Create a fresh WebSocket mock
    mockWebSocket = new MockWebSocket('ws://localhost:8765');
    global.websocket = mockWebSocket;
    
    // Reset global state
    activeTabId = null;
    contentScriptsReady = new Set();
    
    // Get the message handler function
    messageHandler = chrome.runtime.onMessage.addListener.mock.calls[0]?.[0];
  });

  describe('GET_POPUP_STATUS handler', () => {
    test('should return Connected when WebSocket is open', () => {
      const sendResponse = jest.fn();
      mockWebSocket.readyState = WebSocket.OPEN;
      
      const result = messageHandler(
        { type: 'GET_POPUP_STATUS' },
        { tab: null },
        sendResponse
      );
      
      expect(sendResponse).toHaveBeenCalledWith({ status: 'Connected' });
      expect(result).toBe(false); // Synchronous response
    });

    test('should return Disconnected when WebSocket is closed', () => {
      const sendResponse = jest.fn();
      mockWebSocket.readyState = WebSocket.CLOSED;
      
      const result = messageHandler(
        { type: 'GET_POPUP_STATUS' },
        { tab: null },
        sendResponse
      );
      
      expect(sendResponse).toHaveBeenCalledWith({ status: 'Disconnected' });
      expect(result).toBe(false);
    });

    test('should return Disconnected when WebSocket is null', () => {
      const sendResponse = jest.fn();
      global.websocket = null;
      
      const result = messageHandler(
        { type: 'GET_POPUP_STATUS' },
        { tab: null },
        sendResponse
      );
      
      expect(sendResponse).toHaveBeenCalledWith({ status: 'Disconnected' });
      expect(result).toBe(false);
    });
  });

  describe('SUBMIT_TASK handler', () => {
    test('should send task to Python server when WebSocket is connected', () => {
      const sendResponse = jest.fn();
      const taskData = {
        type: 'SUBMIT_TASK',
        task: 'Find cheap laptops on Amazon',
        context: {
          url: 'https://example.com',
          title: 'Example Page',
          tabId: 123
        }
      };
      
      const result = messageHandler(taskData, { tab: null }, sendResponse);
      
      // Should send to WebSocket
      expect(mockWebSocket.send).toHaveBeenCalledWith(
        expect.stringContaining('"event_name":"user_task_submitted"')
      );
      
      // Verify the message structure
      const sentMessage = JSON.parse(mockWebSocket.send.mock.calls[0][0]);
      expect(sentMessage).toMatchObject({
        type: 'extension_event',
        data: {
          event_name: 'user_task_submitted',
          task: 'Find cheap laptops on Amazon',
          context: taskData.context,
          tabId: 123
        }
      });
      
      // Should respond with success
      expect(sendResponse).toHaveBeenCalledWith({ success: true });
      expect(result).toBe(false);
    });

    test('should handle WebSocket not connected', () => {
      const sendResponse = jest.fn();
      mockWebSocket.readyState = WebSocket.CLOSED;
      
      const taskData = {
        type: 'SUBMIT_TASK',
        task: 'Test task',
        context: { tabId: 123 }
      };
      
      const result = messageHandler(taskData, { tab: null }, sendResponse);
      
      expect(mockWebSocket.send).not.toHaveBeenCalled();
      expect(sendResponse).toHaveBeenCalledWith({
        success: false,
        error: 'WebSocket not connected to Python server'
      });
      expect(result).toBe(false);
    });

    test('should handle WebSocket null', () => {
      const sendResponse = jest.fn();
      global.websocket = null;
      
      const taskData = {
        type: 'SUBMIT_TASK',
        task: 'Test task',
        context: { tabId: 123 }
      };
      
      const result = messageHandler(taskData, { tab: null }, sendResponse);
      
      expect(sendResponse).toHaveBeenCalledWith({
        success: false,
        error: 'WebSocket not connected to Python server'
      });
      expect(result).toBe(false);
    });

    test('should update activeTabId from context', () => {
      const sendResponse = jest.fn();
      
      // Mock the activeTabId variable
      let mockActiveTabId = null;
      
      const taskData = {
        type: 'SUBMIT_TASK',
        task: 'Test task',
        context: {
          tabId: 456,
          url: 'https://test.com',
          title: 'Test'
        }
      };
      
      // Simulate the handler updating activeTabId
      const result = messageHandler(taskData, { tab: null }, sendResponse);
      
      // In actual implementation, activeTabId would be updated
      // Here we verify the message sent includes the correct tabId
      const sentMessage = JSON.parse(mockWebSocket.send.mock.calls[0][0]);
      expect(sentMessage.data.tabId).toBe(456);
    });

    test('should handle WebSocket send error', () => {
      const sendResponse = jest.fn();
      mockWebSocket.send.mockImplementation(() => {
        throw new Error('WebSocket send failed');
      });
      
      const taskData = {
        type: 'SUBMIT_TASK',
        task: 'Test task',
        context: { tabId: 123 }
      };
      
      const result = messageHandler(taskData, { tab: null }, sendResponse);
      
      expect(sendResponse).toHaveBeenCalledWith({
        success: false,
        error: 'Failed to send task to server: WebSocket send failed'
      });
      expect(result).toBe(false);
    });

    test('should handle missing context gracefully', () => {
      const sendResponse = jest.fn();
      
      const taskData = {
        type: 'SUBMIT_TASK',
        task: 'Test task'
        // No context provided
      };
      
      const result = messageHandler(taskData, { tab: null }, sendResponse);
      
      // Should still send the message
      expect(mockWebSocket.send).toHaveBeenCalled();
      
      const sentMessage = JSON.parse(mockWebSocket.send.mock.calls[0][0]);
      expect(sentMessage.data).toMatchObject({
        event_name: 'user_task_submitted',
        task: 'Test task',
        context: undefined
      });
      
      expect(sendResponse).toHaveBeenCalledWith({ success: true });
    });
  });

  describe('Message handler fallback', () => {
    test('should warn about unhandled message types', () => {
      const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();
      const sendResponse = jest.fn();
      
      const result = messageHandler(
        { type: 'UNKNOWN_TYPE', data: 'test' },
        { tab: { id: 123, url: 'https://test.com' } },
        sendResponse
      );
      
      expect(consoleWarnSpy).toHaveBeenCalledWith(
        expect.stringContaining('Unhandled runtime message type')
      );
      expect(result).toBe(false);
      
      consoleWarnSpy.mockRestore();
    });
  });

  describe('Integration with existing handlers', () => {
    test('should not interfere with content_script_ready handler', () => {
      const sendResponse = jest.fn();
      
      const result = messageHandler(
        { type: 'content_script_ready' },
        { tab: { id: 789, url: 'https://test.com' } },
        sendResponse
      );
      
      // This should be handled by existing logic
      expect(result).toBe(true); // Async response for content_script_ready
    });

    test('should not interfere with debug_get_ready_tabs handler', () => {
      const sendResponse = jest.fn();
      
      const result = messageHandler(
        { type: 'debug_get_ready_tabs' },
        { tab: null },
        sendResponse
      );
      
      expect(sendResponse).toHaveBeenCalledWith({
        status: 'ok',
        readyTabs: expect.any(Array)
      });
      expect(result).toBe(false); // Sync response
    });
  });
});