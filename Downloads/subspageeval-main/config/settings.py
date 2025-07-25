"""
Configuration settings for the Subscription Page Analyzer.
Loads environment variables and validates required settings.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        self._validate_required_settings()
        self._setup_logging()
    
    # Anthropic API Configuration
    ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY', '')
    CLAUDE_MODEL: str = os.getenv('CLAUDE_MODEL', 'claude-3-sonnet-20240229')
    
    # Analysis Configuration
    ANALYSIS_MODE: str = os.getenv('ANALYSIS_MODE', 'claude_only')
    MAX_CONCURRENT_ANALYSES: int = int(os.getenv('MAX_CONCURRENT_ANALYSES', '3'))
    CACHE_ANALYSES: bool = os.getenv('CACHE_ANALYSES', 'true').lower() == 'true'
    CACHE_EXPIRY_HOURS: int = int(os.getenv('CACHE_EXPIRY_HOURS', '24'))
    
    # Flask Configuration
    FLASK_SECRET_KEY: str = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_DEBUG: bool = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    FLASK_PORT: int = int(os.getenv('FLASK_PORT', '5001'))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/analyzer.log')
    
    # Rate Limiting
    API_RATE_LIMIT_PER_MINUTE: int = int(os.getenv('API_RATE_LIMIT_PER_MINUTE', '60'))
    REQUEST_TIMEOUT_SECONDS: int = int(os.getenv('REQUEST_TIMEOUT_SECONDS', '120'))
    
    # Language Configuration  
    DEFAULT_LANGUAGE: str = os.getenv('DEFAULT_LANGUAGE', 'auto')
    _SUPPORTED_LANGUAGES_STR: str = os.getenv(
        'SUPPORTED_LANGUAGES', 
        'cs,pl,sk,hu,ro,de,es,fr,lt,lv,pt,nl,sv,da,fi,no,en'
    )
    
    # Parse supported languages
    SUPPORTED_LANGUAGES: List[str] = [lang.strip() for lang in _SUPPORTED_LANGUAGES_STR.split(',')]
    
    # Language name mapping
    LANGUAGE_NAMES: Dict[str, str] = {
        'cs': 'Czech',
        'pl': 'Polish', 
        'sk': 'Slovak',
        'hu': 'Hungarian',
        'ro': 'Romanian',
        'de': 'German',
        'es': 'Spanish',
        'fr': 'French',
        'lt': 'Lithuanian',
        'lv': 'Latvian',
        'pt': 'Portuguese',
        'nl': 'Dutch',
        'sv': 'Swedish',
        'da': 'Danish',
        'fi': 'Finnish',
        'no': 'Norwegian',
        'en': 'English',
        'auto': 'Auto-detect'
    }
    
    # File paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    CACHE_DIR: Path = PROJECT_ROOT / 'cache' / 'analyses'
    LOGS_DIR: Path = PROJECT_ROOT / 'logs'
    RESULTS_DIR: Path = PROJECT_ROOT / 'results'
    
    def _validate_required_settings(self):
        """Validate that all required settings are present."""
        if not self.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY is required. Please set it in your .env file or environment variables."
            )
        
        if not self.ANTHROPIC_API_KEY.startswith('sk-ant-'):
            raise ValueError(
                "ANTHROPIC_API_KEY appears to be invalid. It should start with 'sk-ant-'"
            )
        
        if self.CLAUDE_MODEL not in ['claude-3-sonnet-20240229', 'claude-3-opus-20240229', 'claude-3-haiku-20240307']:
            logging.warning(f"Unusual Claude model specified: {self.CLAUDE_MODEL}")
    
    def _setup_logging(self):
        """Set up logging configuration."""
        # Create logs directory if it doesn't exist
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Set up logging level
        log_level = getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.LOGS_DIR / 'analyzer.log'),
                logging.StreamHandler()
            ]
        )
    
    def create_directories(self):
        """Create necessary directories."""
        directories = [self.CACHE_DIR, self.LOGS_DIR, self.RESULTS_DIR]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_language_name(self, lang_code: str) -> str:
        """Get human-readable language name from code."""
        return self.LANGUAGE_NAMES.get(lang_code, lang_code.upper())
    
    def is_supported_language(self, lang_code: str) -> bool:
        """Check if a language code is supported."""
        return lang_code in self.SUPPORTED_LANGUAGES or lang_code == 'auto'

# Create global settings instance
settings = Settings()

# Create directories on import
settings.create_directories()