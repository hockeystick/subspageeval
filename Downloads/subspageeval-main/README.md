# Multilingual Subscription Page Analyzer 🌍

**Powered by Claude AI** - A sophisticated tool for analyzing behavioral economics principles in news publisher subscription pages across **17 European languages**.

## 🚀 What's New

- **🤖 Claude AI Integration**: Replaced keyword-based analysis with Claude's advanced language understanding
- **🌍 17 Language Support**: Analyze subscription pages in Czech, Polish, Slovak, Hungarian, Romanian, German, Spanish, French, Lithuanian, Latvian, Portuguese, Dutch, Swedish, Danish, Finnish, Norwegian, and English
- **🎨 Cultural Intelligence**: Detects culture-specific persuasion techniques and communication styles
- **📊 Enhanced Analysis**: New emotional appeals and authority trigger detection
- **🖥️ Web Interface**: User-friendly interface with language selection and real-time analysis

## 🌟 Features

### Multilingual Analysis
- **Auto-language detection** or manual language selection
- **Cultural adaptation analysis** for different European markets
- **Consistent scoring** across all languages using Claude AI
- **Original language examples** with English explanations

### Behavioral Economics Analysis
- **Motivation Framework**: Support vs transactional language, mission-driven messaging
- **Behavioral Triggers**: Scarcity, social proof, loss aversion, reciprocity, authority
- **Habit Formation**: Temporal anchors, convenience, platform flexibility  
- **Emotional Appeals**: Fear, hope, belonging, status (NEW)
- **Cultural Adaptations**: Communication styles, local references, trust-building (NEW)

### Advanced Features
- **Dynamic page scraping** with JavaScript support
- **Screenshot capture** and OCR text extraction
- **Intelligent caching** to reduce API costs
- **Interactive web interface** with visualizations
- **Multiple export formats** (CSV, JSON)

## 🛠️ Quick Setup

### Prerequisites
- Python 3.8+
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- Tesseract OCR (optional, for image text extraction)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd subspageeval-main
```

2. **Run the setup script**
```bash
python setup.py
```
This will:
- Install all dependencies
- Create configuration files
- Set up directories
- Install Playwright browsers

3. **Configure your API key**
```bash
# Edit .env file
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

4. **Test the installation**
```bash
python test_claude_integration.py
```

## 🚀 Usage

### Web Interface (Recommended)

Start the web application:
```bash
python web_app.py
```

Open your browser to `http://localhost:5001`

Features:
- **Single page analysis** with language selection
- **Batch comparison** of multiple publishers
- **Interactive charts** and cultural insights
- **Export results** as CSV or JSON

### Command Line Interface

For batch processing:
```bash
python subscription_analyzer.py --input subscription_pages.csv --output results/
```

### Programmatic Usage

```python
from utils.analyzer import analyze_text

# Analyze text in any supported language
results = analyze_text(
    text="Votre texte en français ici...",
    publisher_name="Le Monde",
    language="fr"  # or "auto" for detection
)

print(f"Sophistication Score: {results['sophistication_score']}")
print(f"Cultural Style: {results['cultural_adaptations']['communication_style']}")
```

## 🌍 Supported Languages

| Language | Code | Cultural Focus |
|----------|------|----------------|
| Czech | `cs` | Skepticism, intellectual heritage |
| Polish | `pl` | Tradition, community solidarity |
| Slovak | `sk` | Community focus, cultural preservation |
| Hungarian | `hu` | Cultural uniqueness, intellectual tradition |
| Romanian | `ro` | Family values, European integration |
| German | `de` | Directness, precision, order |
| Spanish | `es` | Community, family values |
| French | `fr` | Formality, intellectual sophistication |
| Lithuanian | `lt` | Independence, cultural resilience |
| Latvian | `lv` | Cultural preservation, nature connection |
| Portuguese | `pt` | Warmth, personal connection |
| Dutch | `nl` | Pragmatism, egalitarian values |
| Swedish | `sv` | Minimalism, environmental consciousness |
| Danish | `da` | Hygge, work-life balance |
| Finnish | `fi` | Practicality, education values |
| Norwegian | `no` | Nature connection, quality of life |
| English | `en` | Universal baseline |

## 📊 Analysis Output

### Individual Analysis
```json
{
  "publisher_name": "Publisher Name",
  "detected_language": "de",
  "language_name": "German",
  "sophistication_score": 7.8,
  "primary_strategy": "mission-driven-sophisticated",
  "motivation_framework": {
    "support_ratio": 0.75,
    "mission_density": 0.023,
    // ... detailed scores
  },
  "cultural_adaptations": {
    "communication_style": "direct",
    "cultural_elements": ["Engineering precision references", "Order concepts"],
    "trust_building": ["Institutional credibility", "Expert authority"]
  },
  "key_insights": [
    "Strong community emphasis with German directness",
    "High reciprocity-based messaging",
    "Cultural adaptation for German market"
  ]
}
```

### Comparative Analysis
- Side-by-side publisher comparison
- Language-specific strategy insights
- Cultural adaptation effectiveness
- Market positioning analysis

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
CLAUDE_MODEL=claude-3-sonnet-20240229

# Optional
CACHE_ANALYSES=true
MAX_CONCURRENT_ANALYSES=3
LOG_LEVEL=INFO
```

### Supported Models
- `claude-3-opus-20240229` (most capable)
- `claude-3-sonnet-20240229` (balanced, recommended)
- `claude-3-haiku-20240307` (fastest)

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_claude_integration.py
```

Tests include:
- API connectivity
- Language detection accuracy
- Analysis quality across languages
- Caching functionality
- Cultural adaptation detection

## 📈 Performance

- **Analysis Speed**: ~30-45 seconds per page (first time)
- **Cached Results**: ~1-2 seconds for repeated analysis
- **Batch Processing**: 3 concurrent analyses (configurable)
- **Memory Usage**: Efficient caching with auto-cleanup

## 🔍 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your Anthropic API key is correctly set in `.env`
   - Verify the key starts with `sk-ant-api03-`

2. **Language Detection Issues**
   - Ensure text is at least 50 characters
   - Check if language is in supported list
   - Use manual language selection if auto-detection fails

3. **Slow Performance**
   - Enable caching: `CACHE_ANALYSES=true`
   - Reduce concurrent analyses: `MAX_CONCURRENT_ANALYSES=1`
   - Use Haiku model for faster processing

4. **Memory Issues**
   - Clear cache: `python -c "from utils.analyzer import clear_analysis_cache; clear_analysis_cache()"`
   - Reduce screenshot quality in settings

## 🤝 Contributing

We welcome contributions! Areas for improvement:
- Additional language support
- New behavioral economics patterns
- Performance optimizations
- Cultural insight refinements

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- **Anthropic** for Claude AI capabilities
- **Behavioral Economics Research** community
- **European Media** organizations for inspiring multilingual support

---

**Ready to analyze subscription strategies across Europe? Start with `python setup.py`!** 🚀