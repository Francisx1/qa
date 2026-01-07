---
title: Agents - Planning (8)
tags: [agent, tools, langchain, autogen, planning]
created: 2024-09-27
source: synthetic-demo-corpus
---


# Agents - Planning (8)

> Topic: **Agents**  |  Focus: **Planning**

## Notes

- Key idea: separate retrieval / representation / ranking concerns.
- Failure mode: distribution shift; test with adversarial queries.
- Engineering note: cache embeddings; re-index incrementally.

### Mini example
Agent loop (tool use):
1) Observe user goal
2) Plan steps
3) Call tools (search, DB, calculator)
4) Verify output + guardrails
Common issue: tool hallucination; mitigate with schema validation.

### Quick Q&A
**Q:** What should I remember about *Planning*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Agents_Planning_3]]
- [[Agents_Tool_Use_7]]
- [[VectorDB_HNSW图_10]]
- [[Blockchain_Reentrancy_7]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
