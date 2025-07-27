import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

function App() {
  const [tasks, setTasks] = useState([]);
  const [taskDescription, setTaskDescription] = useState('');
  const [suggestedSchedule, setSuggestedSchedule] = useState([]);
  const [loadBurnoutMessage, setLoadBurnoutMessage] = useState('');

  useEffect(() => {
    async function fetchSuggestedSchedule() {
      const response = await axios.get('/suggest_schedule');
      setSuggestedSchedule(response.data);
    }
    fetchSuggestedSchedule();
  }, [tasks]);

  useEffect(() => {
    async function checkBurnout() {
      const response = await axios.get('/check_burnout');
      setLoadBurnoutMessage(response.data.message);
    }
    checkBurnout();
  }, [tasks]);
  
  const addTask = async () => {
    await axios.post('/add_task', { description: taskDescription });
    setTasks([...tasks, { name: taskDescription, status: 'in progress' }]);
    setTaskDescription('');
  };

  return (
    <div>
      <h1>Intelligent Student Planner</h1>
      <input
        type="text"
        value={taskDescription}
        onChange={(e) => setTaskDescription(e.target.value)}
        placeholder="Add a task (e.g., 'Finish comp sci paper by Friday')"
      />
      <button onClick={addTask}>Add Task</button>
      <h2>Current Tasks</h2>
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>{task.name} - {task.status}</li>
        ))}
      </ul>
      <h2>Suggested Schedule</h2>
      <ul>
        {suggestedSchedule.map((schedule, index) => (
          <li key={index}>{schedule.task} at {schedule.scheduled_time}</li>
        ))}
      </ul>
      {loadBurnoutMessage && <div>{loadBurnoutMessage}</div>}
    </div>
  );
}

const rootElement = document.getElementById('root');
ReactDOM.render(<App />, rootElement);