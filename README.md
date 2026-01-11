# QuickHelp - Intelligent Knowledge Base

> AI-powered knowledge management with hybrid search, auto-clustering, and intelligent Q&A using DeepSeek

## Quick Start

```bash
# Windows
run_web.bat

# Linux/Mac
python app.py
```

Then open: **http://127.0.0.1:5000**

## Features

- **Hybrid Search** - Combines keyword + semantic search for best results
- **AI Q&A** - Ask questions, get answers with DeepSeek AI
- **Auto-Clustering** - Automatically organizes documents by similarity
- **Markdown Support** - Process markdown files with frontmatter
- **Tag System** - Organize content with tags
- **Web UI** - Modern, responsive interface

## How It Works

### 1. Index Documents
Go to **Manage** tab → Enter `./data/documents` → Click **Index Documents**

### 2. Search
Go to **Search** tab → Type query → Select mode (Hybrid/Keyword/Semantic) → Search

### 3. Ask Questions
Go to **Ask Question** tab → Type question → Get AI answer with sources

### 4. View Clusters
Go to **Clusters** tab → Select algorithm (HDBSCAN/K-Means/Hierarchical) → Generate

### 5. Evaluate & Visualize Search Performance
## Search Evaluation & Visualization 

This module is responsible for evaluating and visualizing the performance of different search methods in the system, including keyword search, semantic search, and hybrid search.

### Search Evaluation

**File:** `evaluate_all_methods.py`

This script quantitatively evaluates multiple search strategies by computing clustering and retrieval quality metrics.  
It is designed to support experimental comparison and offline analysis.

Main evaluation metrics include:
- Silhouette Score
- Davies–Bouldin Index
- Calinski–Harabasz Score

Run the evaluation script:
```bash
python evaluate_all_methods.py
```
Evaluation results are saved to the data/ directory for further analysis and reporting.

### Search Result Visualization

**File:** `visualize_all_methods.py`

This script visualizes document embeddings and clustering results produced by different search methods.
It provides an intuitive way to compare semantic structure and cluster quality.

The visualization includes:
- Dimensionality reduction (e.g., PCA or t-SNE)
- Cluster-based scatter plots for each search method

Run the visualization script:
```bash
python visualize_all_methods.py
```
Generated figures are saved to the data/ directory and can be directly used in reports or presentations.


## Configuration

Edit `config.yaml`:

```yaml
# DeepSeek AI
rag:
  provider: "deepseek"
  model: "deepseek-chat"
  deepseek_api_key: "your-key-here"

# Search weights
search:
  hybrid:
    keyword_weight: 0.4
    semantic_weight: 0.6

# Clustering
clustering:
  algorithm: "hdbscan"
  min_cluster_size: 3
```

## Tech Stack

- **Backend**: Flask, Python 3.8+
- **AI/ML**: DeepSeek API, Sentence-Transformers, FAISS, HDBSCAN
- **Frontend**: HTML/CSS/JavaScript
- **Search**: Hybrid (BM25 + semantic embeddings)

## Documentation

- [Technical Details](TECHNICAL.md) - Architecture and implementation

## Project Structure

```
qa/
├── app.py                 # Flask web server
├── run_web.bat           # Quick start script
├── config.yaml           # Configuration
├── requirements.txt      # Dependencies
│
├── src/
│   ├── indexer.py        # Document processing
│   ├── search.py         # Hybrid search engine
│   ├── clustering.py     # Auto-clustering
│   ├── rag.py            # AI Q&A with DeepSeek
│   └── config.py         # Config management
│
├── templates/
│   └── index.html        # Web UI
│
├── static/
│   ├── style.css         # Styling
│   └── app.js            # Frontend logic
│
└── data/
    ├── documents/        # Your markdown files
    └── index/            # Generated index (auto)
```

## Requirements

- Python 3.8+
- 2GB RAM minimum
- Internet connection (for DeepSeek API)

## Installation

```bash
# Clone/download project
cd qa

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

## API Endpoints

```
GET  /              - Web UI
GET  /api/stats     - Knowledge base statistics
POST /api/search    - Search documents
POST /api/ask       - Ask question (RAG)
POST /api/cluster   - Generate clusters
POST /api/index     - Index documents
```

## Contributing

This is an educational project built for learning purposes. Feel free to fork and modify!

## License

MIT License

## Support

- Review configuration in `config.yaml`
- Check browser console (F12) for errors
- View server logs in terminal

---

**Made with Flask, DeepSeek AI, and Modern ML**
