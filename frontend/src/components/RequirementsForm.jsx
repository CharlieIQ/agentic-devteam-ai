import React from 'react';
import { saveRequirements } from '../services/api';
// Import modern icons
import { ClipboardList, Save } from 'lucide-react';

/**
 * RequirementsForm component allows users to input and save product requirements.
 * @param {Object} param0 - The props object.
 * @param {string} param0.requirements - The current requirements text.
 * @param {Function} param0.setRequirements - The function to update the requirements text.
 * @returns {JSX.Element} The rendered component.
 */
function RequirementsForm({ requirements, setRequirements }) {
    /**
     * Handles saving the requirements to the backend.
     * Alerts the user upon success or failure.
     * @returns {Promise<void>} - Saves the current requirements.
     */
    const handleSaveRequirements = async () => {
        try {
            await saveRequirements(requirements);
            alert('Requirements saved!');
        } catch (error) {
            console.error('Failed to save requirements:', error);
            alert('Failed to save requirements. Please try again.');
        }
    };

    return (
        <div className="section requirements">
            <h2>
                <ClipboardList className="section-icon" />
                Enter Your Product Requirements
            </h2>
            <textarea
                rows={8}
                value={requirements}
                onChange={e => setRequirements(e.target.value)}
                placeholder="Describe your product requirements in detail...

Example: Create a task management system with the ability to create, read, update, and delete tasks. Each task should have a title, description, due date, and status."
            />
            <button type="button" onClick={handleSaveRequirements}>
                <Save className="btn-icon" />
                Save Requirements
            </button>
        </div>
    );
}

export default RequirementsForm;
