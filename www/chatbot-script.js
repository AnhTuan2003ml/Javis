class ChatApp {
    constructor() {
        this.currentProvider = 'auto';
        this.currentModel = null;
        this.uploadedFile = null;
        this.autoCompleteTimeout = null;
        this.selectedSuggestionIndex = -1;
        this.suggestions = [];
        this.isVoiceChatActive = false;
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.currentUtterance = null;
        this.isListening = false;
        this.selectedVoice = null;
        this.voiceGender = 'male';
        this.speechRate = 0.85;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadProviders();
        this.loadChatHistory();
        this.autoResizeTextarea();
        this.updateModelDisplay();
        this.initVoices();
    }

    bindEvents() {
        // Send message
        document.getElementById('sendBtn').addEventListener('click', () => this.sendMessage());
        document.getElementById('messageInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (this.selectedSuggestionIndex >= 0) {
                    this.selectSuggestion(this.selectedSuggestionIndex);
                } else {
                    this.sendMessage();
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.navigateSuggestions(1);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.navigateSuggestions(-1);
            } else if (e.key === 'Escape') {
                this.hideAutoComplete();
            }
        });
        
        document.getElementById('messageInput').addEventListener('input', (e) => {
            this.handleAutoComplete(e.target.value);
        });

        // New chat
        document.getElementById('newChatBtn').addEventListener('click', () => this.createNewChat());

        // Model selection
        document.getElementById('modelSelect').addEventListener('change', (e) => {
            const [provider, model] = e.target.value.split('|');
            this.currentProvider = provider;
            this.currentModel = model || null;
            this.updateModelDisplay();
        });

        // Voice chat button
        document.getElementById('voiceBtn').addEventListener('click', () => this.toggleVoiceChat());
        
        // Voice selection dropdown
        document.getElementById('voiceSelect').addEventListener('change', (e) => this.selectVoice(e.target.value));
        
        // Speed control button
        document.getElementById('speedBtn').addEventListener('click', () => this.showSpeedControl());
        
        // Settings popup
        document.getElementById('settingsBtn').addEventListener('click', () => {
            const popup = document.getElementById('settingsPopup');
            popup.style.display = popup.style.display === 'none' ? 'block' : 'none';
        });
        
        document.getElementById('closeSettings').addEventListener('click', () => {
            document.getElementById('settingsPopup').style.display = 'none';
        });
        
        // Auto-expand dropdown on select hover only
        document.getElementById('modelSelect').addEventListener('mouseenter', () => {
            const select = document.getElementById('modelSelect');
            select.size = select.options.length;
        });
        
        document.getElementById('modelSelect').addEventListener('mouseleave', () => {
            const select = document.getElementById('modelSelect');
            select.size = 1;
        });
        
        // File upload
        document.getElementById('attachBtn').addEventListener('click', () => {
            document.getElementById('fileInput').click();
        });
        
        // Clear history
        document.getElementById('clearHistoryBtn').addEventListener('click', () => this.clearAllHistory());



        document.getElementById('fileInput').addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileUpload(e.target.files[0]);
            }
        });

        document.getElementById('removeFile').addEventListener('click', () => {
            this.removeFile();
        });
        
        // Hide autocomplete when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.input-container-wrapper')) {
                this.hideAutoComplete();
            }
        });
    }

    autoResizeTextarea() {
        const textarea = document.getElementById('messageInput');
        textarea.addEventListener('input', () => {
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
        });
    }

    async loadProviders() {
        try {
            const response = await fetch('http://localhost:5000/providers');
            const providers = await response.json();
            
            const providerSelect = document.getElementById('providerSelect');
            const modelSelect = document.getElementById('modelSelect');
            
            // Clear existing options except auto
            Array.from(providerSelect.options).forEach(option => {
                if (option.value !== 'auto') {
                    option.disabled = !providers[option.value];
                }
            });
            
            this.providers = providers;
            this.updateModelOptions();
        } catch (error) {
            console.error('Failed to load providers:', error);
        }
    }


    
    updateModelDisplay() {
        const display = document.getElementById('modelDisplay');
        const select = document.getElementById('modelSelect');
        const selectedText = select.options[select.selectedIndex].text;
        display.textContent = selectedText;
    }
    
    async clearAllHistory() {
        if (confirm('Are you sure you want to clear all chat history?')) {
            try {
                await fetch('http://localhost:5000/clear-all-history', { method: 'POST' });
                this.loadChatHistory();
                this.newChat();
            } catch (error) {
                console.error('Failed to clear history:', error);
            }
        }
    }

    async handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);

        this.setStatus('Uploading file...', 'loading');

        try {
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.uploadedFile = {
                    name: result.filename
                };
                this.showFilePreview(result.filename);
                this.setStatus(result.message, 'success');
            } else {
                this.setStatus(result.error, 'error');
            }
        } catch (error) {
            this.setStatus('Upload failed', 'error');
            console.error('Upload error:', error);
        }
    }

    showFilePreview(filename) {
        document.getElementById('fileName').textContent = filename;
        document.getElementById('filePreview').style.display = 'block';
    }

    async removeFile() {
        this.uploadedFile = null;
        document.getElementById('filePreview').style.display = 'none';
        document.getElementById('fileInput').value = '';
        
        // Clear file content from backend
        try {
            await fetch('http://localhost:5000/clear-file', { method: 'POST' });
        } catch (error) {
            console.error('Error clearing file:', error);
        }
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();

        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        messageInput.value = '';
        messageInput.style.height = 'auto';

        // Hide welcome message
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.display = 'none';
        }

        // Show typing indicator
        this.showTypingIndicator();
        this.setStatus('Thinking...', 'loading');

        try {
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    provider: this.currentProvider,
                    model: this.currentModel
                })
            });

            this.hideTypingIndicator();

            // Check if response is a file download
            const contentType = response.headers.get('content-type');
            if (contentType && (
                contentType.includes("application/vnd.openxmlformats-officedocument.presentationml.presentation") || 
                contentType.includes("application/vnd.openxmlformats-officedocument.wordprocessingml.document") ||
                contentType.includes("application/pdf") ||
                contentType.includes("image/")
            )) {
                // Handle file download
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                
                // Extract filename from response headers
                const contentDisposition = response.headers.get('content-disposition');
                let filename = 'document';
                if (contentDisposition) {
                    const match = contentDisposition.match(/filename=(.+)/);
                    if (match) filename = match[1].replace(/"/g, '');
                }
                
                a.download = filename;
                a.click();
                window.URL.revokeObjectURL(url);
                
                this.addMessage(`✅ Document created and downloaded: ${filename}`, 'assistant', message);
                this.setStatus('Document downloaded', 'success');
            } else {
                // Handle regular JSON response
                const result = await response.json();
                
                if (result.error) {
                    this.addMessage(`Error: ${result.error}`, 'assistant');
                    this.setStatus('Error occurred', 'error');
                } else {
                    this.addMessage(result.response, 'assistant', message);
                    this.setStatus('Ready', 'ready');
                    // Speak the response
                    this.speakResponse(result.response);
                }
            }
            
            // Refresh chat history after new message
            this.loadChatHistory();
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
            this.setStatus('Connection error', 'error');
            console.error('Chat error:', error);
        }

        // Clear uploaded file after sending
        if (this.uploadedFile) {
            this.removeFile();
        }
    }

    addMessage(content, sender, userMessage = null) {
        const chatContainer = document.getElementById('chatContainer');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const messageWrapper = document.createElement('div');
        messageWrapper.className = 'message-wrapper';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Format message content (handle code blocks, etc.)
        messageContent.innerHTML = this.formatMessage(content);
        
        messageWrapper.appendChild(avatar);
        messageWrapper.appendChild(messageContent);
        messageDiv.appendChild(messageWrapper);
        
        // Add action buttons for AI responses (below the message)
        if (sender === 'assistant') {
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'message-actions';
            actionsDiv.innerHTML = `
                <button class="action-btn copy-btn" onclick="chatApp.copyMessage(this)" title="Copy message">
                    <i class="fas fa-copy"></i>
                </button>
                <button class="action-btn" onclick="chatApp.likeMessage(this)" title="Good response">
                    <i class="fas fa-thumbs-up"></i>
                </button>
                <button class="action-btn" onclick="chatApp.dislikeMessage(this)" title="Bad response">
                    <i class="fas fa-thumbs-down"></i>
                </button>
                <button class="action-btn" onclick="chatApp.retryMessage(this, '${userMessage ? userMessage.replace(/'/g, "\\'") : ''}')" title="Try again">
                    <i class="fas fa-redo"></i>
                </button>
            `;
            messageDiv.appendChild(actionsDiv);
        }
        chatContainer.appendChild(messageDiv);

        // Scroll to bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    formatMessage(content) {
        let formatted = content;

        // Handle code blocks first (before other formatting)
        formatted = formatted.replace(/```([\s\S]*?)```/g, (match, code) => {
            const codeId = 'code-' + Math.random().toString(36).substr(2, 9);
            let cleanCode = code.trim();
            let language = 'python'; // default
            
            // Detect language from first line
            const lines = cleanCode.split('\n');
            if (lines[0]) {
                const firstLine = lines[0].trim().toLowerCase();
                if (['python', 'py'].includes(firstLine)) {
                    language = 'python';
                    lines.shift();
                } else if (['javascript', 'js', 'node'].includes(firstLine)) {
                    language = 'javascript';
                    lines.shift();
                } else if (['java'].includes(firstLine)) {
                    language = 'java';
                    lines.shift();
                } else if (['cpp', 'c++'].includes(firstLine)) {
                    language = 'cpp';
                    lines.shift();
                } else if (['c'].includes(firstLine)) {
                    language = 'c';
                    lines.shift();
                } else if (['html'].includes(firstLine)) {
                    language = 'html';
                    lines.shift();
                } else if (['css'].includes(firstLine)) {
                    language = 'css';
                    lines.shift();
                }
                cleanCode = lines.join('\n').trim();
            }
            
            // Store original code for execution, escape for display
            const escapedCode = cleanCode
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;');
            
            return `<div class="code-block" data-code="${encodeURIComponent(cleanCode)}" data-language="${language}">
                <div class="code-actions">
                    <button class="code-run-btn" onclick="chatApp.runCodeInteractive('${codeId}')" title="Run code">
                        <i class="fas fa-play"></i>
                    </button>
                    <button class="code-copy-btn" onclick="chatApp.copyCode('${codeId}')" title="Copy code">
                        <i class="fas fa-copy"></i>
                    </button>
                </div>
                <pre><code id="${codeId}">${escapedCode}</code></pre>
            </div>`;
        });

        // Handle inline code
        formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Basic markdown-like formatting
        formatted = formatted
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');

        return formatted;
    }

    showTypingIndicator() {
        const chatContainer = document.getElementById('chatContainer');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant';
        typingDiv.id = 'typingIndicator';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';

        const typingContent = document.createElement('div');
        typingContent.className = 'typing-indicator';
        typingContent.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

        typingDiv.appendChild(avatar);
        typingDiv.appendChild(typingContent);
        chatContainer.appendChild(typingDiv);

        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    setStatus(text, type) {
        const statusText = document.getElementById('statusText');
        const statusDot = document.getElementById('statusDot');
        
        statusText.textContent = text;
        
        statusDot.className = 'status-dot';
        if (type === 'loading') {
            statusDot.style.background = '#ffa500';
        } else if (type === 'error') {
            statusDot.style.background = '#ff4444';
        } else if (type === 'success') {
            statusDot.style.background = '#10a37f';
        } else {
            statusDot.style.background = '#10a37f';
        }
    }

    async loadChatHistory() {
        try {
            const response = await fetch('http://localhost:5000/all-chats');
            const chats = await response.json();
            this.displayChatHistory(chats);
        } catch (error) {
            console.error('Failed to load chat history:', error);
        }
    }

    displayChatHistory(chats) {
        const chatList = document.getElementById('chatHistoryList');
        chatList.innerHTML = '';
        
        chats.forEach(chat => {
            const chatItem = document.createElement('div');
            chatItem.className = 'chat-item';
            chatItem.onclick = () => {
                this.loadChat(chat.chat_id);
                if (window.setCurrentChatId) {
                    window.setCurrentChatId(chat.chat_id);
                }
            };
            
            const date = new Date(chat.created_at).toLocaleDateString();
            const preview = chat.first_message || 'New Chat';
            chatItem.innerHTML = `
                <div class="chat-date">${date} • ${chat.message_count} msgs</div>
                <div class="chat-preview">${preview}</div>
            `;
            
            chatList.appendChild(chatItem);
        });
    }

    async loadChat(chatId) {
        try {
            const response = await fetch(`http://localhost:5000/chat-history/${chatId}`);
            const chatData = await response.json();
            
            const chatContainer = document.getElementById('chatContainer');
            chatContainer.innerHTML = '';
            
            chatData.messages.forEach(msg => {
                this.addMessage(msg.user_message, 'user');
                this.addMessage(msg.ai_response, 'assistant');
            });
            
            // Update active chat
            document.querySelectorAll('.chat-item').forEach(item => {
                item.classList.remove('active');
            });
            event.target.closest('.chat-item').classList.add('active');
            
        } catch (error) {
            console.error('Failed to load chat:', error);
        }
    }

    async createNewChat() {
        try {
            const response = await fetch('http://localhost:5000/new-chat', { method: 'POST' });
            const result = await response.json();
            
            this.newChat();
            this.loadChatHistory();
            if (window.setCurrentChatId) {
                window.setCurrentChatId(result.chat_id);
            }
            
        } catch (error) {
            console.error('Failed to create new chat:', error);
            this.newChat();
            if (window.setCurrentChatId) {
                window.setCurrentChatId(null);
            }
        }
    }


    copyMessage(button) {
        const messageContent = button.closest('.message').querySelector('.message-content');
        const text = messageContent.textContent.replace(/\s+/g, ' ').trim();
        navigator.clipboard.writeText(text).then(() => {
            const originalHTML = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i>';
            button.style.color = '#10a37f';
            setTimeout(() => {
                button.innerHTML = originalHTML;
                button.style.color = '';
            }, 1500);
        }).catch(err => {
            console.error('Failed to copy message:', err);
            button.innerHTML = '<i class="fas fa-times"></i>';
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-copy"></i>';
            }, 1500);
        });
    }
    
    copyCode(codeId) {
        const codeElement = document.getElementById(codeId);
        const text = codeElement.textContent;
        navigator.clipboard.writeText(text).then(() => {
            // Find the copy button
            const button = codeElement.closest('.code-block').querySelector('.code-copy-btn');
            const originalHTML = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i>';
            button.style.color = '#10a37f';
            setTimeout(() => {
                button.innerHTML = originalHTML;
                button.style.color = '';
            }, 1500);
        }).catch(err => {
            console.error('Failed to copy code:', err);
        });
    }
    
    async runCode(codeId) {
        const codeElement = document.getElementById(codeId);
        const codeBlock = codeElement.closest('.code-block');
        const code = decodeURIComponent(codeBlock.dataset.code);
        const language = codeBlock.dataset.language || 'python';
        const button = codeBlock.querySelector('.code-run-btn');
        
        // Show running state
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        button.disabled = true;
        
        try {
            const response = await fetch('http://localhost:5000/run-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code, language: language })
            });
            
            const result = await response.json();
            
            // Add output below code block
            let outputDiv = codeBlock.querySelector('.code-output');
            if (!outputDiv) {
                outputDiv = document.createElement('div');
                outputDiv.className = 'code-output';
                codeBlock.appendChild(outputDiv);
            }
            
            if (result.success) {
                outputDiv.innerHTML = `<div class="output-header">${language.toUpperCase()} Output:</div><pre>${result.output}</pre>`;
            } else {
                outputDiv.innerHTML = `<div class="output-header error">${language.toUpperCase()} Error:</div><pre>${result.error}</pre>`;
            }
            
        } catch (error) {
            console.error('Failed to run code:', error);
        } finally {
            // Restore button
            button.innerHTML = originalHTML;
            button.disabled = false;
        }
    }
    
    async runCodeInteractive(codeId) {
        const codeElement = document.getElementById(codeId);
        const codeBlock = codeElement.closest('.code-block');
        const code = decodeURIComponent(codeBlock.dataset.code);
        const language = codeBlock.dataset.language || 'python';
        
        // Create interactive terminal
        let outputDiv = codeBlock.querySelector('.code-output');
        if (!outputDiv) {
            outputDiv = document.createElement('div');
            outputDiv.className = 'code-output';
            codeBlock.appendChild(outputDiv);
        }
        
        outputDiv.innerHTML = `
            <div class="output-header">${language.toUpperCase()} Output:</div>
            <div class="terminal">
                <div class="terminal-output" id="terminal-${codeId}"></div>
                <div class="terminal-input" id="input-area-${codeId}">
                    <input type="text" class="terminal-input-field" id="input-${codeId}" placeholder="Enter value and press Enter">
                    <button onclick="chatApp.sendInput('${codeId}')" class="terminal-send">Send</button>
                </div>
            </div>
        `;
        
        // Start code execution
        this.executeInteractive(codeId, code, language);
    }
    
    async executeInteractive(codeId, code, language) {
        const terminalOutput = document.getElementById(`terminal-${codeId}`);
        const inputField = document.getElementById(`input-${codeId}`);
        
        try {
            const response = await fetch('http://localhost:5000/run-interactive', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code, language: language, session_id: codeId })
            });
            
            const result = await response.json();
            
            if (result.waiting_for_input) {
                terminalOutput.innerHTML += `<div class="terminal-line">${result.output}</div>`;
                inputField.focus();
                inputField.dataset.sessionId = codeId;
            } else if (result.success) {
                terminalOutput.innerHTML += `<div class="terminal-line">${result.output}</div>`;
                inputField.style.display = 'none';
            } else {
                terminalOutput.innerHTML += `<div class="terminal-line error">${result.error}</div>`;
                inputField.style.display = 'none';
            }
            
        } catch (error) {
            terminalOutput.innerHTML += `<div class="terminal-line error">Connection error</div>`;
        }
    }
    
    async sendInput(codeId) {
        const inputField = document.getElementById(`input-${codeId}`);
        const terminalOutput = document.getElementById(`terminal-${codeId}`);
        const userInput = inputField.value;
        
        if (!userInput) return;
        
        // Show user input
        terminalOutput.innerHTML += `<div class="terminal-line user-input">${userInput}</div>`;
        inputField.value = '';
        
        try {
            const response = await fetch('http://localhost:5000/send-input', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ session_id: codeId, input: userInput })
            });
            
            const result = await response.json();
            
            if (result.waiting_for_input) {
                terminalOutput.innerHTML += `<div class="terminal-line">${result.output}</div>`;
                inputField.focus();
            } else {
                terminalOutput.innerHTML += `<div class="terminal-line">${result.output}</div>`;
                document.querySelector(`#input-area-${codeId}`).style.display = 'none';
            }
            
        } catch (error) {
            terminalOutput.innerHTML += `<div class="terminal-line error">Connection error</div>`;
        }
    }
    
    likeMessage(button) {
        button.classList.toggle('liked');
        button.closest('.message-actions').querySelector('.action-btn:nth-child(3)').classList.remove('disliked');
    }
    
    dislikeMessage(button) {
        button.classList.toggle('disliked');
        button.closest('.message-actions').querySelector('.action-btn:nth-child(2)').classList.remove('liked');
    }
    
    retryMessage(button, userMessage) {
        if (userMessage) {
            document.getElementById('messageInput').value = userMessage;
            this.sendMessage();
        }
    }

    newChat() {
        const chatContainer = document.getElementById('chatContainer');
        chatContainer.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">
                    <i class="fas fa-robot"></i>
                </div>
                <h2>Welcome to AI Assistant</h2>
                <p>Ask me anything or upload a file to analyze!</p>
                <div class="example-prompts">
                    <button class="example-btn" onclick="sendExample('Explain quantum computing')">
                        Explain quantum computing
                    </button>
                    <button class="example-btn" onclick="sendExample('Write a Python function')">
                        Write a Python function
                    </button>
                    <button class="example-btn" onclick="sendExample('Summarize this document')">
                        Summarize this document
                    </button>
                </div>
            </div>
        `;
        this.removeFile();
        this.setStatus('Ready', 'ready');
    }
    
    handleAutoComplete(text) {
        clearTimeout(this.autoCompleteTimeout);
        
        if (text.length < 2) {
            this.hideAutoComplete();
            return;
        }
        
        this.autoCompleteTimeout = setTimeout(() => {
            this.showAutoComplete(text);
        }, 300);
    }
    
    showAutoComplete(text) {
        const suggestions = this.generateSuggestions(text);
        
        if (suggestions.length === 0) {
            this.hideAutoComplete();
            return;
        }
        
        this.suggestions = suggestions;
        this.selectedSuggestionIndex = -1;
        
        const dropdown = document.getElementById('autoCompleteDropdown');
        dropdown.innerHTML = suggestions.map((suggestion, index) => 
            `<div class="autocomplete-item" data-index="${index}">${suggestion}</div>`
        ).join('');
        
        // Add click handlers
        dropdown.querySelectorAll('.autocomplete-item').forEach((item, index) => {
            item.addEventListener('click', () => this.selectSuggestion(index));
        });
        
        dropdown.style.display = 'block';
    }
    
    hideAutoComplete() {
        document.getElementById('autoCompleteDropdown').style.display = 'none';
        this.selectedSuggestionIndex = -1;
    }
    
    generateSuggestions(text) {
        const commonPrompts = [
            'Write a Python function to',
            'Explain how to',
            'What is the difference between',
            'How do I implement',
            'Create a JavaScript function that',
            'Write code to',
            'Help me debug this',
            'Optimize this code',
            'Convert this to',
            'Translate this text to',
            'Summarize the following',
            'Generate a list of',
            'Compare and contrast',
            'What are the benefits of',
            'How can I improve',
            'Show me an example of'
        ];
        
        return commonPrompts
            .filter(prompt => prompt.toLowerCase().includes(text.toLowerCase()))
            .slice(0, 5);
    }
    
    navigateSuggestions(direction) {
        if (this.suggestions.length === 0) return;
        
        const dropdown = document.getElementById('autoCompleteDropdown');
        if (dropdown.style.display === 'none') return;
        
        // Remove previous selection
        if (this.selectedSuggestionIndex >= 0) {
            dropdown.children[this.selectedSuggestionIndex].classList.remove('selected');
        }
        
        // Update index
        this.selectedSuggestionIndex += direction;
        
        if (this.selectedSuggestionIndex < 0) {
            this.selectedSuggestionIndex = this.suggestions.length - 1;
        } else if (this.selectedSuggestionIndex >= this.suggestions.length) {
            this.selectedSuggestionIndex = 0;
        }
        
        // Add new selection
        dropdown.children[this.selectedSuggestionIndex].classList.add('selected');
    }
    
    selectSuggestion(index) {
        if (index >= 0 && index < this.suggestions.length) {
            document.getElementById('messageInput').value = this.suggestions[index];
            this.hideAutoComplete();
            document.getElementById('messageInput').focus();
        }
    }
    
    async toggleVoiceChat() {
        try {
            // Use JARVIS listening function
            const result = await eel.chatbot_listen()();
            if (result && result.trim()) {
                // Add user message and send to chatbot
                this.addMessage(result, 'user');
                document.getElementById('messageInput').value = result;
                this.sendMessage();
            }
        } catch (error) {
            console.error('Voice input error:', error);
            this.setStatus('Voice input failed', 'error');
        }
    }
    
    startVoiceChat() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('Speech recognition not supported in this browser');
            return;
        }
        
        this.isVoiceChatActive = true;
        const voiceBtn = document.getElementById('voiceBtn');
        voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
        voiceBtn.title = 'Stop Voice Chat';
        voiceBtn.classList.add('voice-active');
        
        this.initSpeechRecognition();
        this.startListening();
        
        this.setStatus('Voice chat active - Say something', 'success');
    }
    
    stopVoiceChat() {
        this.isVoiceChatActive = false;
        this.isListening = false;
        
        if (this.recognition) {
            this.recognition.stop();
        }
        
        if (this.currentUtterance) {
            this.synthesis.cancel();
        }
        
        const voiceBtn = document.getElementById('voiceBtn');
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        voiceBtn.title = 'Start Voice Chat';
        voiceBtn.classList.remove('voice-active');
        
        this.setStatus('Voice chat stopped', 'ready');
    }
    
    initSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.setStatus('Listening...', 'loading');
        };
        
        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            if (finalTranscript) {
                this.handleVoiceInput(finalTranscript.trim());
            }
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            if (this.isVoiceChatActive) {
                setTimeout(() => this.startListening(), 1000);
            }
        };
        
        this.recognition.onend = () => {
            if (this.isVoiceChatActive && !this.isListening) {
                setTimeout(() => this.startListening(), 500);
            }
        };
    }
    
    startListening() {
        if (this.isVoiceChatActive && this.recognition) {
            try {
                this.recognition.start();
            } catch (e) {
                console.error('Recognition start error:', e);
            }
        }
    }
    
    handleVoiceInput(text) {
        if (!text || text.length < 2) return;
        
        // Stop current speech if speaking
        if (this.synthesis.speaking) {
            this.synthesis.cancel();
        }
        
        // Check for stop commands
        if (text.toLowerCase().includes('stop') || text.toLowerCase().includes('quiet')) {
            this.synthesis.cancel();
            this.setStatus('Listening...', 'loading');
            return;
        }
        
        this.setStatus('Processing voice input...', 'loading');
        
        // Add voice input to chat and send
        document.getElementById('messageInput').value = text;
        this.sendVoiceMessage(text);
    }
    
    async sendVoiceMessage(message) {
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Hide welcome message
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.display = 'none';
        }
        
        this.setStatus('AI is thinking...', 'loading');
        
        try {
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    provider: this.currentProvider,
                    model: this.currentModel
                })
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.addMessage(`Error: ${result.error}`, 'assistant');
                this.speakText('Sorry, there was an error processing your request.');
            } else {
                this.addMessage(result.response, 'assistant', message);
                this.speakText(result.response);
            }
            
        } catch (error) {
            this.addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
            this.speakText('Sorry, I encountered an error. Please try again.');
            console.error('Voice chat error:', error);
        }
        
        // Clear input
        document.getElementById('messageInput').value = '';
    }
    
    initVoices() {
        // Wait for voices to load
        const loadVoices = () => {
            const voices = this.synthesis.getVoices();
            this.listAvailableVoices(voices);
            this.selectBestVoice(voices);
        };
        
        if (this.synthesis.getVoices().length > 0) {
            loadVoices();
        } else {
            this.synthesis.onvoiceschanged = loadVoices;
        }
    }
    
    listAvailableVoices(voices) {
        console.log('🎤 Available Voices on Your System:');
        console.log('=====================================');
        
        const maleVoices = [];
        const femaleVoices = [];
        const otherVoices = [];
        
        voices.forEach(voice => {
            if (!voice.lang.startsWith('en')) return;
            
            const voiceInfo = `${voice.name} (${voice.lang})`;
            
            if (voice.name.toLowerCase().includes('male') ||
                voice.name.toLowerCase().includes('david') ||
                voice.name.toLowerCase().includes('alex') ||
                voice.name.toLowerCase().includes('daniel') ||
                voice.name.toLowerCase().includes('thomas') ||
                voice.name.toLowerCase().includes('mark')) {
                maleVoices.push(voiceInfo);
            } else if (voice.name.toLowerCase().includes('female') ||
                       voice.name.toLowerCase().includes('samantha') ||
                       voice.name.toLowerCase().includes('victoria') ||
                       voice.name.toLowerCase().includes('susan') ||
                       voice.name.toLowerCase().includes('zira')) {
                femaleVoices.push(voiceInfo);
            } else {
                otherVoices.push(voiceInfo);
            }
        });
        
        console.log('👨 MALE VOICES:');
        maleVoices.forEach(voice => console.log('  ✓', voice));
        if (maleVoices.length === 0) console.log('  ❌ No specific male voices found');
        
        console.log('\n👩 FEMALE VOICES:');
        femaleVoices.forEach(voice => console.log('  ✓', voice));
        if (femaleVoices.length === 0) console.log('  ❌ No specific female voices found');
        
        console.log('\n🔊 OTHER ENGLISH VOICES:');
        otherVoices.forEach(voice => console.log('  •', voice));
        
        console.log('\n💡 Open browser console (F12) to see this list');
    }
    
    selectBestVoice(voices) {
        this.allVoices = voices;
        
        // Set default voices based on your available voices
        this.maleVoice = voices.find(v => v.name === 'Microsoft David English (United States)') || 
                        voices.find(v => v.name.includes('David'));
        this.femaleVoice = voices.find(v => v.name === 'Microsoft Zira English (United States)') || 
                          voices.find(v => v.name.includes('Zira'));
        
        // Set current voice
        this.selectedVoice = this.voiceGender === 'male' ? this.maleVoice : this.femaleVoice;
    }
    
    selectVoice(voiceName) {
        // Find voice by name matching
        if (voiceName.includes('David')) {
            this.selectedVoice = this.allVoices.find(v => v.name.includes('David'));
        } else if (voiceName.includes('Mark')) {
            this.selectedVoice = this.allVoices.find(v => v.name.includes('Mark'));
        } else if (voiceName.includes('Ravi')) {
            this.selectedVoice = this.allVoices.find(v => v.name.includes('Ravi'));
        } else if (voiceName.includes('Zira')) {
            this.selectedVoice = this.allVoices.find(v => v.name.includes('Zira'));
        } else if (voiceName.includes('Heera')) {
            this.selectedVoice = this.allVoices.find(v => v.name.includes('Heera'));
        } else if (voiceName.includes('Google UK English Male')) {
            this.selectedVoice = this.allVoices.find(v => v.name.includes('Google UK English Male'));
        } else if (voiceName.includes('Google UK English Female')) {
            this.selectedVoice = this.allVoices.find(v => v.name.includes('Google UK English Female'));
        }
        
        this.speakText('Voice selected');
    }
    
    showSpeedControl() {
        const currentSpeed = this.speechRate;
        const speedName = this.getSpeedName(currentSpeed);
        
        const popup = document.createElement('div');
        popup.className = 'speed-popup';
        popup.innerHTML = `
            <div class="speed-popup-content">
                <h4>🏃♂️ Speech Speed</h4>
                <div class="speed-slider-container">
                    <label>Speed: <span id="speedValue">${speedName}</span></label>
                    <input type="range" id="speedSlider" min="0.5" max="2.0" step="0.1" value="${currentSpeed}">
                    <div class="speed-presets">
                        <button onclick="chatApp.setSpeed(0.5)">Very Slow</button>
                        <button onclick="chatApp.setSpeed(0.75)">Slow</button>
                        <button onclick="chatApp.setSpeed(0.85)">Normal</button>
                        <button onclick="chatApp.setSpeed(1.0)">Fast</button>
                        <button onclick="chatApp.setSpeed(1.25)">Very Fast</button>
                        <button onclick="chatApp.setSpeed(1.5)">Rapid</button>
                    </div>
                </div>
                <div class="speed-actions">
                    <button onclick="chatApp.testSpeed()">🔊 Test</button>
                    <button onclick="chatApp.closeSpeedControl()">Close</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(popup);
        
        // Add slider event listener
        const slider = document.getElementById('speedSlider');
        slider.addEventListener('input', (e) => {
            this.speechRate = parseFloat(e.target.value);
            document.getElementById('speedValue').textContent = this.getSpeedName(this.speechRate);
        });
    }
    
    getSpeedName(speed) {
        if (speed <= 0.6) return 'Very Slow';
        if (speed <= 0.8) return 'Slow';
        if (speed <= 0.9) return 'Normal';
        if (speed <= 1.1) return 'Fast';
        if (speed <= 1.3) return 'Very Fast';
        return 'Rapid';
    }
    
    setSpeed(speed) {
        this.speechRate = speed;
        const slider = document.getElementById('speedSlider');
        if (slider) {
            slider.value = speed;
            document.getElementById('speedValue').textContent = this.getSpeedName(speed);
        }
    }
    
    testSpeed() {
        this.speakText(`Testing speech speed at ${this.getSpeedName(this.speechRate)}`);
    }
    
    closeSpeedControl() {
        const popup = document.querySelector('.speed-popup');
        if (popup) {
            popup.remove();
        }
    }
    
    toggleVoiceGender() {
        this.voiceGender = this.voiceGender === 'male' ? 'female' : 'male';
        this.selectedVoice = this.voiceGender === 'male' ? this.maleVoice : this.femaleVoice;
        
        const btn = document.getElementById('voiceGenderBtn');
        btn.innerHTML = this.voiceGender === 'male' ? '<i class="fas fa-mars"></i>' : '<i class="fas fa-venus"></i>';
        btn.title = `Voice: ${this.voiceGender === 'male' ? 'Male' : 'Female'}`;
        
        // Test the voice
        if (this.selectedVoice) {
            this.speakText('Voice changed to ' + this.voiceGender);
        }
    }
    
    speakResponse(text) {
        // Only speak if microphone is active
        console.log('Checking if should speak:', window.isListening);
        if (window.isListening) {
            console.log('Speaking response:', text.substring(0, 50) + '...');
            this.speakText(text, true);
        } else {
            console.log('Not speaking - microphone not active');
        }
    }
    
    speakText(text, forceSpeak = false) {
        // Allow speaking for voice tests, voice chat, and forced responses
        const isTest = text.includes('Testing speech') || text.includes('Voice selected') || text.includes('Speed set to');
        if (!this.isVoiceChatActive && !isTest && !forceSpeak) return;
        
        // Clean text for speech
        let cleanText = text.replace(/[*#`]/g, '').replace(/\n/g, ' ').replace(/```[\s\S]*?```/g, 'code block');
        
        // Cancel any current speech
        if (this.synthesis.speaking) {
            this.synthesis.cancel();
        }
        
        this.currentUtterance = new SpeechSynthesisUtterance(cleanText);
        
        // Use selected voice for natural speech
        if (this.selectedVoice) {
            this.currentUtterance.voice = this.selectedVoice;
        }
        
        // Apply current speech settings
        this.currentUtterance.rate = this.speechRate || 0.85;
        this.currentUtterance.pitch = 1.0;
        this.currentUtterance.volume = 0.9;
        
        console.log(`Speaking: "${cleanText}" at rate ${this.currentUtterance.rate}`);
        
        this.currentUtterance.onstart = () => {
            if (this.isVoiceChatActive) {
                this.setStatus('AI is speaking...', 'success');
                this.isListening = false;
                if (this.recognition) {
                    this.recognition.stop();
                }
            }
        };
        
        this.currentUtterance.onend = () => {
            this.currentUtterance = null;
            window.lastSpeechEnd = Date.now();
            if (this.isVoiceChatActive) {
                this.setStatus('Listening...', 'loading');
                setTimeout(() => this.startListening(), 500);
            }
        };
        
        this.currentUtterance.onerror = (e) => {
            console.error('Speech error:', e);
            this.currentUtterance = null;
            if (this.isVoiceChatActive) {
                setTimeout(() => this.startListening(), 500);
            }
        };
        
        this.synthesis.speak(this.currentUtterance);
    }
    
    showVoicesModal() {
        const voices = this.synthesis.getVoices();
        const maleVoices = [];
        const femaleVoices = [];
        const otherVoices = [];
        
        voices.forEach(voice => {
            if (!voice.lang.startsWith('en')) return;
            
            const voiceInfo = { name: voice.name, lang: voice.lang };
            
            if (voice.name.toLowerCase().includes('male') ||
                voice.name.toLowerCase().includes('david') ||
                voice.name.toLowerCase().includes('alex') ||
                voice.name.toLowerCase().includes('daniel') ||
                voice.name.toLowerCase().includes('thomas') ||
                voice.name.toLowerCase().includes('mark')) {
                maleVoices.push(voiceInfo);
            } else if (voice.name.toLowerCase().includes('female') ||
                       voice.name.toLowerCase().includes('samantha') ||
                       voice.name.toLowerCase().includes('victoria') ||
                       voice.name.toLowerCase().includes('susan') ||
                       voice.name.toLowerCase().includes('zira')) {
                femaleVoices.push(voiceInfo);
            } else {
                otherVoices.push(voiceInfo);
            }
        });
        
        let modalContent = `
            <div class="modal" id="voicesModal" style="display: block;">
                <div class="modal-content">
                    <h3>🎤 Available Voices on Your System</h3>
                    
                    <div style="text-align: left; margin: 20px 0;">
                        <h4>👨 Male Voices:</h4>
                        ${maleVoices.length > 0 ? 
                            maleVoices.map(v => `<div style="margin: 5px 0; color: #10a37f;">✓ ${v.name} (${v.lang})</div>`).join('') :
                            '<div style="color: #ff4444;">❌ No specific male voices found</div>'
                        }
                        
                        <h4 style="margin-top: 15px;">👩 Female Voices:</h4>
                        ${femaleVoices.length > 0 ? 
                            femaleVoices.map(v => `<div style="margin: 5px 0; color: #10a37f;">✓ ${v.name} (${v.lang})</div>`).join('') :
                            '<div style="color: #ff4444;">❌ No specific female voices found</div>'
                        }
                        
                        <h4 style="margin-top: 15px;">🔊 Other English Voices:</h4>
                        ${otherVoices.map(v => `<div style="margin: 5px 0; color: #ccc;">• ${v.name} (${v.lang})</div>`).join('')}
                    </div>
                    
                    <p style="font-size: 12px; color: #888; margin-top: 20px;">
                        💡 The system automatically selects the best available voice for each gender.
                    </p>
                    
                    <button onclick="document.getElementById('voicesModal').remove()" class="close-btn">Close</button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalContent);
    }

}

// Initialize the app
const chatApp = new ChatApp();

// Global function for example buttons
function sendExample(text) {
    document.getElementById('messageInput').value = text;
    chatApp.sendMessage();
}