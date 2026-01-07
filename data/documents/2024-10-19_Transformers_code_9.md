---
title: Transformers - 位置编码（9）
tags: [nlp, transformer, attention, deep-learning, positional-encoding]
created: 2024-10-19
source: synthetic-demo-corpus
---


# Transformers - 位置编码（9）

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
- [[Transformers_QKV_2]]
- [[Transformers_Training_Tricks_7]]
- [[Blockchain_Reentrancy_7]]
- [[Agents_Function_Calling_9]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |

```python
# pseudo-code
def hybrid_score(lex, sem, alpha=0.6):
    return alpha * lex + (1 - alpha) * sem
```
