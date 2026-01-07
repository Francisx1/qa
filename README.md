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

- 🔍 **Hybrid Search** - Combines keyword + semantic search for best results
- 💬 **AI Q&A** - Ask questions, get answers with DeepSeek AI
- 🎯 **Auto-Clustering** - Automatically organizes documents by similarity
- 📝 **Markdown Support** - Process markdown files with frontmatter
- 🏷️ **Tag System** - Organize content with tags
- 📊 **Web UI** - Modern, responsive interface

## How It Works

### 1. Index Documents
Go to **Manage** tab → Enter `./data/documents` → Click **Index Documents**

### 2. Search
Go to **Search** tab → Type query → Select mode (Hybrid/Keyword/Semantic) → Search

### 3. Ask Questions
Go to **Ask Question** tab → Type question → Get AI answer with sources

### 4. View Clusters
Go to **Clusters** tab → Select algorithm (HDBSCAN/K-Means/Hierarchical) → Generate

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

- [User Guide](GUIDE.md) - Complete guide to using QuickHelp
- [Technical Details](TECHNICAL.md) - Architecture and implementation
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions

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

- Check [Troubleshooting Guide](TROUBLESHOOTING.md)
- Review configuration in `config.yaml`
- Check browser console (F12) for errors
- View server logs in terminal

---

**Made with ❤️ using Flask, DeepSeek AI, and Modern ML**
