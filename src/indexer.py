"""
Document indexer for QuickHelp
Handles document loading, processing, and indexing
"""
import os
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json

try:
    import frontmatter
except ImportError:
    frontmatter = None


@dataclass
class Document:
    """Represents a document in the knowledge base"""
    id: str
    path: str
    title: str
    content: str
    metadata: Dict[str, Any]
    created_at: str
    updated_at: str
    word_count: int
    tags: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        """Create from dictionary"""
        return cls(**data)


class DocumentIndexer:
    """
    Indexes documents from the knowledge base
    Handles markdown parsing, chunking, and metadata extraction
    """
    
    def __init__(self, config):
        """
        Initialize document indexer
        
        Args:
            config: Config object
        """
        self.config = config
        self.documents: List[Document] = []
        self.doc_formats = config.get('documents.formats', ['.md', '.txt'])
        self.chunking_enabled = config.get('documents.chunking.enabled', True)
        self.chunk_size = config.get('documents.chunking.chunk_size', 500)
        self.chunk_overlap = config.get('documents.chunking.chunk_overlap', 50)
    
    def index_directory(self, directory: str, recursive: bool = True) -> List[Document]:
        """
        Index all documents in a directory
        
        Args:
            directory: Path to directory
            recursive: Whether to search recursively
        
        Returns:
            List of indexed documents
        """
        directory = Path(directory)
        
        if not directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        
        documents = []
        
        # Find all supported files
        if recursive:
            files = []
            for ext in self.doc_formats:
                files.extend(directory.rglob(f"*{ext}"))
        else:
            files = []
            for ext in self.doc_formats:
                files.extend(directory.glob(f"*{ext}"))
        
        # Process each file
        for file_path in files:
            try:
                doc = self.process_file(file_path)
                if doc:
                    documents.append(doc)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        by_path={d.path:d for d in self.documents} # deduplicate
        for d in documents: #deduplicate
            by_path[d.path]=d  #deduplicate
        self.documents=list(by_path.values()) #deduplicate
        #self.documents.extend(documents)
        return documents
    
    def process_file(self, file_path: Path) -> Optional[Document]:
        """
        Process a single file into a Document
        
        Args:
            file_path: Path to file
        
        Returns:
            Document object or None if processing fails
        """
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            # Extract frontmatter if available
            metadata = {}
            content = raw_content
            
            if frontmatter and self.config.get('documents.extract_frontmatter', True):
                try:
                    post = frontmatter.loads(raw_content)
                    metadata = dict(post.metadata)
                    content = post.content
                except:
                    pass
            
            # Extract title
            title = metadata.get('title', self._extract_title(content, file_path))
            
            # Extract tags
            tags = metadata.get('tags', [])
            if self.config.get('documents.extract_tags', True):
                tags.extend(self._extract_tags(content))
            tags = list(set(tags))  # Remove duplicates
            
            # Get file stats
            stats = file_path.stat()
            created_at = datetime.fromtimestamp(stats.st_ctime).isoformat()
            updated_at = datetime.fromtimestamp(stats.st_mtime).isoformat()
            
            # Calculate word count
            word_count = len(content.split())
            
            # Generate document ID
            doc_id = self._generate_id(file_path)
            
            # Create document
            doc = Document(
                id=doc_id,
                path=str(file_path),
                title=title,
                content=content,
                metadata=metadata,
                created_at=created_at,
                updated_at=updated_at,
                word_count=word_count,
                tags=tags
            )
            
            return doc
            
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return None
    
    def _extract_title(self, content: str, file_path: Path) -> str:
        """Extract title from content or filename"""
        # Try to find H1 heading
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Use filename as fallback
        return file_path.stem
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract hashtags from content"""
        # Find #tag patterns
        tags = re.findall(r'#(\w+)', content)
        return list(set(tags))
    
    def _generate_id(self, file_path: Path) -> str:
        """Generate unique ID for document"""
        # Use file path hash as ID
        path_str = str(file_path.absolute())
        return hashlib.md5(path_str.encode()).hexdigest()
    
    def chunk_document(self, doc: Document) -> List[Dict[str, Any]]:
        """
        Split document into chunks for better retrieval
        
        Args:
            doc: Document to chunk
        
        Returns:
            List of chunks with metadata
        """
        if not self.chunking_enabled:
            return [{
                'doc_id': doc.id,
                'chunk_id': 0,
                'content': doc.content,
                'metadata': doc.metadata
            }]
        
        words = doc.content.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_content = ' '.join(chunk_words)
            
            chunks.append({
                'doc_id': doc.id,
                'chunk_id': len(chunks),
                'content': chunk_content,
                'start_word': i,
                'end_word': min(i + self.chunk_size, len(words)),
                'metadata': {
                    'title': doc.title,
                    'path': doc.path,
                    'tags': doc.tags
                }
            })
        
        return chunks
    
    def save_index(self, output_path: str):
        """
        Save indexed documents to file
        
        Args:
            output_path: Path to output file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert documents to dicts and sanitize metadata
        documents = []
        for doc in self.documents:
            doc_dict = doc.to_dict()
            # Sanitize metadata - convert date objects to strings
            if 'metadata' in doc_dict:
                doc_dict['metadata'] = self._sanitize_metadata(doc_dict['metadata'])
            documents.append(doc_dict)
        
        data = {
            'documents': documents,
            'indexed_at': datetime.now().isoformat(),
            'total_documents': len(self.documents)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_index(self, input_path: str) -> List[Document]:
        """
        Load indexed documents from file
        
        Args:
            input_path: Path to index file
        
        Returns:
            List of documents
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            return []
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.documents = [Document.from_dict(doc_data) for doc_data in data['documents']]
        return self.documents
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get indexing statistics"""
        if not self.documents:
            return {
                'total_documents': 0,
                'total_words': 0,
                'avg_words_per_doc': 0,
                'total_tags': 0,
                'unique_tags': 0
            }
        
        total_words = sum(doc.word_count for doc in self.documents)
        all_tags = []
        for doc in self.documents:
            all_tags.extend(doc.tags)
        
        return {
            'total_documents': len(self.documents),
            'total_words': total_words,
            'avg_words_per_doc': total_words / len(self.documents),
            'total_tags': len(all_tags),
            'unique_tags': len(set(all_tags)),
            'formats': list(set(Path(doc.path).suffix for doc in self.documents))
        }
    
    def _sanitize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize metadata by converting date objects to ISO strings
        
        Args:
            metadata: Metadata dictionary
        
        Returns:
            Sanitized metadata with dates as strings
        """
        from datetime import date, datetime
        
        sanitized = {}
        for key, value in metadata.items():
            if isinstance(value, (date, datetime)):
                sanitized[key] = value.isoformat()
            elif isinstance(value, list):
                sanitized[key] = [
                    v.isoformat() if isinstance(v, (date, datetime)) else v
                    for v in value
                ]
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_metadata(value)
            else:
                sanitized[key] = value
        return sanitized
