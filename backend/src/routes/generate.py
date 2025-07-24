"""
Routes for code generation.
"""
from flask import Blueprint, request, jsonify
from ..services.crewai_service import crewai_service
from ..services.requirements_service import requirements_service

generate_bp = Blueprint('generate', __name__)

@generate_bp.route('/generate', methods=['POST'])
def generate_code():
    """Generate code using CrewAI."""
    try:
        if not crewai_service.is_available:
            error_msg = 'CrewAI not available. Please install with: pip install crewai[tools]'
            print(f"❌ {error_msg}")
            return jsonify({
                'status': 'error', 
                'message': error_msg
            }), 500
        
        # Check if requirements were provided in the request body first
        data = request.get_json() or {}
        requirements = data.get('requirements')
        
        # If no requirements in request, use stored requirements
        if not requirements:
            requirements = requirements_service.get_requirements()
        
        if not requirements or not requirements.strip():
            print("❌ No requirements found in request or storage")
            return jsonify({
                'status': 'error', 
                'message': 'No requirements provided. Please save your requirements first.'
            }), 400
        
        # Generate code using the service
        result = crewai_service.generate_code(requirements)
        return jsonify(result)
        
    except ValueError as e:
        print(f"❌ Validation error: {e}")
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 400
    except RuntimeError as e:
        print(f"❌ Runtime error: {e}")
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 500
    except Exception as e:
        print(f"❌ Unexpected error generating code: {e}")
        return jsonify({
            'status': 'error', 
            'message': f"Code generation failed: {str(e)}"
        }), 500
