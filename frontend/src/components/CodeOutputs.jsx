import React from 'react';
import AgentOutput from './AgentOutput';

/**
 * CodeOutputs component displays the generated code outputs from the AI agents.
 * @param {Object} param0 - The props object.
 * @param {Object} param0.outputs - The generated code outputs.
 * @param {boolean} param0.loading - The loading state.
 * @returns {JSX.Element} The rendered component.
 */
function CodeOutputs({ outputs, loading }) {
    // Configuration for different output types
    const outputConfig = {
        design: { title: 'Technical Design', icon: '📐', agent: 'ChAIrlie' },
        backend_code: { title: 'Backend Code', icon: '⚙️', agent: 'Jimmy Backend' },
        frontend_code: { title: 'Frontend Code', icon: '🎨', agent: 'Wally WebDev' },
        tests: { title: 'Test Suite', icon: '🧪', agent: 'Bug Zapper' },
        complete_result: { title: 'Complete Output', icon: '💻', agent: 'Engineering Team' }
    };

    if (loading) {
        return (
            <div className="section">
                <h2>💻 Generated Code</h2>
                <div className="loading-state">
                    <div className="loading-spinner">🔄</div>
                    <p>Your development team is working...</p>
                </div>
            </div>
        );
    }

    if (!outputs || Object.keys(outputs).length === 0) {
        return (
            <div className="section">
                <h2>💻 Generated Code</h2>
                <div className="empty-state">
                    <p>💡 Click "Generate Code" to start building your project!</p>
                </div>
            </div>
        );
    }

    return (
        <div className="section">
            <h2>💻 Generated Code</h2>
            <div className="outputs-container">
                {Object.entries(outputs).map(([key, output]) => {
                    const config = outputConfig[key] || { title: key, icon: '📄', agent: output.agent || 'Unknown' };
                    return (
                        <AgentOutput
                            key={key}
                            title={config.title}
                            agent={config.agent}
                            output={output.output}
                            icon={config.icon}
                        />
                    );
                })}
            </div>
        </div>
    );
}

export default CodeOutputs;
