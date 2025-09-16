import React, { useEffect, useState, useRef } from "react";
import "../styles/livelogs.css";
// Import modern icons
import { 
  Bot, 
  Wifi, 
  WifiOff, 
  ChevronDown, 
  ChevronRight, 
  Play, 
  Square, 
  Trash2,
  Activity,
  Zap
} from 'lucide-react';

/**
 * LiveLogs component displays live logs from a server-sent events (SSE) source.
 * @returns {JSX.Element} The rendered LiveLogs component.
 */
const LiveLogs = () => {
    // State to manage logs and connection status
    const [logs, setLogs] = useState([]);
    // State to manage connection status
    const [isConnected, setIsConnected] = useState(false);
    // State to manage autoscroll functionality
    const [autoscroll, setAutoscroll] = useState(false);
    // State to manage visibility of logs
    const [showLogs, setShowLogs] = useState(false);
    const logsEndRef = useRef(null);

    /**
     * Scrolls to the bottom of the logs container.
     * This function is called to ensure the latest logs are visible when autoscroll is enabled
     */
    const scrollToBottom = () => {
        logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    /**
     * Effect to handle autoscroll functionality.
     * If autoscroll is enabled and logs are being shown, it scrolls to the bottom
     * whenever new logs are added.
     */
    useEffect(() => {
        if (autoscroll && showLogs) {
            scrollToBottom();
        }
    }, [logs, autoscroll, showLogs]);

    /**
     * Effect to establish a connection to the server-sent events (SSE) source.
     * This effect sets up the event source and handles incoming log messages.
     */
    useEffect(() => {
        // Ensure the connection is established only once
        console.log("Connecting to live agent logs...");
        const eventSource = new EventSource("http://localhost:5001/api/logs");
        // Handle connection open event
        eventSource.onopen = () => {
            console.log("Connected to live agent logs");
            setIsConnected(true);
        };
        // Handle incoming messages
        eventSource.onmessage = (event) => {
            const logData = event.data;
            if (!logData.includes('[HEARTBEAT]')) {
                setLogs((prev) => [...prev, logData]);
            }
        };
        // Handle connection close event
        eventSource.onerror = (error) => {
            console.error("SSE connection error:", error);
            setIsConnected(false);
        };
        // Cleanup function to close the event source when the component unmounts
        return () => {
            console.log("Disconnecting from live agent logs");
            eventSource.close();
            setIsConnected(false);
        };
    }, []);

    /**
     * Clears the logs displayed in the component.
     * This function resets the logs state to an empty array.
     */
    const clearLogs = () => {
        setLogs([]);
    };

    /**
     * Toggles the autoscroll functionality.
     * When autoscroll is enabled, the logs will automatically scroll to the bottom
     * whenever new logs are added.
     */
    const toggleAutoscroll = () => {
        setAutoscroll((prev) => !prev);
    };

    /**
     * Toggles the visibility of the logs.
     * This function updates the showLogs state to either show or hide the logs.
     */
    const toggleShowLogs = () => {
        setShowLogs((prev) => !prev);
    };

    return (
        <div className="section live-logs-section">
            <div className="live-logs-header">
                <h2>
                    <Bot className="section-icon" />
                    Live Agent Activity
                </h2>
                <div className="logs-controls">
                    <div className="connection-status">
                        {isConnected ? (
                            <>
                                <Wifi className="status-icon connected" />
                                <span className="status-text connected">Connected</span>
                            </>
                        ) : (
                            <>
                                <WifiOff className="status-icon disconnected" />
                                <span className="status-text disconnected">Disconnected</span>
                            </>
                        )}
                    </div>
                    <button 
                        onClick={toggleShowLogs}
                        className={`logs-toggle-button ${showLogs ? 'active' : ''}`}
                    >
                        {showLogs ? <ChevronDown /> : <ChevronRight />}
                        {showLogs ? 'Hide Logs' : 'Show Logs'}
                    </button>
                    {showLogs && (
                        <>
                            <button 
                                onClick={toggleAutoscroll}
                                className={`autoscroll-btn ${autoscroll ? 'active' : ''}`}
                                title={autoscroll ? 'Autoscroll enabled' : 'Autoscroll disabled'}
                            >
                                {autoscroll ? <Play /> : <Square />}
                                {autoscroll ? 'Auto' : 'Manual'}
                            </button>
                            <button 
                                onClick={clearLogs}
                                className="clear-btn"
                                title="Clear all logs"
                            >
                                <Trash2 />
                                Clear
                            </button>
                        </>
                    )}
                </div>
            </div>
            {showLogs && (
                <div className="logs-container">
                    {logs.length === 0 ? (
                        <div className="logs-empty">
                            {isConnected ? (
                                <>
                                    <Bot className="empty-icon" />
                                    <div className="empty-text">Waiting for AI agents to start working...</div>
                                    <div className="empty-hint">
                                        Click "Generate Code" to see live agent activity
                                    </div>
                                </>
                            ) : (
                                <>
                                    <Activity className="empty-icon" />
                                    <div className="empty-text">Connecting to agent logs...</div>
                                </>
                            )}
                        </div>
                    ) : (
                        logs.map((log, idx) => (
                            <div
                                key={idx}
                                className={
                                    "log-line" +
                                    (log.includes('🤖') ? ' log-line-agent' :
                                     log.includes('✅') ? ' log-line-success' :
                                     log.includes('❌') ? ' log-line-error' :
                                     log.includes('⚠️') ? ' log-line-warning' :
                                     log.includes('📋') ? ' log-line-copy' :
                                     log.includes('Agent:') ? ' log-line-agentname' :
                                     '')
                                }
                            >
                                {log}
                            </div>
                        ))
                    )}
                    <div ref={logsEndRef} />
                </div>
            )}
        </div>
    );
};

export default LiveLogs;