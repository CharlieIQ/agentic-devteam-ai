"""
Routes for requirements management.
"""
from flask import Blueprint, request, jsonify
from ..services.requirements_service import requirements_service
from ..config import Config

requirements_bp = Blueprint('requirements', __name__)

@requirements_bp.route('/requirements', methods=['POST'])
def set_requirements():
    """Set user requirements."""
    try:
        data = request.get_json()
        if not data or 'requirements' not in data:
            return jsonify({
                'status': 'error', 
                'message': 'Missing requirements data'
            }), 400
        
        user_requirements = data['requirements']
        
        # Validate requirements
        try:
            requirements_service.validate_requirements(
                user_requirements, 
                Config.MAX_REQUIREMENTS_LENGTH
            )
        except ValueError as e:
            return jsonify({
                'status': 'error', 
                'message': str(e)
            }), 400
        
        # Store requirements
        requirements_service.set_requirements(user_requirements)
        print("📝 Requirements stored successfully")
        
        return jsonify({
            'status': 'success', 
            'requirements': user_requirements
        })
        
    except Exception as e:
        print(f"❌ Error setting requirements: {e}")
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 500

@requirements_bp.route('/requirements', methods=['GET'])
def get_requirements():
    """Get stored requirements."""
    try:
        stored = requirements_service.get_requirements()
        return jsonify({
            'status': 'success',
            'requirements': stored,
            'has_requirements': requirements_service.has_requirements()
        })
    except Exception as e:
        print(f"❌ Error getting requirements: {e}")
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 500
