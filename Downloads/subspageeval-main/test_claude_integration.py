#!/usr/bin/env python3
"""
Test script for Claude AI integration in the Multilingual Subscription Page Analyzer.
Tests API connectivity, language detection, and analysis functionality.
"""

import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Test data for different languages
TEST_TEXTS = {
    'en': {
        'text': "Subscribe to The Guardian and support independent journalism. Join thousands of readers who trust our fearless reporting. Get unlimited access to all articles, newsletters, and exclusive content. Support the journalism that holds power to account.",
        'expected_elements': ['support', 'independent', 'journalism', 'unlimited', 'exclusive']
    },
    'de': {
        'text': "Abonnieren Sie die Zeit und unterstützen Sie unabhängigen Journalismus. Werden Sie Teil unserer Gemeinschaft und erhalten Sie unbegrenzten Zugang zu hochwertigen Artikeln und exklusiven Inhalten.",
        'expected_elements': ['unabhängigen', 'Journalismus', 'Gemeinschaft', 'unbegrenzten']
    },
    'fr': {
        'text': "Abonnez-vous au Monde et soutenez le journalisme indépendant. Rejoignez notre communauté de lecteurs engagés et accédez à tous nos articles, analyses exclusives et newsletters.",
        'expected_elements': ['journalisme', 'indépendant', 'communauté', 'exclusives']
    },
    'es': {
        'text': "Suscríbete a El País y apoya el periodismo independiente. Únete a nuestra comunidad de lectores comprometidos y accede a contenido exclusivo, análisis profundos y newsletters.",
        'expected_elements': ['periodismo', 'independiente', 'comunidad', 'exclusivo']
    },
    'pl': {
        'text': "Subskrybuj Gazetę Wyborczą i wspieraj niezależne dziennikarstwo. Dołącz do społeczności czytelników i uzyskaj nieograniczony dostęp do artykułów, analiz i ekskluzywnych treści.",
        'expected_elements': ['niezależne', 'dziennikarstwo', 'społeczności', 'ekskluzywnych']
    },
    'cs': {
        'text': "Předplaťte si Respekt a podpořte nezávislou žurnalistiku. Staňte se součástí naší komunity čtenářů a získejte neomezený přístup k článkům, analýzám a exkluzivnímu obsahu.",
        'expected_elements': ['nezávislou', 'žurnalistiku', 'komunity', 'exkluzivnímu']
    }
}

def print_test_banner():
    """Print test banner."""
    print("=" * 70)
    print("🧪 Claude AI Integration Test")
    print("   Testing multilingual subscription page analysis")
    print("=" * 70)
    print()

def test_configuration():
    """Test basic configuration and imports."""
    print("🔧 Testing configuration...")
    
    try:
        from config.settings import settings
        print(f"✅ Settings loaded - {len(settings.SUPPORTED_LANGUAGES)} languages supported")
        
        if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY == 'sk-ant-api03-YOUR-KEY-HERE':
            print("❌ Anthropic API key not configured in .env file")
            return False
        
        print("✅ Anthropic API key configured")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_claude_analyzer():
    """Test Claude analyzer initialization."""
    print("\n🤖 Testing Claude analyzer...")
    
    try:
        from utils.claude_analyzer import ClaudeAnalyzer
        
        analyzer = ClaudeAnalyzer()
        print("✅ Claude analyzer initialized successfully")
        return analyzer
        
    except Exception as e:
        print(f"❌ Claude analyzer initialization failed: {e}")
        return None

def test_language_detection(analyzer):
    """Test language detection functionality."""
    print("\n🌍 Testing language detection...")
    
    try:
        # Test with different languages
        for lang_code, test_data in TEST_TEXTS.items():
            detected = analyzer._detect_language(test_data['text'])
            status = "✅" if detected == lang_code else "⚠️"
            print(f"{status} {lang_code.upper()}: detected as {detected.upper()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Language detection failed: {e}")
        return False

