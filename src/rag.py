"""
RAG (Retrieval-Augmented Generation) system for Q&A
Combines search with LLM to answer questions about documents
Supports OpenAI and DeepSeek APIs
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import requests

try:
    import openai
    import tiktoken
except ImportError:
    openai = None
    tiktoken = None


class RAGSystem:
    """
    Retrieval-Augmented Generation system
    Uses hybrid search to find relevant context, then LLM to generate answers
    """
    
    def __init__(self, config, search_engine):
        """
        Initialize RAG system
        
        Args:
            config: Config object
            search_engine: HybridSearch instance
        """
        self.config = config
        self.search_engine = search_engine
        
        # LLM configuration
        self.provider = config.get('rag.provider', 'openai')
        self.model = config.get('rag.model', 'gpt-3.5-turbo')
        self.temperature = config.get('rag.temperature', 0.7)
        self.max_tokens = config.get('rag.max_tokens', 500)
        
        # Context configuration
        self.max_context_docs = config.get('rag.max_context_documents', 5)
        self.context_window = config.get('rag.context_window', 4000)
        self.include_sources = config.get('rag.include_sources', True)
        
        # Initialize API client
        if self.provider == 'openai':
            if openai is None:
                raise ImportError("openai package not installed")
            
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                openai.api_key = api_key
            else:
                print("Warning: OPENAI_API_KEY not set")
        
        elif self.provider == 'deepseek':
            # DeepSeek API configuration
            self.deepseek_api_key = config.get('rag.deepseek_api_key') or os.getenv('DEEPSEEK_API_KEY')
            self.deepseek_base_url = config.get('rag.deepseek_base_url', 'https://api.deepseek.com/v1')
            
            if not self.deepseek_api_key:
                print("Warning: DeepSeek API key not configured")

        
        # Initialize tokenizer
        if tiktoken:
            try:
                self.tokenizer = tiktoken.encoding_for_model(self.model)
            except:
                self.tokenizer = tiktoken.get_encoding("cl100k_base")
        else:
            self.tokenizer = None
    
    def ask(self, question: str, search_mode: str = 'hybrid') -> Dict[str, Any]:
        """
        Ask a question and get an answer with sources
        
        Args:
            question: Question to answer
            search_mode: Search mode ('keyword', 'semantic', 'hybrid')
        
        Returns:
            Dictionary with answer, sources, and metadata
        """
        # Step 1: Retrieve relevant documents
        search_results = self.search_engine.search(
            query=question,
            mode=search_mode,
            max_results=self.max_context_docs
        )
        
        if not search_results:
            return {
                'answer': "I couldn't find any relevant information to answer your question.",
                'sources': [],
                'question': question,
                'success': False
            }
        
        # Step 2: Prepare context from retrieved documents
        context = self._prepare_context(search_results)
        
        # Step 3: Generate answer using LLM
        answer = self._generate_answer(question, context)
        
        # Step 4: Prepare sources
        sources = self._prepare_sources(search_results)
        
        return {
            'answer': answer,
            'sources': sources,
            'question': question,
            'num_sources': len(sources),
            'search_mode': search_mode,
            'success': True
        }
    
    def _prepare_context(self, search_results: List[Dict[str, Any]]) -> str:
        """
        Prepare context from search results
        Truncates to fit within context window
        
        Args:
            search_results: List of search results
        
        Returns:
            Formatted context string
        """
        contexts = []
        total_tokens = 0
        
        for i, result in enumerate(search_results):
            doc = result['document']
            content = doc.get('content', '')
            
            # Get metadata
            metadata = doc.get('metadata', {})
            title = metadata.get('title', f"Document {i+1}")
            
            # Format context piece
            context_piece = f"[Source {i+1}: {title}]\n{content}\n"
            
            # Count tokens
            if self.tokenizer:
                tokens = len(self.tokenizer.encode(context_piece))
            else:
                tokens = len(context_piece.split()) * 1.3  # Rough estimate
            
            # Check if we exceed context window
            if total_tokens + tokens > self.context_window:
                break
            
            contexts.append(context_piece)
            total_tokens += tokens
        
        return "\n---\n".join(contexts)
    
    def _generate_answer(self, question: str, context: str) -> str:
        """
        Generate answer using LLM
        
        Args:
            question: User question
            context: Retrieved context
        
        Returns:
            Generated answer
        """
        if self.provider == 'openai':
            return self._generate_with_openai(question, context)
        elif self.provider == 'deepseek':
            return self._generate_with_deepseek(question, context)
        else:
            # Fallback to extractive answer
            return self._generate_extractive(question, context)
    
    def _generate_with_openai(self, question: str, context: str) -> str:
        """Generate answer using OpenAI API"""
        if openai is None or not openai.api_key:
            return "OpenAI API not configured. Please set OPENAI_API_KEY environment variable."
        
        # Create prompt
        system_prompt = """You are a helpful assistant that answers questions based on the provided context.
