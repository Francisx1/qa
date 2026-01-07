---
title: Transformers - MoE (1)
tags: [nlp, transformer, attention, deep-learning]
created: 2024-12-11
source: synthetic-demo-corpus
---


# Transformers - MoE (1)

> Topic: **Transformers**  |  Focus: **MoE**

## Notes

- Key idea: separate retrieval / representation / ranking concerns.
- Failure mode: distribution shift; test with adversarial queries.
- Engineering note: cache embeddings; re-index incrementally.

### Mini example
We often write: `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V`.
Notes:
- Q/K/V come from linear projections of hidden states.
- MoE relates to training stability and inference (KV cache).

### Quick Q&A
**Q:** What should I remember about *MoE*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Transformers_QKV_10]]
- [[Transformers_RoPE_4]]
- [[DistributedSystems_Consensus_9]]
- [[ProductNotes_用户调研_3]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
