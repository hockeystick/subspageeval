#!/usr/bin/env python3
"""Simple test to verify Flask setup"""

try:
    from flask import Flask
    print("✓ Flask is installed")
    
    # Test other imports
    import pandas as pd
    print("✓ Pandas is installed")
    
    import matplotlib
    print("✓ Matplotlib is installed")
    
    from utils.enhanced_scraper import scrape_page_enhanced
    print("✓ Enhanced scraper can be imported")
    
    # Try to start a simple Flask app
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return '<h1>Flask is working! Navigate to <a href="/app">/app</a> for the main application.</h1>'
    
    @app.route('/app')
    def main_app():
        # Serve the main app HTML
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Subscription Analyzer Test</title>
        </head>
        <body>
            <h1>Subscription Page Analyzer</h1>
            <p>Flask server is running correctly!</p>
            <p>To use the full application, ensure all dependencies are installed.</p>
            <hr>
            <h2>Quick Test</h2>
            <form method="GET" action="/test">
                <label>URL: <input type="url" name="url" placeholder="https://example.com/subscribe" style="width: 400px;"></label>
                <button type="submit">Test Scraping</button>
            </form>
        </body>
        </html>
        '''
    
    @app.route('/test')
    def test_scrape():
        from flask import request
        url = request.args.get('url', '')
        if url:
            return f'<h1>Would scrape: {url}</h1><p><a href="/app">Back</a></p>'
        return '<h1>No URL provided</h1><p><a href="/app">Back</a></p>'
    
    print("✓ Flask app created successfully")
    print("\nStarting Flask server on http://localhost:5002")
    print("Press Ctrl+C to stop")
    
    app.run(debug=False, port=5002, host='127.0.0.1')
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\nPlease install missing dependencies:")
    print("pip3 install flask pandas matplotlib")
except Exception as e:
    print(f"✗ Error: {e}")