---
title: ProductNotes - Roadmap (10)
tags: [product, pm, metrics]
created: 2024-09-16
source: synthetic-demo-corpus
---


# ProductNotes - Roadmap (10)

> Topic: **ProductNotes**  |  Focus: **Roadmap**

## Notes

- Define success metric before building features.
- Use a counterfactual: what would users do otherwise?
- Prefer leading indicators (activation) over vanity metrics.

### Mini example
Metrics:
- Activation rate = users who reach "Aha moment" / signups
- Retention = cohort-based D1/D7
A/B testing: guard against novelty effects; pre-register success metrics.

### Quick Q&A
**Q:** What should I remember about *Roadmap*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[ProductNotes_User_Research_6]]
- [[ProductNotes_Metrics_4]]
- [[VectorDB_HNSW图_10]]
- [[DistributedSystems_Consensus_9]]

```python
# pseudo-code
def hybrid_score(lex, sem, alpha=0.6):
    return alpha * lex + (1 - alpha) * sem
```
