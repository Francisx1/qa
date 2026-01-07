---
title: RAG - Reranking (5)
tags: [rag, retrieval, embedding, llm, reranking]
created: 2024-09-19
source: synthetic-demo-corpus
---


# RAG - Reranking (5)

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
- [[RAG_Prompt_Assembly_7]]
- [[RAG_Reranking_9]]
- [[Blockchain_Reentrancy_7]]
- [[Transformers_Attention_6]]
