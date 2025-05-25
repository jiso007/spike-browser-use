// browser_use_ext/tests/javascript/content.test.js

// Mock chrome APIs before importing the content script
// jest-chrome (https://github.com/seznam/jest-chrome) is great for this.
// If not using jest-chrome, you'd build more extensive manual mocks.
global.chrome = {
    runtime: {
        sendMessage: jest.fn((message, callback) => {
            // Default mock implementation: Simulate successful ack
            // console.log("[Mock chrome.runtime.sendMessage] Called with:", message);
            if (typeof callback === 'function') {
                // Simulate async callback behavior
                setTimeout(() => callback({ status: "mock_acknowledged", tabId: message.tabId || 123 }), 0);
            }
            return Promise.resolve({ status: "mock_acknowledged_promise" });
        }),
        onMessage: {
            addListener: jest.fn(),
            removeListener: jest.fn(),
            hasListener: jest.fn(() => true)
        },
        lastError: null // Will be set by tests to simulate errors
    },
    // Mock other chrome APIs if content.js uses them directly.
};

// Mock DOM environment using JSDOM (Jest default) or a more specific setup if needed.
document.body.innerHTML = '<div id="test-div"><p>Hello</p><button id="test-btn">Click Me</button></div>';

// Import functions from content.js to be tested.
// This assumes content.js is structured to export its functions or that you can 
// load it in a way that makes its functions available in the test scope.
// For simplicity, let's imagine a scenario where key functions are accessible.
// If content.js is a single immediately-invoked script, testing becomes harder without refactoring.

// --- OPTION 1: If functions are globally available after script load (less ideal but common for content scripts)
// require('../../extension/content.js'); // This would execute the content script

// --- OPTION 2: If content.js exports its functions (better for testing)
// For this to work, content.js would need something like:
// if (typeof module !== 'undefined' && module.exports) {
//   module.exports = { signalReadyToBackground, handleGetState, ... };
// }
// For now, let's assume we can somehow access/mock the functions or test their effects.


// --- Mocks for functions within content.js if they are not directly testable or need to be isolated ---
let mockDetectActionableElements = jest.fn(() => [
    { id: 'el1', type: 'button', text_content: 'Mock Button', is_visible: true }
]);
let mockGenerateStableElementId = jest.fn(element => `mock_id_for_${element.tagName.toLowerCase()}`);

// --- Test Suite for signalReadyToBackground ---
ddescribe('signalReadyToBackground', () => {
    let signalReadyToBackground; // Will be assigned the actual function

    beforeEach(() => {
        // Reset mocks and chrome.runtime.lastError before each test
        chrome.runtime.sendMessage.mockClear();
        chrome.runtime.lastError = null;

        // Simulate loading content.js and getting the function
        // This is a simplified way; in a real setup, you might need to re-require or use a module system.
        // For this example, let's assume signalReadyToBackground is globally available or imported.
        // To make this runnable, signalReadyToBackground would need to be exposed by content.js
        // e.g. by attaching it to window for testing: window.signalReadyToBackground = async function() { ... }
        // Or by properly exporting it if content.js is treated as a module.
        
        // TEMPORARY: Define a mock version here based on your actual code if direct import is hard.
        // This should ideally be the *actual* function from content.js.
        signalReadyToBackground = async function () {
            // console.log("content.js: Attempting to send content_script_ready message.");
            const maxAttempts = 3;
            const retryDelayMs = 10; // Shorter delay for tests

            for (let attempt = 1; attempt <= maxAttempts; attempt++) {
                try {
                    // console.log(`content.js: Sending content_script_ready, attempt ${attempt}/${maxAttempts}`);
                    await new Promise((resolve, reject) => {
                        chrome.runtime.sendMessage({ type: "content_script_ready" }, response => {
                            if (chrome.runtime.lastError) {
                                const errorMsg = chrome.runtime.lastError.message;
                                // console.warn(`content.js: sendMessage CALLBACK - chrome.runtime.lastError detected...`);
                                if (errorMsg === "Could not establish connection. Receiving end does not exist.") {
                                    reject(new Error(errorMsg)); 
                                } else {
                                    reject(new Error(errorMsg));
                                }
                            } else {
                                // console.log("content.js: Background acked content_script_ready:", response);
                                resolve(response); 
                            }
                        });
                    });
                    // console.log("content.js: content_script_ready message successfully sent and acknowledged.");
                    return; 
                } catch (error) {
                    if (error.message === "Could not establish connection. Receiving end does not exist.") {
                        if (attempt < maxAttempts) {
                            // console.log(`content.js: Will retry sending content_script_ready...`);
                            await new Promise(resolve => setTimeout(resolve, retryDelayMs));
                        } else {
                            // console.error(`content.js: Failed to send content_script_ready after ${maxAttempts} attempts...`);
                            throw error; // Rethrow to fail the test if all attempts fail
                        }
                    } else {
                        throw error; // Rethrow other errors
                    }
                }
            }
        }
    });

    test('should send content_script_ready message successfully on first attempt', async () => {
        await signalReadyToBackground();
        expect(chrome.runtime.sendMessage).toHaveBeenCalledTimes(1);
        expect(chrome.runtime.sendMessage).toHaveBeenCalledWith({ type: "content_script_ready" }, expect.any(Function));
    });

    test('should retry if "Could not establish connection" error occurs', async () => {
        // Simulate error on first two attempts, success on third
        let callCount = 0;
        chrome.runtime.sendMessage.mockImplementation((message, callback) => {
            callCount++;
            if (callCount <= 2) {
                chrome.runtime.lastError = { message: "Could not establish connection. Receiving end does not exist." };
            } else {
                chrome.runtime.lastError = null; // Success on 3rd attempt
            }
            // Need to call the callback for the Promise in signalReadyToBackground to resolve/reject
            if (typeof callback === 'function') {
                 setTimeout(() => callback(chrome.runtime.lastError ? undefined : { status: "mock_success" }), 0);
            }
        });

        await signalReadyToBackground();
        expect(chrome.runtime.sendMessage).toHaveBeenCalledTimes(3);
    });

    test('should fail after max attempts if connection error persists', async () => {
        chrome.runtime.sendMessage.mockImplementation((message, callback) => {
            chrome.runtime.lastError = { message: "Could not establish connection. Receiving end does not exist." };
            if (typeof callback === 'function') {
                setTimeout(() => callback(undefined), 0); // Simulate error by not passing response
            }
        });
        
        await expect(signalReadyToBackground()).rejects.toThrow("Could not establish connection. Receiving end does not exist.");
        expect(chrome.runtime.sendMessage).toHaveBeenCalledTimes(3); // Max attempts
    });

    test('should not retry for other types of errors', async () => {
        chrome.runtime.sendMessage.mockImplementationOnce((message, callback) => {
            chrome.runtime.lastError = { message: "Some other runtime error." };
            if (typeof callback === 'function') {
                setTimeout(() => callback(undefined),0);
            }
        });

        await expect(signalReadyToBackground()).rejects.toThrow("Some other runtime error.");
        expect(chrome.runtime.sendMessage).toHaveBeenCalledTimes(1);
    });
});

