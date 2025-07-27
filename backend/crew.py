from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.config import Config
import yaml
import os

@CrewBase
class EngineeringTeam():
    """
    This class defines the Engineering Team crew, which dynamically configures agents and tasks based on the provided YAML configuration files.
    It includes core agents like engineering lead, backend engineer, frontend engineer, test engineer, and
    additional agents like documentation engineer, security engineer, performance engineer, and devops engineer if they are enabled in the configuration.
    The crew also includes core tasks such as design, code, frontend, test, documentation,
    security audit, performance optimization, and deployment tasks.
    
    Each agent and task is created with its configuration, and the crew is built to include only
    the enabled agents and tasks based on the task order defined in the configuration.
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        super().__init__()
        self.enabled_agents = Config.get_enabled_agents()
        self.task_order = Config.get_task_order()

    # Core agents (always available)
    @agent
    def engineering_lead(self) -> Agent:
        """Creates the engineering lead agent"""
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        """Creates the backend engineer agent"""
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        """Creates the frontend engineer agent"""
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
        )
    
    @agent
    def test_engineer(self) -> Agent:
        """Creates the test engineer agent"""
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
        )

    @agent
    def documentation_engineer(self) -> Agent:
        """Creates the documentation engineer agent"""
        return Agent(
            config=self.agents_config.get('documentation_engineer', {
                'role': 'Documentation Engineer',
                'goal': 'Create documentation',
                'backstory': 'Documentation specialist'
            }),
            verbose=True,
        )

    @agent
    def security_engineer(self) -> Agent:
        """Creates the security engineer agent"""
        return Agent(
            config=self.agents_config.get('security_engineer', {
                'role': 'Security Engineer',
                'goal': 'Perform security analysis',
                'backstory': 'Security specialist'
            }),
            verbose=True,
        )

    @agent
    def performance_engineer(self) -> Agent:
        """Creates the performance engineer agent"""
        return Agent(
            config=self.agents_config.get('performance_engineer', {
                'role': 'Performance Engineer',
                'goal': 'Optimize performance',
                'backstory': 'Performance specialist'
            }),
            verbose=True,
        )

    @agent
    def devops_engineer(self) -> Agent:
        """Creates the devops engineer agent"""
        return Agent(
            config=self.agents_config.get('devops_engineer', {
                'role': 'DevOps Engineer',
                'goal': 'Handle deployment',
                'backstory': 'DevOps specialist'
            }),
            verbose=True,
        )

    # Core tasks
    @task
    def design_task(self) -> Task:
        """Creates the design task"""
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def code_task(self) -> Task:
        """Creates the backend code task"""
        return Task(
            config=self.tasks_config['code_task'],
        )

    @task
    def frontend_task(self) -> Task:
        """Creates the frontend task"""
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @task
    def test_task(self) -> Task:
        """Creates the test task"""
        return Task(
            config=self.tasks_config['test_task'],
        )

    @task
    def documentation_task(self) -> Task:
        """Creates the documentation task"""
        if 'documentation' in self.enabled_agents:
            return Task(
                description=self.enabled_agents['documentation']['task_description'],
                expected_output=self.enabled_agents['documentation']['expected_output'],
                agent=self.documentation_engineer(),
                context=[self.code_task(), self.frontend_task()],
                output_file=self.enabled_agents['documentation']['output_file']
            )
        else:
            # Return a minimal task that won't be included in the crew
            return Task(
                description="Placeholder documentation task",
                expected_output="Documentation placeholder",
                agent=self.documentation_engineer(),
            )

    @task
    def security_audit_task(self) -> Task:
        """Creates the security audit task"""
        if 'security_audit' in self.enabled_agents:
            return Task(
                description=self.enabled_agents['security_audit']['task_description'],
                expected_output=self.enabled_agents['security_audit']['expected_output'],
                agent=self.security_engineer(),
                context=[self.code_task()],
                output_file=self.enabled_agents['security_audit']['output_file']
            )
        else:
            # Return a minimal task that won't be included in the crew
            return Task(
                description="Placeholder security task",
                expected_output="Security placeholder",
                agent=self.security_engineer(),
            )

    @task
    def performance_task(self) -> Task:
        """Creates the performance optimization task"""
        if 'performance_optimizer' in self.enabled_agents:
            return Task(
                description=self.enabled_agents['performance_optimizer']['task_description'],
                expected_output=self.enabled_agents['performance_optimizer']['expected_output'],
                agent=self.performance_engineer(),
                context=[self.code_task()],
                output_file=self.enabled_agents['performance_optimizer']['output_file']
            )
        else:
            # Return a minimal task that won't be included in the crew
            return Task(
                description="Placeholder performance task",
                expected_output="Performance placeholder",
                agent=self.performance_engineer(),
            )

    @task
    def deployment_task(self) -> Task:
        """Creates the deployment task"""
        if 'deployment' in self.enabled_agents:
            return Task(
                description=self.enabled_agents['deployment']['task_description'],
                expected_output=self.enabled_agents['deployment']['expected_output'],
                agent=self.devops_engineer(),
                context=[self.code_task(), self.frontend_task(), self.test_task()],
                output_file=self.enabled_agents['deployment']['output_file']
            )
        else:
            # Return a minimal task that won't be included in the crew
            return Task(
                description="Placeholder deployment task",
                expected_output="Deployment placeholder",
                agent=self.devops_engineer(),
            )

    @crew
    def crew(self) -> Crew:
        """Creates the engineering crew with only enabled agents and tasks"""
        # Get all enabled agents and tasks
        enabled_agents = []
        enabled_tasks = []
        
        # Map of agent methods
        agent_methods = {
            'design': self.engineering_lead,
            'backend_code': self.backend_engineer,
            'frontend_code': self.frontend_engineer,
            'tests': self.test_engineer,
            'documentation': self.documentation_engineer,
            'security_audit': self.security_engineer,
            'performance_optimizer': self.performance_engineer,
            'deployment': self.devops_engineer,
        }
        
        # Map of task methods
        task_methods = {
            'design': self.design_task,
            'backend_code': self.code_task,
            'frontend_code': self.frontend_task,
            'tests': self.test_task,
            'documentation': self.documentation_task,
            'security_audit': self.security_audit_task,
            'performance_optimizer': self.performance_task,
            'deployment': self.deployment_task,
        }
        
        # Add enabled agents and tasks in dependency order
        for agent_key in self.task_order:
            # Check if the agent is enabled and exists in the agent methods
            if agent_key in agent_methods and agent_key in self.enabled_agents:
                # Create the agent and task if they are enabled
                agent = agent_methods[agent_key]()
                enabled_agents.append(agent)
                
                task = task_methods[agent_key]()
                enabled_tasks.append(task)
        
        return Crew(
            agents=enabled_agents,
            tasks=enabled_tasks,
            process=Process.sequential,
            verbose=True,
        )