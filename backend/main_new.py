#!/usr/bin/env python3
"""
New entry point for the refactored Flask application.
This provides the same functionality as app.py but uses the new modular structure.
"""
import sys
import os

# Add the src directory to Python path for modular imports
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import and run the refactored application
from src.flask_app import run_app

if __name__ == '__main__':
    run_app()
