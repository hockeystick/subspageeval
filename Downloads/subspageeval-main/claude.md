## claude.md - Subscription Page Linguistic Analyzer

### Project Overview
Build a Python application that analyzes the language used on news publisher subscription pages to identify behavioral economics principles in their marketing copy. The tool will help understand how publishers use preference formation theory in their subscription marketing.

### Your Task
Create a complete Python application that:
1. Reads a CSV file containing publisher names and subscription page URLs
2. Scrapes the text content from each subscription page
3. Analyzes the language using predefined word lists and patterns
4. Calculates scores for various behavioral economics principles
5. Outputs individual and comparative analysis reports

### Input Specification
The user will provide a CSV file named `subscription_pages.csv` with this format:
```csv
publisher_name,subscription_url,language
The Guardian,https://www.theguardian.com/subscribe,en
Financial Times,https://www.ft.com/products,en
NZZ,https://www.nzz.ch/abonnemente,de
```

### Core Implementation Requirements

#### 1. Project Structure
Create the following files:
```
subscription_analyzer.py  # Main script
requirements.txt         # Dependencies
utils/
  scraper.py           # Web scraping functions
  text_processor.py    # Text processing functions
  analyzer.py          # Linguistic analysis engine
  reporter.py          # Report generation
data/
  word_lists.py        # All word lists and patterns
results/               # Output directory
```

#### 2. Word Lists to Implement
Create comprehensive word lists in `data/word_lists.py`:

**Motivation Framework:**
- Support terms: support, contribute, fund, enable, help, sustain, back, empower, donation, contribution
- Transactional terms: buy, purchase, subscribe, order, get, start, sign up, register, checkout, cart
- Mission terms: journalism, democracy, truth, independent, fearless, quality, investigative, reporting, accountability, public interest, free press, fourth estate
- Feature terms: access, content, articles, digital, unlimited, exclusive, ad-free, premium, archive, newsletter
- Identity terms: member, supporter, reader, community, partner, patron, backer, champion, advocate
- Community terms: our, we, us, together, join, fellow, collective, shared, common

**Behavioral Triggers:**
- Scarcity terms: limited time, ends, only, exclusive, last chance, today only, hurry, final, remaining, expires
- Social proof terms: most popular, recommended, bestseller, readers choice, trusted by, joined by
- Social proof regex patterns for finding subscriber counts
- Loss aversion terms: miss, lose, don't miss out, never miss, missing out, full access, complete, everything, all, entire
- Reciprocity terms: support enables, your contribution, thanks to readers, rely on, made possible, because of you, your support

**Habit Formation:**
- Temporal anchors: daily, morning, evening, weekly, everyday, routine, breakfast, commute, lunch break, bedtime
- Frequency terms: always, whenever, anytime, regularly, every morning, each day, constantly, 24/7, round the clock
- Convenience terms: easy, simple, seamless, convenient, anywhere, effortless, instant, quick, straightforward, hassle-free
- Platform terms: app, mobile, tablet, desktop, device, platform, ios, android, smartphone, computer, all your devices

#### 3. Web Scraping Requirements
In `utils/scraper.py`:
- Use requests and BeautifulSoup
- Extract all visible text from h1-h6, p, span, div, button, a tags
- Exclude script, style, meta tags
- Handle timeouts (30 seconds max)
- Retry failed requests up to 3 times
- Log errors but continue processing

#### 4. Analysis Calculations
In `utils/analyzer.py`, calculate these scores for each page:

```python
# Motivation Framework Scores
support_ratio = support_count / (support_count + transactional_count)
mission_density = mission_terms_count / total_words
feature_density = feature_terms_count / total_words
identity_score = identity_terms_count / total_words
community_score = community_terms_count / total_words

# Behavioral Trigger Scores
scarcity_score = scarcity_terms_count / total_words
social_proof_score = (social_proof_terms + regex_matches) / total_words
loss_aversion_score = loss_aversion_terms_count / total_words
reciprocity_score = reciprocity_terms_count / total_words

# Habit Formation Scores
temporal_score = temporal_anchors_count / total_words
frequency_score = frequency_terms_count / total_words
convenience_score = convenience_terms_count / total_words
platform_score = platform_terms_count / total_words

# Overall Sophistication Score (weighted average, scale 0-10)
```

#### 5. Output Requirements

**A. Individual JSON reports** (`results/{publisher_name}_analysis.json`):
- Include all calculated scores
- Add top phrases found for each category
- Classify primary strategy (mission-driven, feature-driven, hybrid)
- Include timestamp and basic metadata

**B. Comparative CSV** (`results/comparative_analysis.csv`):
- One row per publisher
- All scores as columns
- Sort by sophistication score

**C. Summary Report** (`results/subscription_language_analysis_report.md`):
- Executive summary with key findings
- Publisher rankings by sophistication
- Innovation highlights (unique language patterns)
- Market-wide statistics

#### 6. Error Handling
- Create `results/error_log.txt` for all errors
- Continue processing if individual sites fail
- Flag suspicious results (e.g., <100 words)
- Save progress after each site

#### 7. Key Functions to Implement

```python
def main():
    # Read CSV input
    # For each publisher:
    #   - Scrape page
    #   - Process text
    #   - Analyze language
    #   - Generate individual report
    # Generate comparative analysis
    # Create summary report

def scrape_page(url):
    # Return cleaned text or None if failed

def analyze_text(text, publisher_name):
    # Return dictionary of all scores

def generate_individual_report(analysis_results):
    # Save JSON file

def generate_comparative_report(all_results):
    # Create CSV and markdown summary
```

#### 8. Additional Considerations
- Make word matching case-insensitive
- Handle multi-word phrases properly
- Extract actual phrases containing matched terms for reporting
- Preserve examples of high-scoring phrases
- Consider stemming for better matching (optional)

#### 9. Testing
Include test capability with sample HTML files to verify analysis accuracy without repeated scraping.

### Expected Usage
```bash
python subscription_analyzer.py --input subscription_pages.csv --output results/
```

### Success Criteria
The tool should:
1. Successfully process 30 subscription pages in under 20 minutes
2. Generate actionable insights about linguistic strategies
3. Identify innovative approaches to subscription marketing
4. Provide clear rankings and comparisons
5. Handle errors gracefully without stopping execution

### Note for Implementation
Focus on accuracy of linguistic analysis over perfect web scraping. If a page has dynamic content that's hard to capture, log it and move on. The linguistic patterns in the captured text are more important than getting every word on complex pages.