---
title: VectorDB - Recall/Latency（4）
tags: [vectordb, faiss, hnsw, approx-nn, recall/latency]
created: 2024-09-16
source: synthetic-demo-corpus
---


# VectorDB - Recall/Latency（4）

> Topic: **VectorDB**  |  Focus: **Recall/Latency**

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
**Q:** What should I remember about *Recall/Latency*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[VectorDB_Filtering_6]]
- [[VectorDB_HNSW图_10]]
- [[DistributedSystems_Consensus_9]]
- [[RAG_Evaluation_8]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
