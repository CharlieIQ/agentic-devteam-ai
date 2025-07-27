"""
Flask application factory and configuration.
"""
import sys
import os
from flask import Flask
from flask_cors import CORS

from .config import Config
from .utils.logging import setup_logging, setup_crewai_log_capture
from .routes.logs import logs_bp
from .routes.requirements import requirements_bp
from .routes.generate import generate_bp
from .routes.health import health_bp
from .routes.team import team_bp

def create_app() -> Flask:
    """Create and configure the Flask application."""
    # Validate configuration
    Config.validate()
    
    # Set up logging
    setup_logging(Config.LOG_LEVEL)
    
    # Set up CrewAI log capture
    setup_crewai_log_capture()
    
    # Create Flask app
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Register blueprints
    app.register_blueprint(logs_bp)
    app.register_blueprint(requirements_bp)
    app.register_blueprint(generate_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(team_bp)
    
    return app

def run_app() -> None:
    """Run the Flask application."""
    from .services.crewai_service import crewai_service
    
    if not crewai_service.is_available:
        print("⚠️  CrewAI is not installed. Please run: pip install crewai")
    
    print(f"🚀 Starting Flask app on {Config.HOST}:{Config.PORT}...")
    
    app = create_app()
    
    # Start Flask with minimal logging
    app.run(
        debug=Config.DEBUG, 
        port=Config.PORT, 
        host=Config.HOST, 
        use_reloader=False
    )
