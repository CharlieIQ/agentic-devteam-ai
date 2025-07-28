"""
Logging utilities for capturing and streaming CrewAI agent logs.
"""
import io
import queue
import re
import sys
import logging
from typing import Optional

# Global queue for live logs
log_queue = queue.Queue()

class CrewAILogCapture:
    """
    Captures stdout/stderr to forward CrewAI agent logs to SSE.
    This class filters and processes log lines to only include relevant agent activity.
    
    It removes ANSI escape codes, cursor movement codes, and filters based on
    specific patterns to determine if a line is substantive agent activity.
    
    It also handles writing to the original stream while capturing logs.
    The captured logs are sent to a global queue for streaming to clients.
    This allows for real-time log streaming without cluttering the output with noise.
    
    Attributes:
        original_stream: The original stdout or stderr stream being captured.
        buffer: A StringIO buffer to temporarily hold log lines before processing.
        recent_logs: A set to track recent log messages to prevent infinite repetition.
    Methods:
        write(text: str) -> None: Write text to the original stream and process for log queue.
        _clean_ansi_codes(text: str) -> str: Remove ANSI escape codes and clean up the text.
        _is_agent_log(line: str) -> bool: Check if the log line is substantive agent activity.
        flush() -> None: Flush the original stream.
        isatty() -> bool: Check if the stream is interactive.
        readable() -> bool: Check if the stream supports reading.
        writable() -> bool: Check if the stream supports writing.
        seekable() -> bool: Check if the stream supports seeking.
        fileno() -> Optional[int]: Return file descriptor if available.
        __getattr__(name: str): Delegate any other attributes to the original stream.
    Usage:
        To use this class, replace sys.stdout and sys.stderr with instances of CrewAILogCapture
        during application startup. This will capture all logs written to stdout/stderr
        and filter them according to the defined criteria.
        The captured logs can then be accessed via the global log queue.
        Example:
            original_stdout, original_stderr = setup_crewai_log_capture()
            # Now all logs written to stdout/stderr will be captured and processed.
    """
    def __init__(self, original_stream):
        self.original_stream = original_stream
        self.buffer = io.StringIO()
        self.recent_logs = set()  # Track recent logs to prevent repetition
        self.max_recent_logs = 100  # Maximum number of recent logs to track
        self.message_counts = {}  # Track how many times each message appears
        self.max_repetitions = 3  # Maximum times a message can be repeated
        
    def write(self, text: str) -> None:
        """Write text to original stream and process for log queue."""
        # Write to original stream
        self.original_stream.write(text)
        self.original_stream.flush()
        
        # Filter and send relevant lines to log queue
        lines = text.strip().split('\n') if text.strip() else []
        for line in lines:
            cleaned_line = self._clean_ansi_codes(line)
            if self._is_agent_log(cleaned_line) and cleaned_line.strip():
                # Check for repetition to prevent infinite loops
                if cleaned_line not in self.recent_logs:
                    # Check rate limiting
                    if cleaned_line in self.message_counts:
                        if self.message_counts[cleaned_line] >= self.max_repetitions:
                            continue  # Skip this message, it's been repeated too much
                        self.message_counts[cleaned_line] += 1
                    else:
                        self.message_counts[cleaned_line] = 1
                    
                    try:
                        log_queue.put(cleaned_line)
                        # Add to recent logs and maintain size limit
                        self.recent_logs.add(cleaned_line)
                        if len(self.recent_logs) > self.max_recent_logs:
                            # Remove oldest entries (convert to list, remove first, convert back)
                            self.recent_logs = set(list(self.recent_logs)[-self.max_recent_logs//2:])
                    except:
                        pass
    
    def _clean_ansi_codes(self, text: str) -> str:
        """Remove ANSI escape codes and clean up the text."""
        # Remove ANSI escape sequences
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cleaned = ansi_escape.sub('', text)
        
        # Remove cursor movement codes
        cursor_codes = re.compile(r'\[2K\[1A|\[2K|\[1A')
        cleaned = cursor_codes.sub('', cleaned)
        
        # Clean up extra whitespace but preserve formatting
        cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
        
        return cleaned.strip()
    
    def _is_agent_log(self, line: str) -> bool:
        """Check if the log line is a substantive agent/task/requirements/instructions log."""
        if not line or len(line.strip()) < 3:
            return False

        # More restrictive include patterns - focus on actual agent activity
        include_patterns = [
            r'^Agent:\s',                # Agent: ...
            r'^Task:\s',                 # Task: ...
            r'Requirements:',            # Requirements: ...
            r'Design:',                  # Design discussions
            r'Implementation:',          # Implementation notes
            r'Testing:',                 # Testing discussions
            r'Frontend:',                # Frontend discussions
            r'Backend:',                 # Backend discussions
            r'\banalyzing\b',            # analyzing
            r'\bimplementing\b',         # implementing
            r'\bcreating\b',             # creating
            r'\bbuilding\b',             # building
            r'\bdesigning\b',            # designing
            r'\btesting\b',              # testing
            r'\bwriting\b',              # writing
            r'\bcode\b',                 # code
            r'\bfunction\b',             # function
            r'\bclass\b',                # class
            r'\bmethod\b',               # method
            r'\bAPI\b',                  # API
            r'\bUI\b',                   # UI
            r'\bcomponent\b',            # component
            r'📝',                       # Emoji for requirements
            r'🔧',                       # Tools/implementation
            r'💻',                       # Code/development
            r'🎨',                       # Design/frontend
            r'🧪',                       # Testing
            r'⚙️',                       # Backend/systems
            r'^\s*\d+\.\s',              # Numbered lists
            r'^\s*[-*]\s',               # Bullet points
            r'Let me',                   # Agent thinking
            r'I need to',                # Agent planning
            r'I will',                   # Agent actions
            r'Here is',                  # Agent output
            r'Here\'s',                  # Agent output
            r'Executing Task', r'Agent Started', r'Agent Completed',  # Status messages
        ]

        # Much more restrictive exclude patterns - exclude CrewAI noise
        exclude_patterns = [
            r'werkzeug', r'HTTP/1.1', r'Starting Flask', r'Running on',
            r'__main__', r'\[HEARTBEAT\]', r'Traceback', r'^\s*$',
            r'Client connected', r'Client disconnected',
            r'^Status:', r'^Assigned to:', r'^Crew:',  # CrewAI internal messages
            r'^├──', r'^└──', r'^│', r'^╭─', r'^╰─', r'─────',  # Tree structures
            r'🤖', r'📋', r'✅$', r'⚠️', r'❌',  # Status emojis
            r'Engineering Team Lead', r'Senior Backend Engineer',  # Role assignments
            r'Frontend Engineer', r'Test Engineer', r'Task Completion',
            r'Python Engineer who can write code',  # Specific repetitive assignment
            r'─{3,}',  # Long dashes (borders)
            r'^\s*$',  # Empty lines
        ]

        import re
        # If any exclude pattern matches, skip
        for pat in exclude_patterns:
            if re.search(pat, line, re.IGNORECASE):
                return False

        # If any include pattern matches, allow
        for pat in include_patterns:
            if re.search(pat, line, re.IGNORECASE):
                return True

        # Also allow any line that's reasonably long and contains useful words
        useful_keywords = ['develop', 'build', 'create', 'implement', 'design', 'test', 'user', 'data', 'system', 'application']
        if len(line) > 20:  # Reasonable length
            for keyword in useful_keywords:
                if keyword.lower() in line.lower():
                    return True

        return False

    def flush(self):
        """Flush the original stream."""
        self.original_stream.flush()
    
    def isatty(self) -> bool:
        """Return whether this is an 'interactive' stream."""
        return getattr(self.original_stream, 'isatty', lambda: False)()
    
    def readable(self) -> bool:
        """Return whether object supports reading."""
        return getattr(self.original_stream, 'readable', lambda: False)()
    
    def writable(self) -> bool:
        """Return whether object supports writing."""
        return getattr(self.original_stream, 'writable', lambda: True)()
    
    def seekable(self) -> bool:
        """Return whether object supports seeking."""
        return getattr(self.original_stream, 'seekable', lambda: False)()
    
    def fileno(self):
        """Return file descriptor if available."""
        return getattr(self.original_stream, 'fileno', lambda: None)()
    
    def __getattr__(self, name):
        """Delegate any other attributes to the original stream."""
        return getattr(self.original_stream, name)


def setup_logging(log_level: str = 'WARNING') -> None:
    """Set up logging configuration for the application."""
    # Set up basic logging (but we'll mainly use stdout capture)
    logging.basicConfig(level=getattr(logging, log_level.upper()))
    
    # Disable Flask's default logging to reduce noise
    logging.getLogger('werkzeug').setLevel(logging.ERROR)


def setup_crewai_log_capture() -> tuple:
    """Set up CrewAI log capture for stdout and stderr."""
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    # Capture stdout and stderr for CrewAI logs
    sys.stdout = CrewAILogCapture(original_stdout)
    sys.stderr = CrewAILogCapture(original_stderr)
    
    return original_stdout, original_stderr


def get_log_queue() -> queue.Queue:
    """Get the global log queue."""
    return log_queue


def test_log_filtering():
    """Test the log filtering functionality."""
    # Create a test instance
    import io
    test_stream = io.StringIO()
    capture = CrewAILogCapture(test_stream)
    
    # Test messages that should be included
    good_messages = [
        "Agent: I will analyze the requirements",
        "Let me implement this feature",
        "Requirements: Create a user management system",
        "Design: The system will have these components",
        "I need to write unit tests for this",
        "Here is the implementation:",
        "Testing: Running unit tests",
        "Frontend: Creating the UI components",
        "Backend: Implementing the API",
        "1. First step",
        "2. Second step",
        "- Bullet point",
        "* Another bullet",
        "📝 Requirements analysis",
        "🔧 Implementation",
        "💻 Code development",
        "🎨 UI design",
        "🧪 Testing",
        "⚙️ Backend systems"
    ]
    
    # Test messages that should be excluded
    bad_messages = [
        "Assigned to: Python Engineer who can write code",
        "Status: Starting",
        "Status: Complete",
        "Crew: Engineering Team",
        "Executing Task",
        "Agent Started",
        "Agent Completed",
        "Engineering Team Lead",
        "Senior Backend Engineer",
        "Frontend Engineer",
        "Test Engineer",
        "Task Completion",
        "🤖 Agent",
        "📋 Task",
        "✅ Complete",
        "⚠️ Warning",
        "❌ Error",
        "├── Task",
        "└── Agent",
        "│   Assigned to:",
        "╭─ Crew",
        "╰─ End",
        "─────",
        "werkzeug",
        "HTTP/1.1",
        "Starting Flask",
        "Running on",
        "__main__",
        "[HEARTBEAT]",
        "Traceback",
        "",
        "   ",
        "Client connected",
        "Client disconnected"
    ]
    
    print("🧪 Testing log filtering...")
    
    # Test good messages
    included_count = 0
    for msg in good_messages:
        capture.write(msg + "\n")
        if msg in capture.recent_logs:
            included_count += 1
    
    # Test bad messages
    excluded_count = 0
    for msg in bad_messages:
        capture.write(msg + "\n")
        if msg not in capture.recent_logs:
            excluded_count += 1
    
    print(f"✅ Included {included_count}/{len(good_messages)} good messages")
    print(f"✅ Excluded {excluded_count}/{len(bad_messages)} bad messages")
    
    return included_count == len(good_messages) and excluded_count == len(bad_messages)
