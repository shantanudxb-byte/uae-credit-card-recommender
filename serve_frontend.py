#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend
"""
import http.server
import socketserver
import os
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open('http://localhost:8000')

def main():
    PORT = 8000
    
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    if os.path.exists(frontend_dir):
        os.chdir(frontend_dir)
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 Serving frontend at http://localhost:{PORT}")
        print("📝 Make sure the API server is running on port 5001")
        print("🚀 Opening browser in 2 seconds...")
        
        # Open browser after 2 seconds
        Timer(2.0, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Frontend server stopped")

if __name__ == "__main__":
    main()