import { useState } from 'react';
// Import necessary components
import RequirementsForm from './components/RequirementsForm';
import TeamOverview from './components/TeamOverview';
import CodeOutputs from './components/CodeOutputs';
import LiveLogs from './components/LiveLogs';
// Import API service methods
import { generateCode as apiGenerateCode } from './services/api';
import './App.css';

/**
 * Main application component that manages the state and UI for the DevTeam Code Generator.
 * It allows users to input project requirements, generates code based on those requirements,
 * and displays the generated code outputs.
 */
function App() {
  // State to manage requirements and outputs
  const [requirements, setRequirements] = useState('');
  const [outputs, setOutputs] = useState({});
  const [loading, setLoading] = useState(false);

  /**
   * Generates code based on the provided requirements.
   * Sends a request to the backend to process the requirements and generate code.
   * Displays the generated code in the UI.
   * If requirements are empty, alerts the user to enter them first.
   * @returns {Promise<void>} - Generates code based on the provided requirements.
   */
  const generateCode = async () => {
    // Validate requirements input
    if (!requirements.trim()) {
      alert('Please enter your requirements first!');
      return;
    }
    // Reset outputs and set loading state
    setLoading(true);
    setOutputs({});
    
    try {
      const data = await apiGenerateCode(requirements);
      
      // Check if the response is successful
      if (data.status === 'success') {
        setOutputs(data.outputs || {});
      } else {
        console.error('Error:', data.message);
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      console.error('Error generating code:', error);
      alert('Error generating code. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <header className="app-header">
        <h1>Charlie's AI Development Team</h1>
        <p className="app-subtitle">Let my state of the art AI development team build your project</p>
      </header>

      <div className="main-content">
        <TeamOverview />
        <RequirementsForm requirements={requirements} setRequirements={setRequirements} />

        <div className="section generate-section">
          <button
            className="generate-btn"
            onClick={generateCode}
            disabled={loading || !requirements.trim()}
          >
            {loading ? '⏳ Generating...' : '🎯 Generate Code'}
          </button>
        </div>
        
        <CodeOutputs outputs={outputs} loading={loading} />
        <LiveLogs />
      </div>
    </div>
  );
}

export default App;
