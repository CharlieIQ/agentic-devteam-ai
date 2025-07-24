import sys
import os

# Add the src directory to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
import traceback
import logging
import queue
import threading
import time
import io

# Load environment variables
load_dotenv()

# Global queue for live logs
log_queue = queue.Queue()

class CrewAILogCapture:
    """Captures stdout/stderr to forward CrewAI agent logs to SSE"""
    def __init__(self, original_stream):
        self.original_stream = original_stream
        self.buffer = io.StringIO()
        
    def write(self, text):
        # Write to original stream
        self.original_stream.write(text)
        self.original_stream.flush()
        
        # Filter and send relevant lines to log queue
        lines = text.strip().split('\n') if text.strip() else []
        for line in lines:
            cleaned_line = self._clean_ansi_codes(line)
            if self._is_agent_log(cleaned_line) and cleaned_line.strip():
                try:
                    log_queue.put(cleaned_line)
                except:
                    pass
    
    def _clean_ansi_codes(self, text):
        """Remove ANSI escape codes and clean up the text"""
        import re
        # Remove ANSI escape sequences
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cleaned = ansi_escape.sub('', text)
        
        # Remove cursor movement codes
        cursor_codes = re.compile(r'\[2K\[1A|\[2K|\[1A')
        cleaned = cursor_codes.sub('', cleaned)
        
        # Clean up extra whitespace but preserve formatting
        cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
        
        return cleaned.strip()
    
    def _is_agent_log(self, line):
        """Check if the log line is a substantive agent/task/requirements/instructions log"""
        if not line or len(line.strip()) < 3:
            return False

        # Only include lines that are:
        # - Agent role lines
        # - Task lines
        # - Requirements/instructions/test instructions
        # - Lines containing 'Requirements:', '📝', or test-related keywords
        include_patterns = [
            r'^Agent:\s',                # Agent: ...
            r'^Task:\s',                 # Task: ...
            r'Requirements:',            # Requirements: ...
            r'📝',                       # Emoji for requirements
            r'\btest(s)?\b',             # test, tests
            r'\bunit test(s)?\b',        # unit test(s)
            r'\bintegration test(s)?\b', # integration test(s)
            r'\bend-to-end\b',           # end-to-end
            r'\bmock\b',                 # mock
            r'\bcoverage\b',             # coverage
            r'\bedge case(s)?\b',        # edge case(s)
            r'^\s*\d+\.\s',              # Numbered requirements/instructions
            r'^\s*✅',                   # Checked requirements
            r'^\s*⚙️',                   # Non-functional requirements
        ]

        # Exclude lines that are:
        # - Status/progress/crew/assignment/emoji/status lines
        # - Empty or whitespace
        # - Borders, progress, assignment, or emoji-only lines
        exclude_patterns = [
            r'^Status:', r'^Assigned to:', r'^Crew:', r'^├──', r'^└──', r'^│', r'^╭─', r'^╰─', r'─────',
            r'🤖', r'📋', r'✅$', r'⚠️', r'❌', r'Executing Task', r'Agent Started', r'Agent Completed',
            r'^Let me', r'^I need to', r'Engineering Team Lead', r'Senior Backend Engineer',
            r'Frontend Engineer', r'Test Engineer', r'Task Completion', r'Client connected', r'Client disconnected',
            r'werkzeug', r'INFO', r'DEBUG', r'WARNING', r'ERROR', r'HTTP/1.1', r'Starting Flask', r'Running on',
            r'__main__', r'\[HEARTBEAT\]', r'crewai\[tools\]', r'Traceback'
        ]

        import re
        # If any exclude pattern matches, skip
        for pat in exclude_patterns:
            if re.search(pat, line):
                return False

        # If any include pattern matches, allow
        for pat in include_patterns:
            if re.search(pat, line, re.IGNORECASE):
                return True

        # Otherwise, skip
        return False

    def flush(self):
        self.original_stream.flush()
    
    def isatty(self):
        """Return whether this is an 'interactive' stream"""
        return getattr(self.original_stream, 'isatty', lambda: False)()
    
    def readable(self):
        """Return whether object supports reading"""
        return getattr(self.original_stream, 'readable', lambda: False)()
    
    def writable(self):
        """Return whether object supports writing"""
        return getattr(self.original_stream, 'writable', lambda: True)()
    
    def seekable(self):
        """Return whether object supports seeking"""
        return getattr(self.original_stream, 'seekable', lambda: False)()
    
    def fileno(self):
        """Return file descriptor if available"""
        return getattr(self.original_stream, 'fileno', lambda: None)()
    
    def __getattr__(self, name):
        """Delegate any other attributes to the original stream"""
        return getattr(self.original_stream, name)

