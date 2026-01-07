"""
Generate additional sample documents for testing QuickHelp
Run this to create more test data for better clustering demonstration
"""
from pathlib import Path
from datetime import datetime, timedelta
import random


SAMPLE_DOCUMENTS = [
    {
        "filename": "bert_model.md",
        "title": "BERT: Bidirectional Encoder Representations",
        "tags": ["bert", "transformers", "nlp", "pre-training"],
        "content": """# BERT: Bidirectional Encoder Representations

BERT revolutionized NLP by introducing bidirectional pre-training of transformers.

## Key Innovation

Unlike previous models that read text sequentially, BERT reads text bidirectionally using masked language modeling.

## Architecture

- Based on transformer encoder
- 12 layers (BERT-base) or 24 layers (BERT-large)
- Multi-head self-attention
- Pre-trained on massive text corpus

## Training Objectives

1. **Masked Language Modeling (MLM)**: Randomly mask tokens and predict them
2. **Next Sentence Prediction (NSP)**: Predict if two sentences are consecutive

## Applications

- Question answering
- Named entity recognition
- Sentiment analysis
- Text classification

#bert #transformers #nlp"""
    },
    {
        "filename": "gpt_architecture.md",
        "title": "GPT: Generative Pre-trained Transformer",
        "tags": ["gpt", "transformers", "language-models", "generation"],
        "content": """# GPT: Generative Pre-trained Transformer

GPT models use decoder-only transformer architecture for text generation.

## Evolution

- GPT-1: 117M parameters
- GPT-2: 1.5B parameters
- GPT-3: 175B parameters
- GPT-4: >1T parameters (estimated)

## Key Features

- Autoregressive generation
- Causal attention (only attends to previous tokens)
- Zero-shot and few-shot learning
- Emergent capabilities at scale

## Training

Pre-trained on internet text to predict next token:
```
P(w_t | w_1, w_2, ..., w_{t-1})
```

## Use Cases

- Text completion
- Creative writing
- Code generation
- Conversational AI

#gpt #language-models #generation"""
    },
    {
        "filename": "embedding_techniques.md",
        "title": "Modern Embedding Techniques",
        "tags": ["embeddings", "word2vec", "glove", "transformers"],
        "content": """# Modern Embedding Techniques

Embeddings are dense vector representations of words, sentences, or documents.

## Word Embeddings

### Word2Vec
- Skip-gram and CBOW architectures
- Captures semantic relationships
- Fast training on large corpora

### GloVe (Global Vectors)
- Matrix factorization approach
- Combines global statistics with local context
- Pre-trained vectors available

### FastText
- Subword information
- Better for rare words
- Morphologically rich languages

## Sentence Embeddings

### Sentence-BERT
- Fine-tuned BERT for sentence similarity
- Siamese network architecture
- Efficient similarity computation

### Universal Sentence Encoder
- Transformer or DAN architecture
- Multi-task learning
- Multiple languages

## Applications

- Semantic search
- Document clustering
- Recommendation systems
- Transfer learning

#embeddings #word2vec #nlp"""
    },
    {
        "filename": "knowledge_graphs.md",
        "title": "Knowledge Graphs and Semantic Networks",
        "tags": ["knowledge-graphs", "semantic-web", "graph-database"],
        "content": """# Knowledge Graphs and Semantic Networks

Knowledge graphs structure information as entities and relationships.

## Components

- **Entities**: Nodes representing concepts (people, places, things)
- **Relations**: Edges connecting entities
- **Attributes**: Properties of entities

## Examples

- Google Knowledge Graph
- Wikidata
- DBpedia
- YAGO

## Representation

Triple format: (Subject, Predicate, Object)
```
(Albert Einstein, born_in, Germany)
(Germany, is_a, Country)
```

## Applications

- Search enhancement
- Question answering
- Recommendation
- Data integration

## Graph Databases

- Neo4j
- Amazon Neptune
- Azure Cosmos DB
- OrientDB

#knowledge-graphs #semantic-web"""
    },
    {
        "filename": "information_retrieval.md",
        "title": "Information Retrieval Systems",
        "tags": ["ir", "search", "retrieval", "ranking"],
        "content": """# Information Retrieval Systems

IR systems help users find relevant information from large collections.

## Classical IR

### Boolean Retrieval
- AND, OR, NOT operators
- Fast but no ranking
- Exact matching

### Vector Space Model
- Documents and queries as vectors
- TF-IDF weighting
- Cosine similarity

### Probabilistic Models
- BM25 ranking function
- Relevance probability
- Term frequency saturation

## Modern Neural IR

### Dense Retrieval
- Embed queries and documents
- Semantic matching
- BERT-based encoders

### Re-ranking
- Cross-encoders
- Two-stage pipeline
- Better accuracy, slower

## Evaluation Metrics

- Precision and Recall
- MAP (Mean Average Precision)
- NDCG (Normalized Discounted Cumulative Gain)
- MRR (Mean Reciprocal Rank)

#information-retrieval #search"""
    },
    {
        "filename": "llm_prompting.md",
        "title": "Prompt Engineering for Large Language Models",
        "tags": ["llm", "prompting", "gpt", "few-shot"],
        "content": """# Prompt Engineering for Large Language Models

Effective prompting is crucial for getting good results from LLMs.

## Prompt Patterns

### Zero-Shot
```
Translate to French: Hello, how are you?
```

### Few-Shot
```
English: Hello
French: Bonjour

English: Thank you
French: Merci

English: Goodbye
French: [to be filled]
```

### Chain-of-Thought
```
Question: A cafeteria had 23 apples. They used 20 for lunch.
They bought 6 more. How many do they have?

Let's think step by step:
1. Started with 23 apples
2. Used 20, so 23-20 = 3 left
3. Bought 6 more, so 3+6 = 9
Answer: 9 apples
```

## Best Practices

1. Be specific and clear
2. Provide context
3. Use examples
4. Specify format
5. Iterate and refine

## Advanced Techniques

- Role prompting
- System messages
- Temperature tuning
- Token limits

#llm #prompting #gpt"""
    },
    {
        "filename": "neural_search.md",
        "title": "Neural Search and Semantic Matching",
        "tags": ["neural-search", "semantic-search", "embeddings"],
        "content": """# Neural Search and Semantic Matching

Neural search uses deep learning for better information retrieval.

## Architecture

```
Query → Encoder → Query Vector
           ↓
      Similarity
           ↓
Documents → Encoder → Doc Vectors
```

## Dense vs Sparse

### Sparse (Traditional)
- TF-IDF, BM25
- Exact term matching
- Fast, interpretable

### Dense (Neural)
- Learned embeddings
- Semantic matching
- Better recall

### Hybrid
- Combine both approaches
- Best of both worlds
- Used by Cursor, Elastic

## Implementation

1. Encode all documents
2. Store in vector database
3. Encode query
4. Find nearest neighbors
5. Return top-K results

## Challenges

- Cold start problem
- Computational cost
- Index size
- Latency requirements

#neural-search #semantic-search"""
    },
    {
        "filename": "text_preprocessing.md",
        "title": "Text Preprocessing for NLP",
        "tags": ["nlp", "preprocessing", "tokenization"],
        "content": """# Text Preprocessing for NLP

Preprocessing is essential for effective NLP systems.

## Common Steps

### 1. Tokenization
- Word tokenization
- Subword (BPE, WordPiece)
- Character-level

### 2. Normalization
- Lowercasing
- Unicode normalization
- Accents removal

### 3. Cleaning
- Remove HTML tags
- Remove URLs
- Remove special characters

### 4. Stopword Removal
- Remove common words
- Context-dependent
- Not always beneficial

### 5. Stemming/Lemmatization
- Reduce to root form
- Stemming: crude chopping
- Lemmatization: linguistic analysis

## Modern Approaches

Transformer models often require minimal preprocessing:
- Keep case information
- Keep punctuation
- No stopword removal
- Tokenize with BPE

## Tools

- NLTK
- spaCy
- Hugging Face Tokenizers

#nlp #preprocessing"""
    }
]


