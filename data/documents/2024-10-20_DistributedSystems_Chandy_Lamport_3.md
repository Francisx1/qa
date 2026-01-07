---
title: DistributedSystems - Chandy-Lamport (3)
tags: [distributed-systems, consensus, reliability]
created: 2024-10-20
source: synthetic-demo-corpus
---


# DistributedSystems - Chandy-Lamport (3)

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
- [[DistributedSystems_Chandy_Lamport_5]]
- [[DistributedSystems_Lamport_Clock_2]]
- [[Blockchain_Reentrancy_7]]
- [[Transformers_Attention_6]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
