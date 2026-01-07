---
title: Transformers - Attention (3)
tags: [nlp, transformer, attention, deep-learning]
created: 2024-10-25
source: synthetic-demo-corpus
---


# Transformers - Attention (3)

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
- [[Transformers_QKV_2]]
- [[Transformers_MoE_1]]
- [[Agents_Function_Calling_9]]
- [[DistributedSystems_Consensus_9]]
