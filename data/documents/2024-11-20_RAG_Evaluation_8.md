---
title: RAG - Evaluation (8)
tags: [rag, retrieval, embedding, llm, evaluation]
created: 2024-11-20
source: synthetic-demo-corpus
---


# RAG - Evaluation (8)

> Topic: **RAG**  |  Focus: **Evaluation**

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
**Q:** What should I remember about *Evaluation*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[RAG_Prompt_Assembly_7]]
- [[RAG_Reranking_5]]
- [[Blockchain_Reentrancy_7]]
- [[VectorDB_HNSW图_10]]
