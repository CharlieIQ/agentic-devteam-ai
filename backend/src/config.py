"""
Configuration management for the Flask application.
"""
import os
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

class Config:
    """
    This class manages the configuration for the Flask application.
    It loads configuration values from environment variables and provides methods to access them.
    It also includes validation methods to ensure the configuration is correct.
    
    Attributes:
        SECRET_KEY (str): Secret key for the Flask application.
        DEBUG (bool): Debug mode for the Flask application.
        HOST (str): Host address for the Flask application.
        PORT (int): Port number for the Flask application.
        LOG_LEVEL (str): Logging level for the application.
        CREWAI_TIMEOUT (int): Timeout for CrewAI operations.
        MAX_REQUIREMENTS_LENGTH (int): Maximum length for requirements.
        CORS_ORIGINS (str): Allowed origins for CORS requests.
        AGENT_CONFIG (Dict[str, Dict[str, Any]]): Configuration for agents.
    
        get_enabled_agents (classmethod): Returns only the enabled agents.
        get_task_order (classmethod): Returns the order of tasks based on dependencies.
        validate (classmethod): Validates configuration values.
        get_agent_config (classmethod): Returns configuration for a specific agent.
        get_all_agents (classmethod): Returns all agent configurations.
    """
    
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
    
    # ENHANCED AGENT CONFIGURATION - Single Source of Truth!
    AGENT_CONFIG = {
        'design': {
            'name': 'ChAIrlie',
            'title': 'Technical Design',
            'icon': '📐',
            'role': 'engineering_lead',
            'description': 'Creates detailed technical designs and architecture. Loves diagrams and hates typos.',
            'llm': 'openai/gpt-4o-mini',
            'enabled': True,
            'dependencies': [],
            'output_file': 'output/design.md',
            'backstory': "You're a seasoned engineering lead with a knack for writing clear and concise designs.",
            'goal_template': "Take the high level requirements and prepare a detailed design for the backend developer; everything should be in 1 python module; describe the function and method signatures in the module. The python module must be completely self-contained, and ready so that it can be tested or have a simple UI built for it. The module should be named {module_name} and the class should be named {class_name}",
            'task_description': "Take the high level requirements described here and prepare a detailed design for the engineer; everything should be in 1 python module, but outline the classes and methods in the module. Also include steps for the engineer to follow in order to implement the module. Here are the requirements: {requirements} IMPORTANT: Only output the design in markdown format, laying out in detail the classes and functions in the module, describing the functionality.",
            'expected_output': "A detailed design for the engineer, identifying the classes and functions in the module."
        },
        'backend_code': {
            'name': 'Jimmy Backend', 
            'title': 'Backend Code',
            'icon': '⚙️',
            'role': 'backend_engineer',
            'description': 'Implements server-side logic and APIs. Temperamental, hates unit testing.',
            'llm': 'openai/gpt-4o-mini',
            'enabled': True,
            'dependencies': ['design'],
            'output_file': 'output/{module_name}',
            'backstory': "You're a seasoned python engineer with a knack for writing clean, efficient code. You follow the design instructions carefully. You produce 1 python module named {module_name} that implements the design and achieves the requirements.",
            'goal_template': "Write a python module that implements the design described by the engineering lead, in order to achieve the requirements. The python module must be completely self-contained, and ready so that it can be tested or have a simple UI built for it. The module should be named {module_name} and the class should be named {class_name}",
            'task_description': "Write a python module that implements the design described by the engineering lead, in order to achieve the requirements. Here are the requirements: {requirements}",
            'expected_output': "A python module that implements the design and achieves the requirements. IMPORTANT: Output ONLY the raw Python code without any markdown formatting, code block delimiters, or backticks. The output should be valid Python code that can be directly saved to a file and executed."
        },
        'frontend_code': {
            'name': 'Willy WebDev',
            'title': 'Frontend Code', 
            'icon': '🎨',
            'role': 'frontend_engineer',
            'description': 'Creates user interfaces and client-side code. Lives on coffee and centering divs.',
            'llm': 'openai/gpt-4o-mini',
            'enabled': True,
            'dependencies': ['backend_code'],
            'output_file': 'output/App.jsx',
            'backstory': "You're a seasoned frontend engineer highly skilled at writing beautiful UIs for a backend class.",
            'goal_template': "Write a frontend UI that demonstrates the given backend, all in one file to be in the same directory as the backend module {module_name}. Here are the requirements: {requirements}",
            'task_description': "Write a UI in a framework (Like React + Vite) that demonstrates the given backend class in {module_name}. Assume there is only 1 user, and keep the UI very simple indeed - just a prototype or demo. Here are the requirements: {requirements}",
            'expected_output': "A UI in that demonstrates the given backend class. The file should be ready so that it can be run as-is, in the same directory as the backend module, and it should import the backend class from {module_name}. IMPORTANT: Output ONLY the raw code without any markdown formatting, code block delimiters, or backticks. The output should be valid code that can be directly saved to a file and executed. Also, ensure that the frontend code is compatible with the backend module."
        },
        'tests': {
            'name': 'Bug Zapper',
            'title': 'Test Suite',
            'icon': '🧪', 
            'role': 'test_engineer',
            'description': 'Writes comprehensive unit and integration tests. Simply loves breaking things.',
            'llm': 'openai/gpt-4o-mini',
            'enabled': True,
            'dependencies': ['backend_code'],
            'output_file': 'output/test_{module_name}',
            'backstory': "You're a seasoned QA engineer and software developer who writes great unit tests for any code.",
            'goal_template': "Write unit tests for the given backend module {module_name} and create a test_{module_name} in the same directory as the backend module.",
            'task_description': "Write unit tests for the given backend module {module_name} and create a test_{module_name} in the same directory as the backend module.",
            'expected_output': "A test_{module_name} module that tests the given backend module. IMPORTANT: Output ONLY the raw Python code without any markdown formatting, code block delimiters, or backticks. The output should be valid Python code that can be directly saved to a file and executed."
        },
        
        # New agents and tasks
        'documentation': {
            'name': 'Doc Writer',
            'title': 'Documentation',
            'icon': '📚',
            'role': 'documentation_engineer',
            'description': 'Creates comprehensive project documentation. Memorized the Miriam Webster dictionary.',
            'llm': 'openai/gpt-4o-mini',
            'enabled': True,  # Set to True to activate
            'dependencies': ['backend_code', 'frontend_code'],
            'output_file': 'output/README.md',
            'backstory': "You're a technical writer who creates clear, comprehensive documentation that developers actually want to read.",
            'goal_template': "Create comprehensive documentation for the project including setup instructions, API documentation, and usage examples.",
            'task_description': "Write comprehensive documentation for the project including a README.md with setup instructions, API documentation, and usage examples. Include the requirements: {requirements}",
            'expected_output': "A comprehensive README.md file with setup instructions, API documentation, and usage examples."
        },
        'security_audit': {
            'name': 'Cyber Sam',
            'title': 'Security Audit',
            'icon': '🔒',
            'role': 'security_engineer',
            'description': 'Performs security audits and suggests improvements. Paranoid about everything.',
            'llm': 'openai/gpt-4o-mini',
            'enabled': True,
            'dependencies': ['backend_code'],
            'output_file': 'output/security_report.md',
            'backstory': "You're a cybersecurity expert who identifies security vulnerabilities and provides actionable recommendations.",
            'goal_template': "Perform a security audit of the backend code and provide recommendations for improvements.",
            'task_description': "Analyze the backend code for security vulnerabilities including input validation, authentication, authorization, and data handling. Provide specific recommendations.",
            'expected_output': "A detailed security audit report with identified vulnerabilities and specific recommendations for improvement."
        },
        'performance_optimizer': {
            'name': 'Speedy Steve',
            'title': 'Optimizer',
            'icon': '⚡',
            'role': 'performance_engineer',
            'description': 'Optimizes code for speed and efficiency. Hates slow queries.',
            'llm': 'openai/gpt-4o-mini',
            'enabled': True,
            'dependencies': ['backend_code'],
            'output_file': 'output/performance_report.md',
            'backstory': "You're a performance engineering expert who identifies bottlenecks and optimizes code for maximum efficiency.",
            'goal_template': "Analyze the code for performance bottlenecks and provide optimization recommendations.",
            'task_description': "Review the backend code for performance issues including algorithmic complexity, database queries, memory usage, and suggest specific optimizations.",
            'expected_output': "A performance analysis report with identified bottlenecks and specific optimization recommendations."
        },
        'deployment': {
            'name': 'Deploy Dan',
            'title': 'DevOps',
            'icon': '🚀',
            'role': 'devops_engineer',
            'description': 'Creates deployment scripts and CI/CD pipelines. Lives in the cloud.',
            'llm': 'openai/gpt-4o-mini',
            'enabled': True,
            'dependencies': ['backend_code', 'frontend_code', 'tests'],
            'output_file': 'output/deploy.sh',
            'backstory': "You're a DevOps engineer who creates reliable deployment scripts and CI/CD pipelines.",
            'goal_template': "Create deployment scripts and configuration for the application.",
            'task_description': "Create deployment scripts, Docker configuration, and CI/CD pipeline setup for the application. Include environment setup and production deployment steps.",
            'expected_output': "Deployment scripts and configuration files ready for production deployment."
        }
    }
    
    @classmethod
    def get_enabled_agents(cls) -> Dict[str, Dict[str, Any]]:
        """Get only the enabled agent configurations."""
        return {key: config for key, config in cls.AGENT_CONFIG.items() if config.get('enabled', True)}
    
    @classmethod
    def get_task_order(cls) -> List[str]:
        """Get the order in which tasks should be executed based on dependencies."""
        enabled_agents = cls.get_enabled_agents()
        ordered = []
        
        def add_agent(agent_key):
            if agent_key in ordered or agent_key not in enabled_agents:
                return
            
            # Add dependencies first
            for dep in enabled_agents[agent_key].get('dependencies', []):
                add_agent(dep)
            
            ordered.append(agent_key)
        
        # Add all enabled agents in dependency order
        for agent_key in enabled_agents.keys():
            add_agent(agent_key)
        
        return ordered
    
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
