---
title: DistributedSystems - Lamport Clock (1)
tags: [distributed-systems, consensus, reliability, lamport-clock]
created: 2024-10-29
source: synthetic-demo-corpus
---


# DistributedSystems - Lamport Clock (1)

> Topic: **DistributedSystems**  |  Focus: **Lamport Clock**

## Notes

- Safety vs liveness: define invariants before optimizing.
- Clock assumptions matter: partial synchrony vs async.
- Observe: tail latency dominates user experience.

### Mini example
Consensus properties:
- Safety: no two nodes decide different values.
- Liveness: eventually a value is decided.
Tools: Raft for practical logs; Paxos family for theory.

### Quick Q&A
**Q:** What should I remember about *Lamport Clock*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[DistributedSystems_Paxos_Raft_6]]
- [[DistributedSystems_Chandy_Lamport_3]]
- [[Agents_Function_Calling_9]]
- [[Transformers_Attention_6]]

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
