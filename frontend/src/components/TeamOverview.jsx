import React, { useState, useEffect } from 'react';
import { getTeamConfig } from '../services/api';
// Import modern icons
import { 
  Layout, 
  Server, 
  Palette, 
  TestTube, 
  Loader2,
  AlertTriangle 
} from 'lucide-react';

/**
 * TeamOverview component displays information about the AI development team.
 * Now dynamically loads team configuration from the backend!
 * @returns {JSX.Element} The rendered component.
 */
function TeamOverview() {
    const [teamConfig, setTeamConfig] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Fetch team configuration from backend
        const fetchTeamConfig = async () => {
            try {
                const config = await getTeamConfig();
                setTeamConfig(config);
                setError(null);
            } catch (err) {
                console.warn('Could not fetch team config from backend, using fallback:', err);
                setTeamConfig(FALLBACK_TEAM_CONFIG);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchTeamConfig();
    }, []);

    if (loading) {
        return (
            <div className="section team-overview">
                <h2>
                    <Layout className="section-icon" />
                    Meet the Team!
                </h2>
                <div className="loading-state">
                    <Loader2 className="loading-spinner" />
                    <p>Loading team information...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="section team-overview">
                <h2>
                    <Layout className="section-icon" />
                    Meet the Team!
                </h2>
                <div className="error-state">
                    <AlertTriangle className="error-icon" />
                    <p>Could not load team information: {error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="section team-overview">
            <h2>
                <Layout className="section-icon" />
                Meet the Team!
            </h2>
            <div className="agents-grid">
                {Object.entries(teamConfig).map(([key, agent]) => (
                    <div key={key} className={`agent-card ${agent.enabled ? 'enabled' : 'disabled'}`}>
                        <div className="agent-role">
                            {getAgentIcon(agent.title)}
                            {agent.title}
                        </div>
                        <div className="agent-name">{agent.name}</div>
                        <div className="agent-description">{agent.description}</div>
                        {!agent.enabled && <div className="agent-status">Coming Soon!</div>}
                    </div>
                ))}
            </div>
        </div>
    );
}

// Helper function to get the appropriate icon for each agent type
const getAgentIcon = (title) => {
    switch (title.toLowerCase()) {
        case 'technical design':
            return <Layout className="agent-icon" />;
        case 'backend code':
            return <Server className="agent-icon" />;
        case 'frontend code':
            return <Palette className="agent-icon" />;
        case 'test suite':
            return <TestTube className="agent-icon" />;
        default:
            return <Layout className="agent-icon" />;
    }
};

// Fallback configuration in case backend is unavailable
const FALLBACK_TEAM_CONFIG = {
    design: {
        name: 'ChAIrlie',
        title: 'Technical Design',
        icon: '📐',
        description: 'Creates detailed technical designs and system architecture. Loves diagrams and hates typos.',
        enabled: true
    },
    backend_code: {
        name: 'Jimmy Backend',
        title: 'Backend Code',
        icon: '⚙️',
        description: 'Implements robust server-side logic, APIs, and data structures. Temperamental, hates unit testing.',
        enabled: true
    },
    frontend_code: {
        name: 'Willy WebDev',
        title: 'Frontend Code',
        icon: '🎨',
        description: 'Crafts beautiful user interfaces and seamless user experiences. Lives on coffee and centering divs.',
        enabled: true
    },
    tests: {
        name: 'Bug Zapper',
        title: 'Test Suite',
        icon: '🧪',
        description: 'Ensures code quality through comprehensive testing strategies. Simply loves breaking things.',
        enabled: true
    }
};

export default TeamOverview;



