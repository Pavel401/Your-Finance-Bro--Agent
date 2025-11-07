// Global state
let financeData = null;
let chatHistory = [];
let isProcessing = false;

// API Configuration - Will be loaded from backend
let API_BASE_URL = window.location.origin; // Default to current origin

// DOM Elements
const uploadSection = document.getElementById('uploadSection');
const chatSection = document.getElementById('chatSection');
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileStats = document.getElementById('fileStats');
const removeFileBtn = document.getElementById('removeFile');
const startChatBtn = document.getElementById('startChatBtn');
const newChatBtn = document.getElementById('newChatBtn');
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatSubtitle = document.getElementById('chatSubtitle');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
  // Load configuration from backend
  await loadConfig();
  initializeEventListeners();
});

async function loadConfig() {
  try {
    const response = await fetch('/config');
    if (response.ok) {
      const config = await response.json();
      API_BASE_URL = config.apiBaseUrl;
      console.log('API Base URL loaded:', API_BASE_URL);
    } else {
      console.warn('Failed to load config, using default:', API_BASE_URL);
    }
  } catch (error) {
    console.error('Error loading config:', error);
    console.warn('Using default API Base URL:', API_BASE_URL);
  }
}

function initializeEventListeners() {
  // File upload events
  dropZone.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', handleFileSelect);

  // Drag and drop events
  dropZone.addEventListener('dragover', handleDragOver);
  dropZone.addEventListener('dragleave', handleDragLeave);
  dropZone.addEventListener('drop', handleDrop);

  // Button events
  removeFileBtn.addEventListener('click', resetFileUpload);
  startChatBtn.addEventListener('click', showChatSection);
  newChatBtn.addEventListener('click', resetToUpload);

  // Chat events
  chatForm.addEventListener('submit', handleChatSubmit);
  chatInput.addEventListener('input', handleInputChange);
  chatInput.addEventListener('keydown', handleKeyDown);

  // Suggestion chips
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('suggestion-chip')) {
      const suggestion = e.target.dataset.suggestion;
      chatInput.value = suggestion;
      handleInputChange();
      handleChatSubmit(new Event('submit'));
    }
  });
}

// File Upload Handlers
function handleDragOver(e) {
  e.preventDefault();
  dropZone.classList.add('drag-over');
}

function handleDragLeave(e) {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
}

function handleDrop(e) {
  e.preventDefault();
  dropZone.classList.remove('drag-over');

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    processFile(files[0]);
  }
}

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) {
    processFile(file);
  }
}

function processFile(file) {
  // Check file type
  if (!file.name.endsWith('.json')) {
    showError('Please upload a JSON file');
    return;
  }

  // Check file size (max 10MB)
  if (file.size > 10 * 1024 * 1024) {
    showError('File size exceeds 10MB limit');
    return;
  }

  const reader = new FileReader();

  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result);
      validateAndStoreFinanceData(data, file.name);
    } catch (error) {
      showError('Invalid JSON file. Please check the file format.');
    }
  };

  reader.onerror = () => {
    showError('Error reading file. Please try again.');
  };

  reader.readAsText(file);
}

function validateAndStoreFinanceData(data, name) {
  // Basic validation
  if (!data.transactions && !data.accounts && !data.budgets) {
    showError('Invalid finance data format. Missing required fields.');
    return;
  }

  // Store the data
  financeData = data;

  // Convert snake_case to camelCase for API compatibility
  financeData = convertToCamelCase(data);

  // Display file info
  displayFileInfo(name, data);
}

function convertToCamelCase(obj) {
  if (Array.isArray(obj)) {
    return obj.map((item) => convertToCamelCase(item));
  } else if (obj !== null && typeof obj === 'object') {
    return Object.keys(obj).reduce((acc, key) => {
      const camelKey = key.replace(/_([a-z])/g, (g) => g[1].toUpperCase());
      acc[camelKey] = convertToCamelCase(obj[key]);
      return acc;
    }, {});
  }
  return obj;
}

function displayFileInfo(name, data) {
  fileName.textContent = name;

  const stats = [];
  if (data.transactions) stats.push(`${data.transactions.length} transactions`);
  if (data.accounts) stats.push(`${data.accounts.length} accounts`);
  if (data.budgets) stats.push(`${data.budgets.length} budgets`);

  fileStats.textContent = stats.join(' • ');

  dropZone.style.display = 'none';
  fileInfo.style.display = 'block';
}

function resetFileUpload() {
  financeData = null;
  fileInput.value = '';
  dropZone.style.display = 'block';
  fileInfo.style.display = 'none';
  fileName.textContent = '';
  fileStats.textContent = '';
}

function showChatSection() {
  if (!financeData) {
    showError('Please upload a file first');
    return;
  }

  uploadSection.style.display = 'none';
  chatSection.style.display = 'flex';

  // Update chat subtitle with file stats
  const stats = [];
  if (financeData.transactions) stats.push(`${financeData.transactions.length} transactions`);
  if (financeData.accounts) stats.push(`${financeData.accounts.length} accounts`);
  if (financeData.budgets) stats.push(`${financeData.budgets.length} budgets`);
  chatSubtitle.textContent = stats.join(' • ');

  // Focus on input
  chatInput.focus();
}

function resetToUpload() {
  chatSection.style.display = 'none';
  uploadSection.style.display = 'flex';

  // Clear chat history
  chatHistory = [];

  // Remove all messages except welcome message
  const messages = chatMessages.querySelectorAll('.message, .typing-indicator');
  messages.forEach((msg) => msg.remove());

  // Reset input
  chatInput.value = '';
  handleInputChange();
}

