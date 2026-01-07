// QuickHelp Web UI JavaScript

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs and contents
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab
        tab.classList.add('active');
        
        // Show corresponding content
        const tabName = tab.dataset.tab;
        document.getElementById(tabName + 'Tab').classList.add('active');
        
        // Load clusters when switching to clusters tab
        if (tabName === 'cluster') {
            loadClusters();
        }
    });
});

// Load stats on page load
window.addEventListener('load', () => {
    loadStats();
});

// Load saved clusters
async function loadClusters() {
    const resultsDiv = document.getElementById('clusterResults');
    
    try {
        const response = await fetch('/api/clusters');
        const data = await response.json();
        
        if (data.success && data.clusters && data.clusters.length > 0) {
            displayClusters(data.clusters, resultsDiv);
        } else {
            showMessage(resultsDiv, data.message || 'No clusters available. Click "Run Clustering" to generate.', 'info');
        }
    } catch (error) {
        console.error('Error loading clusters:', error);
    }
}

// Enter key handlers
document.getElementById('searchQuery')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
});

// API Functions
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (data.success && data.stats) {
            document.getElementById('docCount').textContent = data.stats.total_documents;
            document.getElementById('wordCount').textContent = data.stats.total_words.toLocaleString();
            document.getElementById('tagCount').textContent = data.stats.unique_tags;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function performSearch() {
    const query = document.getElementById('searchQuery').value.trim();
    const mode = document.getElementById('searchMode').value;
    const resultsDiv = document.getElementById('searchResults');
    
    if (!query) {
        showMessage(resultsDiv, 'Please enter a search query', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, mode, max_results: 10 })
        });
        
        const data = await response.json();
        
        showLoading(false);
        
        if (!data.success) {
            showMessage(resultsDiv, data.message || data.error, 'error');
            return;
        }
        
        if (data.results.length === 0) {
            showMessage(resultsDiv, 'No results found', 'info');
            return;
        }
        
        displaySearchResults(data.results, resultsDiv);
        
    } catch (error) {
        showLoading(false);
        showMessage(resultsDiv, 'Error performing search: ' + error.message, 'error');
    }
}

function displaySearchResults(results, container) {
    let html = `<h3>Found ${results.length} results:</h3>`;
    
    results.forEach((result, index) => {
        const tags = result.tags.map(tag => `<span class="tag">#${tag}</span>`).join('');
        
        html += `
            <div class="result-item">
                <div class="result-title">
                    ${index + 1}. ${result.title}
                    <span class="result-score">${result.score.toFixed(3)}</span>
                </div>
                <div class="result-content">${result.content}</div>
                <div class="result-meta">
                    <small>${result.path}</small><br>
                    ${tags}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

async function askQuestion() {
    const question = document.getElementById('questionInput').value.trim();
    const resultsDiv = document.getElementById('answerResult');
    
    if (!question) {
        showMessage(resultsDiv, 'Please enter a question', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question, mode: 'hybrid' })
        });
        
        const data = await response.json();
        
        showLoading(false);
        
        if (!data.success) {
            showMessage(resultsDiv, data.message || data.error, 'error');
            return;
        }
        
        displayAnswer(data, resultsDiv);
        
    } catch (error) {
        showLoading(false);
        showMessage(resultsDiv, 'Error asking question: ' + error.message, 'error');
    }
}

function displayAnswer(data, container) {
    let html = `
        <div class="answer-box">
            <h3>Answer:</h3>
            <div class="answer-text">${data.answer}</div>
        </div>
    `;
    
    if (data.sources && data.sources.length > 0) {
        html += '<div class="sources-section">';
        html += '<h3 class="sources-title">Sources:</h3>';
        
        data.sources.forEach(source => {
            const tags = source.tags ? source.tags.map(tag => `<span class="tag">#${tag}</span>`).join('') : '';
            
            html += `
                <div class="source-item">
                    <strong>[${source.id}] ${source.title}</strong>
                    <span class="result-score">${source.score.toFixed(3)}</span>
                    <br>
                    <small>${source.path}</small>
                    <br>
                    ${tags}
                </div>
            `;
        });
        
        html += '</div>';
    }
    
    container.innerHTML = html;
}

async function performClustering() {
    const algorithm = document.getElementById('clusterAlgorithm').value;
    const resultsDiv = document.getElementById('clusterResults');
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/cluster', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ algorithm })
        });
        
        const data = await response.json();
        
        showLoading(false);
        
        if (!data.success) {
            showMessage(resultsDiv, data.message || data.error, 'error');
            return;
        }
        
        displayClusters(data.clusters, resultsDiv);
        
    } catch (error) {
        showLoading(false);
        showMessage(resultsDiv, 'Error clustering: ' + error.message, 'error');
    }
}

function displayClusters(clusters, container) {
    let html = `<h3>Generated ${clusters.length} clusters:</h3>`;
    
    clusters.forEach(cluster => {
        const keywords = cluster.keywords.map(kw => `<span class="keyword">${kw}</span>`).join('');
        const tags = cluster.tags.map(tag => `<span class="tag">#${tag}</span>`).join('');
        
        html += `
            <div class="cluster-item">
                <div class="cluster-header">
                    <div class="cluster-name">${cluster.name}</div>
                    <div class="cluster-size">${cluster.size} documents</div>
                </div>
                
                ${keywords ? `<div class="cluster-keywords"><strong>Keywords:</strong> ${keywords}</div>` : ''}
                ${tags ? `<div><strong>Tags:</strong> ${tags}</div>` : ''}
                
                <div class="cluster-documents">
                    <strong>Sample Documents:</strong>
                    ${cluster.documents.map(doc => `
                        <div class="cluster-doc">• ${doc.title}</div>
                    `).join('')}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

async function indexDocuments() {
    const path = document.getElementById('docPath').value.trim();
    const resultsDiv = document.getElementById('indexResult');
    
    if (!path) {
        showMessage(resultsDiv, 'Please enter a document path', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/index', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path })
        });
        
        const data = await response.json();
        
        showLoading(false);
        
        if (!data.success) {
            showMessage(resultsDiv, data.message || data.error, 'error');
            return;
        }
        
        let html = `
            <div class="message message-success">
                <strong>✓ Success!</strong><br>
                ${data.message}
            </div>
        `;
        
        if (data.stats) {
            html += `
                <div class="result-item">
                    <h4>Statistics:</h4>
                    <ul style="margin-left: 20px; margin-top: 10px;">
                        <li>Total Documents: ${data.stats.total_documents}</li>
                        <li>Total Words: ${data.stats.total_words.toLocaleString()}</li>
                        <li>Average Words per Document: ${data.stats.avg_words_per_doc.toFixed(1)}</li>
                        <li>Unique Tags: ${data.stats.unique_tags}</li>
                        <li>Formats: ${data.stats.formats.join(', ')}</li>
                    </ul>
                </div>
            `;
        }
        
        resultsDiv.innerHTML = html;
        
        // Reload stats
        loadStats();
        
    } catch (error) {
        showLoading(false);
        showMessage(resultsDiv, 'Error indexing documents: ' + error.message, 'error');
    }
}

// Helper Functions
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.classList.remove('hidden');
    } else {
        overlay.classList.add('hidden');
    }
}

function showMessage(container, message, type) {
    const icon = type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ';
    container.innerHTML = `
        <div class="message message-${type}">
            <strong>${icon} ${type.charAt(0).toUpperCase() + type.slice(1)}</strong><br>
            ${message}
        </div>
    `;
}
