"""
Flask web application for multilingual subscription page analysis using Claude AI.
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import logging
from datetime import datetime
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, List

from utils.scraper import scrape_page
from utils.text_processor import clean_text
from utils.analyzer import analyze_text, get_supported_languages
from utils.reporter import save_individual_report
from config.settings import settings

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size
app.config['SECRET_KEY'] = settings.FLASK_SECRET_KEY

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Store analysis results in memory (in production, use a database)
analysis_cache = {}


@app.route('/')
def index():
    """Main page with input form."""
    supported_languages = get_supported_languages()
    return render_template('index.html', supported_languages=supported_languages)


@app.route('/languages')
def get_languages():
    """Get supported languages for AJAX requests."""
    return jsonify(get_supported_languages())


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze a single subscription page using Claude AI."""
    data = request.get_json()
    url = data.get('url')
    publisher_name = data.get('publisher_name', 'Unknown Publisher')
    language = data.get('language', 'auto')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Validate language
    if not settings.is_supported_language(language):
        return jsonify({'error': f'Unsupported language: {language}'}), 400
    
    logger.info(f"Analyzing {publisher_name} at {url} (language: {language})")
    
    try:
        # Check cache first (include language in cache key for multilingual support)
        cache_key = f"{publisher_name}_{url}_{language}"
        if cache_key in analysis_cache:
            cached_result = analysis_cache[cache_key]
            cached_result['from_cache'] = True
            return jsonify(cached_result)
        
        # Scrape the page
        text = scrape_page(url)
        screenshot, metadata = None, {}
        
        if not text:
            return jsonify({'error': 'Failed to scrape the page'}), 500
        
        # Clean and analyze the text using Claude AI
        cleaned_text = clean_text(text)
        results = analyze_text(cleaned_text, publisher_name, language)
        
        # Add additional web app specific data
        results['url'] = url
        results['screenshot'] = screenshot
        results['metadata'] = metadata
        results['scrape_timestamp'] = datetime.now().isoformat()
        results['requested_language'] = language
        
        # Sophistication score is already calculated by Claude pipeline
        if 'sophistication_score' not in results:
            results['sophistication_score'] = 0.0
        
        # Generate visualizations
        results['charts'] = generate_charts(results)
        
        # Cache the results
        analysis_cache[cache_key] = results
        
        # Save to file system as well
        save_individual_report(results, 'results')
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/compare', methods=['POST'])
def compare():
    """Compare multiple publishers using Claude AI analysis."""
    data = request.get_json()
    urls = data.get('urls', [])
    default_language = data.get('default_language', 'auto')
    
    if not urls or len(urls) < 2:
        return jsonify({'error': 'At least 2 URLs required for comparison'}), 400
    
    logger.info(f"Comparing {len(urls)} publishers with default language: {default_language}")
    
    try:
        all_results = []
        
        for item in urls:
            url = item.get('url')
            publisher_name = item.get('publisher_name', f'Publisher {len(all_results) + 1}')
            language = item.get('language', default_language)
            
            # Check cache (include language in cache key)
            cache_key = f"{publisher_name}_{url}_{language}"
            if cache_key in analysis_cache:
                all_results.append(analysis_cache[cache_key])
            else:
                # Analyze new URL
                text = scrape_page(url)
                screenshot, metadata = None, {}
                if text:
                    cleaned_text = clean_text(text)
                    results = analyze_text(cleaned_text, publisher_name, language)
                    results['url'] = url
                    results['requested_language'] = language
                    
                    # Sophistication score is already calculated by Claude
                    if 'sophistication_score' not in results:
                        results['sophistication_score'] = 0.0
                    
                    analysis_cache[cache_key] = results
                    all_results.append(results)
        
        # Generate comparative visualizations
        comparison_data = {
            'publishers': all_results,
            'comparison_charts': generate_comparison_charts(all_results),
            'summary_stats': generate_summary_stats(all_results)
        }
        
        return jsonify(comparison_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/export/<format>')
def export_data(format):
    """Export analysis data in various formats."""
    if format not in ['csv', 'json', 'pdf']:
        return jsonify({'error': 'Invalid format'}), 400
    
    try:
        # Get all cached results
        all_results = list(analysis_cache.values())
        
        if format == 'csv':
            df = create_dataframe_from_results(all_results)
            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            return send_file(
                csv_buffer,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'subscription_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            )
        
        elif format == 'json':
            json_data = json.dumps(all_results, indent=2)
            json_buffer = BytesIO(json_data.encode())
            return send_file(
                json_buffer,
                mimetype='application/json',
                as_attachment=True,
                download_name=f'subscription_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Sophistication score calculation is now handled by Claude AI in the enhanced pipeline


def generate_charts(results: Dict) -> Dict[str, str]:
    """Generate visualization charts for a single analysis."""
    charts = {}
    
    # Motivation Framework Pie Chart
    plt.figure(figsize=(8, 6))
    motivation = results.get('motivation_framework', {}).get('counts', {})
    if sum(motivation.values()) > 0:
        plt.pie(motivation.values(), labels=motivation.keys(), autopct='%1.1f%%')
        plt.title('Motivation Framework Distribution')
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        charts['motivation_pie'] = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
    
    # Behavioral Triggers Bar Chart (now includes authority)
    plt.figure(figsize=(12, 6))
    behavioral = results.get('behavioral_triggers', {})
    triggers = ['scarcity_score', 'social_proof_score', 'loss_aversion_score', 'reciprocity_score', 'authority_score']
    values = [behavioral.get(t, 0) * 100 for t in triggers]
    labels = ['Scarcity', 'Social Proof', 'Loss Aversion', 'Reciprocity', 'Authority']
    
    plt.bar(labels, values)
    plt.ylabel('Score (normalized)')
    plt.title('Behavioral Triggers Analysis')
    plt.ylim(0, 10)
    plt.xticks(rotation=45, ha='right')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    charts['behavioral_bar'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Emotional Appeals Chart (new)
    plt.figure(figsize=(10, 6))
    emotional = results.get('emotional_appeals', {})
    emotions = ['fear_score', 'hope_score', 'belonging_score', 'status_score']
    emotion_values = [emotional.get(e, 0) * 100 for e in emotions]
    emotion_labels = ['Fear', 'Hope', 'Belonging', 'Status']
    
    if sum(emotion_values) > 0:
        plt.bar(emotion_labels, emotion_values, color=['red', 'green', 'blue', 'purple'])
        plt.ylabel('Score (normalized)')
        plt.title('Emotional Appeals Analysis')
        plt.ylim(0, 10)
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        charts['emotional_bar'] = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
    
    return charts


def generate_comparison_charts(results: List[Dict]) -> Dict[str, str]:
    """Generate comparison charts for multiple publishers."""
    charts = {}
    
    # Sophistication Score Comparison
    plt.figure(figsize=(12, 6))
    publishers = [r['publisher_name'] for r in results]
    scores = [r.get('sophistication_score', 0) for r in results]
    
    plt.bar(publishers, scores)
    plt.ylabel('Sophistication Score (0-10)')
    plt.title('Publisher Sophistication Comparison')
    plt.xticks(rotation=45, ha='right')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    charts['sophistication_comparison'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Heatmap of all metrics
    plt.figure(figsize=(14, 8))
    
    # Prepare data for heatmap
    metrics = []
    metric_names = [
        'Support Ratio', 'Mission Density', 'Feature Density',
        'Scarcity', 'Social Proof', 'Loss Aversion', 'Reciprocity'
    ]
    
    for r in results:
        row = []
        m = r.get('motivation_framework', {})
        b = r.get('behavioral_triggers', {})
        
        row.append(m.get('support_ratio', 0))
        row.append(m.get('mission_density', 0) * 50)
        row.append(m.get('feature_density', 0) * 50)
        row.append(b.get('scarcity_score', 0) * 100)
        row.append(b.get('social_proof_score', 0) * 50)
        row.append(b.get('loss_aversion_score', 0) * 50)
        row.append(b.get('reciprocity_score', 0) * 50)
        
        metrics.append(row)
    
    sns.heatmap(
        metrics,
        annot=True,
        fmt='.2f',
        xticklabels=metric_names,
        yticklabels=publishers,
        cmap='YlOrRd'
    )
    plt.title('Linguistic Strategy Heatmap')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    charts['strategy_heatmap'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return charts


def generate_summary_stats(results: List[Dict]) -> Dict:
    """Generate summary statistics for comparison."""
    stats = {
        'total_publishers': len(results),
        'avg_sophistication': round(sum(r.get('sophistication_score', 0) for r in results) / len(results), 2),
        'most_sophisticated': max(results, key=lambda x: x.get('sophistication_score', 0))['publisher_name'],
        'most_mission_driven': max(results, key=lambda x: x.get('motivation_framework', {}).get('mission_density', 0))['publisher_name'],
        'most_community_focused': max(results, key=lambda x: x.get('motivation_framework', {}).get('community_score', 0))['publisher_name']
    }
    return stats


def create_dataframe_from_results(results: List[Dict]) -> pd.DataFrame:
    """Create a pandas DataFrame from analysis results."""
    data = []
    
    for r in results:
        row = {
            'Publisher': r.get('publisher_name'),
            'URL': r.get('url'),
            'Sophistication Score': r.get('sophistication_score', 0),
            'Total Words': r.get('total_words', 0),
            'Support Ratio': r.get('motivation_framework', {}).get('support_ratio', 0),
            'Mission Density': r.get('motivation_framework', {}).get('mission_density', 0),
            'Scarcity Score': r.get('behavioral_triggers', {}).get('scarcity_score', 0),
            'Social Proof Score': r.get('behavioral_triggers', {}).get('social_proof_score', 0),
            'Timestamp': r.get('timestamp', '')
        }
        data.append(row)
    
    return pd.DataFrame(data)


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Start the Flask app
    logger.info(f"Starting Claude-powered multilingual subscription analyzer on port {settings.FLASK_PORT}")
    logger.info(f"Supported languages: {', '.join(settings.SUPPORTED_LANGUAGES)}")
    
    app.run(
        debug=True,
        port=settings.FLASK_PORT,
        host='0.0.0.0'
    )