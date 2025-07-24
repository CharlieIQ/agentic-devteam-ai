import React from 'react';

/**
 * RequirementsForm component allows users to input and save product requirements.
 * @param {Object} param0 - The props object.
 * @param {string} param0.requirements - The current requirements text.
 * @param {Function} param0.setRequirements - The function to update the requirements text.
 * @returns {JSX.Element} The rendered component.
 */
function RequirementsForm({ requirements, setRequirements }) {
    return (
        <div className="section requirements">
            <h2>📋 Product Requirements</h2>
            <textarea
                rows={8}
                value={requirements}
                onChange={e => setRequirements(e.target.value)}
                placeholder="Describe your product requirements in detail...

Example: Create a task management system with the ability to create, read, update, and delete tasks. Each task should have a title, description, due date, and status."
            />
            <button type="button" onClick={async () => {
                await fetch('http://localhost:5001/requirements', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ requirements })
                });
                alert('Requirements saved!');
            }}>💾 Save Requirements</button>
        </div>
    );
}

export default RequirementsForm;
