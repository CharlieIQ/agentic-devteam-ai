import React from 'react';

// Centralized agent configuration - easy to modify!
const TEAM_CONFIG = {
    design: {
        name: 'ChAIrlie',
        role: '🎯 Technical Design Lead',
        description: 'Creates detailed technical designs and system architecture. Loves diagrams and hates typos.'
    },
    backend_code: {
        name: 'Jimmy Backend',
        role: '⚙️ Backend Engineer', 
        description: 'Implements robust server-side logic, APIs, and data structures. Tempermental, hates unit testing.'
    },
    frontend_code: {
        name: 'Willy WebDev',
        role: '🎨 Frontend Engineer',
        description: 'Crafts beautiful user interfaces and seamless user experiences. Lives on coffee and centering divs.'
    },
    tests: {
        name: 'Bug Zapper',
        role: '🧪 QA Tester',
        description: 'Ensures code quality through comprehensive testing strategies. Simply loves breaking things.'
    }
    // documentation: {
    //     name: 'Doc Writer',
    //     role: '📚 Documentation Specialist',
    //     description: 'Creates clear and comprehensive project documentation'
    // }
};

/**
 * TeamOverview component displays information about the AI development team.
 * @returns {JSX.Element} The rendered component.
 */
function TeamOverview() {
    return (
        <div className="section team-overview">
            <h2>Meet the Team!</h2>
            <div className="agents-grid">
                {Object.entries(TEAM_CONFIG).map(([key, agent]) => (
                    <div key={key} className="agent-card">
                        <div className="agent-role">{agent.role}</div>
                        <div className="agent-name">{agent.name}</div>
                        <div className="agent-description">{agent.description}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default TeamOverview;
