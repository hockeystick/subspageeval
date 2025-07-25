#!/usr/bin/env python3
"""
Setup script for the Multilingual Subscription Page Analyzer.
Handles environment setup, dependency installation, and configuration.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner."""
    print("=" * 70)
    print("🌍 Multilingual Subscription Page Analyzer Setup")
    print("   Powered by Claude AI - Supporting 17 European Languages")
    print("=" * 70)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_tesseract():
    """Check if Tesseract OCR is installed."""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, check=True)
        version = result.stdout.split('\n')[0]
        print(f"✅ Tesseract OCR: {version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Tesseract OCR not found")
        print("   Please install Tesseract OCR:")
        print("   - macOS: brew install tesseract")
        print("   - Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path('.env')
    template_file = Path('.env.template')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not template_file.exists():
        print("❌ Error: .env.template file not found")
        return False
    
    # Copy template to .env
    shutil.copy(template_file, env_file)
    print("✅ Created .env file from template")
    
    # Prompt for API key
    print("\n📋 Please configure your environment:")
    print("1. Edit the .env file and add your Anthropic API key")
    print("2. Get your API key from: https://console.anthropic.com/")
    print("3. Replace 'sk-ant-api03-YOUR-KEY-HERE' with your actual key")
    
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def install_playwright():
    """Install Playwright browsers."""
    print("\n🎭 Installing Playwright browsers...")
    try:
        subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'], 
                      check=True)
        print("✅ Playwright browsers installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Playwright browsers: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    directories = [
        'cache/analyses',
        'logs',
        'results',
        'templates',
        'static/css',
        'static/js'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created necessary directories")

def run_initial_test():
    """Run initial configuration test."""
    print("\n🧪 Testing configuration...")
    
    try:
        # Test imports
        from config.settings import settings
        from utils.claude_analyzer import ClaudeAnalyzer
        
        print("✅ Configuration imports successful")
        
        # Check API key
        if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY == 'sk-ant-api03-YOUR-KEY-HERE':
            print("⚠️  Warning: Please configure your Anthropic API key in .env file")
            return False
        
        print("✅ Anthropic API key configured")
        print(f"✅ Supported languages: {len(settings.SUPPORTED_LANGUAGES)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Configure your Anthropic API key in .env file (if not done already)")
    print("2. Test the installation:")
    print("   python test_claude_integration.py")
    print("3. Start the web application:")
    print("   python web_app.py")
    print("4. Or run command-line analysis:")
    print("   python subscription_analyzer.py --input subscription_pages.csv")
    print("\n🌍 Supported Languages:")
    print("   Czech, Polish, Slovak, Hungarian, Romanian, German,")
    print("   Spanish, French, Lithuanian, Latvian, Portuguese,")
    print("   Dutch, Swedish, Danish, Finnish, Norwegian, English")
    print("\n🔗 Documentation: README_ENHANCED.md")

def main():
    """Main setup function."""
    print_banner()
    
    # Check requirements
    check_python_version()
    tesseract_ok = check_tesseract()
    
    # Setup steps
    steps = [
        ("Creating environment file", create_env_file),
        ("Installing Python dependencies", install_dependencies),
        ("Installing Playwright browsers", install_playwright),
        ("Creating directories", create_directories),
        ("Running configuration test", run_initial_test)
    ]
    
    success = True
    for step_name, step_func in steps:
        print(f"\n🔧 {step_name}...")
        if not step_func():
            success = False
            break
    
    if success:
        print_next_steps()
    else:
        print("\n❌ Setup incomplete. Please resolve the errors above and run setup again.")
        sys.exit(1)
    
    if not tesseract_ok:
        print("\n⚠️  Note: Some visual analysis features may not work without Tesseract OCR")

if __name__ == '__main__':
    main()