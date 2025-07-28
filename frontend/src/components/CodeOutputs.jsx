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
  TestTube
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

    // Fetch the output configuration from the backend on component mount
    useEffect(() => {
        // Fetch output configuration from backend
        const fetchOutputConfig = async () => {
            try {
                const config = await getTeamConfig();
                setOutputConfig(config);
            } catch (err) {
                console.warn('Could not fetch output config, using fallback:', err);
                setOutputConfig(FALLBACK_OUTPUT_CONFIG);
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
        
        return Object.entries(outputs)
            .filter(([key]) => key !== 'complete_result') // Skip complete_result
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

    return (
        <div className="section">
            <h2>
                <Code className="section-icon" />
                Generated Code
            </h2>
            <div className="outputs-container">
                {/* Combined output at the top */}
                <AgentOutput
                    key="combined"
                    title="Complete Project Output"
                    agent="Engineering Team"
                    output={getCombinedOutput()}
                    icon={<Package className="output-icon" />}
                />
                
                {/* Individual outputs - now dynamically configured */}
                {Object.entries(filteredOutputs).map(([key, output]) => {
                    const config = outputConfig[key] || { 
                        title: key, 
                        icon: '📄', 
                        name: output.agent || 'Unknown' 
                    };
                    return (
                        <AgentOutput
                            key={key}
                            title={config.title}
                            agent={config.name}
                            output={output.output}
                            icon={getOutputIcon(config.title)}
                        />
                    );
                })}
            </div>
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

// Fallback configuration
const FALLBACK_OUTPUT_CONFIG = {
    design: { title: 'Technical Design', icon: '📐', name: 'ChAIrlie' },
    backend_code: { title: 'Backend Code', icon: '⚙️', name: 'Jimmy Backend' },
    frontend_code: { title: 'Frontend Code', icon: '🎨', name: 'Willy WebDev' },
    tests: { title: 'Test Suite', icon: '🧪', name: 'Bug Zapper' }
};

export default CodeOutputs;
