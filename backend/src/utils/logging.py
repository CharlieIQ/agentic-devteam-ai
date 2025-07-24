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
