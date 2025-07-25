"""
Claude AI-powered analyzer for subscription page linguistic analysis.
Supports multilingual analysis across 17 European languages.
"""

import json
import hashlib
import logging
import asyncio
import time
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

import anthropic
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException as LangDetectError

from config.settings import settings

logger = logging.getLogger(__name__)


class ClaudeAnalyzer:
    """
    Claude AI-powered analyzer for subscription page text analysis.
    Supports behavioral economics analysis in multiple languages.
    """
    
    def __init__(self):
        """Initialize the Claude analyzer with API client."""
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.cache_dir = settings.CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 60 / settings.API_RATE_LIMIT_PER_MINUTE
        
        logger.info(f"Claude analyzer initialized with model: {settings.CLAUDE_MODEL}")
    
    def analyze_subscription_page(self, text: str, publisher_name: str, language: str = 'auto') -> Dict:
        """
        Analyze subscription page text using Claude AI.
        
        Args:
            text: Text content from subscription page
            publisher_name: Name of the publisher
            language: Language code (auto-detect if 'auto')
            
        Returns:
            Dict containing comprehensive analysis results
        """
        logger.info(f"Starting Claude analysis for {publisher_name} (language: {language})")
        
        # Check cache first
        if settings.CACHE_ANALYSES:
            cached_result = self._get_cached_analysis(text, publisher_name, language)
            if cached_result:
                logger.info(f"Retrieved cached analysis for {publisher_name}")
                return cached_result
        
        # Detect language if needed
        if language == 'auto':
            language = self._detect_language(text)
        
        # Validate language support
        if not settings.is_supported_language(language):
            language = 'en'  # Fallback to English
            logger.warning(f"Unsupported language detected, falling back to English")
        
        # Rate limiting
        self._handle_rate_limiting()
        
        try:
            # Get analysis from Claude
            analysis_result = self._call_claude_api(text, publisher_name, language)
            
            # Add metadata
            analysis_result.update({
                'publisher_name': publisher_name,
                'detected_language': language,
                'language_name': settings.get_language_name(language),
                'analysis_timestamp': datetime.now().isoformat(),
                'analysis_method': 'claude_ai',
                'claude_model': settings.CLAUDE_MODEL
            })
            
            # Cache the results
            if settings.CACHE_ANALYSES:
                self._cache_analysis(text, publisher_name, language, analysis_result)
            
            logger.info(f"Completed Claude analysis for {publisher_name}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Claude analysis failed for {publisher_name}: {str(e)}")
            raise
    
    def _detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code (ISO 639-1)
        """
        try:
            # Clean text for better detection
            clean_text = text.strip()[:1000]  # Use first 1000 chars for detection
            
            if len(clean_text) < 50:
                logger.warning("Text too short for reliable language detection")
                return 'en'
            
            detected_lang = detect(clean_text)
            
            # Map some common variations
            lang_mapping = {
                'ca': 'es',  # Catalan -> Spanish
                'gl': 'es',  # Galician -> Spanish
                'eu': 'es',  # Basque -> Spanish
            }
            
            detected_lang = lang_mapping.get(detected_lang, detected_lang)
            
            if detected_lang in settings.SUPPORTED_LANGUAGES:
                logger.info(f"Detected language: {detected_lang}")
                return detected_lang
            else:
                logger.warning(f"Detected unsupported language: {detected_lang}, using English")
                return 'en'
                
        except LangDetectError as e:
            logger.warning(f"Language detection failed: {e}, using English")
            return 'en'
    
    def _handle_rate_limiting(self):
        """Handle API rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _call_claude_api(self, text: str, publisher_name: str, language: str) -> Dict:
        """
        Make API call to Claude for text analysis.
        
        Args:
            text: Text to analyze
            publisher_name: Publisher name
            language: Language code
            
        Returns:
            Analysis results dictionary
        """
        prompt = self._build_analysis_prompt(text, publisher_name, language)
        
        try:
            response = self.client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=4000,
                temperature=0.1,  # Low temperature for consistent analysis
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse the JSON response
            response_text = response.content[0].text
            
            # Extract JSON from response (handle cases where Claude adds explanatory text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in Claude response")
            
            json_content = response_text[json_start:json_end]
            analysis_result = json.loads(json_content)
            
            return analysis_result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {e}")
            logger.debug(f"Raw response: {response_text[:500]}...")
            raise ValueError(f"Invalid JSON response from Claude: {e}")
        
        except Exception as e:
            logger.error(f"Claude API call failed: {e}")
            raise
    
    def _build_analysis_prompt(self, text: str, publisher_name: str, language: str) -> str:
        """
        Build the analysis prompt for Claude.
        
        Args:
            text: Text to analyze
            publisher_name: Publisher name
            language: Language code
            
        Returns:
            Formatted prompt string
        """
        language_name = settings.get_language_name(language)
        
        # Cultural context for different language families
        cultural_context = self._get_cultural_context(language)
        
        prompt = f"""
You are an expert in behavioral economics and multilingual marketing analysis. Analyze this subscription page text from {publisher_name}.

The text is in {language_name} ({language}). {cultural_context}

TEXT TO ANALYZE:
{text}

Analyze the text for behavioral economics principles and return ONLY a valid JSON object with this exact structure:

{{
    "motivation_framework": {{
        "support_ratio": 0.0,
        "mission_density": 0.0,
        "feature_density": 0.0,
        "identity_score": 0.0,
        "community_score": 0.0,
        "counts": {{
            "support": 0,
            "transactional": 0,
            "mission": 0,
            "feature": 0,
            "identity": 0,
            "community": 0
        }},
        "examples": {{
            "support": ["example quotes"],
            "transactional": ["example quotes"],
            "mission": ["example quotes"],
            "feature": ["example quotes"],
            "identity": ["example quotes"],
            "community": ["example quotes"]
        }}
    }},
    "behavioral_triggers": {{
        "scarcity_score": 0.0,
        "social_proof_score": 0.0,
        "loss_aversion_score": 0.0,
        "reciprocity_score": 0.0,
        "authority_score": 0.0,
        "counts": {{
            "scarcity": 0,
            "social_proof": 0,
            "loss_aversion": 0,
            "reciprocity": 0,
            "authority": 0
        }},
        "examples": {{
            "scarcity": ["example quotes"],
            "social_proof": ["example quotes"],
            "loss_aversion": ["example quotes"],
            "reciprocity": ["example quotes"],
            "authority": ["example quotes"]
        }}
    }},
    "habit_formation": {{
        "temporal_score": 0.0,
        "frequency_score": 0.0,
        "convenience_score": 0.0,
        "platform_score": 0.0,
        "counts": {{
            "temporal": 0,
            "frequency": 0,
            "convenience": 0,
            "platform": 0
        }},
        "examples": {{
            "temporal": ["example quotes"],
            "frequency": ["example quotes"],
            "convenience": ["example quotes"],
            "platform": ["example quotes"]
        }}
    }},
    "emotional_appeals": {{
        "fear_score": 0.0,
        "hope_score": 0.0,
        "belonging_score": 0.0,
        "status_score": 0.0,
        "examples": {{
            "fear": ["example quotes"],
            "hope": ["example quotes"],
            "belonging": ["example quotes"],
            "status": ["example quotes"]
        }}
    }},
    "cultural_adaptations": {{
        "cultural_elements": ["list of culture-specific elements"],
        "local_references": ["local cultural references"],
        "communication_style": "direct/indirect/formal/informal",
        "trust_building": ["trust-building elements specific to this culture"]
    }},
    "total_words": 0,
    "sophistication_score": 0.0,
    "primary_strategy": "mission-driven/feature-driven/hybrid",
    "key_insights": ["3-5 key insights about the strategy"]
}}

SCORING GUIDELINES:
- All scores should be between 0.0 and 1.0
- support_ratio: Ratio of support language vs transactional language
- Density scores: Count of relevant terms / total words
- Sophistication score: Overall marketing sophistication (0-10 scale, but return as 0.0-1.0)
- Include actual quotes from the text in examples arrays
- Provide counts of relevant terms found
- Focus on culture-specific persuasion techniques for {language_name}

Return ONLY the JSON object, no additional text or explanation.
"""
        
        return prompt.strip()
    
    def _get_cultural_context(self, language: str) -> str:
        """
        Get cultural context prompt for different languages.
        
        Args:
            language: Language code
            
        Returns:
            Cultural context string
        """
        contexts = {
            'de': "Pay attention to German directness, engineering precision references, and Ordnung (order) concepts.",
            'fr': "Look for French formality, intellectual appeals, and cultural sophistication references.",
            'es': "Notice Spanish community emphasis, family values, and relationship-building language.",
            'pt': "Look for Portuguese warmth, personal connection, and community-focused messaging.",
            'nl': "Pay attention to Dutch pragmatism, consensus-building, and egalitarian values.",
            'sv': "Notice Swedish minimalism, environmental consciousness, and collective welfare themes.",
            'da': "Look for Danish hygge concepts, work-life balance, and trust-based society references.",
            'no': "Pay attention to Norwegian nature connections, egalitarian values, and quality of life themes.",
            'fi': "Notice Finnish practicality, education values, and reserved but trustworthy communication.",
            'pl': "Look for Polish tradition respect, community solidarity, and historical awareness.",
            'cs': "Pay attention to Czech skepticism, intellectual heritage, and European identity themes.",
            'sk': "Notice Slovak community focus, cultural preservation, and regional identity elements.",
            'hu': "Look for Hungarian uniqueness emphasis, cultural pride, and intellectual tradition.",
            'ro': "Pay attention to Romanian family values, cultural richness, and European integration themes.",
            'lt': "Notice Lithuanian independence values, cultural resilience, and Baltic identity.",
            'lv': "Look for Latvian cultural preservation, nature connection, and independence themes."
        }
        
        return contexts.get(language, "Analyze using general European cultural contexts.")
    
    def _get_cache_key(self, text: str, publisher_name: str, language: str) -> str:
        """
        Generate cache key for analysis results.
        
        Args:
            text: Text content
            publisher_name: Publisher name
            language: Language code
            
        Returns:
            Cache key string
        """
        content = f"{text}|{publisher_name}|{language}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cached_analysis(self, text: str, publisher_name: str, language: str) -> Optional[Dict]:
        """
        Retrieve cached analysis if available and not expired.
        
        Args:
            text: Text content
            publisher_name: Publisher name  
            language: Language code
            
        Returns:
            Cached analysis results or None
        """
        cache_key = self._get_cache_key(text, publisher_name, language)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Check if cache is expired
            cache_time = datetime.fromisoformat(cached_data.get('cache_timestamp', ''))
            expiry_time = cache_time + timedelta(hours=settings.CACHE_EXPIRY_HOURS)
            
            if datetime.now() > expiry_time:
                cache_file.unlink()  # Delete expired cache
                return None
            
            return cached_data.get('analysis_result')
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"Invalid cache file {cache_file}: {e}")
            cache_file.unlink()  # Delete corrupted cache
            return None
    
    def _cache_analysis(self, text: str, publisher_name: str, language: str, result: Dict):
        """
        Cache analysis results.
        
        Args:
            text: Text content
            publisher_name: Publisher name
            language: Language code
            result: Analysis results to cache
        """
        cache_key = self._get_cache_key(text, publisher_name, language)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        cache_data = {
            'cache_timestamp': datetime.now().isoformat(),
            'publisher_name': publisher_name,
            'language': language,
            'analysis_result': result
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Cached analysis for {publisher_name}")
        except Exception as e:
            logger.warning(f"Failed to cache analysis: {e}")
    
    def clear_cache(self, max_age_hours: Optional[int] = None):
        """
        Clear expired cache files.
        
        Args:
            max_age_hours: Maximum age in hours (use settings default if None)
        """
        if max_age_hours is None:
            max_age_hours = settings.CACHE_EXPIRY_HOURS
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        cleared_count = 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                cache_time = datetime.fromisoformat(cached_data.get('cache_timestamp', ''))
                
                if cache_time < cutoff_time:
                    cache_file.unlink()
                    cleared_count += 1
                    
            except Exception as e:
                logger.warning(f"Error processing cache file {cache_file}: {e}")
                cache_file.unlink()  # Delete corrupted files
                cleared_count += 1
        
        logger.info(f"Cleared {cleared_count} expired cache files")
        return cleared_count