---
title: Transformers - Training Tricks（7）
tags: [nlp, transformer, attention, deep-learning, training-tricks]
created: 2024-10-05
source: synthetic-demo-corpus
---


# Transformers - Training Tricks（7）

> Topic: **Transformers**  |  Focus: **Training Tricks**

## Notes

- Key idea: separate retrieval / representation / ranking concerns.
- Failure mode: distribution shift; test with adversarial queries.
- Engineering note: cache embeddings; re-index incrementally.

### Mini example
We often write: `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V`.
Notes:
- Q/K/V come from linear projections of hidden states.
- Training Tricks relates to training stability and inference (KV cache).

### Quick Q&A
**Q:** What should I remember about *Training Tricks*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Transformers_RoPE_5]]
- [[Transformers_位置编码_9]]
- [[DistributedSystems_Consensus_9]]
- [[ProductNotes_用户调研_3]]
