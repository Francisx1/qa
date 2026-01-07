---
title: VectorDB - Filtering (6)
tags: [vectordb, faiss, hnsw, approx-nn, filtering]
created: 2024-10-13
source: synthetic-demo-corpus
---


# VectorDB - Filtering (6)

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
- [[VectorDB_FAISS索引_1]]
- [[VectorDB_Recall_Latency_4]]
- [[DistributedSystems_Consensus_9]]
- [[Blockchain_Reentrancy_7]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
