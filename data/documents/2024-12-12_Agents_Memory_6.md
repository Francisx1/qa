---
title: Agents - Memory（6）
tags: [agent, tools, langchain, autogen, memory]
created: 2024-12-12
source: synthetic-demo-corpus
---


# Agents - Memory（6）

> Topic: **Agents**  |  Focus: **Memory**

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
**Q:** What should I remember about *Memory*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Agents_Function_Calling_2]]
- [[Agents_Planning_3]]
- [[Blockchain_Reentrancy_7]]
- [[DistributedSystems_Consensus_9]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |

```python
# pseudo-code
def hybrid_score(lex, sem, alpha=0.6):
    return alpha * lex + (1 - alpha) * sem
```
