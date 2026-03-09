// State Management
let currentSessionId = null;
let currentLanguage = 'auto';
let currentCode = '';
let reviewResults = null;

// DOM Elements
const themeToggle = document.getElementById('themeToggle');
const codeEditor = document.getElementById('codeEditor');
const languageSelect = document.getElementById('languageSelect');
const fileInput = document.getElementById('fileInput');
const reviewBtn = document.getElementById('reviewBtn');
const chatBtn = document.getElementById('chatBtn');
const sendChatBtn = document.getElementById('sendChatBtn');
const chatInput = document.getElementById('chatInput');
const loadingOverlay = document.getElementById('loadingOverlay');
const toast = document.getElementById('toast');
const sampleBtn = document.getElementById('sampleBtn');
const clearBtn = document.getElementById('clearBtn');
const exportBtn = document.getElementById('exportBtn');

// Sample Codes
const SAMPLES = {
    python: `def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def main():
    number = 10
    result = calculate_fibonacci(number)
    print(f"Fibonacci of {number} is: {result}")

if __name__ == "__main__":
    main()`,

    javascript: `function factorial(n) {
    if (n === 0 || n === 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

function main() {
    const num = 5;
    const result = factorial(num);
    console.log(\`Factorial of \${num} is: \${result}\`);
}

main();`,

    typescript: `interface User {
    id: number;
    name: string;
    email: string;
}

class UserService {
    private users: User[] = [];
    
    addUser(user: User): void {
        this.users.push(user);
    }
    
    getUserById(id: number): User | undefined {
        return this.users.find(user => user.id === id);
    }
}

const service = new UserService();
service.addUser({ id: 1, name: "John", email: "john@example.com" });`
};

// Check if elements exist
console.log('DOM Elements loaded:', {
    themeToggle: !!themeToggle,
    codeEditor: !!codeEditor,
    languageSelect: !!languageSelect,
    reviewBtn: !!reviewBtn,
    chatBtn: !!chatBtn
});

// Test API connection on load
async function testAPIConnection() {
    try {
        console.log('Testing API connection...');
        const response = await fetch('/api/languages');
        const data = await response.json();
        console.log('API connection successful:', data);
        showToast('Connected to backend successfully!', 'success');
    } catch (error) {
        console.error('API connection failed:', error);
        showToast('Cannot connect to backend. Make sure Flask is running!', 'error');
    }
}

// Run API test when page loads
window.addEventListener('load', testAPIConnection);

// Theme Toggle
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        const icon = themeToggle.querySelector('i');
        if (document.body.classList.contains('dark-theme')) {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    });
}

// Code Editor Stats
if (codeEditor) {
    codeEditor.addEventListener('input', () => {
        currentCode = codeEditor.value;
        updateEditorStats();
    });
}

function updateEditorStats() {
    if (!codeEditor) return;
    const lines = codeEditor.value.split('\n').length;
    const chars = codeEditor.value.length;
    const lineCountEl = document.getElementById('lineCount');
    const charCountEl = document.getElementById('charCount');
    if (lineCountEl) lineCountEl.textContent = `Lines: ${lines}`;
    if (charCountEl) charCountEl.textContent = `Chars: ${chars}`;
}

// File Upload
if (fileInput) {
    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            codeEditor.value = e.target.result;
            currentCode = e.target.result;
            updateEditorStats();
            showToast(`File "${file.name}" loaded successfully!`, 'success');
            
            // Auto-detect language from file extension
            const ext = file.name.split('.').pop().toLowerCase();
            const langMap = {
                'py': 'python',
                'js': 'javascript',
                'ts': 'typescript'
            };
            if (langMap[ext] && languageSelect) {
                languageSelect.value = langMap[ext];
            }
        };
        reader.readAsText(file);
    });
}

// Sample Code Loader
if (sampleBtn) {
    sampleBtn.addEventListener('click', () => {
        const selectedLang = languageSelect ? (languageSelect.value === 'auto' ? 'python' : languageSelect.value) : 'python';
        if (SAMPLES[selectedLang] && codeEditor) {
            codeEditor.value = SAMPLES[selectedLang];
            currentCode = SAMPLES[selectedLang];
            updateEditorStats();
            showToast(`Sample ${selectedLang} code loaded!`, 'success');
        } else if (codeEditor) {
            codeEditor.value = SAMPLES.python;
            currentCode = SAMPLES.python;
            updateEditorStats();
        }
    });
}

// Clear Button
if (clearBtn) {
    clearBtn.addEventListener('click', () => {
        if (codeEditor) {
            codeEditor.value = '';
            currentCode = '';
            updateEditorStats();
            resetResults();
            showToast('Editor cleared', 'success');
        }
    });
}

