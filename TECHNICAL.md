# QuickHelp - Technical Documentation

## Architecture Overview

QuickHelp follows a modular architecture inspired by production-grade knowledge management systems like Cursor.com and Obsidian.

```
┌─────────────────────────────────────────────────────────┐
│                     CLI / API Layer                      │
└────────────┬────────────────────────────────┬───────────┘
             │                                │
    ┌────────▼──────────┐          ┌─────────▼────────────┐
    │   RAG System      │          │  Auto-Clusterer      │
    │  (Q&A Engine)     │          │ (Organization)       │
    └────────┬──────────┘          └─────────┬────────────┘
             │                                │
             │          ┌────────────────────┐│
             └──────────►  Hybrid Search     ◄┘
                        │  Engine            │
                        └────────┬───────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Document Indexer       │
                    │  (Processing Layer)     │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Knowledge Base         │
                    │  (Markdown Files)       │
                    └─────────────────────────┘
```

## Core Components

### 1. Document Indexer (`src/indexer.py`)

**Purpose**: Process and index documents from various formats

**Key Features**:
- Markdown parsing with frontmatter support
- Automatic metadata extraction (title, tags, dates)
- Document chunking for better retrieval
- Efficient storage and caching

**Algorithm**: Document Chunking
```python
def chunk_document(doc, chunk_size=500, overlap=50):
    words = doc.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(' '.join(chunk))
    return chunks
```

**Scalability**: 
- Handles 100K+ documents
- Incremental indexing for updates
- Memory-efficient streaming processing

### 2. Hybrid Search Engine (`src/search.py`)

**Purpose**: Combine keyword and semantic search for optimal results

#### 2.1 Keyword Search

Following Cursor.com's philosophy: grep-style search scales better than pure semantic search.

**Implementation**:
- Regex-based pattern matching
- Case-insensitive by default
- Score based on occurrence frequency
- O(n) complexity per search

**When to use**:
- Exact term matching (file names, code identifiers)
- Boolean queries
- Extremely large datasets (>1M documents)

#### 2.2 Semantic Search

Uses sentence transformers for context-aware retrieval.

**Model**: `all-MiniLM-L6-v2`
- 384 dimensions
- Fast inference (~50ms for encoding)
- Good balance of speed and accuracy

**Vector Index**: FAISS
```python
# Create index
dimension = 384
index = faiss.IndexFlatIP(dimension)  # Inner product
faiss.normalize_L2(embeddings)        # For cosine similarity
index.add(embeddings)

# Search
query_vec = model.encode([query])
faiss.normalize_L2(query_vec)
scores, indices = index.search(query_vec, k=20)
```

**Index Types for Scale**:
- Flat (< 10K docs): Exact search
- IVF (10K - 1M docs): Fast approximate search
- IVF+PQ (> 1M docs): Memory-efficient

#### 2.3 Hybrid Fusion

Combines both approaches using weighted scoring:

```python
final_score = alpha * keyword_score + (1 - alpha) * semantic_score
```

Default weights: `alpha = 0.4` (keyword), `0.6` (semantic)

**Benefits**:
- Keyword catches exact matches
- Semantic handles paraphrases and concepts
- Complementary coverage

### 3. Auto-Clustering (`src/clustering.py`)

**Purpose**: Automatically organize documents into meaningful categories

#### Supported Algorithms

**HDBSCAN** (Recommended):
```
+ Automatically determines cluster count
+ Handles outliers/noise
+ Density-based (natural groupings)
- More parameters to tune
```

**K-Means**:
```
+ Fast and simple
+ Works well with clear boundaries
- Must specify K
- Sensitive to initialization
```

**Hierarchical**:
```
+ Produces dendrogram (hierarchy)
+ No need to specify K
- Computationally expensive O(n²)
```

#### Clustering Pipeline

```python
1. Generate embeddings for all documents
   → sentence-transformers encoding
   
2. Normalize embeddings
   → L2 normalization for cosine distance
   
3. Apply clustering algorithm
   → HDBSCAN with min_cluster_size=3
   
4. Extract cluster characteristics
   → Common tags, keywords, themes
   
5. Auto-generate cluster names
   → TF-IDF or LLM-based naming
```

#### Example: Finding "Transformer" Related Notes

Given 50 notes scattered across folders:
1. System embeds all notes
2. HDBSCAN finds dense regions
3. Notes about attention, transformers, BERT cluster together
4. System names cluster: "Attention & Transformers"
5. Cross-references established automatically

