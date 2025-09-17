import React, { useState, useEffect } from 'react';
import AgentOutput from './AgentOutput';
import { getTeamConfig } from '../services/api';
// Import modern icons
import { 
  Code, 
  Package, 
  Loader2,
  Lightbulb,
  Layout,
  Server,
  Palette,
  TestTube,
  Eye
} from 'lucide-react';

/**
 * CodeOutputs component displays the generated code outputs from the AI agents.
 * Now dynamically adapts to any number of agents!
 * @param {Object} param0 - The props object.
 * @param {Object} param0.outputs - The generated code outputs.
 * @param {boolean} param0.loading - The loading state.
 * @returns {JSX.Element} The rendered component.
 */
function CodeOutputs({ outputs, loading }) {
    // State to hold the output configuration
    const [outputConfig, setOutputConfig] = useState({});
    // State for selected output to view in detail
    const [selectedOutput, setSelectedOutput] = useState(null);
    // State for view mode: 'overview' or 'detailed'
    const [viewMode, setViewMode] = useState('overview');

    /**
     * Fetches the team configuration on component mount.
     * Sets the output configuration state.
     * Falls back to a default configuration if fetching fails.
     * @returns {Promise<void>} - Fetches and sets the output configuration.
     */
    useEffect(() => {
        // Fetch output configuration from backend
        const fetchOutputConfig = async () => {
            try {
                const config = await getTeamConfig();
                setOutputConfig(config);
            } catch (err) {
                // I got rid of the fallback config
                console.warn('Could not fetch output config, using fallback:', err);
            }
        };

        fetchOutputConfig();
    }, []);

    /**
     * This function is a helper to combine all outputs into a single string,
     * excluding the 'complete_result' key.
     * It formats each output with its title and agent name.
     * @returns The combined output string.
     */
    const getCombinedOutput = () => {
        if (!outputs || Object.keys(outputs).length === 0) return '';
        // Combine all outputs into a single string
        return Object.entries(outputs)
            .filter(([key]) => key !== 'complete_result') // Skip complete_result
            // Format each output section one by one
            .map(([key, output]) => {
                const config = outputConfig[key] || { 
                    title: key, 
                    name: output.agent || 'Unknown',
                    icon: '📄'
                };
                return `# ${config.title} (by ${config.name})\n\n${output.output}\n\n---\n\n`;
            })
            .join('');
    };

    if (loading) {
        return (
            <div className="section">
                <h2>
                    <Code className="section-icon" />
                    Generated Code
                </h2>
                <div className="loading-state">
                    <Loader2 className="loading-spinner" />
                    <p>Your development team is working...</p>
                </div>
            </div>
        );
    }

    if (!outputs || Object.keys(outputs).length === 0) {
        return (
            <div className="section">
                <h2>
                    <Code className="section-icon" />
                    Generated Code
                </h2>
                <div className="empty-state">
                    <Lightbulb className="empty-icon" />
                    <p>Click "Generate Code" to start building your project!</p>
                </div>
            </div>
        );
    }

    // Filter out complete_result if it exists
    const filteredOutputs = Object.fromEntries(
        Object.entries(outputs).filter(([key]) => key !== 'complete_result')
    );

    // Helper function to truncate text for preview
    const truncateText = (text, maxLength = 150) => {
        if (!text || text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    };

    return (
        <div className="section">
            <h2>
                <Code className="section-icon" />
                Generated Code
            </h2>
            
            {viewMode === 'overview' ? (
                <div className="outputs-overview">
                    {/* Combined output card */}
                    <div className="output-card combined-output">
                        <div className="output-card-header">
                            <div className="output-card-title">
                                <Package className="output-icon" />
                                <div>
                                    <h3>Complete Project Output</h3>
                                    <p className="output-subtitle">Engineering Team</p>
                                </div>
                            </div>
                            <button 
                                className="view-detailed-btn"
                                onClick={() => {
                                    setSelectedOutput('combined');
                                    setViewMode('detailed');
                                }}
                            >
                                <Eye className="btn-icon" />
                                View Details
                            </button>
                        </div>
                        <div className="output-preview">
                            <p>{truncateText(getCombinedOutput())}</p>
                        </div>
                    </div>

                    {/* Individual output cards */}
                    <div className="outputs-grid">
                        {Object.entries(filteredOutputs).map(([key, output]) => {
                            const config = outputConfig[key] || { 
                                title: key, 
                                icon: '📄', 
                                name: output.agent || 'Unknown' 
                            };
                            return (
                                <div key={key} className="output-card">
                                    <div className="output-card-header">
                                        <div className="output-card-title">
                                            {getOutputIcon(config.title)}
                                            <div>
                                                <h3>{config.title}</h3>
                                                <p className="output-subtitle">by {config.name}</p>
                                            </div>
                                        </div>
                                        <button 
                                            className="view-detailed-btn"
                                            onClick={() => {
                                                setSelectedOutput(key);
                                                setViewMode('detailed');
                                            }}
                                        >
                                            <Eye className="btn-icon" />
                                            View
                                        </button>
                                    </div>
                                    <div className="output-preview">
                                        <p>{truncateText(output.output)}</p>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            ) : (
                /* Detailed view */
                <div className="detailed-view">
                    <div className="detailed-header">
                        <button 
                            className="back-btn"
                            onClick={() => setViewMode('overview')}
                        >
                            ← Back to Overview
                        </button>
                    </div>
                    
                    {selectedOutput === 'combined' ? (
                        <AgentOutput
                            title="Complete Project Output"
                            agent="Engineering Team"
                            output={getCombinedOutput()}
                            icon={<Package className="output-icon" />}
                            isExpanded={true}
                        />
                    ) : selectedOutput && filteredOutputs[selectedOutput] && (
                        <AgentOutput
                            title={outputConfig[selectedOutput]?.title || selectedOutput}
                            agent={outputConfig[selectedOutput]?.name || filteredOutputs[selectedOutput].agent || 'Unknown'}
                            output={filteredOutputs[selectedOutput].output}
                            icon={getOutputIcon(outputConfig[selectedOutput]?.title || selectedOutput)}
                            isExpanded={true}
                        />
                    )}
                </div>
            )}
        </div>
    );
}

// Helper function to get the appropriate icon for each output type
const getOutputIcon = (title) => {
    switch (title.toLowerCase()) {
        case 'technical design':
            return <Layout className="output-icon" />;
        case 'backend code':
            return <Server className="output-icon" />;
        case 'frontend code':
            return <Palette className="output-icon" />;
        case 'test suite':
            return <TestTube className="output-icon" />;
        default:
            return <Code className="output-icon" />;
    }
};

export default CodeOutputs;
