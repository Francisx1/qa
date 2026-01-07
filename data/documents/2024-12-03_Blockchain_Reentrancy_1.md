---
title: Blockchain - Reentrancy (1)
tags: [blockchain, ethereum, defi, security, reentrancy]
created: 2024-12-03
source: synthetic-demo-corpus
---


# Blockchain - Reentrancy (1)

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
- [[Blockchain_Ethereum_Gas_2]]
- [[Blockchain_MakerDAO_5]]
- [[Transformers_Attention_6]]
- [[ProductNotes_用户调研_3]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
