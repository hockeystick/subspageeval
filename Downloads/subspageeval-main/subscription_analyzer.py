#!/usr/bin/env python3
"""
Subscription Page Linguistic Analyzer
Main script for analyzing behavioral economics principles in subscription pages.
"""

import csv
import argparse
import logging
import os
import sys
from datetime import datetime
from typing import List, Dict

from utils.enhanced_scraper import scrape_page_enhanced
from utils.text_processor import clean_text
from utils.analyzer import analyze_text
from utils.reporter import (
    save_individual_report,
    generate_comparative_csv,
    generate_summary_report,
    log_error,
    save_progress
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def read_input_csv(filepath: str) -> List[Dict[str, str]]:
    """
    Read publisher information from CSV file.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        List of dictionaries with publisher info
    """
    publishers = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'publisher_name' in row and 'subscription_url' in row:
                    publishers.append({
                        'name': row['publisher_name'].strip(),
                        'url': row['subscription_url'].strip(),
                        'language': row.get('language', 'en').strip()
                    })
        
        logger.info(f"Read {len(publishers)} publishers from {filepath}")
        return publishers
        
    except Exception as e:
        logger.error(f"Failed to read input CSV: {e}")
        return []


def process_publisher(publisher: Dict[str, str], output_dir: str) -> Dict:
    """
    Process a single publisher's subscription page.
    
    Args:
        publisher: Publisher information
        output_dir: Directory for output files
        
    Returns:
        Analysis results or None if failed
    """
    logger.info(f"Processing {publisher['name']}...")
    
    try:
        # Scrape the page with enhanced scraper
        text, screenshot, metadata = scrape_page_enhanced(publisher['url'])
        
        if not text:
            error_msg = f"Failed to scrape {publisher['name']} at {publisher['url']}"
            logger.error(error_msg)
            log_error(error_msg, output_dir)
            return None
        
        # Clean the text
        cleaned_text = clean_text(text)
        
        # Analyze the text
        results = analyze_text(cleaned_text, publisher['name'])
        results['url'] = publisher['url']
        results['language'] = publisher['language']
        results['screenshot'] = screenshot
        results['metadata'] = metadata
        
        # Save individual report
        save_individual_report(results, output_dir)
        
        return results
        
    except Exception as e:
        error_msg = f"Error processing {publisher['name']}: {str(e)}"
        logger.error(error_msg)
        log_error(error_msg, output_dir)
        return None


def main():
    """Main function to orchestrate the analysis."""
    parser = argparse.ArgumentParser(
        description='Analyze subscription pages for behavioral economics principles'
    )
    parser.add_argument(
        '--input',
        default='subscription_pages.csv',
        help='Input CSV file with publisher information'
    )
    parser.add_argument(
        '--output',
        default='results',
        help='Output directory for results'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of publishers to process (for testing)'
    )
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Read input publishers
    publishers = read_input_csv(args.input)
    
    if not publishers:
        logger.error("No publishers found in input file")
        return
    
    # Apply limit if specified
    if args.limit:
        publishers = publishers[:args.limit]
        logger.info(f"Limited to {len(publishers)} publishers")
    
    # Process each publisher
    all_results = []
    failed_count = 0
    
    start_time = datetime.now()
    
    for i, publisher in enumerate(publishers, 1):
        logger.info(f"Processing {i}/{len(publishers)}: {publisher['name']}")
        
        results = process_publisher(publisher, args.output)
        
        if results:
            all_results.append(results)
            # Save progress after each successful analysis
            save_progress({
                'processed': i,
                'total': len(publishers),
                'successful': len(all_results),
                'failed': failed_count
            }, args.output)
        else:
            failed_count += 1
        
        # Log progress
        if i % 5 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = i / elapsed * 60  # publishers per minute
            logger.info(f"Progress: {i}/{len(publishers)} ({rate:.1f} publishers/min)")
    
    # Generate comparative reports
    if all_results:
        logger.info("Generating comparative analysis...")
        generate_comparative_csv(all_results, args.output)
        generate_summary_report(all_results, args.output)
    
    # Final summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logger.info("=" * 50)
    logger.info(f"Analysis complete!")
    logger.info(f"Total publishers: {len(publishers)}")
    logger.info(f"Successful: {len(all_results)}")
    logger.info(f"Failed: {failed_count}")
    logger.info(f"Duration: {duration/60:.1f} minutes")
    logger.info(f"Results saved to: {args.output}/")
    logger.info("=" * 50)


if __name__ == '__main__':
    main()