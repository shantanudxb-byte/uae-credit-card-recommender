#!/usr/bin/env python3
"""
Startup script for UAE Credit Card Recommender API
"""
import os
import sys

def main():
    print("🏦 Starting UAE Credit Card Recommender API...")
    
    # Check if we're in the right directory
    if not os.path.exists('app/api.py'):
        print("❌ Error: Please run this from the project root directory")
        print("   Current directory should contain 'app/api.py'")
        sys.exit(1)
    
    # Check if required files exist
    required_files = [
        'data/uae_cards.json',
        'app/agent.py',
        'app/rag_pipeline.py'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Error: Required file missing: {file_path}")
            sys.exit(1)
    
    print("✅ All required files found")
    print("🚀 Starting API server on http://localhost:5001")
    print("📝 API endpoints:")
    print("   POST /api/recommend - Get card recommendations")
    print("   POST /api/chat - Chat with advisor")
    print("   GET /health - Health check")
    print()
    print("💡 To test the API, run: python test_api.py")
    print("🌐 To use the web interface, open: frontend/index.html")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Import and run the Flask app
    try:
        from app.api import app
        app.run(debug=True, port=5001, host='0.0.0.0')
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you've installed requirements: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()