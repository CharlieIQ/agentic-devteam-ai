```markdown
# Flappy Bird Clone with Punishment

Welcome to the Flappy Bird Clone! This project is a simple adaptation of the classic Flappy Bird, but every time you die, you undergo a brief punishment period before you can restart the game. 

## Table of Contents
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Game Instructions](#game-instructions)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)

## Requirements

- Python 3.x
- Pygame library (`pygame` for the Python version)
- React and ReactDOM (for the React version)

## Setup Instructions

### Python

1. Ensure you have Python 3.x installed on your machine.
2. Install Pygame by running:
   ```bash
   pip install pygame
   ```
3. Save the following code as `flappy_bird.py`:
   ```python
   import pygame
   import random

   class Application:
       def __init__(self):
           pygame.init()
           self.screen = pygame.display.set_mode((400, 600))
           self.clock = pygame.time.Clock()
           self.bird_y = 250
           self.bird_velocity = 0
           self.gravity = 0.5
           self.game_over = False
           self.score = 0
           self.pipes = []
           self.frame_counter = 0
           self.punishment_duration = 3  # Punishment delay in seconds
           self.punishment_start_time = 0

           # Font for displaying scores
           self.font = pygame.font.Font(None, 36)
           self.add_pipe()

       def run(self):
           while True:
               self.handle_input()
               if not self.game_over:
                   self.update()
               self.render()
               self.clock.tick(60)

       def handle_input(self):
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   pygame.quit()
                   exit()
               if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_SPACE and not self.game_over:
                       self.bird_velocity = -10
                   if self.game_over and (pygame.time.get_ticks() - self.punishment_start_time) // 1000 >= self.punishment_duration:
                       self.reset_game()

       def update(self):
           self.bird_velocity += self.gravity
           self.bird_y += self.bird_velocity

           if self.bird_y >= 600:
               self.game_over = True
               self.apply_punishment()

           if self.bird_y < 0:
               self.bird_y = 0

           self.frame_counter += 1
           if self.frame_counter % 100 == 0:  # Add a new pipe every 100 frames
               self.add_pipe()

           for pipe in self.pipes:
               pipe['x'] -= 5  # Move pipes to the left
               if pipe['x'] < -50:  # Remove off-screen pipes
                   self.pipes.remove(pipe)
                   self.score += 1  # Increase score when a pipe is passed

           if self.check_collisions():
               self.game_over = True
               self.apply_punishment()

       def render(self):
           self.screen.fill((135, 206, 235))  # Sky color
           pygame.draw.rect(self.screen, (255, 215, 0), (50, self.bird_y, 30, 30))  # Bird

           for pipe in self.pipes:
               pygame.draw.rect(self.screen, (0, 255, 0), (pipe['x'], 0, 50, pipe['height']))  # Top pipe
               pygame.draw.rect(self.screen, (0, 255, 0), (pipe['x'], pipe['height'] + 150, 50, 600 - pipe['height'] - 150))  # Bottom pipe

           score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
           self.screen.blit(score_surface, (10, 10))

           if self.game_over:
               game_over_surface = self.font.render('Game Over! Press SPACE to restart', True, (255, 0, 0))
               self.screen.blit(game_over_surface, (50, 300))

           pygame.display.flip()

       def check_collisions(self):
           bird_rect = pygame.Rect(50, self.bird_y, 30, 30)
           for pipe in self.pipes:
               top_pipe_rect = pygame.Rect(pipe['x'], 0, 50, pipe['height'])
               bottom_pipe_rect = pygame.Rect(pipe['x'], pipe['height'] + 150, 50, 600 - pipe['height'] - 150)
               if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                   return True
           return False

       def apply_punishment(self):
           self.punishment_start_time = pygame.time.get_ticks()

       def reset_game(self):
           self.bird_y = 250
           self.bird_velocity = 0
           self.game_over = False
           self.score = 0
           self.pipes.clear()
           self.add_pipe()  # Restart with one pipe

       def add_pipe(self):
           height = random.randint(100, 400)
           self.pipes.append({'x': 400, 'height': height})

   if __name__ == "__main__":
       app = Application()
       app.run()
   ```

4. Run the application using:
   ```bash
   python flappy_bird.py
   ```

### React

1. Make sure you have Node.js and npm installed.
2. Create a new React app using Create React App:
   ```bash
   npx create-react-app flappy-bird-react
   cd flappy-bird-react
   ```
3. Replace the content in `src/index.js` with the following code:
   ```javascript
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
   ```

4. Start the React application:
   ```bash
   npm start
   ```

## Game Instructions

- Press the **Space** key to make the bird jump.
- Avoid the pipes. If you hit a pipe or fall to the ground, the game ends, and you must wait for 3 seconds (punishment) before you can restart by pressing the **Space** key again.

## API Documentation

### Classes (Python Version)
- **`Application`**
  - **Methods**
    - `__init__`: Initializes the game variables and sets up the game window.
    - `run`: Main loop that handles input and manages the game state.
    - `handle_input`: Listens for keyboard events to control the bird.
    - `update`: Updates the bird's position and handles the game logic.
    - `render`: Draws the current game frame.
    - `check_collisions`: Checks if the bird collides with any pipes.
    - `apply_punishment`: Initiates the punishment phase after a collision.
    - `reset_game`: Resets the game state to start anew.
    - `add_pipe`: Adds a new pipe to the game.

### Components (React Version)
- **`App`**
  - **States**
    - `birdY`: Current vertical position of the bird.
    - `birdVelocity`: Current vertical speed of the bird.
    - `gameOver`: Boolean indicating if the game is over.
    - `score`: Current player score.
    - `pipes`: Array holding the current pipes on screen.
    - `punishmentStartTime`: Timestamp for when the punishment started.
  - **Methods**
    - `handleInput`: Listens for keyboard events to perform actions.
    - `updateGame`: Updates game state and checks for conditions.
    - `checkCollisions`: Detects any collisions between the bird and pipes.
    - `collides`: Helper function to check rectangle intersection.
    - `applyPunishment`: Starts the punishment delay after a collision.
    - `resetGame`: Resets game state.
    - `addPipe`: Generates a new pipe.

## Usage Examples

### Running the Python Game

1. Navigate to the folder containing `flappy_bird.py` and run the Python script:
   ```bash
   python flappy_bird.py
   ```

### Running the React Application

1. In the terminal, navigate to the React application folder:
   ```bash
   cd flappy-bird-react
   ```
2. Start the application:
   ```bash
   npm start
   ```

Happy flapping! May you achieve high scores with minimal punishment!
```