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
    """Captures stdout/stderr to forward CrewAI agent logs to SSE."""
    
    def __init__(self, original_stream):
        self.original_stream = original_stream
        self.buffer = io.StringIO()
        
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
                try:
                    log_queue.put(cleaned_line)
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

        # Much more relaxed include patterns - capture most agent activity
        include_patterns = [
            r'^Agent:\s',                # Agent: ...
            r'^Task:\s',                 # Task: ...
            r'Agent.*:',                 # Any agent speaking
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
        ]

        # Much more restricted exclude patterns - only exclude noise
        exclude_patterns = [
            r'werkzeug', r'HTTP/1.1', r'Starting Flask', r'Running on',
            r'__main__', r'\[HEARTBEAT\]', r'Traceback', r'^\s*$',
            r'Client connected', r'Client disconnected',
            r'^Status: (Starting|Stopping|Complete)$',  # Only exclude basic status
            r'─{3,}',  # Long dashes (borders)
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
