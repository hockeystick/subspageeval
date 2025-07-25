#!/usr/bin/env python3
"""
Launch the web application with browser opening
"""
import webbrowser
import time
import threading
import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:5001')
    print("\n" + "="*50)
    print("Web app should open in your browser automatically.")
    print("If not, manually navigate to: http://localhost:5001")
    print("="*50 + "\n")

# Start browser opening in background
browser_thread = threading.Thread(target=open_browser)
browser_thread.daemon = True
browser_thread.start()

# Import and run the Flask app
try:
    from web_app import app
    print("Starting Subscription Page Analyzer...")
    print("Server running on http://localhost:5001")
    # Run with host 0.0.0.0 to ensure it's accessible
    app.run(debug=True, port=5001, host='0.0.0.0', use_reloader=False)
except Exception as e:
    print(f"Error starting web app: {e}")
    print("\nTroubleshooting:")
    print("1. Ensure all dependencies are installed: pip3 install -r requirements.txt")
    print("2. Check if port 5001 is already in use")
    print("3. Try running: python3 web_app.py directly")