// --- Test Suite for handleGetState (Simplified Example) ---
// Assuming handleGetState is exposed or can be invoked for testing
ddescribe('handleGetState', () => {
    let handleGetState; // Would be the actual function

    beforeAll(() => {
        // This is highly dependent on how handleGetState is defined and what it depends on.
        // We'd need to mock its dependencies like detectActionableElements.
        // For this example, let's define a mock version.
        handleGetState = async function(requestId) {
            // console.log(`handleGetState called for requestId: ${requestId}`);
            try {
                const actionableElements = mockDetectActionableElements(); // Use mock
                return {
                    type: "state_response",
                    status: "success",
                    state: {
                        url: window.location.href,
                        title: document.title,
                        actionable_elements: actionableElements,
                        // ... other state fields
                    }
                };
            } catch (error) {
                return { type: "state_response", status: "error", error: error.message };
            }
        };
    });

    beforeEach(() => {
        mockDetectActionableElements.mockClear();
        // Reset DOM or other global state if necessary
        window.location.href = 'http://testhost/page1';
        document.title = 'Test Page Title';
    });

    test('should return page state successfully', async () => {
        mockDetectActionableElements.mockReturnValue([
            { id: 'btn1', type: 'button', text_content: 'Submit' }
        ]);
        const stateResponse = await handleGetState("req1");
        
        expect(stateResponse.status).toBe("success");
        expect(stateResponse.state.url).toBe("http://testhost/page1");
        expect(stateResponse.state.title).toBe("Test Page Title");
        expect(stateResponse.state.actionable_elements).toEqual([
            { id: 'btn1', type: 'button', text_content: 'Submit' }
        ]);
        expect(mockDetectActionableElements).toHaveBeenCalledTimes(1);
    });

    test('should handle errors during state extraction', async () => {
        mockDetectActionableElements.mockImplementation(() => {
            throw new Error("DOM parsing failed");
        });
        const stateResponse = await handleGetState("req2");
        expect(stateResponse.status).toBe("error");
        expect(stateResponse.error).toBe("DOM parsing failed");
    });
});

// To run these tests:
// 1. Ensure Jest and jest-chrome are installed (`npm install --save-dev jest jest-chrome @types/jest` or `yarn add --dev ...`).
// 2. Configure Jest in package.json or jest.config.js.
// 3. Ensure your content.js functions are structured to be importable/testable.
//    (e.g., using module.exports or by attaching to `window` under a test flag).
// 4. Run `npx jest` or `yarn test`.

// Note: Testing content scripts that heavily manipulate a real DOM or rely on complex Chrome API
// interactions can be challenging. Sometimes, focusing on E2E tests with Playwright/Selenium
// for these parts is more practical, while unit testing more isolated logic pieces. 