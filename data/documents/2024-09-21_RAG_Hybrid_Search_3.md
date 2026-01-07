---
title: RAG - Hybrid Search (3)
tags: [rag, retrieval, embedding, llm]
created: 2024-09-21
source: synthetic-demo-corpus
---


# RAG - Hybrid Search (3)

> Topic: **RAG**  |  Focus: **Hybrid Search**

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
**Q:** What should I remember about *Hybrid Search*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[RAG_Reranking_5]]
- [[RAG_Evaluation_4]]
- [[ProductNotes_用户调研_3]]
- [[Blockchain_Reentrancy_7]]
