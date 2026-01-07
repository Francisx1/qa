---
title: Agents - AutoGen (4)
tags: [agent, tools, langchain, autogen]
created: 2024-09-14
source: synthetic-demo-corpus
---


# Agents - AutoGen (4)

> Topic: **Agents**  |  Focus: **AutoGen**

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
**Q:** What should I remember about *AutoGen*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Agents_Tool_Use_7]]
- [[Agents_Planning_3]]
- [[Transformers_Attention_6]]
- [[VectorDB_HNSW图_10]]
