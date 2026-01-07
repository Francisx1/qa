---
title: RAG - Chunking (10)
tags: [rag, retrieval, embedding, llm]
created: 2024-12-31
source: synthetic-demo-corpus
---


# RAG - Chunking (10)

> Topic: **RAG**  |  Focus: **Chunking**

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
**Q:** What should I remember about *Chunking*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[RAG_Prompt_Assembly_7]]
- [[RAG_Prompt_Assembly_2]]
- [[Agents_Function_Calling_9]]
- [[Transformers_Attention_6]]
