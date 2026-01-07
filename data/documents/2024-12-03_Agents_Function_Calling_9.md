---
title: Agents - Function Calling (9)
tags: [agent, tools, langchain, autogen]
created: 2024-12-03
source: synthetic-demo-corpus
---


# Agents - Function Calling (9)

> Topic: **Agents**  |  Focus: **Function Calling**

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
**Q:** What should I remember about *Function Calling*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Agents_Planning_3]]
- [[Agents_LangChain_1]]
- [[ProductNotes_用户调研_3]]
- [[DistributedSystems_Consensus_9]]
