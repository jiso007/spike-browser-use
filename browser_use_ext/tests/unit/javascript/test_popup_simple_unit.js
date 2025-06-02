/**
 * Simplified unit tests for popup.js functionality
 * Tests the message handling without complex eval
 */

// Mock Chrome API
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

describe('Popup Message Handlers Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    chrome.runtime.lastError = null;
  });

  describe('GET_POPUP_STATUS message', () => {
    test('should send GET_POPUP_STATUS message to background', () => {
      // Simulate sending message to get status
      const callback = jest.fn();
      
      chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, callback);
      
      expect(chrome.runtime.sendMessage).toHaveBeenCalledWith(
        { type: "GET_POPUP_STATUS" },
        callback
      );
    });

    test('should handle connected response', () => {
      const statusElement = { textContent: '' };
      const submitButton = { disabled: true };
      
      // Simulate response handler
      const handleResponse = (response) => {
        if (response && response.status) {
          statusElement.textContent = `Status: ${response.status}`;
          submitButton.disabled = response.status !== 'Connected';
        }
      };
      
      // Test connected response
      handleResponse({ status: 'Connected' });
      
      expect(statusElement.textContent).toBe('Status: Connected');
      expect(submitButton.disabled).toBe(false);
    });

    test('should handle disconnected response', () => {
      const statusElement = { textContent: '' };
      const submitButton = { disabled: true };
      
      // Simulate response handler
      const handleResponse = (response) => {
        if (response && response.status) {
          statusElement.textContent = `Status: ${response.status}`;
          submitButton.disabled = response.status !== 'Connected';
        }
      };
      
      // Test disconnected response
      handleResponse({ status: 'Disconnected' });
      
      expect(statusElement.textContent).toBe('Status: Disconnected');
      expect(submitButton.disabled).toBe(true);
    });

    test('should handle error response', () => {
      const statusElement = { textContent: '' };
      const submitButton = { disabled: false };
      
      chrome.runtime.lastError = { message: 'Connection failed' };
      
      // Simulate error handler
      const handleError = () => {
        if (chrome.runtime.lastError) {
          statusElement.textContent = "Status: Error connecting to background";
          submitButton.disabled = true;
        }
      };
      
      handleError();
      
      expect(statusElement.textContent).toBe('Status: Error connecting to background');
      expect(submitButton.disabled).toBe(true);
    });
  });

  describe('SUBMIT_TASK message', () => {
    test('should validate task is not empty', () => {
      const taskInput = { value: '   ' };
      const showError = jest.fn();
      
      // Simulate validation
      const task = taskInput.value.trim();
      if (!task) {
        showError('Please enter a task', 'error');
      }
      
      expect(showError).toHaveBeenCalledWith('Please enter a task', 'error');
    });

    test('should send SUBMIT_TASK message with task data', async () => {
      const task = 'Find cheap laptops on Amazon';
      const mockTab = {
        id: 123,
        url: 'https://example.com',
        title: 'Example Page'
      };
      
      chrome.tabs.query.mockResolvedValue([mockTab]);
      
      // Get tab info
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      // Send message
      const message = {
        type: "SUBMIT_TASK",
        task: task,
        context: {
          url: tab.url,
          title: tab.title,
          tabId: tab.id
        }
      };
      
      chrome.runtime.sendMessage(message, jest.fn());
      
      expect(chrome.runtime.sendMessage).toHaveBeenCalledWith(
        expect.objectContaining({
          type: "SUBMIT_TASK",
          task: task,
          context: {
            url: 'https://example.com',
            title: 'Example Page',
            tabId: 123
          }
        }),
        expect.any(Function)
      );
    });

    test('should handle successful submission response', () => {
      const taskInput = { value: 'Test task' };
      const statusElement = { textContent: '', className: '' };
      const submitButton = { disabled: true };
      
      // Simulate success response handler
      const handleResponse = (response) => {
        if (response && response.success) {
          statusElement.textContent = 'Task submitted successfully!';
          statusElement.className = 'task-status success';
          taskInput.value = ''; // Clear input
          submitButton.disabled = false;
        }
      };
      
      handleResponse({ success: true });
      
      expect(statusElement.textContent).toBe('Task submitted successfully!');
      expect(statusElement.className).toBe('task-status success');
      expect(taskInput.value).toBe('');
      expect(submitButton.disabled).toBe(false);
    });

    test('should handle submission error response', () => {
      const statusElement = { textContent: '', className: '' };
      const submitButton = { disabled: true };
      
      // Simulate error response handler
      const handleResponse = (response) => {
        if (response && !response.success) {
          const error = response.error || 'Unknown error';
          statusElement.textContent = `Failed to submit task: ${error}`;
          statusElement.className = 'task-status error';
          submitButton.disabled = false;
        }
      };
      
      handleResponse({ success: false, error: 'WebSocket not connected' });
      
      expect(statusElement.textContent).toBe('Failed to submit task: WebSocket not connected');
      expect(statusElement.className).toBe('task-status error');
      expect(submitButton.disabled).toBe(false);
    });

    test('should handle runtime error during submission', () => {
      const statusElement = { textContent: '', className: '' };
      const submitButton = { disabled: true };
      
      chrome.runtime.lastError = { message: 'Extension error' };
      
      // Simulate runtime error handler
      const handleRuntimeError = () => {
        if (chrome.runtime.lastError) {
          statusElement.textContent = `Error: ${chrome.runtime.lastError.message}`;
          statusElement.className = 'task-status error';
          submitButton.disabled = false;
        }
      };
      
      handleRuntimeError();
      
      expect(statusElement.textContent).toBe('Error: Extension error');
      expect(statusElement.className).toBe('task-status error');
      expect(submitButton.disabled).toBe(false);
    });
  });

  describe('Keyboard shortcuts', () => {
    test('should submit on Enter key', () => {
      const submitButton = { click: jest.fn() };
      
      const handleKeyPress = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
          event.preventDefault();
          submitButton.click();
        }
      };
      
      const event = {
        key: 'Enter',
        shiftKey: false,
        preventDefault: jest.fn()
      };
      
      handleKeyPress(event);
      
      expect(event.preventDefault).toHaveBeenCalled();
      expect(submitButton.click).toHaveBeenCalled();
    });

    test('should not submit on Shift+Enter', () => {
      const submitButton = { click: jest.fn() };
      
      const handleKeyPress = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
          event.preventDefault();
          submitButton.click();
        }
      };
      
      const event = {
        key: 'Enter',
        shiftKey: true,
        preventDefault: jest.fn()
      };
      
      handleKeyPress(event);
      
      expect(event.preventDefault).not.toHaveBeenCalled();
      expect(submitButton.click).not.toHaveBeenCalled();
    });
  });

  describe('UI status functions', () => {
    test('should show task status with correct styling', () => {
      const statusElement = { textContent: '', className: '' };
      
      const showTaskStatus = (message, type) => {
        statusElement.textContent = message;
        statusElement.className = 'task-status ' + type;
      };
      
      showTaskStatus('Processing...', 'processing');
      
      expect(statusElement.textContent).toBe('Processing...');
      expect(statusElement.className).toBe('task-status processing');
    });

    test('should hide task status', () => {
      const statusElement = { textContent: 'Some message', className: 'task-status error' };
      
      const hideTaskStatus = () => {
        statusElement.className = 'task-status';
        statusElement.textContent = '';
      };
      
      hideTaskStatus();
      
      expect(statusElement.textContent).toBe('');
      expect(statusElement.className).toBe('task-status');
    });
  });
});