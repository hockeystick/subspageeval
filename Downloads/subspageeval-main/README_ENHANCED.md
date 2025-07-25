# Enhanced Subscription Page Linguistic Analyzer

An advanced Python tool for analyzing the language used on news publisher subscription pages, now with dynamic page handling, visual analysis, and a web interface.

## New Features

### 1. Dynamic Page Scraping
- **Playwright Integration**: Handles JavaScript-rendered content
- **Smart Waiting**: Waits for subscription-related elements to load
- **Full Page Scrolling**: Triggers lazy-loaded content
- **Fallback Strategy**: Tries static scraping first, then dynamic

### 2. Visual Page Analysis
- **Screenshot Capture**: Full-page screenshots of subscription pages
- **OCR Text Extraction**: Extracts text from images and graphics
- **Combined Analysis**: Merges DOM text with visual text for comprehensive coverage

### 3. Web Interface
- **Single Page Analysis**: Analyze individual subscription pages
- **Batch Comparison**: Compare multiple publishers side-by-side
- **Interactive Visualizations**: Real-time charts and graphs
- **Data Export**: Download results as CSV or JSON

## Installation

### Prerequisites
- Python 3.8+
- Tesseract OCR (for visual text extraction)

### Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

### Install Python Dependencies

```bash
# Clone or download the repository
cd subpageevaluation

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Usage

### 1. Web Interface (Recommended)

Start the web server:
```bash
python web_app.py
```

Open your browser to `http://localhost:5000`

#### Features:
- **Single Analysis**: Enter publisher name and URL to analyze
- **Batch Comparison**: Add multiple publishers and compare
- **Visual Results**: See charts, scores, and screenshots
- **Export Options**: Download results as CSV or JSON

### 2. Command Line Interface

For batch processing:
```bash
python subscription_analyzer.py --input subscription_pages.csv --output results/
```

Options:
- `--input`: CSV file with publisher data
- `--output`: Output directory for results
- `--limit`: Limit number of publishers to process

### 3. Programmatic Usage

```python
from utils.enhanced_scraper import scrape_page_enhanced
from utils.analyzer import analyze_text
from utils.text_processor import clean_text

# Scrape a page
text, screenshot, metadata = scrape_page_enhanced("https://example.com/subscribe")

# Analyze the text
cleaned_text = clean_text(text)
results = analyze_text(cleaned_text, "Publisher Name")

# Access scores
print(f"Sophistication Score: {results['sophistication_score']}")
print(f"Support Ratio: {results['motivation_framework']['support_ratio']}")
```

## Analysis Metrics

### Motivation Framework
- **Support Ratio**: Balance of support vs transactional language
- **Mission Density**: Frequency of purpose-driven messaging
- **Feature Density**: Product feature mentions
- **Identity Score**: Reader identity/community language
- **Community Score**: Collective/shared language

### Behavioral Triggers
- **Scarcity**: Limited time offers, urgency
- **Social Proof**: Subscriber counts, testimonials
- **Loss Aversion**: Fear of missing out
- **Reciprocity**: Reader contribution enables journalism

### Habit Formation
- **Temporal Anchors**: Daily/routine references
- **Convenience**: Ease of access messaging
- **Platform Availability**: Multi-device support

## Output Files

### Web Interface Outputs
- Interactive dashboards with real-time analysis
- Downloadable CSV/JSON exports
- Screenshot previews

### CLI Outputs
1. **Individual Reports** (`{publisher}_analysis.json`)
   - Complete analysis with all scores
   - Screenshot in base64 format
   - Metadata and pricing information

2. **Comparative Analysis** (`comparative_analysis.csv`)
   - All publishers in spreadsheet format
   - Sortable by any metric

3. **Summary Report** (`subscription_language_analysis_report.md`)
   - Executive summary
   - Key insights and patterns

## Troubleshooting

### Common Issues

1. **Playwright Installation**
   ```bash
   playwright install-deps  # Install system dependencies
   playwright install chromium  # Install browser
   ```

2. **OCR Not Working**
   - Ensure Tesseract is installed and in PATH
   - Test with: `tesseract --version`

3. **Memory Issues with Screenshots**
   - Reduce screenshot quality in `dynamic_scraper.py`
   - Process fewer sites at once

4. **Slow Performance**
   - Dynamic scraping is slower than static
   - Use `--limit` flag for testing
   - Consider running headless (default)

## Advanced Configuration

### Custom Word Lists
Edit `data/word_lists.py` to add industry-specific terms:

```python
CUSTOM_TERMS = [
    'your-term-here',
    'industry-specific-phrase'
]
```

### Scraping Timeouts
Adjust in `utils/dynamic_scraper.py`:

```python
# Page load timeout (milliseconds)
await page.goto(url, wait_until='networkidle', timeout=60000)

# Element wait timeout
await page.wait_for_selector(selector, timeout=30000)
```

## Performance Tips

1. **Static First**: The tool tries static scraping first for speed
2. **Cache Results**: Web interface caches results in memory
3. **Batch Processing**: Process multiple URLs in parallel via web interface
4. **Headless Mode**: Runs headless by default for better performance

## Security Considerations

- The web interface is designed for local use
- Don't expose port 5000 to the internet without authentication
- Be respectful of website terms of service
- Consider rate limiting for large batches

## Contributing

Feel free to submit issues or pull requests. Areas for improvement:
- Additional language support
- More behavioral economics patterns
- PDF report generation
- Database storage for results