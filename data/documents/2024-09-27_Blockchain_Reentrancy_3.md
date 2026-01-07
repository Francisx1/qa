---
title: Blockchain - Reentrancy（3）
tags: [blockchain, ethereum, defi, security]
created: 2024-09-27
source: synthetic-demo-corpus
---


# Blockchain - Reentrancy（3）

> Topic: **Blockchain**  |  Focus: **Reentrancy**

## Notes

- Threat model: adversary controls ordering (MEV) and can replay calls.
- Checklist: access control, reentrancy guard, oracle freshness.
- Metric: gas cost vs safety (e.g., extra SSTORE).

### Mini example
Solidity pitfall (reentrancy):
- External call before state update can allow re-entry.
Mitigation: checks-effects-interactions + ReentrancyGuard.
Gas note: EVM gas acts as a buffer against ETH volatility and miner/validator incentives.

### Quick Q&A
**Q:** What should I remember about *Reentrancy*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Blockchain_MakerDAO_10]]
- [[Blockchain_MakerDAO_5]]
- [[Agents_Function_Calling_9]]
- [[VectorDB_HNSW图_10]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
