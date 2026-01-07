---
title: Transformers - QKV (2)
tags: [nlp, transformer, attention, deep-learning, qkv]
created: 2024-09-25
source: synthetic-demo-corpus
---


# Transformers - QKV (2)

> Topic: **Transformers**  |  Focus: **QKV**

## Notes

- Key idea: separate retrieval / representation / ranking concerns.
- Failure mode: distribution shift; test with adversarial queries.
- Engineering note: cache embeddings; re-index incrementally.

### Mini example
We often write: `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V`.
Notes:
- Q/K/V come from linear projections of hidden states.
- QKV relates to training stability and inference (KV cache).

### Quick Q&A
**Q:** What should I remember about *QKV*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Transformers_RoPE_4]]
- [[Transformers_MoE_1]]
- [[VectorDB_HNSW图_10]]
- [[ProductNotes_用户调研_3]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
