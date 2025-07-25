"""
Text processing functions for cleaning and preparing text for analysis.
"""

import re
from typing import List, Dict, Tuple
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
import logging

logger = logging.getLogger(__name__)

# Try to download required NLTK data
try:
    nltk.download('punkt', quiet=True)
except:
    pass


def clean_text(text: str) -> str:
    """
    Clean and normalize text for analysis.
    
    Args:
        text: Raw text from web scraping
        
    Returns:
        Cleaned text
    """
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Keep punctuation for now (needed for some patterns)
    return text


def tokenize_text(text: str) -> List[str]:
    """
    Tokenize text into words.
    
    Args:
        text: Text to tokenize
        
    Returns:
        List of tokens
    """
    try:
        tokens = word_tokenize(text.lower())
    except:
        # Fallback to simple tokenization if NLTK fails
        tokens = re.findall(r'\b\w+\b', text.lower())
    
    return tokens


def count_words(text: str) -> int:
    """
    Count total words in text.
    
    Args:
        text: Text to count words in
        
    Returns:
        Word count
    """
    tokens = tokenize_text(text)
    # Filter out very short tokens
    words = [t for t in tokens if len(t) > 1]
    return len(words)


def find_term_matches(text: str, terms: List[str]) -> Tuple[int, List[str]]:
    """
    Find matches for a list of terms in text.
    
    Args:
        text: Text to search in
        terms: List of terms to search for
        
    Returns:
        Tuple of (count, list of matched phrases)
    """
    text_lower = text.lower()
    matches = []
    
    for term in terms:
        term_lower = term.lower()
        # Use word boundaries for single words, exact match for phrases
        if ' ' in term:
            # Multi-word phrase
            pattern = re.escape(term_lower)
        else:
            # Single word with word boundaries
            pattern = r'\b' + re.escape(term_lower) + r'\b'
        
        found_matches = re.finditer(pattern, text_lower)
        for match in found_matches:
            # Extract context around the match (20 chars before and after)
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 20)
            context = text[start:end].strip()
            # Clean up context
            context = ' '.join(context.split())
            matches.append(context)
    
    return len(matches), matches[:10]  # Return top 10 examples


def find_pattern_matches(text: str, patterns: List[str]) -> Tuple[int, List[str]]:
    """
    Find matches for regex patterns in text.
    
    Args:
        text: Text to search in
        patterns: List of regex patterns
        
    Returns:
        Tuple of (count, list of matched phrases)
    """
    matches = []
    
    for pattern in patterns:
        try:
            found_matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in found_matches:
                matches.append(match.group(0))
        except re.error as e:
            logger.warning(f"Invalid regex pattern {pattern}: {e}")
    
    return len(matches), matches[:10]  # Return top 10 examples


def extract_sentences_with_terms(text: str, terms: List[str], max_sentences: int = 5) -> List[str]:
    """
    Extract full sentences containing specific terms.
    
    Args:
        text: Text to search in
        terms: Terms to look for
        max_sentences: Maximum number of sentences to return
        
    Returns:
        List of sentences
    """
    # Simple sentence splitting
    sentences = re.split(r'[.!?]+', text)
    matching_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        sentence_lower = sentence.lower()
        for term in terms:
            if term.lower() in sentence_lower:
                matching_sentences.append(sentence)
                break
        
        if len(matching_sentences) >= max_sentences:
            break
    
    return matching_sentences


def get_word_frequency(text: str, min_length: int = 4) -> Dict[str, int]:
    """
    Get frequency of words in text.
    
    Args:
        text: Text to analyze
        min_length: Minimum word length to include
        
    Returns:
        Dictionary of word frequencies
    """
    tokens = tokenize_text(text)
    # Filter out short words and common stop words
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'his', 'has', 'had', 'were', 'been', 'have', 'their', 'they', 'will', 'with', 'this', 'that', 'from', 'what', 'which', 'when', 'where', 'who', 'why', 'how'}
    
    filtered_tokens = [t for t in tokens if len(t) >= min_length and t not in stop_words]
    
    return dict(Counter(filtered_tokens).most_common(50))


def calculate_readability_metrics(text: str) -> Dict[str, float]:
    """
    Calculate basic readability metrics.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary of readability metrics
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    words = tokenize_text(text)
    words = [w for w in words if len(w) > 1]
    
    if not sentences or not words:
        return {
            'avg_sentence_length': 0,
            'avg_word_length': 0,
            'sentence_count': 0,
            'word_count': 0
        }
    
    avg_sentence_length = len(words) / len(sentences)
    avg_word_length = sum(len(w) for w in words) / len(words)
    
    return {
        'avg_sentence_length': round(avg_sentence_length, 2),
        'avg_word_length': round(avg_word_length, 2),
        'sentence_count': len(sentences),
        'word_count': len(words)
    }