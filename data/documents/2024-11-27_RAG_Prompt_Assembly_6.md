---
title: RAG - Prompt Assembly（6）
tags: [rag, retrieval, embedding, llm, prompt-assembly]
created: 2024-11-27
source: synthetic-demo-corpus
---


# RAG - Prompt Assembly（6）

> Topic: **RAG**  |  Focus: **Prompt Assembly**

## Notes

- Key idea: separate retrieval / representation / ranking concerns.
- Failure mode: distribution shift; test with adversarial queries.
- Engineering note: cache embeddings; re-index incrementally.

### Mini example
Pipeline sketch: `chunk -> embed -> retrieve -> (optional rerank) -> prompt assemble -> generate`.
Practical tips:
- Tune chunk size / overlap; evaluate with recall@k and answer faithfulness.
- Hybrid search combines BM25 (lexical) + embedding similarity.

### Quick Q&A
**Q:** What should I remember about *Prompt Assembly*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[RAG_Reranking_5]]
- [[RAG_Prompt_Assembly_2]]
- [[Transformers_Attention_6]]
- [[VectorDB_HNSW图_10]]

```python
# pseudo-code
def hybrid_score(lex, sem, alpha=0.6):
    return alpha * lex + (1 - alpha) * sem
```
