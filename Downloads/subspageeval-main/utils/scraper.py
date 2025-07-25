"""
Web scraping functions for extracting text from subscription pages.
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import Optional, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_page(url: str, max_retries: int = 3, timeout: int = 30) -> Optional[str]:
    """
    Scrape text content from a subscription page.
    
    Args:
        url: The URL to scrape
        max_retries: Maximum number of retry attempts
        timeout: Request timeout in seconds
        
    Returns:
        Cleaned text content or None if failed
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Scraping {url} (attempt {attempt + 1}/{max_retries})")
            
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'meta', 'link', 'noscript']):
                script.decompose()
            
            # Extract text from relevant tags
            text_elements = []
            target_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div', 'button', 'a', 'li', 'label']
            
            for tag in target_tags:
                elements = soup.find_all(tag)
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and len(text) > 2:  # Skip very short text
                        text_elements.append(text)
            
            # Join all text elements
            full_text = ' '.join(text_elements)
            
            # Clean up whitespace
            full_text = ' '.join(full_text.split())
            
            if len(full_text) < 100:
                logger.warning(f"Suspiciously short content from {url}: {len(full_text)} characters")
            
            logger.info(f"Successfully scraped {url}: {len(full_text)} characters")
            return full_text
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error for {url} (attempt {attempt + 1})")
            time.sleep(2 ** attempt)  # Exponential backoff
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url} (attempt {attempt + 1}): {str(e)}")
            time.sleep(2 ** attempt)
            
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {str(e)}")
            return None
    
    logger.error(f"Failed to scrape {url} after {max_retries} attempts")
    return None


def extract_metadata(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Extract metadata from the page if available.
    
    Args:
        soup: BeautifulSoup object of the page
        
    Returns:
        Dictionary of metadata
    """
    metadata = {}
    
    # Try to get page title
    title_tag = soup.find('title')
    if title_tag:
        metadata['title'] = title_tag.get_text(strip=True)
    
    # Try to get meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        metadata['description'] = meta_desc.get('content', '')
    
    # Try to get Open Graph data
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    if og_title:
        metadata['og_title'] = og_title.get('content', '')
    
    return metadata


def save_raw_html(url: str, output_path: str) -> bool:
    """
    Save raw HTML for testing purposes.
    
    Args:
        url: The URL to fetch
        output_path: Path to save the HTML file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        logger.info(f"Saved HTML from {url} to {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save HTML from {url}: {str(e)}")
        return False