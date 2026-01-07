---
title: DistributedSystems - Chandy-Lamport (4)
tags: [distributed-systems, consensus, reliability]
created: 2024-11-29
source: synthetic-demo-corpus
---


# DistributedSystems - Chandy-Lamport (4)

> Topic: **DistributedSystems**  |  Focus: **Chandy-Lamport**

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
**Q:** What should I remember about *Chandy-Lamport*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[DistributedSystems_Mutual_Exclusion_7]]
- [[DistributedSystems_Chandy_Lamport_3]]
- [[Blockchain_Reentrancy_7]]
- [[ProductNotes_用户调研_3]]

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