Use ONLY the information from the context to answer questions.
If the context doesn't contain enough information to answer the question, say so.
Be concise but informative. Cite specific information from the sources when relevant."""
        
        user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""
        
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            answer = response.choices[0].message.content.strip()
            return answer
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def _generate_with_deepseek(self, question: str, context: str) -> str:
        """Generate answer using DeepSeek API"""
        if not self.deepseek_api_key:
            return "DeepSeek API not configured. Please set DeepSeek API key in config."
        
        # Create prompt
        system_prompt = """You are a helpful assistant that answers questions based on the provided context.
Use ONLY the information from the context to answer questions.
If the context doesn't contain enough information to answer the question, say so.
Be concise but informative. Cite specific information from the sources when relevant."""
        
        user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""
        
        try:
            # Call DeepSeek API (compatible with OpenAI API format)
            headers = {
                'Authorization': f'Bearer {self.deepseek_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model,
                'messages': [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                'temperature': self.temperature,
                'max_tokens': self.max_tokens
            }
            
            response = requests.post(
                f'{self.deepseek_base_url}/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content'].strip()
                return answer
            else:
                return f"DeepSeek API error: {response.status_code} - {response.text}"
            
        except Exception as e:
            return f"Error generating answer with DeepSeek: {str(e)}"
    
    def _generate_extractive(self, question: str, context: str) -> str:
        """
        Generate extractive answer (fallback without LLM)
        Simply returns most relevant context snippet
        """
        # Split context into sentences
        sentences = context.split('.')
        
        # Simple heuristic: return first few sentences
        answer_sentences = sentences[:3]
        answer = '. '.join(s.strip() for s in answer_sentences if s.strip())
        
        if answer:
            answer += '.'
        else:
            answer = "Unable to generate answer without LLM configured."
        
        return answer
    
    def _prepare_sources(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prepare source citations from search results
        
        Args:
            search_results: List of search results
        
        Returns:
            List of source dictionaries
        """
        sources = []
        
        for i, result in enumerate(search_results):
            doc = result['document']
            metadata = doc.get('metadata', {})
            
            source = {
                'id': i + 1,
                'title': metadata.get('title', 'Untitled'),
                'path': metadata.get('path', ''),
                'score': result['score'],
                'search_type': result.get('search_type', 'unknown')
            }
            
            # Add tags if available
            if 'tags' in metadata:
                source['tags'] = metadata['tags']
            
            sources.append(source)
        
        return sources
    
    def format_answer(self, result: Dict[str, Any]) -> str:
        """
        Format answer result as readable text
        
        Args:
            result: Result dictionary from ask()
        
        Returns:
            Formatted string
        """
        lines = []
        
        # Question
        lines.append(f"Question: {result['question']}")
        lines.append("")
        
        # Answer
        lines.append(f"Answer:\n{result['answer']}")
        lines.append("")
        
        # Sources
        if self.include_sources and result.get('sources'):
            lines.append("Sources:")
            for source in result['sources']:
                title = source['title']
                score = source['score']
                lines.append(f"  [{source['id']}] {title} (relevance: {score:.2f})")
                
                if source.get('path'):
                    lines.append(f"      Path: {source['path']}")
                
                if source.get('tags'):
                    lines.append(f"      Tags: {', '.join(source['tags'])}")
        
        return '\n'.join(lines)
    
    def batch_ask(self, questions: List[str], search_mode: str = 'hybrid') -> List[Dict[str, Any]]:
        """
        Ask multiple questions in batch
        
        Args:
            questions: List of questions
            search_mode: Search mode to use
        
        Returns:
            List of answer results
        """
        results = []
        
        for question in questions:
            result = self.ask(question, search_mode)
            results.append(result)
        
        return results