// Chat Handlers
function handleInputChange() {
  // Auto-resize textarea
  chatInput.style.height = 'auto';
  chatInput.style.height = chatInput.scrollHeight + 'px';

  // Enable/disable send button
  sendBtn.disabled = !chatInput.value.trim() || isProcessing;
}

function handleKeyDown(e) {
  // Submit on Enter (without Shift)
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    if (!sendBtn.disabled) {
      handleChatSubmit(new Event('submit'));
    }
  }
}

async function handleChatSubmit(e) {
  e.preventDefault();

  if (isProcessing || !chatInput.value.trim()) {
    return;
  }

  const userQuery = chatInput.value.trim();

  // Clear input
  chatInput.value = '';
  chatInput.style.height = 'auto';
  handleInputChange();

  // Add user message to chat
  addUserMessage(userQuery);

  // Show typing indicator
  showTypingIndicator();

  // Process the query
  await sendChatMessage(userQuery);
}

function addUserMessage(message) {
  // Remove welcome message if present
  const welcomeMsg = chatMessages.querySelector('.welcome-message');
  if (welcomeMsg) {
    welcomeMsg.remove();
  }

  const messageDiv = document.createElement('div');
  messageDiv.className = 'message user';
  messageDiv.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content">
            <div class="message-text">${escapeHtml(message)}</div>
        </div>
    `;

  chatMessages.appendChild(messageDiv);
  scrollToBottom();

  // Add to history
  chatHistory.push({
    role: 'user',
    content: message,
  });
}

function addAssistantMessage(message) {
  const messageDiv = document.createElement('div');
  messageDiv.className = 'message assistant';
  messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-text">${formatMessage(message)}</div>
        </div>
    `;

  chatMessages.appendChild(messageDiv);
  scrollToBottom();

  // Add to history
  chatHistory.push({
    role: 'assistant',
    content: message,
  });
}

function showTypingIndicator() {
  const typingDiv = document.createElement('div');
  typingDiv.className = 'typing-indicator';
  typingDiv.id = 'typingIndicator';
  typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="typing-dots">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;

  chatMessages.appendChild(typingDiv);
  scrollToBottom();
}

function hideTypingIndicator() {
  const typingIndicator = document.getElementById('typingIndicator');
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

async function sendChatMessage(userQuery) {
  isProcessing = true;
  sendBtn.disabled = true;

  try {
    const response = await fetch(`${API_BASE_URL}/agent/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_query: userQuery,
        finance_info: financeData,
        chat_history: chatHistory.slice(0, -1), // Exclude the current user message
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let assistantMessage = '';
    let buffer = '';

    hideTypingIndicator();

    // Create assistant message container
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="message-text"></div>
            </div>
        `;
    chatMessages.appendChild(messageDiv);
    const messageText = messageDiv.querySelector('.message-text');

    // Read the stream
    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      // Decode the chunk and add to buffer
      const chunk = decoder.decode(value, { stream: true });
      buffer += chunk;

      // Process complete JSON objects (newline-delimited)
      const lines = buffer.split('\n');

      // Keep the last incomplete line in the buffer
      buffer = lines.pop() || '';

      // Process each complete line
      for (const line of lines) {
        if (line.trim()) {
          try {
            // Parse the JSON object
            const jsonResponse = JSON.parse(line);

            // Extract response_text from the validated response
            if (jsonResponse.response_text) {
              assistantMessage = jsonResponse.response_text;
              messageText.innerHTML = formatMessage(assistantMessage);
              scrollToBottom();
            }
          } catch (parseError) {
            console.error('Error parsing JSON chunk:', parseError);
            // Continue processing other chunks
          }
        }
      }
    }

    // Process any remaining data in buffer
    if (buffer.trim()) {
      try {
        const jsonResponse = JSON.parse(buffer);
        if (jsonResponse.response_text) {
          assistantMessage = jsonResponse.response_text;
          messageText.innerHTML = formatMessage(assistantMessage);
          scrollToBottom();
        }
      } catch (parseError) {
        console.error('Error parsing final JSON chunk:', parseError);
      }
    }

    // Add final message to history
    chatHistory.push({
      role: 'assistant',
      content: assistantMessage,
    });
  } catch (error) {
    console.error('Error sending message:', error);
    hideTypingIndicator();
    showError('Failed to send message. Please check your connection and try again.');
  } finally {
    isProcessing = false;
    handleInputChange();
  }
}

// Utility Functions
function formatMessage(text) {
  // Simple markdown-like formatting
  let formatted = escapeHtml(text);

  // Bold: **text** or __text__
  formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  formatted = formatted.replace(/__(.+?)__/g, '<strong>$1</strong>');

  // Code: `code`
  formatted = formatted.replace(/`(.+?)`/g, '<code>$1</code>');

  // Line breaks
  formatted = formatted.replace(/\n/g, '<br>');

  // Lists (simple implementation)
  formatted = formatted.replace(/^- (.+)$/gm, '<li>$1</li>');
  formatted = formatted.replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');

  return formatted;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showError(message) {
  // Create error message element
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span>${message}</span>
    `;

  // Insert at the top of main content or chat messages
  const container =
    chatSection.style.display === 'none'
      ? uploadSection.querySelector('.upload-card')
      : chatMessages;

  container.insertBefore(errorDiv, container.firstChild);

  // Remove after 5 seconds
  setTimeout(() => {
    errorDiv.remove();
  }, 5000);
}

// Service Worker for offline support (optional)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // Uncomment to enable service worker
    // navigator.serviceWorker.register('/sw.js');
  });
}
