"""
Example script demonstrating QuickHelp functionality
Run this after installing dependencies
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.indexer import DocumentIndexer
from src.search import HybridSearch
from src.clustering import AutoClusterer
from src.rag import RAGSystem


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def main():
    print("QuickHelp - Example Demonstration")
    print("==================================\n")
    
    # Initialize configuration
    config = Config()
    
    # ===== 1. INDEXING =====
    print_section("1. INDEXING DOCUMENTS")
    
    indexer = DocumentIndexer(config)
    doc_path = Path(__file__).parent / "data" / "documents"
    
    if not doc_path.exists():
        print(f"Error: Document directory not found: {doc_path}")
        print("Please create sample documents first!")
        return
    
    print(f"Indexing documents from: {doc_path}")
    documents = indexer.index_directory(str(doc_path))
    
    if not documents:
        print("No documents found!")
        return
    
    stats = indexer.get_statistics()
    print(f"\n✓ Indexed {stats['total_documents']} documents")
    print(f"  Total words: {stats['total_words']:,}")
    print(f"  Average words per document: {stats['avg_words_per_doc']:.1f}")
    print(f"  Unique tags: {stats['unique_tags']}")
    
    # Save index
    index_path = Path(__file__).parent / "data" / "index"
    indexer.save_index(index_path / "documents.json")
    print(f"\n✓ Index saved to: {index_path}")
    
    # ===== 2. HYBRID SEARCH =====
    print_section("2. HYBRID SEARCH")
    
    # Prepare chunks
    all_chunks = []
    for doc in documents:
        chunks = indexer.chunk_document(doc)
        all_chunks.extend(chunks)
    
    print(f"Created {len(all_chunks)} chunks from documents")
    
    # Create and index search engine
    print("\nBuilding search index...")
    search_engine = HybridSearch(config)
    search_engine.index(all_chunks)
    
    # Save search index
    search_engine.save(str(index_path))
    print("✓ Search index built and saved")
    
    # Perform searches
    queries = [
        "attention mechanism",
        "clustering algorithms",
        "RAG retrieval"
    ]
    
    for query in queries:
        print(f"\nSearching for: '{query}'")
        results = search_engine.search(query, mode='hybrid', max_results=3)
        
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            title = result['document']['metadata']['title']
            score = result['score']
            print(f"  {i}. {title} (score: {score:.3f})")
    
    # ===== 3. AUTO-CLUSTERING =====
    print_section("3. AUTO-CLUSTERING")
    
    # Prepare documents for clustering
    docs_for_clustering = [
        {
            'content': doc.content,
            'metadata': {
                'title': doc.title,
                'path': doc.path,
                'tags': doc.tags
            }
        }
        for doc in documents
    ]
    
    print(f"Clustering {len(docs_for_clustering)} documents...")
    clusterer = AutoClusterer(config)
    result = clusterer.fit(docs_for_clustering)
    
    print(f"\n✓ Created {result['num_clusters']} clusters")
    print("\nCluster Summary:")
    print(clusterer.get_cluster_summary())
    
    # Save clustering results
    cluster_path = Path(__file__).parent / "data" / "clusters"
    clusterer.save(str(cluster_path))
    print(f"\n✓ Clusters saved to: {cluster_path}")
    
    # ===== 4. RAG Q&A =====
    print_section("4. RAG-BASED Q&A")
    
    rag_system = RAGSystem(config, search_engine)
    
    questions = [
        "What is the attention mechanism?",
        "How does FAISS work?",
        "What are the benefits of RAG?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        answer_result = rag_system.ask(question, search_mode='hybrid')
        
        if answer_result['success']:
            print(f"Answer: {answer_result['answer'][:200]}...")
            print(f"Sources: {answer_result['num_sources']} documents")
        else:
            print(f"Answer: {answer_result['answer']}")
    
    # ===== 5. DEMONSTRATION COMPLETE =====
    print_section("DEMONSTRATION COMPLETE")
    
    print("Summary:")
    print(f"  • Indexed {len(documents)} documents")
    print(f"  • Created {len(all_chunks)} searchable chunks")
    print(f"  • Built hybrid search index (keyword + semantic)")
    print(f"  • Organized into {result['num_clusters']} clusters")
    print(f"  • Answered {len(questions)} questions using RAG")
    
    print("\nNext Steps:")
    print("  1. Add your own documents to ./data/documents/")
    print("  2. Re-run this script or use CLI commands")
    print("  3. Try: python -m src.cli search 'your query'")
    print("  4. Try: python -m src.cli ask 'your question'")
    
    print("\nFor detailed usage: See USAGE.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
