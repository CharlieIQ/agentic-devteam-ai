import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import './styles.css';

const App = () => {
  const [stepGoal, setStepGoal] = useState(10000);
  const [totalSteps, setTotalSteps] = useState(0);
  const [stepHistory, setStepHistory] = useState({});
  const [roastMessage, setRoastMessage] = useState('');
  const [celebrationMessage, setCelebrationMessage] = useState('');
  
  const roasts = [
    "Wow, did you even get out of bed today?",
    "You call that exercise?",
    "I've seen sloths move faster!",
    "Was that a walk or just a slow shuffle?",
    "I'm starting to think you're part of the furniture."
  ];

  const celebrations = [
    "Amazing! You've crushed your goal! 🎉",
    "You're a walking legend! Go show off!",
    "Did you just save the world by walking? Because it feels like it! 🌟",
    "Confetti for you! You're unstoppable!"
  ];

  const checkProgress = () => {
    if (totalSteps < stepGoal) {
      const randomRoast = roasts[Math.floor(Math.random() * roasts.length)];
      setRoastMessage(randomRoast);
      setCelebrationMessage('');
    } else {
      const randomCelebration = celebrations[Math.floor(Math.random() * celebrations.length)];
      setCelebrationMessage(randomCelebration);
      setRoastMessage('');
      showConfetti();
    }
  };

  const logSteps = (manualSteps) => {
    setTotalSteps(totalSteps + manualSteps);
  };

  const saveDailySteps = () => {
    const today = new Date().toISOString().split('T')[0];
    setStepHistory({ ...stepHistory, [today]: totalSteps });
    setTotalSteps(0);
  };

  const showConfetti = () => {
    const confettiContainer = document.getElementById('confetti');
    if (confettiContainer) {
      confettiContainer.style.display = 'block';
      setTimeout(() => {
        confettiContainer.style.display = 'none';
      }, 3000);
    }
  };

  return (
    <div className="app">
      <h1>Step Tracker</h1>
      <div>
        <input
          type="number"
          value={stepGoal}
          onChange={(e) => setStepGoal(parseInt(e.target.value))}
          placeholder="Set your daily step goal"
        />
        <button onClick={checkProgress}>Check Progress</button>
      </div>
      <div>
        <input
          type="number"
          placeholder="Log steps"
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              logSteps(parseInt(e.target.value));
              e.target.value = '';
            }
          }}
        />
        <button onClick={saveDailySteps}>Save Steps</button>
      </div>
      <h2>Total Steps: {totalSteps}</h2>
      {roastMessage && <h3>{roastMessage}</h3>}
      {celebrationMessage && <h3>{celebrationMessage}</h3>}
      <div id="confetti" style={{ display: 'none', position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', background: 'transparent' }}>
        {/* Put confetti animation here */}
      </div>
      <h3>Step History:</h3>
      <ul>
        {Object.entries(stepHistory).map(([date, steps]) => (
          <li key={date}>{date}: {steps}</li>
        ))}
      </ul>
    </div>
  );
};

ReactDOM.render(<App />, document.getElementById('root'));