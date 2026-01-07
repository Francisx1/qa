---
title: DistributedSystems - Consensus (9)
tags: [distributed-systems, consensus, reliability]
created: 2024-10-22
source: synthetic-demo-corpus
---


# DistributedSystems - Consensus (9)

> Topic: **DistributedSystems**  |  Focus: **Consensus**

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
**Q:** What should I remember about *Consensus*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[DistributedSystems_Paxos_Raft_6]]
- [[DistributedSystems_Lamport_Clock_2]]
- [[Agents_Function_Calling_9]]
- [[ProductNotes_用户调研_3]]
