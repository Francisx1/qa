---
title: RAG - Prompt Assembly (2)
tags: [rag, retrieval, embedding, llm]
created: 2024-11-03
source: synthetic-demo-corpus
---


# RAG - Prompt Assembly (2)

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
- [[RAG_Hybrid_Search_3]]
- [[Blockchain_Reentrancy_7]]
- [[ProductNotes_用户调研_3]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