// Review Button
if (reviewBtn) {
    reviewBtn.addEventListener('click', async () => {
        if (!currentCode || !currentCode.trim()) {
            showToast('Please enter some code to review', 'error');
            return;
        }
        await reviewCode();
    });
}

// Review Code Function
async function reviewCode() {
    if (!currentCode || !currentCode.trim()) {
        showToast('No code to review', 'error');
        return;
    }
    
    loadingOverlay.classList.add('active');
    console.log('Sending review request...');
    
    try {
        const requestData = {
            code: currentCode,
            language: languageSelect ? languageSelect.value : 'auto',
            filename: fileInput && fileInput.files[0] ? fileInput.files[0].name : '',
            session_id: currentSessionId
        };
        
        console.log('Request data:', requestData);
        
        const response = await fetch('/api/review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        console.log('Response status:', response.status);
        
        const data = await response.json();
        console.log('Response data:', data);
        
        if (data.success) {
            reviewResults = data.review;
            currentSessionId = data.session_id;
            currentLanguage = data.language;
            
            // Update UI with results
            updateResultsUI(data.review);
            showToast('Code review completed!', 'success');
            
            // Enable export button
            if (exportBtn) exportBtn.disabled = false;
        } else {
            showToast(data.error || 'Review failed', 'error');
        }
    } catch (error) {
        console.error('Review error:', error);
        showToast('Failed to connect to server. Make sure Flask is running!', 'error');
    } finally {
        loadingOverlay.classList.remove('active');
    }
}

// Update Results UI
function updateResultsUI(review) {
    console.log('Updating UI with review:', review);
    
    // Update language badge
    const langBadge = document.getElementById('languageBadge');
    if (langBadge) langBadge.textContent = `Language: ${review.language || 'Unknown'}`;
    
    // Update summary
    const summaryEl = document.getElementById('summaryText');
    if (summaryEl) summaryEl.textContent = review.summary || 'No summary available';
    
    // Update stats
    const bugCount = review.bugs?.length || 0;
    const securityCount = review.security?.length || 0;
    const qualityCount = review.code_quality?.length || 0;
    const totalIssues = bugCount + securityCount + qualityCount;
    
    const statBugs = document.getElementById('statBugs');
    const statSecurity = document.getElementById('statSecurity');
    const statQuality = document.getElementById('statQuality');
    const statComplexity = document.getElementById('statComplexity');
    
    if (statBugs) statBugs.textContent = bugCount;
    if (statSecurity) statSecurity.textContent = securityCount;
    if (statQuality) statQuality.textContent = totalIssues;
    if (statComplexity) statComplexity.textContent = review.metrics?.function_count || 0;
    
    // Update badges in tabs
    const bugCountBadge = document.getElementById('bugCount');
    const securityCountBadge = document.getElementById('securityCount');
    const qualityCountBadge = document.getElementById('qualityCount');
    
    if (bugCountBadge) bugCountBadge.textContent = bugCount;
    if (securityCountBadge) securityCountBadge.textContent = securityCount;
    if (qualityCountBadge) qualityCountBadge.textContent = totalIssues;
    
    // Calculate health score
    const healthScore = Math.max(0, 100 - (totalIssues * 5));
    const healthScoreEl = document.getElementById('healthScore');
    const healthMeterEl = document.getElementById('healthMeter');
    
    if (healthScoreEl) healthScoreEl.textContent = `${healthScore}%`;
    if (healthMeterEl) healthMeterEl.style.width = `${healthScore}%`;
    
    // Update issues lists
    displayIssues('bugsList', review.bugs || [], 'bug');
    displayIssues('securityList', review.security || [], 'security');
    displayIssues('qualityList', review.code_quality || [], 'quality');
    
    // Update improved code
    const improvedCodeEl = document.getElementById('improvedCode');
    if (improvedCodeEl && review.improved_code) {
        improvedCodeEl.textContent = review.improved_code;
    }
}

function displayIssues(elementId, issues, type) {
    const container = document.getElementById(elementId);
    if (!container) return;
    
    if (!issues || issues.length === 0) {
        container.innerHTML = '<div class="empty-state">No issues detected</div>';
        return;
    }
    
    container.innerHTML = issues.map(issue => {
        const description = typeof issue === 'string' ? issue : issue.description || '';
        const severity = issue.severity || 'medium';
        const line = issue.line || 'N/A';
        
        return `
            <div class="issue-item ${severity}">
                <div class="issue-header">
                    <span class="issue-severity ${severity}">${severity}</span>
                    <span class="issue-line">Line: ${line}</span>
                </div>
                <div class="issue-description">${description}</div>
            </div>
        `;
    }).join('');
}

// Tab Switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
        
        btn.classList.add('active');
        
        const tabName = btn.dataset.tab;
        const tabEl = document.getElementById(`${tabName}Tab`);
        if (tabEl) tabEl.classList.add('active');
    });
});

