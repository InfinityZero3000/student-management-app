"""
WSGI entry point for production deployment
"""
import sys
import os

# Add flask_app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from server import app

if __name__ == "__main__":
    app.run()
