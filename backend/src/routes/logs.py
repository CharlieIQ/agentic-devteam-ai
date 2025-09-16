"""
Routes for live log streaming.
"""
import queue
from flask import Blueprint, Response, stream_with_context
from ..utils.logging import get_log_queue

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/api/logs')
def stream_logs():
    """Server-Sent Events endpoint for streaming live logs."""
    def generate():
        print("🔌 Client connected to live agent logs")
        log_queue = get_log_queue()
        
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
