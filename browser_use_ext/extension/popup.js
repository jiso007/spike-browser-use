// This script can be used to communicate with the background script
// or update the popup's content dynamically.
document.addEventListener('DOMContentLoaded', function() {
  const statusElement = document.getElementById('status');
  
  // Example: Try to get status from background script if needed
  // This is just a placeholder, actual communication might be more complex
  if (chrome && chrome.runtime && chrome.runtime.sendMessage) {
    chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, function(response) {
      if (chrome.runtime.lastError) {
        // console.warn("Error getting popup status:", chrome.runtime.lastError.message);
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
}); 