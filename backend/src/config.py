"""
Configuration management for the Flask application.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class."""
    
    # Flask configuration
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5001))
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING')
    
    # CrewAI configuration
    CREWAI_TIMEOUT = int(os.getenv('CREWAI_TIMEOUT', 30))
    
    # Requirements configuration
    MAX_REQUIREMENTS_LENGTH = int(os.getenv('MAX_REQUIREMENTS_LENGTH', 10000))
    
    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    @classmethod
    def validate(cls):
        """Validate configuration values."""
        if cls.PORT < 1 or cls.PORT > 65535:
            raise ValueError(f"Invalid port number: {cls.PORT}")
        
        if cls.CREWAI_TIMEOUT < 1:
            raise ValueError(f"Invalid CrewAI timeout: {cls.CREWAI_TIMEOUT}")
        
        if cls.MAX_REQUIREMENTS_LENGTH < 1:
            raise ValueError(f"Invalid max requirements length: {cls.MAX_REQUIREMENTS_LENGTH}")
