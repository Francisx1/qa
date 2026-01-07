---
title: Blockchain - MakerDAO (5)
tags: [blockchain, ethereum, defi, security, makerdao]
created: 2025-01-14
source: synthetic-demo-corpus
---


# Blockchain - MakerDAO (5)

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
- [[Blockchain_Oracles_6]]
- [[Blockchain_Ethereum_Gas_2]]
- [[VectorDB_HNSW图_10]]
- [[RAG_Evaluation_8]]

```python
# pseudo-code
def hybrid_score(lex, sem, alpha=0.6):
    return alpha * lex + (1 - alpha) * sem
```
