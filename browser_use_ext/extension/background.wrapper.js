// browser-use-ext/extension/background.wrapper.js
// This file loads the modular background script for testing purposes

// For Jest testing environment
if (typeof module !== 'undefined' && module.exports) {
    // In Node.js/Jest environment, export the modular version
    module.exports = require('./background.modular.js');
} else {
    // In browser environment, load the original background.js
    // The original file will be loaded by the extension manifest
    console.log('Background wrapper loaded in browser environment');
}