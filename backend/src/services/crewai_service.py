"""
Service for CrewAI operations and code generation.
"""
import os
import sys
from typing import Dict, Any, Optional
import traceback
from ..config import Config

class CrewAIService:
    """
    Service for managing CrewAI operations.
    
    This service provides functionality to generate code based on user requirements
    using the CrewAI engineering team. It initializes the CrewAI modules and provides
    methods to generate code, extract outputs, and check availability.
    
    Attributes:
        _crew_available: A boolean indicating if CrewAI is available.
        _engineering_team: The CrewAI engineering team class.
    Methods:
        is_available() -> bool: Check if CrewAI is available.
        generate_code(requirements: str) -> Dict[str, Any]: Generate code based on requirements
        _extract_outputs(result) -> Dict[str, Dict[str, str]]: Extract structured outputs from CrewAI result.
    Usage:
        This service can be used to generate code based on user requirements in applications
        where automated code generation is needed, such as in development tools or AI-assisted coding environments.        
    """
    
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
            raise RuntimeError('CrewAI not available. Please install with: pip install crewai')
        
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
                print(f"🔍 Processing task {i+1}: {type(task_output)}")
                
                # Use config to determine task name and agent info
                task_key = task_order[i] if i < len(task_order) else f'task_{i+1}'
                config = agent_config.get(task_key, {})
                agent_name = config.get('name', 'Unknown')
                
                # Try to get agent name from task output if not in config
                if agent_name == 'Unknown':
                    try:
                        if hasattr(task_output, 'agent') and task_output.agent:
                            agent_name = str(task_output.agent)
                        elif (hasattr(task_output, 'task') and 
                              hasattr(task_output.task, 'agent') and 
                              task_output.task.agent and
                              hasattr(task_output.task.agent, 'role')):
                            agent_name = str(task_output.task.agent.role)
                    except (AttributeError, TypeError) as e:
                        print(f"⚠️ Could not extract agent name from task output: {e}")
                        agent_name = f'Agent_{i+1}'
                
                # Try multiple ways to extract output text
                output_text = ""
                try:
                    # Try different attributes that might contain the output
                    if hasattr(task_output, 'raw') and task_output.raw:
                        output_text = str(task_output.raw)
                    elif hasattr(task_output, 'result') and task_output.result:
                        output_text = str(task_output.result)
                    elif hasattr(task_output, 'output') and task_output.output:
                        output_text = str(task_output.output)
                    elif hasattr(task_output, 'content') and task_output.content:
                        output_text = str(task_output.content)
                    else:
                        # Fallback to string representation
                        output_text = str(task_output)
                        
                    # Clean up the output text
                    if output_text:
                        # Remove common prefixes that might be added by CrewAI
                        output_text = output_text.strip()
                        if output_text.startswith('Output:'):
                            output_text = output_text[7:].strip()
                        if output_text.startswith('Result:'):
                            output_text = output_text[7:].strip()
                            
                except (AttributeError, TypeError) as e:
                    print(f"⚠️ Could not extract output text from task: {e}")
                    output_text = f"Error extracting output from {agent_name}"
                
                # Only add to outputs if we have meaningful content
                if output_text and len(output_text.strip()) > 10:
                    outputs[task_key] = {
                        'agent': agent_name,
                        'output': output_text
                    }
                    print(f"✅ Task {i+1} ({task_key}): {len(output_text)} characters from {agent_name}")
                else:
                    print(f"⚠️ Task {i+1} ({task_key}): No meaningful output from {agent_name}")
        
        # Also check for any additional outputs in the result
        if hasattr(result, 'output') and result.output:
            print(f"📦 Found additional result output: {len(str(result.output))} characters")
            if not outputs:
                outputs['result'] = {
                    'agent': 'CrewAI',
                    'output': str(result.output)
                }
        
        return outputs


# Global instance for the application
crewai_service = CrewAIService()
