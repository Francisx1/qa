"""
QuickHelp - Intelligent Knowledge Base with Auto-Clustering
"""

__version__ = "0.1.0"
__author__ = "QuickHelp Team"

from .config import Config
from .indexer import DocumentIndexer
from .search import HybridSearch
from .clustering import AutoClusterer
from .rag import RAGSystem

__all__ = [
    "Config",
    "DocumentIndexer",
    "HybridSearch",
    "AutoClusterer",
    "RAGSystem",
]
