"""
Hybrid search engine combining keyword and semantic search
Inspired by Cursor.com's scalable search architecture
"""
import re
import numpy as np
from typing import List, Dict, Any, Tuple
from pathlib import Path
import pickle

try:
    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    import faiss
except ImportError:
    SentenceTransformer = None
    BM25Okapi = None
    faiss = None


class KeywordSearch:
    """
    Grep-style keyword search
    Fast and scalable for exact matching
    """
    
    def __init__(self, case_sensitive: bool = False):
        """
        Initialize keyword search
        
        Args:
            case_sensitive: Whether to perform case-sensitive search
        """
        self.case_sensitive = case_sensitive
        self.documents = []
    
    def index(self, documents: List[Dict[str, Any]]):
        """
        Index documents for keyword search
        
        Args:
            documents: List of document chunks
        """
        self.documents = documents
    
    def search(self, query: str, max_results: int = 100) -> List[Tuple[int, float]]:
        """
        Search for documents matching query
        
        Args:
            query: Search query
            max_results: Maximum number of results
        
        Returns:
            List of (doc_index, score) tuples
        """
        if not self.case_sensitive:
            query = query.lower()
        
        results = []
        
        for idx, doc in enumerate(self.documents):
            content = doc['content']
            if not self.case_sensitive:
                content = content.lower()
            
            # Count occurrences
            occurrences = len(re.findall(re.escape(query), content))
            
            if occurrences > 0:
                # Score based on occurrence count and position
                score = occurrences / (len(content.split()) + 1)
                results.append((idx, score))
        
        # Sort by score
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max_results]
    
    def regex_search(self, pattern: str, max_results: int = 100) -> List[Tuple[int, float]]:
        """
        Search using regex pattern
        
        Args:
            pattern: Regex pattern
            max_results: Maximum number of results
        
        Returns:
            List of (doc_index, score) tuples
        """
        try:
            regex = re.compile(pattern, re.IGNORECASE if not self.case_sensitive else 0)
        except re.error:
            return []
        
        results = []
        
        for idx, doc in enumerate(self.documents):
            content = doc['content']
            matches = regex.findall(content)
            
            if matches:
                score = len(matches) / (len(content.split()) + 1)
                results.append((idx, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max_results]


class SemanticSearch:
    """
    Semantic search using sentence embeddings and FAISS
    Provides context-aware similarity matching
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize semantic search
        
        Args:
            model_name: Name of sentence transformer model
        """
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers not installed")
        
        self.model = SentenceTransformer(model_name)
        self.faiss_index = None
        self.documents = []
        self.embeddings = None
    
    def index(self, documents: List[Dict[str, Any]]):
        """
        Index documents for semantic search
        
        Args:
            documents: List of document chunks
        """
        self.documents = documents
        
        # Extract text content
        texts = [doc['content'] for doc in documents]
        
        # Generate embeddings
        print(f"Generating embeddings for {len(texts)} documents...")
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Create FAISS index
        if faiss:
            dimension = self.embeddings.shape[1]
            self.faiss_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(self.embeddings)
            self.faiss_index.add(self.embeddings)
        
        print(f"Indexed {len(documents)} documents")
    
    def search(self, query: str, top_k: int = 20, threshold: float = 0.0) -> List[Tuple[int, float]]:
        """
        Search for semantically similar documents
        
        Args:
            query: Search query
            top_k: Number of results to return
            threshold: Minimum similarity threshold
        
        Returns:
            List of (doc_index, similarity_score) tuples
        """
        if self.faiss_index is None:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search in FAISS index
        scores, indices = self.faiss_index.search(query_embedding, top_k)
        
        # Filter by threshold and return results
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if score >= threshold:
                results.append((int(idx), float(score)))
        
        return results
    
    def save(self, path: str):
        """
        Save index and embeddings to disk
        
        Args:
            path: Directory to save to
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        if self.faiss_index:
            faiss.write_index(self.faiss_index, str(path / "faiss.index"))
        
        # Save embeddings and documents
        with open(path / "embeddings.pkl", 'wb') as f:
            pickle.dump({
                'embeddings': self.embeddings,
                'documents': self.documents
            }, f)
    
    def load(self, path: str):
        """
        Load index and embeddings from disk
        
        Args:
            path: Directory to load from
        """
        path = Path(path)
        
        # Load FAISS index
        index_path = path / "faiss.index"
        if index_path.exists():
            self.faiss_index = faiss.read_index(str(index_path))
        
        # Load embeddings and documents
        with open(path / "embeddings.pkl", 'rb') as f:
            data = pickle.load(f)
            self.embeddings = data['embeddings']
            self.documents = data['documents']


class HybridSearch:
    """
    Hybrid search combining keyword and semantic search
    Routes queries intelligently for optimal performance
    """
    
    def __init__(self, config):
        """
        Initialize hybrid search
        
        Args:
            config: Config object
        """
        self.config = config
        
        # Initialize keyword search
        case_sensitive = config.get('search.keyword.case_sensitive', False)
        self.keyword_search = KeywordSearch(case_sensitive=case_sensitive)
        
        # Initialize semantic search
        if config.get('search.semantic.enabled', True):
            try:
                model_name = config.get('search.semantic.model', 
                                       'sentence-transformers/all-MiniLM-L6-v2')
                self.semantic_search = SemanticSearch(model_name=model_name)
            except ImportError:
                print("Warning: sentence-transformers not available, semantic search disabled")
                self.semantic_search = None
        else:
            self.semantic_search = None
        
        # Weights for hybrid scoring
        self.keyword_weight = config.get('search.hybrid.keyword_weight', 0.4)
        self.semantic_weight = config.get('search.hybrid.semantic_weight', 0.6)
    
    def index(self, documents: List[Dict[str, Any]]):
        """
        Index documents for both keyword and semantic search
        
        Args:
            documents: List of document chunks
        """
        print(f"Indexing {len(documents)} documents...")
        
        # Index for keyword search
        self.keyword_search.index(documents)
        
        # Index for semantic search
        if self.semantic_search:
            self.semantic_search.index(documents)
        
        print("Indexing complete!")
    
    def search(self, query: str, mode: str = 'hybrid', max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Search documents using specified mode
        
        Args:
            query: Search query
            mode: Search mode ('keyword', 'semantic', 'hybrid')
            max_results: Maximum number of results
        
        Returns:
            List of search results with scores
        """
        if mode == 'keyword':
            return self._keyword_search(query, max_results)
        elif mode == 'semantic':
            return self._semantic_search(query, max_results)
        else:  # hybrid
            return self._hybrid_search(query, max_results)
    
    def _keyword_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Perform keyword-only search"""
        results = self.keyword_search.search(query, max_results)
        
        return [
            {
                'doc_index': idx,
                'score': score,
                'document': self.keyword_search.documents[idx],
                'search_type': 'keyword'
            }
            for idx, score in results
        ]
    
    def _semantic_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Perform semantic-only search"""
        if not self.semantic_search:
            return []
        
        threshold = self.config.get('search.semantic.similarity_threshold', 0.6)
        results = self.semantic_search.search(query, max_results, threshold)
        
        return [
            {
                'doc_index': idx,
                'score': score,
                'document': self.semantic_search.documents[idx],
                'search_type': 'semantic'
            }
            for idx, score in results
        ]
    
    def _hybrid_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Perform hybrid search combining both methods"""
        # Get results from both searches
        keyword_results = self.keyword_search.search(query, max_results * 2)
        
        if self.semantic_search:
            semantic_results = self.semantic_search.search(query, max_results * 2)
        else:
            semantic_results = []
        
        # Combine scores
        combined_scores = {}
        
        # Add keyword scores
        for idx, score in keyword_results:
            combined_scores[idx] = self.keyword_weight * score
        
        # Add semantic scores
        for idx, score in semantic_results:
            if idx in combined_scores:
                combined_scores[idx] += self.semantic_weight * score
            else:
                combined_scores[idx] = self.semantic_weight * score
        
        # Sort by combined score
        sorted_results = sorted(combined_scores.items(), 
                              key=lambda x: x[1], 
                              reverse=True)[:max_results]
        
        # Format results
        return [
            {
                'doc_index': idx,
                'score': score,
                'document': self.keyword_search.documents[idx],
                'search_type': 'hybrid'
            }
            for idx, score in sorted_results
        ]
    
    def save(self, path: str):
        """Save search indices"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save keyword documents
        with open(path / "keyword_docs.pkl", 'wb') as f:
            pickle.dump(self.keyword_search.documents, f)
        
        # Save semantic index
        if self.semantic_search:
            self.semantic_search.save(path / "semantic")
    
    def load(self, path: str):
        """Load search indices"""
        path = Path(path)
        
        # Load keyword documents
        with open(path / "keyword_docs.pkl", 'rb') as f:
            docs = pickle.load(f)
            self.keyword_search.index(docs)
        
        # Load semantic index
        if self.semantic_search and (path / "semantic").exists():
            self.semantic_search.load(path / "semantic")
