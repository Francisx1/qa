"""
Unit tests for QuickHelp components
"""
import unittest
from pathlib import Path
import tempfile
import shutil

from src.config import Config
from src.indexer import DocumentIndexer, Document


class TestConfig(unittest.TestCase):
    """Test configuration management"""
    
    def test_config_loading(self):
        config = Config()
        self.assertIsNotNone(config.config)
        self.assertIn('search', config.config)
        self.assertIn('clustering', config.config)
    
    def test_config_get(self):
        config = Config()
        value = config.get('search.semantic.top_k', 10)
        self.assertIsInstance(value, int)
    
    def test_config_set(self):
        config = Config()
        config.set('test.key', 'value')
        self.assertEqual(config.get('test.key'), 'value')


class TestDocumentIndexer(unittest.TestCase):
    """Test document indexing"""
    
    def setUp(self):
        self.config = Config()
        self.indexer = DocumentIndexer(self.config)
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_process_file(self):
        # Create test markdown file
        test_file = Path(self.temp_dir) / "test.md"
        test_file.write_text("# Test\n\nThis is a test document.\n\n#test #demo")
        
        doc = self.indexer.process_file(test_file)
        
        self.assertIsNotNone(doc)
        self.assertEqual(doc.title, "Test")
        self.assertIn("test document", doc.content)
        self.assertIn("test", doc.tags)
    
    def test_document_chunking(self):
        doc = Document(
            id="test",
            path="test.md",
            title="Test",
            content=" ".join(["word"] * 1000),  # 1000 words
            metadata={},
            created_at="2024-01-01",
            updated_at="2024-01-01",
            word_count=1000,
            tags=[]
        )
        
        chunks = self.indexer.chunk_document(doc)
        self.assertGreater(len(chunks), 1)  # Should be chunked
        
        for chunk in chunks:
            self.assertIn('doc_id', chunk)
            self.assertIn('chunk_id', chunk)
            self.assertIn('content', chunk)
    
    def test_statistics(self):
        # Create multiple test files
        for i in range(3):
            test_file = Path(self.temp_dir) / f"test{i}.md"
            test_file.write_text(f"# Test {i}\n\nContent {i}")
        
        self.indexer.index_directory(self.temp_dir)
        stats = self.indexer.get_statistics()
        
        self.assertEqual(stats['total_documents'], 3)
        self.assertGreater(stats['total_words'], 0)


class TestSearch(unittest.TestCase):
    """Test search functionality"""
    
    def setUp(self):
        self.config = Config()
    
    def test_keyword_search(self):
        from src.search import KeywordSearch
        
        search = KeywordSearch(case_sensitive=False)
        docs = [
            {'content': 'The quick brown fox jumps over the lazy dog'},
            {'content': 'A fast red fox leaps across the sleepy cat'},
            {'content': 'The slow blue fox walks around'}
        ]
        
        search.index(docs)
        results = search.search('fox', max_results=10)
        
        self.assertEqual(len(results), 3)
        # All documents contain 'fox'
    
    def test_regex_search(self):
        from src.search import KeywordSearch
        
        search = KeywordSearch()
        docs = [
            {'content': 'The email is test@example.com'},
            {'content': 'Contact user@domain.org'},
            {'content': 'No email here'}
        ]
        
        search.index(docs)
        results = search.regex_search(r'\w+@\w+\.\w+', max_results=10)
        
        self.assertEqual(len(results), 2)  # Two docs with emails


class TestClustering(unittest.TestCase):
    """Test clustering functionality"""
    
    def test_cluster_organization(self):
        from src.clustering import AutoClusterer
        
        config = Config()
        config.set('clustering.algorithm', 'kmeans')
        
        # Create test documents
        docs = [
            {'content': 'machine learning neural networks', 'metadata': {'title': 'ML1'}},
            {'content': 'deep learning transformers attention', 'metadata': {'title': 'DL1'}},
            {'content': 'clustering algorithms kmeans', 'metadata': {'title': 'Cluster1'}},
            {'content': 'neural networks backpropagation', 'metadata': {'title': 'ML2'}},
            {'content': 'unsupervised learning clustering', 'metadata': {'title': 'Cluster2'}},
        ]
        
        # Note: This test requires sentence-transformers
        # Skip if not available
        try:
            clusterer = AutoClusterer(config)
            result = clusterer.fit(docs)
            
            self.assertIn('clusters', result)
            self.assertIn('num_clusters', result)
            self.assertGreater(result['num_clusters'], 0)
        except ImportError:
            self.skipTest("sentence-transformers not installed")


class TestRAG(unittest.TestCase):
    """Test RAG system"""
    
    def test_context_preparation(self):
        from src.search import HybridSearch
        from src.rag import RAGSystem
        
        config = Config()
        search = HybridSearch(config)
        rag = RAGSystem(config, search)
        
        results = [
            {
                'document': {
                    'content': 'Test content about AI',
                    'metadata': {'title': 'AI Doc'}
                },
                'score': 0.9
            }
        ]
        
        context = rag._prepare_context(results)
        self.assertIn('Test content about AI', context)
        self.assertIn('AI Doc', context)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
