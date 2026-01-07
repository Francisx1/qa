---
title: Agents - LangChain (1)
tags: [agent, tools, langchain, autogen]
created: 2024-11-07
source: synthetic-demo-corpus
---


# Agents - LangChain (1)

> Topic: **Agents**  |  Focus: **LangChain**

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
**Q:** What should I remember about *LangChain*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Agents_Tool_Use_10]]
- [[Agents_Memory_6]]
- [[DistributedSystems_Consensus_9]]
- [[RAG_Evaluation_8]]

```python
# pseudo-code
def hybrid_score(lex, sem, alpha=0.6):
    return alpha * lex + (1 - alpha) * sem
```
