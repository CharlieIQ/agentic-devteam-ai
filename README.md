# Charlie's Agentic AI Development Team

## Overview
This repository contains a fully automated AI development team built using [CrewAI](https://github.com/crew-ai/crew-ai), designed to create fullstack software applications from natural language requirements. The system utilizes specialized AI agents that collaborate to handle the entire software development lifecycle - from requirements analysis to testing.

The project demonstrates the power of agentic AI by automating complex development tasks typically requiring multiple human developers, complete with a modern React frontend for real-time interaction and monitoring.

*Built upon concepts from Ed Donner's [Agentic AI course](https://github.com/ed-donner/agents), significantly expanded with a full frontend interface, comprehensive logging, and enhanced workflow management.*

## Features
- **Autonomous Development**: Complete software development from requirements to testing
- **Interactive Frontend**: React-based UI for real-time agent monitoring and task management
- **Robust Backend**: Flask-powered API with comprehensive logging and error handling
- **Live Progress Tracking**: Real-time logs and agent status updates
- **Configurable Agents**: Easily customizable AI agents and tasks through YAML configuration
- **Organized Output**: Structured file generation with proper project organization

## Technologies Used
- **Frontend**: React 19, Vite, CSS3, React Markdown
- **Backend**: Python 3.11+, Flask, CrewAI, OpenAI API
- **AI Model**: GPT-4o-mini for optimal cost-performance balance
- **Development**: ESLint, Hot Reload, Virtual Environment Management

## AI Agents
My system employs four specialized AI agents working in harmony:

- **Engineering Lead**: Analyzes requirements and creates detailed software architecture designs
- **Frontend Engineer**: Develops React-based user interfaces following design specifications
- **Backend Engineer**: Implements Python backend logic with proper class structures and methods
- **QA Engineer**: Creates comprehensive unit tests to ensure code quality and functionality

Each agent is powered by GPT-4o-mini and configured with specific roles, goals, and backstories for optimal performance.
## Project Structure

### Frontend (`/frontend`)
```
frontend/
├── public/                 # Static assets and favicons
├── src/
│   ├── components/         # Reusable React components
│   │   ├── AgentOutput.jsx      # Displays agent execution results
│   │   ├── CodeOutputs.jsx      # Shows generated code files
│   │   ├── LiveLogs.jsx         # Real-time logging display
│   │   ├── RequirementsForm.jsx # User input form for requirements
│   │   └── TeamOverview.jsx     # Agent status and overview
│   ├── styles/            # Component-specific CSS files
│   ├── App.jsx            # Main application component
│   └── main.jsx           # React application entry point
├── package.json           # Dependencies and scripts
└── vite.config.js         # Vite build configuration
```

### Backend (`/backend`)
```
backend/
├── config/                # Agent and task configurations
│   ├── agents.yaml             # AI agent definitions and prompts
│   └── tasks.yaml              # Task workflows and dependencies
├── src/                   # Core application logic
│   ├── routes/                 # Flask API endpoints
│   │   ├── generate.py         # Main generation endpoint
│   │   ├── health.py           # Health check endpoint
│   │   ├── logs.py             # Logging endpoints
│   │   └── requirements.py     # Requirements management
│   ├── services/               # Business logic services
│   │   ├── crewai_service.py   # CrewAI integration service
│   │   └── requirements_service.py # Requirements processing
│   └── utils/                  # Utility functions
│       └── logging.py          # Centralized logging setup
├── tools/                 # Custom CrewAI tools
├── output/                # Generated code and documentation
├── knowledge/             # System knowledge and preferences
├── app.py                 # Main Flask application
├── crew.py                # CrewAI crew configuration
└── requirements.txt       # Python dependencies
```

## Getting Started

### Prerequisites
- **Node.js 18+** for the frontend
- **Python 3.11+** for the backend
- **OpenAI API Key** for AI agent functionality

### Frontend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CharlieIQ/agentic-devteam-ai.git
   cd agentic-devteam-ai
   ```

2. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

3. **Install dependencies:**
   ```bash
   npm install
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:** Navigate to `http://localhost:5173` (default port for Vite)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the backend directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Start the backend server:**
   ```bash
   python app.py
   ```

6. **Verify backend:** The API will be running on `http://localhost:5001`

### Alternative: Using CrewAI CLI
For command-line usage without the frontend:
```bash
# From the backend directory
crewai run
```

## Customizing and Adding Agents

### Adding New Agents
To add new AI agents to your development team:

1. **Define the agent in `backend/config/agents.yaml`:**
   ```yaml
   your_new_agent:
     role: >
       Brief description of the agent's role
     goal: >
       Detailed description of what the agent should accomplish.
       Use {requirements} and other variables as needed.
     backstory: >
       Background story that gives the agent context and personality
     llm: openai/gpt-4o-mini
   ```

2. **Add corresponding task in `backend/config/tasks.yaml`:**
   ```yaml
   your_new_task:
     description: >
       Detailed task description with specific instructions.
       Reference variables like {requirements} or {module_name}.
     expected_output: >
       Clear description of expected deliverable format and content.
     agent: your_new_agent
     context:
       - dependency_task_1  # List any prerequisite tasks
       - dependency_task_2
     output_file: output/your_output_file.ext
   ```

3. **Update the crew configuration in `backend/crew.py`** to include your new agent and task.

### Agent Configuration Best Practices
- **Role**: Keep it concise but descriptive
- **Goal**: Be specific about inputs (`{requirements}`) and expected outputs
- **Backstory**: Provide context that influences the agent's "thinking"
- **Context**: Ensure proper task dependencies for sequential execution
- **Output Files**: Use descriptive names and appropriate file extensions

### Example: Adding a DevOps Agent
```yaml
# In agents.yaml
devops_engineer:
  role: >
    DevOps Engineer specializing in deployment and infrastructure
  goal: >
    Create deployment configuration and CI/CD pipeline for the application.
    Requirements: {requirements}
  backstory: >
    You're an experienced DevOps engineer who excels at containerization,
    cloud deployment, and automated testing pipelines.
  llm: openai/gpt-4o-mini

# In tasks.yaml
deployment_task:
  description: >
    Create Dockerfile, docker-compose.yml, and GitHub Actions workflow
    for the application based on the requirements: {requirements}
  expected_output: >
    Complete deployment configuration including containerization and CI/CD setup.
  agent: devops_engineer
  context:
    - code_task
    - test_task
  output_file: output/deployment_config.yml
```

## Usage

1. **Access the frontend** at `http://localhost:5173`
2. **Enter your software requirements** in natural language
3. **Watch the AI agents collaborate** in real-time through the live logs
4. **Review generated outputs** including:
   - Design documentation (`DESIGN.md`)
   - Backend Python code (`main.py`)
   - Frontend React component (`App.jsx`)
   - Unit tests (`test_main.py`)

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /generate` - Trigger agent workflow with requirements
- `GET /logs` - Retrieve execution logs
- `GET /requirements` - Get current requirements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CrewAI](https://github.com/crew-ai/crew-ai) for the super cool agent framework
- [Ed Donner](https://github.com/ed-donner/agents) for the foundational agentic AI concepts
- OpenAI for providing the GPT-4o-mini model 
- Copilot for code generation assistance (haha)

---

*Built with love and $5 of OpenAI credits*