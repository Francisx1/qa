---
title: VectorDB - FAISS索引（1）
tags: [vectordb, faiss, hnsw, approx-nn]
created: 2024-11-19
source: synthetic-demo-corpus
---


# VectorDB - FAISS索引（1）

> Topic: **VectorDB**  |  Focus: **FAISS**

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
**Q:** What should I remember about *FAISS*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[VectorDB_Index_Maintenance_3]]
- [[VectorDB_IVF_5]]
- [[Transformers_Attention_6]]
- [[Agents_Function_Calling_9]]
