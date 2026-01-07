---
title: DistributedSystems - Chandy-Lamport (8)
tags: [distributed-systems, consensus, reliability]
created: 2024-09-22
source: synthetic-demo-corpus
---


# DistributedSystems - Chandy-Lamport (8)

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
- [[DistributedSystems_Lamport_Clock_2]]
- [[RAG_Evaluation_8]]
- [[Transformers_Attention_6]]
