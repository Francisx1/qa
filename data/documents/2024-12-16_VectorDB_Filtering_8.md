---
title: VectorDB - Filtering (8)
tags: [vectordb, faiss, hnsw, approx-nn]
created: 2024-12-16
source: synthetic-demo-corpus
---


# VectorDB - Filtering (8)

> Topic: **VectorDB**  |  Focus: **Filtering**

## Notes

- Key idea: separate retrieval / representation / ranking concerns.
- Failure mode: distribution shift; test with adversarial queries.
- Engineering note: cache embeddings; re-index incrementally.

### Mini example
Index tradeoffs:
- HNSW: fast queries, higher memory.
- IVF+PQ: lower memory, needs training.
Evaluation:
- recall@k vs latency (p95) is the typical curve.

### Quick Q&A
**Q:** What should I remember about *Filtering*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[VectorDB_Recall_Latency_4]]
- [[VectorDB_HNSW图_10]]
- [[Agents_Function_Calling_9]]
- [[RAG_Evaluation_8]]
