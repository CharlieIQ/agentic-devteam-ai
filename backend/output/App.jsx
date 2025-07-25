import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import './styles.css';

const Cell = ({ cell, onLeftClick, onRightClick }) => {
    return (
        <div
            className={`cell ${cell.is_revealed ? (cell.is_mine ? 'mine' : '') : (cell.is_flagged ? 'flagged' : '')}`}
            onClick={onLeftClick}
            onContextMenu={onRightClick}
        >
            {cell.is_revealed && !cell.is_mine ? (cell.adjacent_mines > 0 ? cell.adjacent_mines : '') : ''}
        </div>
    );
};

const Minesweeper = () => {
    const [grid, setGrid] = useState([]);
    const [gameOver, setGameOver] = useState(false);
    const [won, setWon] = useState(false);
    
    const gridSize = { rows: 9, cols: 9 };
    const mineCount = 10;

    useEffect(() => {
        startGame();
    }, []);

    const startGame = () => {
        // Call backend to initialize the game
        fetch('/api/start-game', { method: 'POST', body: JSON.stringify({ gridSize, mineCount }), headers: { 'Content-Type': 'application/json' } })
            .then(response => response.json())
            .then(data => setGrid(data.grid));
        setGameOver(false);
        setWon(false);
    };

    const handleLeftClick = (row, col) => {
        if (gameOver || grid[row][col].is_revealed) return;
        // Call backend to reveal cell
        fetch(`/api/reveal-cell?row=${row}&col=${col}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                setGrid(data.grid);
                setGameOver(data.game_over);
                setWon(data.has_won);
            });
    };

    const handleRightClick = (row, col) => {
        if (gameOver || grid[row][col].is_revealed) return;
        // Call backend to flag/unflag cell
        fetch(`/api/flag-cell?row=${row}&col=${col}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => setGrid(data.grid));
    };

    const restartGame = () => startGame();

    const showEndDialog = () => {
        const message = won ? "Congratulations! You win!" : "You hit a mine! Game Over!";
        alert(message);
        restartGame();
    };

    return (
        <div className="minesweeper">
            <h1>Minesweeper</h1>
            <div className="grid">
                {grid.map((row, rowIndex) => (
                    <div key={rowIndex} className="row">
                        {row.map((cell, colIndex) => (
                            <Cell
                                key={colIndex}
                                cell={cell}
                                onLeftClick={() => handleLeftClick(rowIndex, colIndex)}
                                onRightClick={(e) => { e.preventDefault(); handleRightClick(rowIndex, colIndex); }}
                            />
                        ))}
                    </div>
                ))}
            </div>
            <button onClick={restartGame}>Restart</button>
            {gameOver && showEndDialog()}
        </div>
    );
};

ReactDOM.render(<Minesweeper />, document.getElementById('root'));