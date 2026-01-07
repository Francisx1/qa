---
title: RAG - Reranking (9)
tags: [rag, retrieval, embedding, llm, reranking]
created: 2024-12-26
source: synthetic-demo-corpus
---


# RAG - Reranking (9)

> Topic: **RAG**  |  Focus: **Reranking**

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
**Q:** What should I remember about *Reranking*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[RAG_Evaluation_8]]
- [[RAG_Prompt_Assembly_6]]
- [[Transformers_Attention_6]]
- [[Agents_Function_Calling_9]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
