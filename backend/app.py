#!/usr/bin/env python3
"""
Refactored Flask application entry point.
Professional, modular backend for the Agentic DevTeam AI system.
"""
import sys
import os

# Add the src directory to Python path for modular imports
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import the refactored application factory
from src.flask_app import run_app

if __name__ == '__main__':
    """
    Entry point for the refactored Flask application.
    
    This file has been refactored to use a modular structure with:
    - Separation of concerns across modules
    - Professional service layer architecture
    - Proper configuration management
    - Clean route organization
    - Comprehensive error handling
    
    The application maintains full backward compatibility while
    providing a much cleaner, more maintainable codebase.
    """
    run_app()