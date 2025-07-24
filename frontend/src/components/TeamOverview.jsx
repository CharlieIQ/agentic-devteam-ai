import React from 'react';

/**
 * This component displays an overview of the development team.
 * It lists the team members, their roles, and a brief description of their responsibilities.
 * @returns {JSX.Element} The rendered component.
 */
function TeamOverview() {
    // Define the team members and their roles
    const agents = [
        { name: 'Engineering Lead', role: 'ChAIrlie 🧠', description: 'Masterful at planning, bad at Fortnite' },
        { name: 'Backend Engineer', role: 'Jimmy Backend ⚙️', description: 'Writes the backend code with ChatGPT and takes credit for it' },
        { name: 'Frontend Engineer', role: 'Wally WebDev 🥊', description: 'Centers <div> elements like a genie. Has a drinking problem.' },
        { name: 'QA Engineer', role: 'Bug Zapper 🧪', description: 'Breaks things on purpose so you don\'t have to' }
    ];

    return (
        <div className="section team-overview">
            <h2>Meet the Team</h2>
            <div className="agents-grid">
                {agents.map((agent, i) => (
                    <div className="agent-card" key={i}>
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
