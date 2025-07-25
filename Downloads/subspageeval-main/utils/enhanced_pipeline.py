"""
Enhanced analysis pipeline using Claude AI for multilingual subscription page analysis.
Replaces keyword-based analysis with AI-powered behavioral economics analysis.
"""

import logging
from typing import Dict, Optional
from datetime import datetime

from utils.claude_analyzer import ClaudeAnalyzer
from utils.text_processor import clean_text, count_words
from config.settings import settings

logger = logging.getLogger(__name__)


class EnhancedAnalysisPipeline:
    """
    Enhanced analysis pipeline that uses Claude AI for comprehensive
    multilingual behavioral economics analysis.
    """
    
    def __init__(self):
        """Initialize the enhanced pipeline with Claude analyzer."""
        self.claude_analyzer = ClaudeAnalyzer()
        logger.info("Enhanced analysis pipeline initialized")
    
    def analyze_text(self, text: str, publisher_name: str, language: str = 'auto') -> Dict:
        """
        Perform comprehensive analysis using Claude AI.
        
        Args:
            text: Cleaned text from subscription page
            publisher_name: Name of the publisher
            language: Language code (auto-detect if 'auto')
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        logger.info(f"Starting enhanced analysis for {publisher_name}")
        
        if not text or not text.strip():
            raise ValueError("Text content is empty or None")
        
        # Get total word count
        total_words = count_words(text)
        
        if total_words < 10:
            logger.warning(f"Very short content for {publisher_name}: {total_words} words")
        
        try:
            # Get Claude AI analysis
            claude_results = self.claude_analyzer.analyze_subscription_page(
                text, publisher_name, language
            )
            
            # Transform Claude results to match expected format
            transformed_results = self._transform_claude_results(claude_results, total_words)
            
            # Add pipeline metadata
            transformed_results.update({
                'analysis_pipeline': 'enhanced_claude',
                'pipeline_version': '2.0',
                'total_words': total_words,
                'analysis_timestamp': datetime.now().isoformat()
            })
            
            logger.info(f"Enhanced analysis completed for {publisher_name}")
            return transformed_results
            
        except Exception as e:
            logger.error(f"Enhanced analysis failed for {publisher_name}: {str(e)}")
            
            # Fallback to basic analysis structure
            return self._create_fallback_results(publisher_name, total_words, str(e))
    
    def _transform_claude_results(self, claude_results: Dict, total_words: int) -> Dict:
        """
        Transform Claude AI results to match the expected analysis format.
        
        Args:
            claude_results: Raw results from Claude analysis
            total_words: Total word count
            
        Returns:
            Transformed results dictionary
        """
        # Extract results with fallbacks
        motivation = claude_results.get('motivation_framework', {})
        behavioral = claude_results.get('behavioral_triggers', {})
        habit = claude_results.get('habit_formation', {})
        emotional = claude_results.get('emotional_appeals', {})
        cultural = claude_results.get('cultural_adaptations', {})
        
        # Calculate sophistication score (convert from 0-1 to 0-10 scale)
        sophistication_raw = claude_results.get('sophistication_score', 0.0)
        sophistication_score = min(max(sophistication_raw * 10, 0), 10)
        
        # Build transformed results
        results = {
            'publisher_name': claude_results.get('publisher_name', 'Unknown'),
            'detected_language': claude_results.get('detected_language', 'en'),
            'language_name': claude_results.get('language_name', 'English'),
            'total_words': total_words,
            
            # Motivation Framework (compatible with existing format)
            'motivation_framework': {
                'support_ratio': motivation.get('support_ratio', 0.0),
                'mission_density': motivation.get('mission_density', 0.0),
                'feature_density': motivation.get('feature_density', 0.0),
                'identity_score': motivation.get('identity_score', 0.0),
                'community_score': motivation.get('community_score', 0.0),
                'counts': motivation.get('counts', {
                    'support': 0, 'transactional': 0, 'mission': 0,
                    'feature': 0, 'identity': 0, 'community': 0
                }),
                'examples': motivation.get('examples', {
                    'support': [], 'transactional': [], 'mission': [],
                    'feature': [], 'identity': [], 'community': []
                })
            },
            
            # Behavioral Triggers (enhanced with authority)
            'behavioral_triggers': {
                'scarcity_score': behavioral.get('scarcity_score', 0.0),
                'social_proof_score': behavioral.get('social_proof_score', 0.0),
                'loss_aversion_score': behavioral.get('loss_aversion_score', 0.0),
                'reciprocity_score': behavioral.get('reciprocity_score', 0.0),
                'authority_score': behavioral.get('authority_score', 0.0),  # New
                'counts': behavioral.get('counts', {
                    'scarcity': 0, 'social_proof': 0, 'loss_aversion': 0,
                    'reciprocity': 0, 'authority': 0
                }),
                'examples': behavioral.get('examples', {
                    'scarcity': [], 'social_proof': [], 'loss_aversion': [],
                    'reciprocity': [], 'authority': []
                })
            },
            
            # Habit Formation (compatible with existing format)
            'habit_formation': {
                'temporal_score': habit.get('temporal_score', 0.0),
                'frequency_score': habit.get('frequency_score', 0.0),
                'convenience_score': habit.get('convenience_score', 0.0),
                'platform_score': habit.get('platform_score', 0.0),
                'counts': habit.get('counts', {
                    'temporal': 0, 'frequency': 0, 'convenience': 0, 'platform': 0
                }),
                'examples': habit.get('examples', {
                    'temporal': [], 'frequency': [], 'convenience': [], 'platform': []
                })
            },
            
            # New: Emotional Appeals
            'emotional_appeals': {
                'fear_score': emotional.get('fear_score', 0.0),
                'hope_score': emotional.get('hope_score', 0.0),
                'belonging_score': emotional.get('belonging_score', 0.0),
                'status_score': emotional.get('status_score', 0.0),
                'examples': emotional.get('examples', {
                    'fear': [], 'hope': [], 'belonging': [], 'status': []
                })
            },
            
            # New: Cultural Adaptations
            'cultural_adaptations': {
                'cultural_elements': cultural.get('cultural_elements', []),
                'local_references': cultural.get('local_references', []),
                'communication_style': cultural.get('communication_style', 'neutral'),
                'trust_building': cultural.get('trust_building', [])
            },
            
            # Overall scores and classification
            'sophistication_score': round(sophistication_score, 2),
            'primary_strategy': claude_results.get('primary_strategy', 'hybrid'),
            'key_insights': claude_results.get('key_insights', []),
            
            # Analysis metadata
            'analysis_method': 'claude_ai',
            'claude_model': claude_results.get('claude_model', settings.CLAUDE_MODEL),
            'analysis_timestamp': claude_results.get('analysis_timestamp', datetime.now().isoformat())
        }
        
        # Add readability metrics placeholder (for compatibility)
        results['readability_metrics'] = {
            'flesch_kincaid_grade': 0.0,
            'flesch_reading_ease': 0.0,
            'avg_sentence_length': 0.0,
            'note': 'Readability analysis not performed in Claude mode'
        }
        
        # Add key sentences (extract from examples)
        results['key_sentences'] = {
            'mission': self._extract_sentences_from_examples(
                motivation.get('examples', {}).get('mission', [])
            ),
            'value_prop': self._extract_sentences_from_examples(
                behavioral.get('examples', {}).get('reciprocity', []) +
                motivation.get('examples', {}).get('support', [])
            )
        }
        
        return results
    
    def _extract_sentences_from_examples(self, examples: list, max_sentences: int = 3) -> list:
        """
        Extract sentences from example quotes.
        
        Args:
            examples: List of example quotes
            max_sentences: Maximum number of sentences to return
            
        Returns:
            List of sentences
        """
        sentences = []
        for example in examples[:max_sentences]:
            if isinstance(example, str) and len(example.strip()) > 10:
                sentences.append(example.strip())
        
        return sentences[:max_sentences]
    
    def _create_fallback_results(self, publisher_name: str, total_words: int, error_msg: str) -> Dict:
        """
        Create fallback results structure when Claude analysis fails.
        
        Args:
            publisher_name: Publisher name
            total_words: Total word count
            error_msg: Error message
            
        Returns:
            Fallback results dictionary
        """
        logger.warning(f"Creating fallback results for {publisher_name}: {error_msg}")
        
        return {
            'publisher_name': publisher_name,
            'detected_language': 'en',
            'language_name': 'English',
            'total_words': total_words,
            'error': error_msg,
            'analysis_method': 'fallback',
            'analysis_timestamp': datetime.now().isoformat(),
            
            # Empty structure for compatibility
            'motivation_framework': {
                'support_ratio': 0.0,
                'mission_density': 0.0,
                'feature_density': 0.0,
                'identity_score': 0.0,
                'community_score': 0.0,
                'counts': {'support': 0, 'transactional': 0, 'mission': 0,
                          'feature': 0, 'identity': 0, 'community': 0},
                'examples': {'support': [], 'transactional': [], 'mission': [],
                           'feature': [], 'identity': [], 'community': []}
            },
            
            'behavioral_triggers': {
                'scarcity_score': 0.0,
                'social_proof_score': 0.0,
                'loss_aversion_score': 0.0,
                'reciprocity_score': 0.0,
                'authority_score': 0.0,
                'counts': {'scarcity': 0, 'social_proof': 0, 'loss_aversion': 0,
                          'reciprocity': 0, 'authority': 0},
                'examples': {'scarcity': [], 'social_proof': [], 'loss_aversion': [],
                           'reciprocity': [], 'authority': []}
            },
            
            'habit_formation': {
                'temporal_score': 0.0,
                'frequency_score': 0.0,
                'convenience_score': 0.0,
                'platform_score': 0.0,
                'counts': {'temporal': 0, 'frequency': 0, 'convenience': 0, 'platform': 0},
                'examples': {'temporal': [], 'frequency': [], 'convenience': [], 'platform': []}
            },
            
            'emotional_appeals': {
                'fear_score': 0.0,
                'hope_score': 0.0,
                'belonging_score': 0.0,
                'status_score': 0.0,
                'examples': {'fear': [], 'hope': [], 'belonging': [], 'status': []}
            },
            
            'cultural_adaptations': {
                'cultural_elements': [],
                'local_references': [],
                'communication_style': 'unknown',
                'trust_building': []
            },
            
            'sophistication_score': 0.0,
            'primary_strategy': 'unknown',
            'key_insights': [f"Analysis failed: {error_msg}"],
            
            'readability_metrics': {
                'flesch_kincaid_grade': 0.0,
                'flesch_reading_ease': 0.0,
                'avg_sentence_length': 0.0,
                'note': 'Analysis failed'
            },
            
            'key_sentences': {
                'mission': [],
                'value_prop': []
            }
        }
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get mapping of supported language codes to names.
        
        Returns:
            Dictionary mapping language codes to names
        """
        return settings.LANGUAGE_NAMES.copy()
    
    def clear_cache(self, max_age_hours: Optional[int] = None):
        """
        Clear analysis cache.
        
        Args:
            max_age_hours: Maximum age in hours
        """
        return self.claude_analyzer.clear_cache(max_age_hours)


# Global pipeline instance
enhanced_pipeline = EnhancedAnalysisPipeline()