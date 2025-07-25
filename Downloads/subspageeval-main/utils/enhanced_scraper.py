"""
Enhanced scraper that combines static and dynamic scraping with visual analysis.
"""

import logging
from typing import Optional, Tuple, Dict
from .scraper import scrape_page as scrape_static
from .dynamic_scraper import scrape_page_dynamic

logger = logging.getLogger(__name__)


def scrape_page_enhanced(url: str) -> Tuple[Optional[str], Optional[str], Dict]:
    """
    Enhanced scraping that tries static first, then falls back to dynamic.
    
    Returns:
        Tuple of (text_content, screenshot_base64, metadata)
    """
    logger.info(f"Starting enhanced scraping for {url}")
    
    # First try static scraping
    static_text = scrape_static(url)
    
    if static_text and len(static_text) > 500:
        # Static scraping worked well
        logger.info(f"Static scraping successful for {url}")
        return static_text, None, {}
    
    # Static scraping didn't get much content, try dynamic
    logger.info(f"Falling back to dynamic scraping for {url}")
    dynamic_text, screenshot, metadata = scrape_page_dynamic(url)
    
    # Combine static and dynamic results if both have content
    if static_text and dynamic_text:
        # Use dynamic as base and add unique content from static
        combined_text = dynamic_text
        static_lower = static_text.lower()
        dynamic_lower = dynamic_text.lower()
        
        # Add static content not in dynamic
        for sentence in static_text.split('.'):
            if sentence.strip() and sentence.strip().lower() not in dynamic_lower:
                combined_text += f" {sentence.strip()}."
        
        return combined_text, screenshot, metadata
    
    # Return whichever has content
    return dynamic_text or static_text or '', screenshot, metadata