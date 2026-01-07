---
title: VectorDB - Index Maintenance (2)
tags: [vectordb, faiss, hnsw, approx-nn]
created: 2024-11-12
source: synthetic-demo-corpus
---


# VectorDB - Index Maintenance (2)

> Topic: **VectorDB**  |  Focus: **Index Maintenance**

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
**Q:** What should I remember about *Index Maintenance*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[VectorDB_Recall_Latency_7]]
- [[VectorDB_Filtering_8]]
- [[Agents_Function_Calling_9]]
- [[DistributedSystems_Consensus_9]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
