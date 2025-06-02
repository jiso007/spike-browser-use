// This script handles the popup UI interactions and communicates with the background script
document.addEventListener('DOMContentLoaded', function() {
  const statusElement = document.getElementById('status');
  const taskInput = document.getElementById('task-input');
  const submitButton = document.getElementById('submit-task');
  const taskStatus = document.getElementById('task-status');
  
  // Get WebSocket connection status from background script
  if (chrome && chrome.runtime && chrome.runtime.sendMessage) {
    chrome.runtime.sendMessage({ type: "GET_POPUP_STATUS" }, function(response) {
      if (chrome.runtime.lastError) {
        statusElement.textContent = "Status: Error connecting to background";
        submitButton.disabled = true;
        return;
      }
      if (response && response.status) {
        statusElement.textContent = `Status: ${response.status}`;
        // Enable submit button only if connected
        submitButton.disabled = response.status !== 'Connected';
      }
    });
  } else {
    statusElement.textContent = "Status: (chrome.runtime not available)";
    submitButton.disabled = true;
  }
  
  // Handle task submission
  submitButton.addEventListener('click', async function() {
    const task = taskInput.value.trim();
    
    if (!task) {
      showTaskStatus('Please enter a task', 'error');
      return;
    }
    
    // Disable button and show processing status
    submitButton.disabled = true;
    showTaskStatus('Processing task...', 'processing');
    
    try {
      // Get current tab info
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      // Send task to background script
      chrome.runtime.sendMessage({
        type: "SUBMIT_TASK",
        task: task,
        context: {
          url: tab.url,
          title: tab.title,
          tabId: tab.id
        }
      }, function(response) {
        if (chrome.runtime.lastError) {
          showTaskStatus('Error: ' + chrome.runtime.lastError.message, 'error');
          submitButton.disabled = false;
          return;
        }
        
        if (response && response.success) {
          showTaskStatus('Task submitted successfully!', 'success');
          taskInput.value = ''; // Clear input
          
          // Re-enable button after a delay
          setTimeout(() => {
            submitButton.disabled = false;
            hideTaskStatus();
          }, 3000);
        } else {
          showTaskStatus('Failed to submit task: ' + (response?.error || 'Unknown error'), 'error');
          submitButton.disabled = false;
        }
      });
    } catch (error) {
      showTaskStatus('Error: ' + error.message, 'error');
      submitButton.disabled = false;
    }
  });
  
  // Helper functions for status display
  function showTaskStatus(message, type) {
    taskStatus.textContent = message;
    taskStatus.className = 'task-status ' + type;
  }
  
  function hideTaskStatus() {
    taskStatus.className = 'task-status';
    taskStatus.textContent = '';
  }
  
  // Allow Enter key to submit task
  taskInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submitButton.click();
    }
  });
}); 