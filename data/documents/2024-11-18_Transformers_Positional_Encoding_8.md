---
title: Transformers - Positional Encoding (8)
tags: [nlp, transformer, attention, deep-learning]
created: 2024-11-18
source: synthetic-demo-corpus
---


# Transformers - Positional Encoding (8)

> Topic: **Transformers**  |  Focus: **Positional Encoding**

## Notes

- Key idea: separate retrieval / representation / ranking concerns.
- Failure mode: distribution shift; test with adversarial queries.
- Engineering note: cache embeddings; re-index incrementally.

### Mini example
We often write: `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V`.
Notes:
- Q/K/V come from linear projections of hidden states.
- Positional Encoding relates to training stability and inference (KV cache).

### Quick Q&A
**Q:** What should I remember about *Positional Encoding*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Transformers_RoPE_4]]
- [[Transformers_RoPE_5]]
- [[DistributedSystems_Consensus_9]]
- [[VectorDB_HNSW图_10]]

```python
# pseudo-code
def hybrid_score(lex, sem, alpha=0.6):
    return alpha * lex + (1 - alpha) * sem
```
