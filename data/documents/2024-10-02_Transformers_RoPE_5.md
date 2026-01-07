---
title: Transformers - RoPE（5）
tags: [nlp, transformer, attention, deep-learning]
created: 2024-10-02
source: synthetic-demo-corpus
---


# Transformers - RoPE（5）

> Topic: **Transformers**  |  Focus: **RoPE**

## Notes

- Key idea: separate retrieval / representation / ranking concerns.
- Failure mode: distribution shift; test with adversarial queries.
- Engineering note: cache embeddings; re-index incrementally.

### Mini example
We often write: `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V`.
Notes:
- Q/K/V come from linear projections of hidden states.
- RoPE relates to training stability and inference (KV cache).

### Quick Q&A
**Q:** What should I remember about *RoPE*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Transformers_QKV_10]]
- [[Transformers_位置编码_9]]
- [[DistributedSystems_Consensus_9]]
- [[RAG_Evaluation_8]]
