"""
Routes for health checks.
"""
from flask import Blueprint, jsonify
from ..services.crewai_service import crewai_service

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy', 
        'message': 'Backend is running',
        'crewai_available': crewai_service.is_available
    })
