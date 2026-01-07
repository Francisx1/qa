---
title: Blockchain - MakerDAO (10)
tags: [blockchain, ethereum, defi, security]
created: 2024-10-20
source: synthetic-demo-corpus
---


# Blockchain - MakerDAO (10)

> Topic: **Blockchain**  |  Focus: **MakerDAO**

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
**Q:** What should I remember about *MakerDAO*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[Blockchain_Reentrancy_8]]
- [[Blockchain_MakerDAO_9]]
- [[Agents_Function_Calling_9]]
- [[Transformers_Attention_6]]
