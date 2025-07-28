import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function App() {
  const [birdY, setBirdY] = useState(250);
  const [birdVelocity, setBirdVelocity] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);
  const [pipes, setPipes] = useState([]);
  const [punishmentStartTime, setPunishmentStartTime] = useState(0);
  const punishmentDuration = 3000; // 3 seconds punishment
  const gravity = 0.5;

  useEffect(() => {
    const handleInput = (e) => {
      if (e.key === ' ') {
        if (!gameOver) {
          setBirdVelocity(-10);
        } else if (Date.now() - punishmentStartTime >= punishmentDuration) {
          resetGame();
        }
      }
    };

    window.addEventListener('keydown', handleInput);
    return () => window.removeEventListener('keydown', handleInput);
  }, [gameOver, punishmentStartTime]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (!gameOver) {
        updateGame();
      }
    }, 16); // approximately 60 frames per second

    return () => clearInterval(interval);
  }, [gameOver]);

  const updateGame = () => {
    setBirdVelocity((prev) => prev + gravity);
    setBirdY((prev) => {
      const newY = prev + birdVelocity;
      if (newY >= 600) {
        setGameOver(true);
        applyPunishment();
        return 600;
      }
      return newY < 0 ? 0 : newY;
    });

    setPipes((prev) => {
      const newPipes = prev.map(pipe => ({ ...pipe, x: pipe.x - 5 }));
      // Remove off-screen pipes and update score
      const filteredPipes = newPipes.filter(pipe => {
        if (pipe.x < -50) {
          setScore((prev) => prev + 1);
          return false;
        }
        return true;
      });
      return filteredPipes;
    });

    checkCollisions();
  };

  const checkCollisions = () => {
    const birdRect = { x: 50, y: birdY, width: 30, height: 30 };
    for (const pipe of pipes) {
      const topPipeRect = { x: pipe.x, y: 0, width: 50, height: pipe.height };
      const bottomPipeRect = { x: pipe.x, y: pipe.height + 150, width: 50, height: 600 - pipe.height - 150 };
      if (collides(birdRect, topPipeRect) || collides(birdRect, bottomPipeRect)) {
        setGameOver(true);
        applyPunishment();
        break;
      }
    }
  };

  const collides = (rectA, rectB) => {
    return rectA.x < rectB.x + rectB.width &&
           rectA.x + rectA.width > rectB.x &&
           rectA.y < rectB.y + rectB.height &&
           rectA.height + rectA.y > rectB.y;
  };

  const applyPunishment = () => {
    setPunishmentStartTime(Date.now());
  };

  const resetGame = () => {
    setBirdY(250);
    setBirdVelocity(0);
    setGameOver(false);
    setScore(0);
    setPipes([{ x: 400, height: Math.floor(Math.random() * 300) + 100 }]);
    addPipe();
  };

  const addPipe = () => {
    setPipes((prev) => [...prev, { x: 400, height: Math.floor(Math.random() * 300) + 100 }]);
  };

  useEffect(() => {
    const pipeInterval = setInterval(() => {
      if (!gameOver) {
        addPipe();
      }
    }, 100);
  
    return () => clearInterval(pipeInterval);
  }, [gameOver]);

  return (
    <div style={{ position: 'relative', width: '400px', height: '600px', overflow: 'hidden' }}>
      <div style={{ position: 'absolute', left: '50px', top: `${birdY}px`, width: '30px', height: '30px', backgroundColor: 'gold' }} />
      {pipes.map((pipe, index) => (
        <div key={index}>
          <div style={{ position: 'absolute', left: `${pipe.x}px`, top: '0', width: '50px', height: `${pipe.height}px`, backgroundColor: 'green' }} />
          <div style={{ position: 'absolute', left: `${pipe.x}px`, top: `${pipe.height + 150}px`, width: '50px', height: `${600 - pipe.height - 150}px`, backgroundColor: 'green' }} />
        </div>
      ))}
      <div style={{ position: 'absolute', left: '10px', top: '10px', color: 'white' }}>Score: {score}</div>
      {gameOver && <div style={{ position: 'absolute', left: '50px', top: '300px', color: 'red' }}>Game Over! Press SPACE to restart</div>}
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));