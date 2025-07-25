"""
Service for CrewAI operations and code generation.
"""
import os
import sys
from typing import Dict, Any, Optional
import traceback
from ..config import Config

class CrewAIService:
    """Service for managing CrewAI operations."""
    
    def __init__(self):
        self._crew_available = False
        self._engineering_team = None
        self._initialize_crew()
    
    def _initialize_crew(self) -> None:
        """Initialize the CrewAI engineering team."""
        try:
            # Import from the existing crew.py file in the backend directory
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
            from crew import EngineeringTeam
            self._engineering_team = EngineeringTeam
            self._crew_available = True
            print("✅ CrewAI modules loaded successfully")
        except ImportError as e:
            print(f"❌ Failed to import EngineeringTeam: {e}")
            print("Please install CrewAI with: pip install crewai[tools]")
            self._crew_available = False
    
    @property
    def is_available(self) -> bool:
        """Check if CrewAI is available."""
        return self._crew_available
    
    def generate_code(self, requirements: str) -> Dict[str, Any]:
        """Generate code using the engineering team."""
        if not self._crew_available:
            raise RuntimeError('CrewAI not available. Please install with: pip install crewai[tools]')
        
        if not requirements or not requirements.strip():
            raise ValueError('No requirements provided')
        
        print("🚀 Starting code generation...")
        print(f"📋 Requirements: {requirements[:200]}...")
        
        try:
            # Create and configure the engineering team
            engineering_team = self._engineering_team()
            
            # Update the crew's requirements data before running
            engineering_team.requirements_data = requirements
            
            # Run the crew with requirements
            inputs = {
                'requirements': requirements,
                'module_name': 'main.py',
                'class_name': 'Application'
            }
            
            print(f"⚙️ Running crew with inputs: {list(inputs.keys())}")
            print("🎬 Starting CrewAI execution - watch the live logs below!")
            
            result = engineering_team.crew().kickoff(inputs=inputs)
            
            # Extract structured outputs from all tasks using config
            outputs = self._extract_outputs(result)
            
            print("🎉 Code generation completed successfully!")
            print(f"📦 Generated {len(outputs)} outputs")
            
            return {
                'status': 'success',
                'requirements': requirements,
                'outputs': outputs
            }
            
        except Exception as e:
            print(f"❌ Error generating code: {e}")
            print(traceback.format_exc())
            raise RuntimeError(f"Code generation failed: {str(e)}")
    
    def _extract_outputs(self, result) -> Dict[str, Dict[str, str]]:
        """Extract structured outputs from CrewAI result using configuration."""
        outputs = {}
        task_order = Config.get_task_order()
        agent_config = Config.get_all_agents()
        
        if hasattr(result, 'tasks_output') and result.tasks_output:
            print(f"📊 Found {len(result.tasks_output)} task outputs")
            
            for i, task_output in enumerate(result.tasks_output):
                # Use config to determine task name and agent info
                task_key = task_order[i] if i < len(task_order) else f'task_{i}'
                config = agent_config.get(task_key, {})
                agent_name = config.get('name', 'Unknown')
                
                # Try to get agent name from task output if not in config
                if agent_name == 'Unknown':
                    if hasattr(task_output, 'agent'):
                        agent_name = str(task_output.agent)
                    elif hasattr(task_output, 'task') and hasattr(task_output.task, 'agent'):
                        agent_name = str(task_output.task.agent.role)
                
                output_text = str(task_output.raw if hasattr(task_output, 'raw') else task_output)
                
                outputs[task_key] = {
                    'agent': agent_name,
                    'output': output_text
                }
                print(f"✅ Task {i+1} ({task_key}): {len(output_text)} characters from {agent_name}")
        
        # No fallback needed - frontend will combine outputs
        return outputs


# Global instance for the application
crewai_service = CrewAIService()
