"""
Configuration loader for QuickHelp
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration management for QuickHelp"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to config.yaml file
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._setup_paths()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            return self._default_config()
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'search': {
                'keyword': {'enabled': True, 'case_sensitive': False},
                'semantic': {'enabled': True, 'top_k': 20},
                'hybrid': {'keyword_weight': 0.4, 'semantic_weight': 0.6}
            },
            'clustering': {
                'algorithm': 'hdbscan',
                'min_cluster_size': 3
            },
            'documents': {
                'formats': ['.md', '.markdown', '.txt']
            },
            'rag': {
                'provider': 'openai',
                'model': 'gpt-3.5-turbo'
            },
            'index': {
                'path': './data/index'
            }
        }
    
    def _setup_paths(self):
        """Create necessary directories"""
        base_path = Path(__file__).parent.parent
        
        # Create data directories
        data_dirs = [
            base_path / 'data' / 'documents',
            base_path / 'data' / 'index',
            base_path / 'data' / 'clusters',
            base_path / 'logs'
        ]
        
        for dir_path in data_dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get(self, key_path: str, default=None):
        """
        Get configuration value by dot-separated path
        
        Args:
            key_path: Dot-separated path (e.g., 'search.semantic.top_k')
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value by dot-separated path
        
        Args:
            key_path: Dot-separated path
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    @property
    def search_config(self) -> Dict[str, Any]:
        """Get search configuration"""
        return self.config.get('search', {})
    
    @property
    def clustering_config(self) -> Dict[str, Any]:
        """Get clustering configuration"""
        return self.config.get('clustering', {})
    
    @property
    def rag_config(self) -> Dict[str, Any]:
        """Get RAG configuration"""
        return self.config.get('rag', {})
    
    @property
    def index_path(self) -> Path:
        """Get index storage path"""
        path = self.get('index.path', './data/index')
        return Path(path).absolute()