# Capture stdout and stderr for CrewAI logs
original_stdout = sys.stdout
original_stderr = sys.stderr
sys.stdout = CrewAILogCapture(original_stdout)
sys.stderr = CrewAILogCapture(original_stderr)

# Set up basic logging (but we'll mainly use stdout capture)
logging.basicConfig(level=logging.WARNING)  # Reduce log level to avoid noise
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Disable Flask's default logging to reduce noise
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# Try to import the engineering team
try:
    from engineering_team.crew import EngineeringTeam
    CREW_AVAILABLE = True
    print("✅ CrewAI modules loaded successfully")
except ImportError as e:
    print(f"❌ Failed to import EngineeringTeam: {e}")
    print("Please install CrewAI with: pip install crewai[tools]")
    CREW_AVAILABLE = False

# In-memory storage for requirements
stored_requirements = ""

@app.route('/logs')
def stream_logs():
    """Server-Sent Events endpoint for streaming live logs"""
    def generate():
        print("🔌 Client connected to live agent logs")
        try:
            while True:
                try:
                    # Get log from queue with timeout
                    log_entry = log_queue.get(timeout=30)
                    yield f"data: {log_entry}\n\n"
                except queue.Empty:
                    # Send heartbeat to keep connection alive
                    yield f"data: [HEARTBEAT] Connection alive\n\n"
                except Exception as e:
                    print(f"❌ Error in log stream: {e}")
                    break
        except GeneratorExit:
            print("🔌 Client disconnected from live agent logs")
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*'
        }
    )

@app.route('/requirements', methods=['POST'])
def set_requirements():
    global stored_requirements
    try:
        data = request.get_json()
        if not data or 'requirements' not in data:
            return jsonify({'status': 'error', 'message': 'Missing requirements data'}), 400
        
        stored_requirements = data['requirements']
        print("📝 Requirements stored successfully")
        return jsonify({'status': 'success', 'requirements': stored_requirements})
    except Exception as e:
        print(f"❌ Error setting requirements: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_code():
    try:
        if not CREW_AVAILABLE:
            error_msg = 'CrewAI not available. Please install with: pip install crewai[tools]'
            print(f"❌ {error_msg}")
            return jsonify({
                'status': 'error', 
                'message': error_msg
            }), 500
        
        # Check if requirements were provided in the request body first
        data = request.get_json() or {}
        requirements = data.get('requirements', stored_requirements)
        
        if not requirements or not requirements.strip():
            print("❌ No requirements found in request or storage")
            return jsonify({'status': 'error', 'message': 'No requirements provided. Please save your requirements first.'}), 400
        
        print("🚀 Starting code generation...")
        print(f"📋 Requirements: {requirements[:200]}...")
        
        # Create and configure the engineering team
        engineering_team = EngineeringTeam()
        
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
        
        # Extract structured outputs from all tasks
        outputs = {}
        if hasattr(result, 'tasks_output') and result.tasks_output:
            print(f"📊 Found {len(result.tasks_output)} task outputs")
            for i, task_output in enumerate(result.tasks_output):
                task_name = ['design', 'backend_code', 'frontend_code', 'tests'][i] if i < 4 else f'task_{i}'
                agent_name = 'Unknown'
                
                # Try to get agent name from task output
                if hasattr(task_output, 'agent'):
                    agent_name = str(task_output.agent)
                elif hasattr(task_output, 'task') and hasattr(task_output.task, 'agent'):
                    agent_name = str(task_output.task.agent.role)
                
                output_text = str(task_output.raw if hasattr(task_output, 'raw') else task_output)
                
                outputs[task_name] = {
                    'agent': agent_name,
                    'output': output_text
                }
                print(f"✅ Task {i+1} ({task_name}): {len(output_text)} characters from {agent_name}")
        else:
            # Fallback for single output
            print("📝 Using fallback for single output")
            outputs['complete_result'] = {
                'agent': 'Engineering Team',
                'output': str(result.raw if hasattr(result, 'raw') else result)
            }
        
        print("🎉 Code generation completed successfully!")
        print(f"📦 Generated {len(outputs)} outputs")
        
        return jsonify({
            'status': 'success',
            'requirements': requirements,
            'outputs': outputs
        })
        
    except Exception as e:
        print(f"❌ Error generating code: {e}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error', 
            'message': f"Code generation failed: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'message': 'Backend is running',
        'crewai_available': CREW_AVAILABLE
    })

if __name__ == '__main__':
    if not CREW_AVAILABLE:
        print("⚠️  CrewAI is not installed. Please run: pip install crewai[tools]")
    print("🚀 Starting Flask app on port 5001...")
    
    # Start Flask with minimal logging
    app.run(debug=False, port=5001, host='0.0.0.0', use_reloader=False)