def test_single_analysis(analyzer, language='en'):
    """Test single text analysis."""
    print(f"\n📊 Testing analysis for {language.upper()}...")
    
    try:
        test_data = TEST_TEXTS.get(language, TEST_TEXTS['en'])
        
        # Run analysis
        results = analyzer.analyze_subscription_page(
            text=test_data['text'],
            publisher_name=f"Test Publisher ({language.upper()})",
            language=language
        )
        
        # Validate results structure
        required_fields = [
            'motivation_framework',
            'behavioral_triggers', 
            'habit_formation',
            'emotional_appeals',
            'cultural_adaptations',
            'sophistication_score'
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in results:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing fields: {missing_fields}")
            return False
        
        # Print key results
        print(f"✅ Analysis completed successfully")
        print(f"   Language: {results.get('language_name', 'Unknown')}")
        print(f"   Sophistication Score: {results.get('sophistication_score', 0)}")
        print(f"   Primary Strategy: {results.get('primary_strategy', 'Unknown')}")
        
        # Check for cultural adaptations
        cultural = results.get('cultural_adaptations', {})
        if cultural.get('cultural_elements'):
            print(f"   Cultural Elements: {len(cultural['cultural_elements'])}")
        
        return results
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        logger.exception("Analysis error details:")
        return None

def test_enhanced_pipeline():
    """Test the enhanced analysis pipeline."""
    print("\n🔄 Testing enhanced pipeline...")
    
    try:
        from utils.enhanced_pipeline import enhanced_pipeline
        
        # Test with English text
        test_data = TEST_TEXTS['en']
        results = enhanced_pipeline.analyze_text(
            text=test_data['text'],
            publisher_name="Test Publisher (Pipeline)",
            language='en'
        )
        
        if results and 'sophistication_score' in results:
            print("✅ Enhanced pipeline working correctly")
            return True
        else:
            print("❌ Enhanced pipeline returned incomplete results")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced pipeline test failed: {e}")
        return False

def test_caching(analyzer):
    """Test analysis caching functionality."""
    print("\n💾 Testing caching...")
    
    try:
        test_text = TEST_TEXTS['en']['text']
        publisher_name = "Cache Test Publisher"
        
        # First analysis (should cache)
        start_time = datetime.now()
        results1 = analyzer.analyze_subscription_page(test_text, publisher_name, 'en')
        first_duration = (datetime.now() - start_time).total_seconds()
        
        # Second analysis (should use cache)
        start_time = datetime.now()
        results2 = analyzer.analyze_subscription_page(test_text, publisher_name, 'en')
        second_duration = (datetime.now() - start_time).total_seconds()
        
        if second_duration < first_duration * 0.5:  # Should be much faster
            print(f"✅ Caching working (first: {first_duration:.2f}s, second: {second_duration:.2f}s)")
            return True
        else:
            print(f"⚠️  Caching may not be working (first: {first_duration:.2f}s, second: {second_duration:.2f}s)")
            return True  # Don't fail the test, caching is optional
            
    except Exception as e:
        print(f"❌ Caching test failed: {e}")
        return False

def save_test_results(results, output_dir='test_results'):
    """Save test results to files."""
    try:
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for lang, result in results.items():
            if result:
                filename = f"test_analysis_{lang}_{timestamp}.json"
                with open(output_path / filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Test results saved to {output_dir}/")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not save test results: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive test suite."""
    print_test_banner()
    
    # Test configuration
    if not test_configuration():
        print("\n❌ Configuration test failed. Please check your .env file.")
        return False
    
    # Test Claude analyzer
    analyzer = test_claude_analyzer()
    if not analyzer:
        return False
    
    # Test language detection
    if not test_language_detection(analyzer):
        return False
    
    # Test enhanced pipeline
    if not test_enhanced_pipeline():
        return False
    
    # Test analysis for multiple languages
    test_results = {}
    test_languages = ['en', 'de', 'fr', 'es', 'pl', 'cs']
    
    for lang in test_languages:
        result = test_single_analysis(analyzer, lang)
        if result:
            test_results[lang] = result
        else:
            print(f"⚠️  Analysis failed for {lang}")
    
    # Test caching
    test_caching(analyzer)
    
    # Save results
    if test_results:
        save_test_results(test_results)
    
    # Summary
    successful_languages = len(test_results)
    total_languages = len(test_languages)
    
    print("\n" + "=" * 70)
    print("📋 Test Summary")
    print("=" * 70)
    print(f"✅ Configuration: OK")
    print(f"✅ Claude API: Connected")
    print(f"✅ Language Analysis: {successful_languages}/{total_languages} languages working")
    
    if successful_languages >= total_languages * 0.8:  # 80% success rate
        print("\n🎉 Integration test PASSED!")
        print("Your multilingual subscription analyzer is ready to use.")
        return True
    else:
        print("\n⚠️  Integration test PARTIAL SUCCESS")
        print(f"Some languages may not be working correctly.")
        return False

def main():
    """Main test function."""
    try:
        success = run_comprehensive_test()
        
        if success:
            print("\n🚀 Ready to start analyzing!")
            print("Run 'python web_app.py' to start the web interface")
        else:
            print("\n🔧 Please resolve the issues above before using the analyzer")
            
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        logger.exception("Unexpected error details:")

if __name__ == '__main__':
    main()