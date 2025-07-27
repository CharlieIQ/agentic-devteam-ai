import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS

from .config import Config
from .utils.logging import setup_logging, setup_crewai_log_capture
from .routes.logs import logs_bp
from .routes.requirements import requirements_bp
from .routes.generate import generate_bp
from .routes.health import health_bp
from .routes.team import team_bp

def create_app() -> Flask:
    """
    Create and configure the Flask application.
    This function sets up the application with necessary configurations,
    logging, and routes.
    It also ensures that the configuration directory exists and loads
    configurations from environment variables or defaults.
    Returns:
        Flask: The configured Flask application instance.
    Raises:
        FileNotFoundError: If the configuration directory does not exist.
    """
    # Ensure the config directory exists
    config_dir = os.path.join(os.path.dirname(__file__), 'config')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    # Load configuration from environment variables or defaults
    Config.load_from_env()
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
    app.register_blueprint(team_bp)  # Add the new team blueprint
    
    return app

def run_app() -> None:
    """
    Run the Flask application.
    This function checks if the CrewAI service is available and starts the
    Flask application with the configured host and port.
    It also prints a message indicating the start of the application.
    Raises:
        ImportError: If the CrewAI service is not available.
    Returns:
        None
    """
    from .services.crewai_service import crewai_service
    
    if not crewai_service.is_available:
        print("⚠️  CrewAI is not installed. Please run: pip install crewai[tools]")
    
    print(f"🚀 Starting Flask app on {Config.HOST}:{Config.PORT}...")
    
    app = create_app()
    
    # Start Flask with minimal logging
    app.run(
        debug=Config.DEBUG, 
        port=Config.PORT, 
        host=Config.HOST, 
        use_reloader=False
    )