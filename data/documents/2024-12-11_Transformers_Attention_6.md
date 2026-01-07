---
title: Transformers - Attention (6)
tags: [nlp, transformer, attention, deep-learning]
created: 2024-12-11
source: synthetic-demo-corpus
---


# Transformers - Attention (6)

> Topic: **Transformers**  |  Focus: **Attention**

## Notes

- Key idea: separate retrieval / representation / ranking concerns.
- Failure mode: distribution shift; test with adversarial queries.
- Engineering note: cache embeddings; re-index incrementally.

### Mini example
We often write: `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V`.
Notes:
- Q/K/V come from linear projections of hidden states.
- Attention relates to training stability and inference (KV cache).

### Quick Q&A
**Q:** What should I remember about *Attention*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Transformers_位置编码_9]]
- [[Transformers_Training_Tricks_7]]
- [[DistributedSystems_Consensus_9]]
- [[ProductNotes_用户调研_3]]

```python
# pseudo-code
def hybrid_score(lex, sem, alpha=0.6):
    return alpha * lex + (1 - alpha) * sem
```
