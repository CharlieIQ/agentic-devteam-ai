"""
Configuration management for the Flask application.
"""
import os
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class."""
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
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
    
    # Agent configuration - Easy to modify and extend!
    AGENT_CONFIG = {
        'design': {
            'name': 'ChAIrlie',
            'title': 'Technical Design',
            'icon': '📐',
            'role': 'engineering_lead',
            'description': 'Creates detailed technical designs and architecture'
        },
        'backend_code': {
            'name': 'Jimmy Backend', 
            'title': 'Backend Code',
            'icon': '⚙️',
            'role': 'backend_engineer',
            'description': 'Implements server-side logic and APIs'
        },
        'frontend_code': {
            'name': 'Wally WebDev',
            'title': 'Frontend Code', 
            'icon': '🎨',
            'role': 'frontend_engineer',
            'description': 'Creates user interfaces and client-side code'
        },
        'tests': {
            'name': 'Bug Zapper',
            'title': 'Test Suite',
            'icon': '🧪', 
            'role': 'test_engineer',
            'description': 'Writes comprehensive unit and integration tests'
        }
        # Easy to add more agents here!
        # 'documentation': {
        #     'name': 'Doc Writer',
        #     'title': 'Documentation',
        #     'icon': '📚',
        #     'role': 'documentation_engineer', 
        #     'description': 'Creates comprehensive project documentation'
        # }
    }
    
    # Task order - defines the sequence of execution
    TASK_ORDER = ['design', 'backend_code', 'frontend_code', 'tests']
    
    @classmethod
    def validate(cls):
        """Validate configuration values."""
        if cls.PORT < 1 or cls.PORT > 65535:
            raise ValueError(f"Invalid port number: {cls.PORT}")
        
        if cls.CREWAI_TIMEOUT < 1:
            raise ValueError(f"Invalid CrewAI timeout: {cls.CREWAI_TIMEOUT}")
        
        if cls.MAX_REQUIREMENTS_LENGTH < 1:
            raise ValueError(f"Invalid max requirements length: {cls.MAX_REQUIREMENTS_LENGTH}")
    
    @classmethod
    def get_agent_config(cls, agent_key: str) -> Dict[str, Any]:
        """Get configuration for a specific agent."""
        return cls.AGENT_CONFIG.get(agent_key, {})
    
    @classmethod
    def get_all_agents(cls) -> Dict[str, Dict[str, Any]]:
        """Get all agent configurations."""
        return cls.AGENT_CONFIG
    
    @classmethod
    def get_task_order(cls) -> List[str]:
        """Get the order in which tasks should be executed."""
        return cls.TASK_ORDER
