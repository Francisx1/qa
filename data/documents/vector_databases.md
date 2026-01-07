---
title: "Vector Databases and FAISS"
tags: [vector-database, faiss, embeddings, search]
date: 2024-01-05
---

# Vector Databases and FAISS

Vector databases are specialized systems designed to store and efficiently search high-dimensional vector embeddings. FAISS (Facebook AI Similarity Search) is one of the most popular libraries for this purpose.

## What are Vector Embeddings?

Vector embeddings are numerical representations of data (text, images, audio) in high-dimensional space. Similar items have similar embeddings.

Example: Word "king" might be represented as [0.2, 0.5, -0.3, ...]

## FAISS Overview

FAISS is a library developed by Facebook AI Research for efficient similarity search and clustering of dense vectors.

### Key Features

1. **Speed**: Optimized for billion-scale datasets
2. **Memory Efficiency**: Compressed index options
3. **GPU Support**: Accelerated search on GPUs
4. **Multiple Index Types**: Different trade-offs between speed and accuracy

## Index Types

### Flat Index (IndexFlatL2, IndexFlatIP)

- Exact search (no approximation)
- Good for: Small datasets (<1M vectors)
- Slow but accurate

### IVF (Inverted File Index)

- Divides space into Voronoi cells
- Good for: Medium datasets (1M-100M vectors)
- Trade-off: Speed vs accuracy with nprobe parameter

### HNSW (Hierarchical Navigable Small World)

- Graph-based approach
- Good for: High accuracy requirements
- Fast but memory-intensive

### PQ (Product Quantization)

- Compresses vectors for memory efficiency
- Good for: Large datasets with memory constraints
- Some accuracy loss

## Similarity Metrics

### Euclidean Distance (L2)

```
d = sqrt(sum((a_i - b_i)^2))
```

### Cosine Similarity (Inner Product)

```
similarity = dot(a, b) / (||a|| * ||b||)
```

## Best Practices

1. **Normalize vectors** for cosine similarity
2. **Choose appropriate index** based on scale
3. **Tune nprobe** for IVF indices
4. **Use GPU** for large-scale searches
5. **Monitor memory usage** with quantization

## Applications in RAG

- Store document embeddings
- Fast nearest neighbor search
- Hybrid search with keyword filtering
- Re-ranking retrieved results

#vector-database #faiss #embeddings #search