// Copy Improved Code
window.copyImprovedCode = function() {
    const codeEl = document.getElementById('improvedCode');
    if (!codeEl) return;
    
    const code = codeEl.textContent;
    navigator.clipboard.writeText(code).then(() => {
        showToast('Code copied to clipboard!', 'success');
    });
};

// Export Results
if (exportBtn) {
    exportBtn.addEventListener('click', () => {
        if (!reviewResults) return;
        
        const dataStr = JSON.stringify(reviewResults, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        
        const exportFileDefaultName = `code-review-${new Date().toISOString()}.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
        
        showToast('Results exported successfully!', 'success');
    });
}

// Toast Notification
function showToast(message, type = 'info') {
    if (!toast) return;
    
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Reset Results
function resetResults() {
    reviewResults = null;
    if (exportBtn) exportBtn.disabled = true;
    
    const summaryEl = document.getElementById('summaryText');
    const healthScoreEl = document.getElementById('healthScore');
    const healthMeterEl = document.getElementById('healthMeter');
    const statBugs = document.getElementById('statBugs');
    const statSecurity = document.getElementById('statSecurity');
    const statQuality = document.getElementById('statQuality');
    const bugCount = document.getElementById('bugCount');
    const securityCount = document.getElementById('securityCount');
    const qualityCount = document.getElementById('qualityCount');
    const improvedCode = document.getElementById('improvedCode');
    
    if (summaryEl) summaryEl.textContent = 'No code reviewed yet. Paste your code and click "Review Code" to get started.';
    if (healthScoreEl) healthScoreEl.textContent = '0%';
    if (healthMeterEl) healthMeterEl.style.width = '0%';
    if (statBugs) statBugs.textContent = '0';
    if (statSecurity) statSecurity.textContent = '0';
    if (statQuality) statQuality.textContent = '0';
    if (bugCount) bugCount.textContent = '0';
    if (securityCount) securityCount.textContent = '0';
    if (qualityCount) qualityCount.textContent = '0';
    if (improvedCode) improvedCode.textContent = '// Improved code will appear here';
    
    const bugsList = document.getElementById('bugsList');
    const securityList = document.getElementById('securityList');
    const qualityList = document.getElementById('qualityList');
    
    if (bugsList) bugsList.innerHTML = '<div class="empty-state">No bugs detected</div>';
    if (securityList) securityList.innerHTML = '<div class="empty-state">No security issues detected</div>';
    if (qualityList) qualityList.innerHTML = '<div class="empty-state">No quality issues detected</div>';
}

// Chat Functionality
if (chatBtn) {
    chatBtn.addEventListener('click', () => {
        // Switch to the chat tab
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
        
        const chatTabBtn = document.querySelector('.tab-btn[data-tab="chat"]');
        const chatTab = document.getElementById('chatTab');
        
        if (chatTabBtn) chatTabBtn.classList.add('active');
        if (chatTab) chatTab.classList.add('active');
    });
}

if (sendChatBtn) {
    sendChatBtn.addEventListener('click', sendChatMessage);
}

if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendChatMessage();
        }
    });
}

async function sendChatMessage() {
    if (!chatInput || !chatInput.value.trim()) return;
    
    const message = chatInput.value.trim();
    chatInput.value = '';
    
    // Add user message to UI
    appendChatMessage('user', message);
    
    // Show typing indicator
    const typingId = 'typing-' + Date.now();
    appendChatMessage('bot', '...', typingId);
    
    try {
        const requestData = {
            message: message,
            session_id: currentSessionId,
            code: currentCode,
            language: languageSelect ? languageSelect.value : 'auto'
        };
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();
        
        if (data.success) {
            currentSessionId = data.session_id; // Save session in case it was newly generated
            appendChatMessage('bot', data.response);
        } else {
            appendChatMessage('bot', 'Error: ' + (data.error || 'Failed to get response'));
        }
    } catch (error) {
        console.error('Chat error:', error);
        
        // Remove typing indicator
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();
        
        appendChatMessage('bot', 'Error: Could not connect to the server.');
    }
}

function appendChatMessage(role, content, id = null) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${role}`;
    if (id) msgDiv.id = id;
    
    // Format content: convert code blocks and newlines if it's the bot
    let displayContent = content;
    if (role === 'bot') {
        displayContent = content.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
        displayContent = displayContent.replace(/\n/g, '<br>');
    }
    
    msgDiv.innerHTML = `
        <div class="message-content">
            <i class="fas ${role === 'user' ? 'fa-user' : 'fa-robot'}"></i>
            <p>${displayContent}</p>
        </div>
    `;
    
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded');
    updateEditorStats();
    resetResults();
    
    // Check for dark mode preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.classList.add('dark-theme');
        if (themeToggle) {
            themeToggle.querySelector('i').className = 'fas fa-sun';
        }
    }
});

