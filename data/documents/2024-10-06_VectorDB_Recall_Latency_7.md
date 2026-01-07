---
title: VectorDB - Recall/Latency (7)
tags: [vectordb, faiss, hnsw, approx-nn]
created: 2024-10-06
source: synthetic-demo-corpus
---


# VectorDB - Recall/Latency (7)

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
- [[VectorDB_Filtering_8]]
- [[VectorDB_Index_Maintenance_9]]
- [[DistributedSystems_Consensus_9]]
- [[Blockchain_Reentrancy_7]]
