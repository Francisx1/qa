---
title: ProductNotes - Metrics (7)
tags: [product, pm, metrics]
created: 2024-10-20
source: synthetic-demo-corpus
---


# ProductNotes - Metrics (7)

> Topic: **ProductNotes**  |  Focus: **Metrics**

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
**Q:** What should I remember about *Metrics*?
**A:** Summarize it in 1 sentence, then link related notes. Start from the cluster and drill down.

### Related notes
- [[ProductNotes_Metrics_8]]
- [[ProductNotes_User_Research_2]]
- [[RAG_Evaluation_8]]
- [[DistributedSystems_Consensus_9]]

### Table
| Item | Pros | Cons |
|---|---|---|
| Lexical search (BM25) | Fast, explainable | Misses paraphrases |
| Semantic search (embeddings) | Finds similar meaning | More compute |
| Hybrid | Best of both | Needs tuning |
