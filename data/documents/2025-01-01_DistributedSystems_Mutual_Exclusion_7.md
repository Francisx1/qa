---
title: DistributedSystems - Mutual Exclusion (7)
tags: [distributed-systems, consensus, reliability]
created: 2025-01-01
source: synthetic-demo-corpus
---


# DistributedSystems - Mutual Exclusion (7)

> Topic: **DistributedSystems**  |  Focus: **Mutual Exclusion**

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
**Q:** What should I remember about *Mutual Exclusion*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[DistributedSystems_Chandy_Lamport_8]]
- [[DistributedSystems_Paxos_Raft_6]]
- [[Transformers_Attention_6]]
- [[VectorDB_HNSW图_10]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
