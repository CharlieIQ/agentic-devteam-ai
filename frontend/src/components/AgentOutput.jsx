import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
// Import modern icons
import { ChevronDown, ChevronRight, Copy } from 'lucide-react';

/**
 * AgentOutput component displays the output from a specific AI agent.
 * @param {Object} param0 - The props object.
 * @param {string} param0.title - The title of the output.
 * @param {string} param0.agent - The name of the agent who generated the output.
 * @param {string} param0.output - The generated output code.
 * @param {React.ReactNode} param0.icon - The icon representing the output type.
 * @returns {JSX.Element} The rendered component.
 */
function AgentOutput({ title, agent, output, icon }) {
    // State to manage the expansion of the output content
    const [isExpanded, setIsExpanded] = useState(false);
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(output);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    };

    return (
        <div className="agent-output">
            <div className="output-header" onClick={() => setIsExpanded(!isExpanded)}>
                <div className="output-title">
                    {icon}
                    <span className="output-name">{title}</span>
                    <span className="output-agent">by {agent}</span>
                </div>
                <button className="expand-btn">
                    {isExpanded ? <ChevronDown /> : <ChevronRight />}
                </button>
            </div>
            {isExpanded && (
                <div className="output-content">
                    <div className="code-actions">
                        <button
                            onClick={handleCopy}
                            className="copy-btn"
                            title={copied ? "Copied!" : "Copy to clipboard"}
                        >
                            <Copy className="copy-icon" />
                            {copied ? "Copied!" : "Copy"}
                        </button>
                    </div>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {output}
                    </ReactMarkdown>
                </div>
            )}
        </div>
    );
}

export default AgentOutput;