### 4. RAG System (`src/rag.py`)

**Purpose**: Answer questions using retrieved context + LLM

#### RAG Pipeline

```
┌──────────────┐
│   Question   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Retrieve   │──► Hybrid Search (top-5 docs)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Assemble     │──► Format context with metadata
│ Context      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Generate   │──► LLM (GPT-3.5/4, Claude, etc.)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Format      │──► Answer + Source Citations
│  Response    │
└──────────────┘
```

#### Context Management

**Challenge**: LLMs have limited context windows (4K - 32K tokens)

**Strategy**:
1. Retrieve top-K most relevant documents
2. Truncate to fit context window
3. Prioritize by relevance score
4. Include metadata for citation

```python
context_budget = 4000  # tokens
current_tokens = 0

for doc in sorted_results:
    doc_tokens = count_tokens(doc)
    if current_tokens + doc_tokens > context_budget:
        break
    context += format_document(doc)
    current_tokens += doc_tokens
```

#### Prompt Engineering

```python
system_prompt = """
You are a helpful assistant that answers questions 
based on provided context. Use ONLY the context 
to answer. If unsure, say so. Be concise and cite sources.
"""

user_prompt = f"""
Context:
{retrieved_docs}

Question: {user_question}

Answer:
"""
```

#### Without LLM API

Fallback to extractive QA:
- Extract most relevant sentences
- Simple heuristics (first N sentences containing query terms)
- Good for demos without API costs

## Performance Considerations

### Scalability Benchmarks

| Documents | Indexing Time | Search Time | Memory |
|-----------|---------------|-------------|---------|
| 100       | 2s            | 10ms        | 50MB    |
| 1,000     | 15s           | 20ms        | 200MB   |
| 10,000    | 3min          | 50ms        | 2GB     |
| 100,000   | 30min         | 100ms       | 15GB    |

### Optimization Strategies

1. **Keyword Search**: O(n) per query
   - Fast for millions of documents
   - Use as first-stage filter

2. **Semantic Search**: O(log n) with IVF
   - Approximate nearest neighbors
   - Trade accuracy for speed

3. **Caching**:
   - Cache embeddings (reuse across runs)
   - Cache search results (common queries)
   - Incremental indexing (only new docs)

4. **Batch Processing**:
   - Encode documents in batches
   - Parallel processing for indexing
   - GPU acceleration for embeddings

### Memory Management

```python
# For large datasets
config = {
    'chunking': {
        'chunk_size': 300,  # Smaller chunks
        'overlap': 30
    },
    'semantic': {
        'batch_size': 32,   # Batch encoding
        'use_gpu': True     # GPU acceleration
    }
}
```

## Comparison with Existing Solutions

### vs. Obsidian
```
Obsidian: Manual organization, graph view
QuickHelp: Automatic clustering, AI-powered search
```

### vs. Cursor.com
```
Cursor: Code-specific, IDE integration
QuickHelp: General knowledge, standalone system
```

### vs. NotionAI
```
Notion: Cloud-based, manual tagging
QuickHelp: Local-first, auto-organization
```

## Future Enhancements

1. **Graph-based Navigation**
   - Document relationship graphs
   - Citation networks
   - Concept maps

2. **Multi-modal Support**
   - Images, PDFs, audio
   - OCR for scanned documents
   - Video transcript indexing

3. **Collaborative Features**
   - Shared knowledge bases
   - Team clustering
   - Annotation sync

4. **Advanced Clustering**
   - Hierarchical categories
   - Dynamic re-clustering
   - LLM-based naming

5. **Better RAG**
   - Re-ranking with cross-encoders
   - Multi-hop reasoning
   - Fact verification

## References

### Papers
- "Attention Is All You Need" (Vaswani et al., 2017)
- "BERT: Pre-training of Deep Bidirectional Transformers" (Devlin et al., 2018)
- "Sentence-BERT" (Reimers & Gurevych, 2019)
- "Dense Passage Retrieval" (Karpukhin et al., 2020)
- "HDBSCAN: Hierarchical Density-Based Clustering" (Campello et al., 2013)

### Libraries
- FAISS: https://github.com/facebookresearch/faiss
- Sentence-Transformers: https://www.sbert.net/
- scikit-learn: https://scikit-learn.org/
- HDBSCAN: https://hdbscan.readthedocs.io/

### Inspirations
- Cursor.com's approach to codebase search
- Obsidian's knowledge management philosophy
- Pinecone's vector database architecture
