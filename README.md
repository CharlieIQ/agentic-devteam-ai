# Charlie's AI Development Team

## Overview
This repository contains the codebase for my agentic AI development team built using [CrewAI](https://github.com/crew-ai/crew-ai), focusing on building fullstack software applications.

The project is designed to automate the process of software development by utilizing AI agents that can handle various tasks such as requirement gathering, design, coding, and testing.

This was a project built based off of a project done for a course in [Agentic AI](https://github.com/ed-donner/agents) by Ed Donner. I just expanded on it to create a frontend, better logging, and more features.

## Features
- **Frontend**: A React-based frontend for interacting with the AI agents.
- **Backend**: A Python-based backend that manages the AI agents and their tasks.
- **Task Management**: AI agents can handle tasks such as requirement gathering, design, coding, and testing.
- **Logging**: Comprehensive logging of agent activities and task progress.
- **Configuration**: Easily configurable tasks and agents through YAML files.

## Technologies Used
- **Frontend**: React, Vite, CSS
- **Backend**: Python, Flask, CrewAI
- **AI**: OpenAI API for natural language processing and task management

## AI Agents
- **Engineering Lead**: Gathers requirements and designs the software architecture.
- **Frontend Engineer**: Implements the frontend based on the design provided by the engineering lead.
- **Backend Engineer**: Implements the backend logic and integrates with the frontend.
- **QA Engineer**: Tests the software to ensure it meets the requirements and is bug-free.

I'm using gpt-4o-mini .
## Getting Started
### Running the frontend
To get started with the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agentic-devteam-ai.git
   ```

2. Navigate to the project directory:
   ```bash
   cd agentic-devteam-ai
   ```

3. Install the required dependencies:
   ```bash
   npm install
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```
5. Open your browser and go to `http://localhost:5173` to view the application.

### Running the backend
To run the backend, follow these steps:
1. Ensure you have Python installed on your machine.
2. Navigate to the backend directory:
3. ```bash
   cd backend
   ```
4. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
5. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
      source venv/bin/activate
      ```
6. Install the required Python packages:
    ```bash
   pip install -r requirements.txt
   ```

7. To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

8. Add your OpenAI API key to the `.env` file in the backend directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

9. Start the backend server:
   ```bash
   python app.py
   ```
10. The backend will be running on `http://localhost:5001`.

