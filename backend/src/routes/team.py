"""
Routes for team configuration.
"""
from flask import Blueprint, jsonify
from ..config import Config
import logging

logger = logging.getLogger(__name__)

team_bp = Blueprint('team', __name__)

@team_bp.route('/team-config', methods=['GET'])
def get_team_config():
    """Get the team configuration for the frontend."""
    try:
        # Get all agent configurations with enabled status
        all_agents = Config.get_all_agents()
        
        # Format the data for frontend consumption
        team_config = {}
        for key, agent in all_agents.items():
            team_config[key] = {
                'name': agent.get('name', 'Unknown'),
                'title': agent.get('title', key.title()),
                'icon': agent.get('icon', '📄'),
                'description': agent.get('description', 'No description available'),
                'enabled': agent.get('enabled', False)
            }
        
        return jsonify(team_config)
    except Exception as e:
        logger.error(f"Error getting team config: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Could not load team configuration'
        }), 500
