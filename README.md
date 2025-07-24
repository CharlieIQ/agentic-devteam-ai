# Charlie's AI Development Team

## Overview
This repository contains the codebase for my agentic AI development team built using CrewAI, focusing on building fullstack software applications. 

The team is dedicated to creating innovative AI solutions that enhance productivity and streamline workflows.

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

