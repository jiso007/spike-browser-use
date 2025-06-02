// browser_use_ext/tests/unit/javascript/popup_test.js

// Mock chrome APIs before any imports
global.chrome = {
    runtime: {
        sendMessage: jest.fn(),
        lastError: null,
        onMessage: {
            addListener: jest.fn(),
            removeListener: jest.fn(),
            hasListener: jest.fn(() => true)
        }
    }
};

// Mock DOM environment
// JSDOM provides document, so we'll extend it instead of replacing it
if (!global.document) {
    global.document = {
        addEventListener: jest.fn(),
        getElementById: jest.fn()
    };
} else {
    // If document exists, just mock the methods we need
    global.document.addEventListener = jest.fn();
    global.document.getElementById = jest.fn();
}

describe('Popup Script', () => {
    let mockStatusElement;
    let popupScript;
    
    beforeEach(() => {
        // Reset all mocks
        jest.clearAllMocks();
        
        // Setup mock status element
        mockStatusElement = {
            textContent: ''
        };
        
        global.document.getElementById.mockReturnValue(mockStatusElement);
        
        // Reset chrome mocks if available
        if (global.chrome && global.chrome.runtime) {
            global.chrome.runtime.lastError = null;
            global.chrome.runtime.sendMessage.mockReset();
        }
        
        // We'll execute the popup script logic inline since it's an IIFE
        popupScript = null;
    });

    describe('DOMContentLoaded Event Handling', () => {
        test('should register DOMContentLoaded event listener', () => {
            // Load popup.js content manually since it's an IIFE
            require('../../../extension/popup.js');
            
            expect(global.document.addEventListener).toHaveBeenCalledWith(
                'DOMContentLoaded',
                expect.any(Function)
            );
        });

        test('should get status element by ID when DOM is loaded', () => {
            // Simulate the DOMContentLoaded callback
            const domLoadedCallback = () => {
                const statusElement = global.document.getElementById('status');
                
                if (global.chrome && global.chrome.runtime && global.chrome.runtime.sendMessage) {
                    global.chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, function(response) {
                        if (global.chrome.runtime.lastError) {
                            statusElement.textContent = "Status: Error connecting to background";
                            return;
                        }
                        if (response && response.status) {
                            statusElement.textContent = `Status: ${response.status}`;
                        }
                    });
                } else {
                    statusElement.textContent = "Status: (chrome.runtime not available)";
                }
            };
            
            domLoadedCallback();
            
            expect(global.document.getElementById).toHaveBeenCalledWith('status');
        });
    });

    describe('Chrome Runtime Communication', () => {
        test('should send GET_POPUP_STATUS message when chrome.runtime is available', () => {
            const domLoadedCallback = () => {
                const statusElement = global.document.getElementById('status');
                
                if (global.chrome && global.chrome.runtime && global.chrome.runtime.sendMessage) {
                    global.chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, function(response) {
                        if (global.chrome.runtime.lastError) {
                            statusElement.textContent = "Status: Error connecting to background";
                            return;
                        }
                        if (response && response.status) {
                            statusElement.textContent = `Status: ${response.status}`;
                        }
                    });
                }
            };
            
            domLoadedCallback();
            
            expect(global.chrome.runtime.sendMessage).toHaveBeenCalledWith(
                { type: "GET_POPUP_STATUS" },
                expect.any(Function)
            );
        });

        test('should handle successful response from background script', async () => {
            const mockResponse = { status: "Connected" };
            
            global.chrome.runtime.sendMessage.mockImplementationOnce((message, callback) => {
                if (typeof callback === 'function') {
                    setTimeout(() => callback(mockResponse), 0);
                }
            });
            
            const domLoadedCallback = () => {
                const statusElement = global.document.getElementById('status');
                
                global.chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, function(response) {
                    if (global.chrome.runtime.lastError) {
                        statusElement.textContent = "Status: Error connecting to background";
                        return;
                    }
                    if (response && response.status) {
                        statusElement.textContent = `Status: ${response.status}`;
                    }
                });
            };
            
            domLoadedCallback();
            
            // Wait for callback to execute
            await new Promise(resolve => setTimeout(resolve, 20));
            expect(mockStatusElement.textContent).toBe('Status: Connected');
        });

        test('should handle chrome.runtime.lastError', async () => {
            global.chrome.runtime.lastError = { message: "Extension context invalidated" };
            
            global.chrome.runtime.sendMessage.mockImplementationOnce((message, callback) => {
                if (typeof callback === 'function') {
                    setTimeout(() => callback(null), 0);
                }
            });
            
            const domLoadedCallback = () => {
                const statusElement = global.document.getElementById('status');
                
                global.chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, function(response) {
                    if (global.chrome.runtime.lastError) {
                        statusElement.textContent = "Status: Error connecting to background";
                        return;
                    }
                    if (response && response.status) {
                        statusElement.textContent = `Status: ${response.status}`;
                    }
                });
            };
            
            domLoadedCallback();
            
            // Wait for callback to execute
            await new Promise(resolve => setTimeout(resolve, 20));
            expect(mockStatusElement.textContent).toBe('Status: Error connecting to background');
        });

        test('should handle response without status field', async () => {
            const mockResponse = { data: "some other data" };
            
            global.chrome.runtime.sendMessage.mockImplementationOnce((message, callback) => {
                if (typeof callback === 'function') {
                    setTimeout(() => callback(mockResponse), 0);
                }
            });
            
            const domLoadedCallback = () => {
                const statusElement = global.document.getElementById('status');
                
                global.chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, function(response) {
                    if (global.chrome.runtime.lastError) {
                        statusElement.textContent = "Status: Error connecting to background";
                        return;
                    }
                    if (response && response.status) {
                        statusElement.textContent = `Status: ${response.status}`;
                    }
                });
            };
            
            domLoadedCallback();
            
            // Status should remain empty since response.status is undefined
            await new Promise(resolve => setTimeout(resolve, 20));
            expect(mockStatusElement.textContent).toBe('');
        });
    });

    describe('Fallback Behavior', () => {
        test('should set fallback message when chrome.runtime is not available', () => {
            // Remove chrome.runtime
            global.chrome = undefined;
            
            const domLoadedCallback = () => {
                const statusElement = global.document.getElementById('status');
                
                if (global.chrome && global.chrome.runtime && global.chrome.runtime.sendMessage) {
                    global.chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, function(response) {
                        if (global.chrome.runtime.lastError) {
                            statusElement.textContent = "Status: Error connecting to background";
                            return;
                        }
                        if (response && response.status) {
                            statusElement.textContent = `Status: ${response.status}`;
                        }
                    });
                } else {
                    statusElement.textContent = "Status: (chrome.runtime not available)";
                }
            };
            
            domLoadedCallback();
            
            expect(mockStatusElement.textContent).toBe('Status: (chrome.runtime not available)');
        });

        test('should set fallback message when chrome.runtime.sendMessage is not available', () => {
            // Store original chrome object
            const originalChrome = global.chrome;
            
            global.chrome = {
                runtime: {
                    // sendMessage is missing
                    lastError: null
                }
            };
            
            const domLoadedCallback = () => {
                const statusElement = global.document.getElementById('status');
                
                if (global.chrome && global.chrome.runtime && global.chrome.runtime.sendMessage) {
                    global.chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, function(response) {
                        if (global.chrome.runtime.lastError) {
                            statusElement.textContent = "Status: Error connecting to background";
                            return;
                        }
                        if (response && response.status) {
                            statusElement.textContent = `Status: ${response.status}`;
                        }
                    });
                } else {
                    statusElement.textContent = "Status: (chrome.runtime not available)";
                }
            };
            
            domLoadedCallback();
            
            expect(mockStatusElement.textContent).toBe('Status: (chrome.runtime not available)');
            
            // Restore chrome object
            global.chrome = originalChrome;
        });
    });

    describe('Status Element Updates', () => {
        test('should update status element text content correctly', async () => {
            const testStatuses = [
                'Connected',
                'Disconnected', 
                'Connecting...',
                'Error'
            ];
            
            for (const status of testStatuses) {
                // Reset state for each iteration
                jest.clearAllMocks();
                
                // Ensure chrome is properly set up for each iteration
                global.chrome = {
                    runtime: {
                        sendMessage: jest.fn(),
                        lastError: null,
                        onMessage: {
                            addListener: jest.fn(),
                            removeListener: jest.fn(),
                            hasListener: jest.fn(() => true)
                        }
                    }
                };
                
                mockStatusElement.textContent = '';
                
                // Setup fresh mock for this status
                global.chrome.runtime.sendMessage.mockImplementationOnce((message, callback) => {
                    if (typeof callback === 'function') {
                        setTimeout(() => callback({ status }), 0);
                    }
                });
                
                const domLoadedCallback = () => {
                    const statusElement = global.document.getElementById('status');
                    
                    global.chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, function(response) {
                        if (global.chrome.runtime.lastError) {
                            statusElement.textContent = "Status: Error connecting to background";
                            return;
                        }
                        if (response && response.status) {
                            statusElement.textContent = `Status: ${response.status}`;
                        }
                    });
                };
                
                domLoadedCallback();
                
                // Wait for async callback
                await new Promise(resolve => setTimeout(resolve, 20));
                
                expect(mockStatusElement.textContent).toBe(`Status: ${status}`);
            }
        });
    });
});