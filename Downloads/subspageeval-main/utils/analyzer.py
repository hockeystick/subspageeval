"""
Enhanced linguistic analysis engine for subscription pages.
Now uses Claude AI for multilingual behavioral economics analysis.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
import logging
from datetime import datetime

from utils.enhanced_pipeline import enhanced_pipeline
from config.settings import settings

logger = logging.getLogger(__name__)


def analyze_text(text: str, publisher_name: str, language: str = 'auto') -> Dict:
    """
    Perform comprehensive linguistic analysis on subscription page text using Claude AI.
    
    Args:
        text: Cleaned text from subscription page
        publisher_name: Name of the publisher
        language: Language code (auto-detect if 'auto')
        
    Returns:
        Dictionary containing all analysis results
    """
    logger.info(f"Starting Claude-powered analysis for {publisher_name} (language: {language})")
    
    try:
        # Use enhanced pipeline for Claude analysis
        results = enhanced_pipeline.analyze_text(text, publisher_name, language)
        
        # Add any backward compatibility adjustments
        results = _ensure_backward_compatibility(results)
        
        logger.info(f"Claude analysis completed for {publisher_name}")
        return results
        
    except Exception as e:
        logger.error(f"Analysis failed for {publisher_name}: {str(e)}")
        raise


def _ensure_backward_compatibility(results: Dict) -> Dict:
    """
    Ensure backward compatibility with existing code that expects certain fields.
    
    Args:
        results: Analysis results from enhanced pipeline
        
    Returns:
        Results with backward compatibility adjustments
    """
    # Ensure timestamp field exists (some code might expect 'timestamp' instead of 'analysis_timestamp')
    if 'analysis_timestamp' in results and 'timestamp' not in results:
        results['timestamp'] = results['analysis_timestamp']
    
    # Ensure word_frequency exists (even if empty for Claude analysis)
    if 'word_frequency' not in results:
        results['word_frequency'] = {}
    
    # Ensure pricing_mentions exists for compatibility
    if 'pricing_mentions' not in results:
        results['pricing_mentions'] = {
            'count': 0,
            'examples': [],
            'note': 'Pricing analysis not performed in Claude mode'
        }
    
    return results


def calculate_sophistication_score(results: Dict) -> float:
    """
    Calculate overall sophistication score based on various metrics.
    This function is maintained for backward compatibility but the Claude pipeline
    already calculates sophistication scores.
    
    Args:
        results: Analysis results dictionary
        
    Returns:
        Sophistication score (0-10 scale)
    """
    # Return the Claude-calculated score if available
    if 'sophistication_score' in results:
        return results['sophistication_score']
    
    # Fallback calculation (should not be needed with Claude analysis)
    logger.warning("Using fallback sophistication score calculation")
    
    # Weights for different components
    weights = {
        'motivation': 0.3,
        'behavioral': 0.3,
        'habit': 0.2,
        'emotional': 0.1,
        'balance': 0.1
    }
    
    # Motivation component
    mot = results.get('motivation_framework', {})
    motivation_score = (
        mot.get('support_ratio', 0) * 2 +  # Favor support over transactional
        mot.get('mission_density', 0) * 100 +
        mot.get('identity_score', 0) * 100 +
        mot.get('community_score', 0) * 100
    ) / 4
    
    # Behavioral component
    beh = results.get('behavioral_triggers', {})
    behavioral_score = (
        beh.get('scarcity_score', 0) * 50 +
        beh.get('social_proof_score', 0) * 100 +
        beh.get('loss_aversion_score', 0) * 50 +
        beh.get('reciprocity_score', 0) * 100 +
        beh.get('authority_score', 0) * 75  # New authority component
    ) / 5
    
    # Habit component
    hab = results.get('habit_formation', {})
    habit_score = (
        hab.get('temporal_score', 0) * 100 +
        hab.get('frequency_score', 0) * 100 +
        hab.get('convenience_score', 0) * 100 +
        hab.get('platform_score', 0) * 100
    ) / 4
    
    # Emotional component (new)
    emo = results.get('emotional_appeals', {})
    emotional_score = (
        emo.get('fear_score', 0) * 50 +
        emo.get('hope_score', 0) * 75 +
        emo.get('belonging_score', 0) * 100 +
        emo.get('status_score', 0) * 75
    ) / 4
    
    # Balance component (diversity of approaches)
    non_zero_scores = 0
    for category in [mot, beh, hab, emo]:
        for score_name, score in category.items():
            if score_name.endswith('_score') and score > 0:
                non_zero_scores += 1
    
    balance_score = min(non_zero_scores / 16 * 10, 10)  # 16 total score types now
    
    # Calculate weighted total
    total = (
        motivation_score * weights['motivation'] +
        behavioral_score * weights['behavioral'] +
        habit_score * weights['habit'] +
        emotional_score * weights['emotional'] +
        balance_score * weights['balance']
    )
    
    # Normalize to 0-10 scale
    return min(max(total, 0), 10)


def classify_strategy(results: Dict) -> str:
    """
    Classify the primary marketing strategy based on analysis.
    
    Args:
        results: Analysis results dictionary
        
    Returns:
        Strategy classification
    """
    # Return Claude classification if available
    if 'primary_strategy' in results:
        return results['primary_strategy']
    
    # Fallback classification
    logger.warning("Using fallback strategy classification")
    
    mot = results.get('motivation_framework', {})
    
    # Calculate strategy indicators
    mission_strength = (
        mot.get('mission_density', 0) + 
        mot.get('community_score', 0) + 
        mot.get('support_ratio', 0)
    )
    feature_strength = mot.get('feature_density', 0) + (1 - mot.get('support_ratio', 0))
    
    # Check for behavioral triggers
    beh = results.get('behavioral_triggers', {})
    behavioral_strength = sum([
        beh.get('scarcity_score', 0),
        beh.get('social_proof_score', 0),
        beh.get('loss_aversion_score', 0),
        beh.get('authority_score', 0)
    ])
    
    # Classify
    if mission_strength > feature_strength * 1.5:
        if behavioral_strength > 0.01:
            return "mission-driven-sophisticated"
        else:
            return "mission-driven-basic"
    elif feature_strength > mission_strength * 1.5:
        if behavioral_strength > 0.01:
            return "feature-driven-sophisticated"
        else:
            return "feature-driven-basic"
    else:
        if behavioral_strength > 0.02:
            return "hybrid-sophisticated"
        else:
            return "hybrid-basic"


def get_innovation_indicators(results: Dict) -> List[str]:
    """
    Identify innovative or unique approaches in the marketing copy.
    
    Args:
        results: Analysis results dictionary
        
    Returns:
        List of innovation indicators
    """
    # Use Claude insights if available
    if 'key_insights' in results:
        return results['key_insights']
    
    # Fallback innovation detection
    innovations = []
    
    mot = results.get('motivation_framework', {})
    beh = results.get('behavioral_triggers', {})
    hab = results.get('habit_formation', {})
    emo = results.get('emotional_appeals', {})
    cultural = results.get('cultural_adaptations', {})
    
    # Check for high community focus
    if mot.get('community_score', 0) > 0.02:
        innovations.append("Strong community emphasis")
    
    # Check for sophisticated social proof
    if beh.get('counts', {}).get('social_proof', 0) > 5:
        innovations.append("Extensive social proof usage")
    
    # Check for habit formation focus
    habit_total = sum(hab.get('counts', {}).values())
    if habit_total > 10:
        innovations.append("Strong habit formation strategy")
    
    # Check for reciprocity emphasis
    if beh.get('reciprocity_score', 0) > 0.01:
        innovations.append("Reciprocity-based messaging")
    
    # Check for multi-platform emphasis
    if hab.get('platform_score', 0) > 0.01:
        innovations.append("Multi-platform accessibility focus")
    
    # Check for emotional sophistication
    if emo.get('belonging_score', 0) > 0.01:
        innovations.append("Strong belonging and identity appeals")
    
    # Check for cultural adaptations
    if cultural.get('cultural_elements'):
        innovations.append(f"Cultural adaptation: {cultural.get('communication_style', 'localized')}")
    
    return innovations


def get_supported_languages() -> Dict[str, str]:
    """
    Get mapping of supported language codes to names.
    
    Returns:
        Dictionary mapping language codes to names
    """
    return enhanced_pipeline.get_supported_languages()


def clear_analysis_cache(max_age_hours: int = None):
    """
    Clear analysis cache.
    
    Args:
        max_age_hours: Maximum age in hours (use settings default if None)
    """
    return enhanced_pipeline.clear_cache(max_age_hours)


# Maintain backward compatibility for direct function imports
def analyze_subscription_page(text: str, publisher_name: str, language: str = 'auto') -> Dict:
    """
    Backward compatibility function for direct analysis calls.
    
    Args:
        text: Text to analyze
        publisher_name: Publisher name
        language: Language code
        
    Returns:
        Analysis results
    """
    return analyze_text(text, publisher_name, language)