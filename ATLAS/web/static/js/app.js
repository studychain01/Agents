/**
 * ATLAS Web Application JavaScript
 * Handles chat interface, agent selection, and API communication
 */

class ATLASApp {
    constructor() {
        this.currentAgent = 'planner';
        this.isProcessing = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkSystemStatus();
        this.autoResizeTextarea();
    }

    setupEventListeners() {
        // Agent selection
        document.querySelectorAll('.agent-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.selectAgent(e.currentTarget.dataset.agent);
            });
        });

        // Chat input
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');

        chatInput.addEventListener('input', () => {
            sendBtn.disabled = !chatInput.value.trim() || this.isProcessing;
        });

        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        sendBtn.addEventListener('click', () => {
            this.sendMessage();
        });
    }

    selectAgent(agentType) {
        this.currentAgent = agentType;
        
        // Update UI
        document.querySelectorAll('.agent-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-agent="${agentType}"]`).classList.add('active');

        // Add system message about agent change
        this.addMessage('assistant', `Switched to ${agentType === 'planner' ? 'Study Planner' : 'Note Writer'}. How can I help you?`);
    }

    async checkSystemStatus() {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            
            this.updateStatusIndicator(status.status, status.initialized);
        } catch (error) {
            console.error('Failed to check system status:', error);
            this.updateStatusIndicator('error', false);
        }
    }

    updateStatusIndicator(status, initialized) {
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');

        statusDot.className = `status-dot ${status}`;
        
        if (initialized) {
            statusText.textContent = 'Ready';
        } else if (status === 'error') {
            statusText.textContent = 'Error';
        } else {
            statusText.textContent = 'Initializing...';
        }
    }

    async sendMessage() {
        const chatInput = document.getElementById('chat-input');
        const message = chatInput.value.trim();

        if (!message || this.isProcessing) return;

        // Add user message to chat
        this.addMessage('user', message);
        chatInput.value = '';
        
        // Update UI state
        this.setProcessing(true);

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: message,
                    agent: this.currentAgent
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.addMessage('assistant', data.response);
            } else {
                this.addMessage('assistant', `Error: ${data.error}`, 'error');
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            this.addMessage('assistant', 'Sorry, I encountered an error. Please try again.', 'error');
        } finally {
            this.setProcessing(false);
        }
    }

    addMessage(type, content, messageType = 'normal') {
        const chatMessages = document.getElementById('chat-messages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = type === 'user' ? 
            '<i class="fas fa-user"></i>' : 
            '<i class="fas fa-robot"></i>';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (messageType === 'error') {
            messageContent.style.background = 'var(--error-color)';
            messageContent.style.color = 'white';
        }

        // Handle markdown-like formatting
        const formattedContent = this.formatMessage(content);
        messageContent.innerHTML = formattedContent;

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    formatMessage(content) {
        // Simple markdown-like formatting
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
            .replace(/^- (.+)$/gm, '<li>$1</li>') // List items
            .replace(/(\n|^)([A-Z][A-Z\s]+:)/g, '$1<strong>$2</strong>') // Section headers
            .replace(/\n/g, '<br>'); // Line breaks
    }

    setProcessing(processing) {
        this.isProcessing = processing;
        const sendBtn = document.getElementById('send-btn');
        const chatInput = document.getElementById('chat-input');
        const loadingOverlay = document.getElementById('loading-overlay');

        sendBtn.disabled = processing || !chatInput.value.trim();
        
        if (processing) {
            loadingOverlay.classList.remove('hidden');
        } else {
            loadingOverlay.classList.add('hidden');
        }
    }

    autoResizeTextarea() {
        const textarea = document.getElementById('chat-input');
        
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    }
}

// Global function for suggestion pills
function sendSuggestion(message) {
    const chatInput = document.getElementById('chat-input');
    chatInput.value = message;
    chatInput.focus();
    
    // Trigger input event to enable send button
    chatInput.dispatchEvent(new Event('input'));
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.atlasApp = new ATLASApp();
});

// Add some visual feedback for interactions
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('pill')) {
        e.target.style.transform = 'scale(0.95)';
        setTimeout(() => {
            e.target.style.transform = '';
        }, 150);
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + / to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        document.getElementById('chat-input').focus();
    }
    
    // Escape to clear input
    if (e.key === 'Escape') {
        const chatInput = document.getElementById('chat-input');
        if (document.activeElement === chatInput) {
            chatInput.value = '';
            chatInput.blur();
        }
    }
});
