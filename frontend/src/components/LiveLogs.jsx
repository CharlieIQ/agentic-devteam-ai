import React, { useEffect, useState, useRef } from "react";
import "../styles/livelogs.css";

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
        const eventSource = new EventSource("http://localhost:5001/logs");
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
        <div className="section">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1em' }}>
                <h2>🤖 Live Agent Activity</h2>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1em' }}>
                    <span style={{ 
                        color: isConnected ? '#28a745' : '#dc3545',
                        fontSize: '0.9em',
                        fontWeight: '600'
                    }}>
                        {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
                    </span>
                    <button 
                        onClick={toggleShowLogs}
                        style={{
                            padding: '0.5em 1em',
                            fontSize: '0.9em',
                            background: showLogs ? '#0d6efd' : '#6c757d',
                            border: 'none',
                            borderRadius: '6px',
                            color: 'white',
                            cursor: 'pointer'
                        }}
                    >
                        {showLogs ? '▼ Hide Logs' : '▶ Show Logs'}
                    </button>
                    <button 
                        onClick={toggleAutoscroll}
                        style={{
                            padding: '0.5em 1em',
                            fontSize: '0.9em',
                            background: autoscroll ? '#198754' : '#6c757d',
                            border: 'none',
                            borderRadius: '6px',
                            color: 'white',
                            cursor: 'pointer'
                        }}
                    >
                        {autoscroll ? '🟢 Autoscroll On' : '⚪ Autoscroll Off'}
                    </button>
                    <button 
                        onClick={clearLogs}
                        style={{
                            padding: '0.5em 1em',
                            fontSize: '0.9em',
                            background: '#6c757d',
                            border: 'none',
                            borderRadius: '6px',
                            color: 'white',
                            cursor: 'pointer'
                        }}
                    >
                        🗑️ Clear
                    </button>
                </div>
            </div>
            {showLogs && (
                <div className="livelogs-container">
                    {logs.length === 0 ? (
                        <div className="livelogs-empty">
                            {isConnected ? (
                                <>
                                    <div className="livelogs-empty-icon">🤖</div>
                                    <div>Waiting for AI agents to start working...</div>
                                    <div className="livelogs-empty-hint">
                                        Click "Generate Code" to see live agent activity
                                    </div>
                                </>
                            ) : (
                                <>
                                    <div className="livelogs-empty-icon">🔌</div>
                                    <div>Connecting to agent logs...</div>
                                </>
                            )}
                        </div>
                    ) : (
                        logs.map((log, idx) => (
                            <div
                                key={idx}
                                className={
                                    "livelogs-line" +
                                    (log.includes('🤖') ? ' livelogs-line-agent' :
                                     log.includes('✅') ? ' livelogs-line-success' :
                                     log.includes('❌') ? ' livelogs-line-error' :
                                     log.includes('⚠️') ? ' livelogs-line-warning' :
                                     log.includes('📋') ? ' livelogs-line-copy' :
                                     log.includes('Agent:') ? ' livelogs-line-agentname' :
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