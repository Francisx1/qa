---
title: DistributedSystems - Chandy-Lamport（5）
tags: [distributed-systems, consensus, reliability, chandy-lamport]
created: 2024-09-27
source: synthetic-demo-corpus
---


# DistributedSystems - Chandy-Lamport（5）

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
- [[DistributedSystems_Chandy_Lamport_4]]
- [[Agents_Function_Calling_9]]
- [[ProductNotes_用户调研_3]]

```python
# pseudo-code
def hybrid_score(lex, sem, alpha=0.6):
    return alpha * lex + (1 - alpha) * sem
```