def generate_documents(output_dir: Path):
    """Generate sample documents"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {len(SAMPLE_DOCUMENTS)} sample documents...")
    
    for i, doc_data in enumerate(SAMPLE_DOCUMENTS, 1):
        # Create file
        file_path = output_dir / doc_data['filename']
        
        # Generate date (spread over past 30 days)
        date = datetime.now() - timedelta(days=random.randint(1, 30))
        date_str = date.strftime("%Y-%m-%d")
        
        # Write file with frontmatter
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(f"title: \"{doc_data['title']}\"\n")
            f.write(f"tags: {doc_data['tags']}\n")
            f.write(f"date: {date_str}\n")
            f.write("---\n\n")
            f.write(doc_data['content'])
        
        print(f"  [{i}/{len(SAMPLE_DOCUMENTS)}] Created: {doc_data['filename']}")
    
    print(f"\n✓ Generated {len(SAMPLE_DOCUMENTS)} documents in {output_dir}")
    print(f"\nTotal documents including existing: {len(SAMPLE_DOCUMENTS) + 5}")
    print("\nNow you can run:")
    print("  python example.py")
    print("  python -m src.cli cluster --algorithm hdbscan")


if __name__ == "__main__":
    # Generate in data/documents directory
    output_dir = Path(__file__).parent / "data" / "documents"
    generate_documents(output_dir)
