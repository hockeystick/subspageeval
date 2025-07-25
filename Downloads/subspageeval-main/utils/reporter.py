"""
Report generation functions for subscription page analysis.
"""

import json
import csv
import os
from typing import List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def save_individual_report(results: Dict, output_dir: str) -> bool:
    """
    Save individual publisher analysis as JSON.
    
    Args:
        results: Analysis results for a publisher
        output_dir: Directory to save reports
        
    Returns:
        True if successful
    """
    try:
        publisher_name = results['publisher_name'].replace(' ', '_').replace('/', '_')
        filename = f"{publisher_name}_analysis.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved individual report to {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save individual report: {e}")
        return False


def generate_comparative_csv(all_results: List[Dict], output_dir: str) -> bool:
    """
    Generate comparative analysis CSV file.
    
    Args:
        all_results: List of all publisher analysis results
        output_dir: Directory to save the CSV
        
    Returns:
        True if successful
    """
    try:
        filepath = os.path.join(output_dir, 'comparative_analysis.csv')
        
        # Sort by sophistication score
        all_results.sort(key=lambda x: x.get('sophistication_score', 0), reverse=True)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            # Define fieldnames
            fieldnames = [
                'publisher_name',
                'sophistication_score',
                'primary_strategy',
                'total_words',
                # Motivation scores
                'support_ratio',
                'mission_density',
                'feature_density',
                'identity_score',
                'community_score',
                # Behavioral scores
                'scarcity_score',
                'social_proof_score',
                'loss_aversion_score',
                'reciprocity_score',
                # Habit scores
                'temporal_score',
                'frequency_score',
                'convenience_score',
                'platform_score',
                # Counts
                'support_count',
                'transactional_count',
                'mission_count',
                'scarcity_count',
                'social_proof_count',
                'price_mentions'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in all_results:
                row = {
                    'publisher_name': result['publisher_name'],
                    'sophistication_score': result['sophistication_score'],
                    'primary_strategy': result['primary_strategy'],
                    'total_words': result['total_words'],
                    # Motivation scores
                    'support_ratio': result['motivation_framework']['support_ratio'],
                    'mission_density': result['motivation_framework']['mission_density'],
                    'feature_density': result['motivation_framework']['feature_density'],
                    'identity_score': result['motivation_framework']['identity_score'],
                    'community_score': result['motivation_framework']['community_score'],
                    # Behavioral scores
                    'scarcity_score': result['behavioral_triggers']['scarcity_score'],
                    'social_proof_score': result['behavioral_triggers']['social_proof_score'],
                    'loss_aversion_score': result['behavioral_triggers']['loss_aversion_score'],
                    'reciprocity_score': result['behavioral_triggers']['reciprocity_score'],
                    # Habit scores
                    'temporal_score': result['habit_formation']['temporal_score'],
                    'frequency_score': result['habit_formation']['frequency_score'],
                    'convenience_score': result['habit_formation']['convenience_score'],
                    'platform_score': result['habit_formation']['platform_score'],
                    # Counts
                    'support_count': result['motivation_framework']['counts']['support'],
                    'transactional_count': result['motivation_framework']['counts']['transactional'],
                    'mission_count': result['motivation_framework']['counts']['mission'],
                    'scarcity_count': result['behavioral_triggers']['counts']['scarcity'],
                    'social_proof_count': result['behavioral_triggers']['counts']['social_proof'],
                    'price_mentions': result['pricing_mentions']['count']
                }
                writer.writerow(row)
        
        logger.info(f"Saved comparative CSV to {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to generate comparative CSV: {e}")
        return False


def generate_summary_report(all_results: List[Dict], output_dir: str) -> bool:
    """
    Generate markdown summary report with insights.
    
    Args:
        all_results: List of all publisher analysis results
        output_dir: Directory to save the report
        
    Returns:
        True if successful
    """
    try:
        filepath = os.path.join(output_dir, 'subscription_language_analysis_report.md')
        
        # Sort by sophistication score
        all_results.sort(key=lambda x: x.get('sophistication_score', 0), reverse=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write("# Subscription Language Analysis Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            f.write(f"Analyzed {len(all_results)} publisher subscription pages to identify behavioral economics principles in marketing copy.\n\n")
            
            # Key findings
            f.write("### Key Findings\n\n")
            
            # Average scores
            avg_sophistication = sum(r['sophistication_score'] for r in all_results) / len(all_results)
            f.write(f"- **Average Sophistication Score**: {avg_sophistication:.2f}/10\n")
            
            # Strategy distribution
            strategies = {}
            for r in all_results:
                strategy = r['primary_strategy']
                strategies[strategy] = strategies.get(strategy, 0) + 1
            
            f.write("- **Strategy Distribution**:\n")
            for strategy, count in sorted(strategies.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(all_results)) * 100
                f.write(f"  - {strategy}: {count} ({percentage:.1f}%)\n")
            
            # Top performers
            f.write("\n### Top 5 Most Sophisticated Publishers\n\n")
            f.write("| Rank | Publisher | Score | Primary Strategy |\n")
            f.write("|------|-----------|-------|------------------|\n")
            for i, result in enumerate(all_results[:5], 1):
                f.write(f"| {i} | {result['publisher_name']} | {result['sophistication_score']:.2f} | {result['primary_strategy']} |\n")
            
            # Innovation highlights
            f.write("\n## Innovation Highlights\n\n")
            from utils.analyzer import get_innovation_indicators
            
            innovation_count = {}
            for result in all_results:
                innovations = get_innovation_indicators(result)
                for innovation in innovations:
                    innovation_count[innovation] = innovation_count.get(innovation, 0) + 1
            
            if innovation_count:
                f.write("Most common innovative approaches:\n\n")
                for innovation, count in sorted(innovation_count.items(), key=lambda x: x[1], reverse=True)[:5]:
                    f.write(f"- **{innovation}**: Used by {count} publishers\n")
            
            # Market-wide statistics
            f.write("\n## Market-Wide Statistics\n\n")
            
            # Calculate averages for key metrics
            metrics = {
                'Support vs Transactional Ratio': 'support_ratio',
                'Mission Messaging Density': 'mission_density',
                'Community Focus': 'community_score',
                'Scarcity Tactics': 'scarcity_score',
                'Social Proof Usage': 'social_proof_score'
            }
            
            f.write("### Average Scores Across All Publishers\n\n")
            for metric_name, metric_key in metrics.items():
                if metric_key in ['support_ratio']:
                    values = [r['motivation_framework'][metric_key] for r in all_results]
                elif metric_key in ['mission_density', 'community_score']:
                    values = [r['motivation_framework'][metric_key] for r in all_results]
                else:
                    values = [r['behavioral_triggers'][metric_key] for r in all_results]
                
                avg_value = sum(values) / len(values)
                f.write(f"- **{metric_name}**: {avg_value:.4f}\n")
            
            # Behavioral techniques usage
            f.write("\n### Behavioral Economics Techniques Usage\n\n")
            technique_usage = {
                'Scarcity': sum(1 for r in all_results if r['behavioral_triggers']['scarcity_score'] > 0),
                'Social Proof': sum(1 for r in all_results if r['behavioral_triggers']['social_proof_score'] > 0),
                'Loss Aversion': sum(1 for r in all_results if r['behavioral_triggers']['loss_aversion_score'] > 0),
                'Reciprocity': sum(1 for r in all_results if r['behavioral_triggers']['reciprocity_score'] > 0),
                'Habit Formation': sum(1 for r in all_results if sum(r['habit_formation']['counts'].values()) > 5)
            }
            
            for technique, count in sorted(technique_usage.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(all_results)) * 100
                f.write(f"- **{technique}**: {count} publishers ({percentage:.1f}%)\n")
            
            # Example phrases
            f.write("\n## Notable Example Phrases\n\n")
            
            # Collect best examples
            example_categories = [
                ('Mission-Driven', 'motivation_framework', 'mission'),
                ('Community Building', 'motivation_framework', 'community'),
                ('Scarcity', 'behavioral_triggers', 'scarcity'),
                ('Social Proof', 'behavioral_triggers', 'social_proof'),
                ('Reciprocity', 'behavioral_triggers', 'reciprocity')
            ]
            
            for category_name, section, example_key in example_categories:
                f.write(f"### {category_name} Examples\n\n")
                examples_found = []
                
                for result in all_results[:10]:  # Check top 10 publishers
                    examples = result[section]['examples'].get(example_key, [])
                    for example in examples[:2]:  # Get up to 2 examples per publisher
                        if example and len(example) > 20:  # Skip very short examples
                            examples_found.append((result['publisher_name'], example))
                
                for publisher, example in examples_found[:5]:  # Show top 5 examples
                    f.write(f"- **{publisher}**: \"{example}\"\n")
                
                if not examples_found:
                    f.write("- No notable examples found\n")
                f.write("\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            f.write("Based on this analysis, publishers looking to optimize their subscription pages should consider:\n\n")
            f.write("1. **Balance mission and features**: The most sophisticated publishers combine purpose-driven messaging with clear value propositions\n")
            f.write("2. **Use behavioral triggers thoughtfully**: Social proof and reciprocity tend to be more effective than aggressive scarcity tactics\n")
            f.write("3. **Build habits**: Emphasize daily utility and cross-platform accessibility\n")
            f.write("4. **Create community**: Foster a sense of belonging and shared purpose among subscribers\n")
            f.write("5. **Personalize the ask**: Use identity-affirming language that makes readers feel like valued partners\n")
            
        logger.info(f"Saved summary report to {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to generate summary report: {e}")
        return False


def log_error(error_message: str, output_dir: str):
    """
    Log error to error file.
    
    Args:
        error_message: Error message to log
        output_dir: Directory for error log
    """
    error_file = os.path.join(output_dir, 'error_log.txt')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(error_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {error_message}\n")


def save_progress(progress_data: Dict, output_dir: str):
    """
    Save progress data for recovery.
    
    Args:
        progress_data: Current progress data
        output_dir: Directory to save progress
    """
    progress_file = os.path.join(output_dir, 'progress.json')
    
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, indent=2)