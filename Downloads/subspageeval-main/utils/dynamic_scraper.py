"""
Enhanced web scraper for dynamic pages using Playwright.
Includes visual scanning capabilities.
"""

import asyncio
import base64
import logging
from typing import Dict, Optional, Tuple
from pathlib import Path
from io import BytesIO

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from PIL import Image
import pytesseract
import cv2
import numpy as np

logger = logging.getLogger(__name__)


class DynamicScraper:
    """Scraper that handles JavaScript-rendered content and captures visual elements."""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.context = None
        
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def scrape_page(self, url: str, wait_for_selector: str = None) -> Dict:
        """
        Scrape a page with dynamic content handling.
        
        Args:
            url: URL to scrape
            wait_for_selector: CSS selector to wait for before extraction
            
        Returns:
            Dictionary with text content, screenshot, and metadata
        """
        page = await self.context.new_page()
        results = {
            'url': url,
            'text': '',
            'screenshot': None,
            'visual_text': '',
            'error': None,
            'metadata': {}
        }
        
        try:
            # Navigate with extended timeout
            await page.goto(url, wait_until='networkidle', timeout=60000)
            
            # Wait for specific element if provided
            if wait_for_selector:
                await page.wait_for_selector(wait_for_selector, timeout=30000)
            else:
                # Wait for common subscription elements
                try:
                    await page.wait_for_selector(
                        'text=/subscribe|subscription|membership|support|contribute/i',
                        timeout=10000
                    )
                except:
                    # Continue even if specific text not found
                    pass
            
            # Scroll to load lazy content
            await self._scroll_page(page)
            
            # Extract text from multiple sources
            text_content = await self._extract_all_text(page)
            results['text'] = text_content
            
            # Capture screenshot
            screenshot_buffer = await page.screenshot(full_page=True)
            results['screenshot'] = base64.b64encode(screenshot_buffer).decode('utf-8')
            
            # Extract visual text using OCR
            visual_text = await self._extract_visual_text(screenshot_buffer)
            results['visual_text'] = visual_text
            
            # Get page metadata
            results['metadata'] = await self._get_page_metadata(page)
            
            logger.info(f"Successfully scraped {url} - Text: {len(text_content)} chars, Visual: {len(visual_text)} chars")
            
        except PlaywrightTimeout:
            error_msg = f"Timeout while loading {url}"
            logger.error(error_msg)
            results['error'] = error_msg
        except Exception as e:
            error_msg = f"Error scraping {url}: {str(e)}"
            logger.error(error_msg)
            results['error'] = error_msg
        finally:
            await page.close()
            
        return results
    
    async def _scroll_page(self, page):
        """Scroll through the page to trigger lazy loading."""
        await page.evaluate("""
            async () => {
                const distance = 500;
                const delay = 100;
                const height = document.body.scrollHeight;
                
                for (let i = 0; i < height; i += distance) {
                    window.scrollBy(0, distance);
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
                
                // Scroll back to top
                window.scrollTo(0, 0);
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        """)
    
    async def _extract_all_text(self, page) -> str:
        """Extract text from various elements on the page."""
        # Get text from specific elements
        selectors = [
            'h1, h2, h3, h4, h5, h6',
            'p',
            'span',
            'div',
            'button',
            'a',
            'li',
            'label',
            '[class*="price"], [class*="cost"], [class*="amount"]',
            '[class*="subscribe"], [class*="membership"], [class*="support"]',
            '[class*="benefit"], [class*="feature"], [class*="perk"]'
        ]
        
        all_text = []
        
        for selector in selectors:
            try:
                elements = await page.query_selector_all(selector)
                for element in elements:
                    text = await element.text_content()
                    if text and text.strip():
                        all_text.append(text.strip())
            except:
                continue
        
        # Also get full page text as fallback
        try:
            body_text = await page.text_content('body')
            if body_text:
                all_text.append(body_text)
        except:
            pass
        
        # Deduplicate while preserving order
        seen = set()
        unique_text = []
        for text in all_text:
            if text not in seen:
                seen.add(text)
                unique_text.append(text)
        
        return '\n'.join(unique_text)
    
    async def _extract_visual_text(self, screenshot_buffer: bytes) -> str:
        """Extract text from screenshot using OCR."""
        try:
            # Convert screenshot buffer to image
            image = Image.open(BytesIO(screenshot_buffer))
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Preprocess for better OCR
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply adaptive threshold for better text detection
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Run OCR
            text = pytesseract.image_to_string(thresh)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return ""
    
    async def _get_page_metadata(self, page) -> Dict:
        """Extract page metadata."""
        metadata = {}
        
        try:
            metadata['title'] = await page.title()
            metadata['url'] = page.url
            
            # Get meta description
            meta_desc = await page.query_selector('meta[name="description"]')
            if meta_desc:
                metadata['description'] = await meta_desc.get_attribute('content')
            
            # Get pricing information
            pricing_data = await page.evaluate("""
                () => {
                    const priceRegex = /[$£€]\\d+\\.?\\d*/g;
                    const bodyText = document.body.innerText;
                    const prices = bodyText.match(priceRegex) || [];
                    return [...new Set(prices)];
                }
            """)
            metadata['prices'] = pricing_data
            
        except Exception as e:
            logger.error(f"Metadata extraction failed: {e}")
            
        return metadata


async def scrape_with_retry(url: str, max_retries: int = 3) -> Dict:
    """Scrape a URL with retries."""
    for attempt in range(max_retries):
        try:
            async with DynamicScraper() as scraper:
                return await scraper.scrape_page(url)
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return {
                    'url': url,
                    'text': '',
                    'screenshot': None,
                    'visual_text': '',
                    'error': str(e),
                    'metadata': {}
                }
            await asyncio.sleep(2 ** attempt)  # Exponential backoff


def scrape_page_dynamic(url: str) -> Tuple[str, Optional[str], Dict]:
    """
    Synchronous wrapper for async scraper.
    
    Returns:
        Tuple of (combined_text, screenshot_base64, metadata)
    """
    try:
        results = asyncio.run(scrape_with_retry(url))
        
        # Combine text from DOM and OCR
        dom_text = results.get('text', '')
        ocr_text = results.get('visual_text', '')
        
        # Merge texts intelligently
        combined_text = dom_text
        if ocr_text:
            # Add OCR text that's not already in DOM text
            ocr_lines = ocr_text.split('\n')
            for line in ocr_lines:
                if line.strip() and line.strip().lower() not in dom_text.lower():
                    combined_text += f"\n{line.strip()}"
        
        return combined_text, results.get('screenshot'), results.get('metadata', {})
        
    except Exception as e:
        logger.error(f"Dynamic scraping failed for {url}: {e}")
        return '', None, {}