"""
Flask web application for QuickHelp
Provides a web UI for document search, clustering, and Q&A
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
from datetime import date, datetime
import json
import sys
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.indexer import DocumentIndexer
from src.search import HybridSearch
from src.clustering import AutoClusterer
from src.rag import RAGSystem


# Custom JSON encoder for date/datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Configure JSON encoding
app.json_encoder = DateTimeEncoder

# Initialize components
config = Config()
indexer = DocumentIndexer(config)
search_engine = None
rag_system = None

# Load index if exists
index_path = Path(__file__).parent / "data" / "index"
if (index_path / "documents.json").exists():
    try:
        indexer.load_index(index_path / "documents.json")
        search_engine = HybridSearch(config)
        search_engine.load(str(index_path))
        rag_system = RAGSystem(config, search_engine)
        print("✓ Loaded existing index")
    except Exception as e:
        print(f"Warning: Could not load index: {e}")


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get knowledge base statistics"""
    try:
        if not indexer.documents:
            return jsonify({
                'success': False,
                'message': 'No documents indexed yet'
            })
        
        stats = indexer.get_statistics()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/index', methods=['POST'])
def index_documents():
    """Index documents from directory"""
    global search_engine, rag_system
    
    try:
        data = request.json
        doc_path = data.get('path', './data/documents')
        
        # Index documents
        documents = indexer.index_directory(doc_path, recursive=True)
        
        if not documents:
            return jsonify({
                'success': False,
                'message': 'No documents found'
            })
        
        # Save index
        index_path = Path(__file__).parent / "data" / "index"
        indexer.save_index(index_path / "documents.json")
        
        # Prepare chunks
        all_chunks = []
        for doc in documents:
            chunks = indexer.chunk_document(doc)
            all_chunks.extend(chunks)
        
        # Build search engine
        search_engine = HybridSearch(config)
        search_engine.index(all_chunks)
        search_engine.save(str(index_path))
        
        # Initialize RAG
        rag_system = RAGSystem(config, search_engine)
        
        stats = indexer.get_statistics()
        
        return jsonify({
            'success': True,
            'message': f'Indexed {len(documents)} documents',
            'stats': stats
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search', methods=['POST'])
def search():
    """Search documents"""
    try:
        if not search_engine:
            return jsonify({
                'success': False,
                'message': 'Please index documents first'
            })
        
        data = request.json
        query = data.get('query', '')
        mode = data.get('mode', 'hybrid')
        max_results = data.get('max_results', 10)
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Query cannot be empty'
            })
        
        # Perform search
        results = search_engine.search(query, mode=mode, max_results=max_results)
        
        # Format results
        formatted_results = []
        for result in results:
            doc = result['document']
            metadata = doc.get('metadata', {})
            
            # Convert any date objects in metadata to strings
            safe_metadata = {}
            for key, value in metadata.items():
                if isinstance(value, (date, datetime)):
                    safe_metadata[key] = value.isoformat()
                elif isinstance(value, list):
                    safe_metadata[key] = [v.isoformat() if isinstance(v, (date, datetime)) else v for v in value]
                else:
                    safe_metadata[key] = value
            
            formatted_results.append({
                'title': safe_metadata.get('title', 'Untitled'),
                'path': safe_metadata.get('path', ''),
                'content': doc.get('content', '')[:300] + '...',
                'score': result['score'],
                'tags': safe_metadata.get('tags', [])
            })
        
        return jsonify({
            'success': True,
            'results': formatted_results,
            'count': len(formatted_results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/cluster', methods=['POST'])
def cluster():
    """Cluster documents"""
    try:
        if not indexer.documents:
            return jsonify({
                'success': False,
                'message': 'Please index documents first'
            })
        
        data = request.json
        algorithm = data.get('algorithm', 'hdbscan')
        
        # Update config
        config.set('clustering.algorithm', algorithm)
        
        # Prepare documents
        docs_for_clustering = [
            {
                'content': doc.content,
                'metadata': {
                    'title': doc.title,
                    'path': doc.path,
                    'tags': doc.tags
                }
            }
            for doc in indexer.documents
        ]
        
        # Cluster
        clusterer = AutoClusterer(config)
        result = clusterer.fit(docs_for_clustering)
        
        # Format clusters
        formatted_clusters = []
        for cluster in clusterer.clusters:
            formatted_clusters.append({
                'id': cluster['id'],
                'name': cluster['name'],
                'size': cluster['size'],
                'keywords': cluster['keywords'][:5],
                'tags': cluster['common_tags'][:3],
                'documents': [
                    {
                        'title': doc['metadata']['title'],
                        'path': doc['metadata']['path']
                    }
                    for doc in cluster['documents'][:5]
                ]
            })
        
        return jsonify({
            'success': True,
            'clusters': formatted_clusters,
            'count': len(formatted_clusters)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ask', methods=['POST'])
def ask():
    """Ask a question using RAG"""
    try:
        if not rag_system:
            return jsonify({
                'success': False,
                'message': 'Please index documents first'
            })
        
        data = request.json
        question = data.get('question', '')
        mode = data.get('mode', 'hybrid')
        
        if not question:
            return jsonify({
                'success': False,
                'message': 'Question cannot be empty'
            })
        
        # Ask question
        result = rag_system.ask(question, search_mode=mode)
        
        if not result['success']:
            return jsonify(result)
        
        # Format response
        return jsonify({
            'success': True,
            'answer': result['answer'],
            'sources': result.get('sources', []),
            'question': question
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  QuickHelp Web UI")
    print("="*60)
    print("\n✓ Starting server...")
    print("✓ Open browser at: http://127.0.0.1:5000")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
