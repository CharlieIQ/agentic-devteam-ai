"""
Service for managing user requirements storage.
"""
from typing import Optional

class RequirementsService:
    """
    Service for storing and retrieving user requirements.
    This service allows setting, getting, checking existence, and clearing requirements.

    It also provides validation for the requirements string to ensure it meets certain criteria.
    Attributes:
        _stored_requirements: A string to hold the user requirements.
    Methods:
        set_requirements(requirements: str) -> None: Store user requirements.
        get_requirements() -> str: Retrieve stored requirements.
        has_requirements() -> bool: Check if requirements are stored.
        clear_requirements() -> None: Clear stored requirements.
        validate_requirements(requirements: str, max_length: int = 10000) -> None:
            Validate the requirements string to ensure it is not empty and does not exceed max length.
    Usage:
        This service can be used to manage user requirements in applications where
        requirements need to be stored and validated, such as in task management or project planning tools.
    """
    
    def __init__(self):
        self._stored_requirements: str = ""
    
    def set_requirements(self, requirements: str) -> None:
        """Store user requirements."""
        if not isinstance(requirements, str):
            raise ValueError("Requirements must be a string")
        
        self._stored_requirements = requirements.strip()
    
    def get_requirements(self) -> str:
        """Get stored requirements."""
        return self._stored_requirements
    
    def has_requirements(self) -> bool:
        """Check if requirements are stored."""
        return bool(self._stored_requirements.strip())
    
    def clear_requirements(self) -> None:
        """Clear stored requirements."""
        self._stored_requirements = ""
    
    def validate_requirements(self, requirements: str, max_length: int = 10000) -> None:
        """Validate requirements string."""
        if not requirements or not requirements.strip():
            raise ValueError("Requirements cannot be empty")
        
        if len(requirements) > max_length:
            raise ValueError(f"Requirements too long (max {max_length} characters)")


# Global instance for the application
requirements_service = RequirementsService()
