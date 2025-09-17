import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
// Import modern icons
import { ChevronDown, ChevronRight, Copy } from 'lucide-react';

/**
 * AgentOutput component displays the output from a specific AI agent.
 * @param {Object} param0 - The props object.
 * @param {string} param0.title - The title of the output.
 * @param {string} param0.agent - The name of the agent who generated the output.
 * @param {string} param0.output - The generated output code.
 * @param {React.ReactNode} param0.icon - The icon representing the output type.
 * @param {boolean} param0.isExpanded - Whether the output should be expanded by default.
 * @returns {JSX.Element} The rendered component.
 */
function AgentOutput({ title, agent, output, icon, isExpanded: defaultExpanded = false }) {
    // State to manage the expansion of the output content
    const [isExpanded, setIsExpanded] = useState(defaultExpanded);
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

    // Custom renderers for ReactMarkdown to handle code blocks
    const components = {
        code: ({ inline, className, children, ...props }) => {
            const match = /language-(\w+)/.exec(className || '');
            const language = match ? match[1] : '';
            
            return !inline && language ? (
                <SyntaxHighlighter
                    style={vscDarkPlus}
                    language={language}
                    PreTag="div"
                    {...props}
                >
                    {String(children).replace(/\n$/, '')}
                </SyntaxHighlighter>
            ) : (
                <code className={`inline-code ${className || ''}`} {...props}>
                    {children}
                </code>
            );
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
                    <ReactMarkdown 
                        remarkPlugins={[remarkGfm]}
                        components={components}
                    >
                        {output}
                    </ReactMarkdown>
                </div>
            )}
        </div>
    );
}

export default AgentOutput;
