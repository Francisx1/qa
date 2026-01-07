---
title: DistributedSystems - Paxos/Raft (6)
tags: [distributed-systems, consensus, reliability]
created: 2025-01-02
source: synthetic-demo-corpus
---


# DistributedSystems - Paxos/Raft (6)

> Topic: **DistributedSystems**  |  Focus: **Paxos/Raft**

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
**Q:** What should I remember about *Paxos/Raft*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[DistributedSystems_Consensus_9]]
- [[DistributedSystems_Paxos_Raft_10]]
- [[Agents_Function_Calling_9]]
- [[VectorDB_HNSW图_10]]
