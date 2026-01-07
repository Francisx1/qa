---
title: VectorDB - IVF（5）
tags: [vectordb, faiss, hnsw, approx-nn, ivf]
created: 2024-11-03
source: synthetic-demo-corpus
---


# VectorDB - IVF（5）

> Topic: **VectorDB**  |  Focus: **IVF**

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
**Q:** What should I remember about *IVF*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[VectorDB_Index_Maintenance_3]]
- [[VectorDB_Filtering_6]]
- [[Agents_Function_Calling_9]]
- [[Transformers_Attention_6]]

```python
# pseudo-code
def hybrid_score(lex, sem, alpha=0.6):
    return alpha * lex + (1 - alpha) * sem
```
