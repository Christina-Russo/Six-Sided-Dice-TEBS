import React from 'react';
import GameGrid from '../../games/snakes-and-ladders/components/GameGrid';
import '../styles/styles.css';

/**
 * Creates an empty game board container on the right side of the display, and passes game 
 * information to the appropriate GameGrid component. 
 *  
 * @param {object} board - The current state of the game board
 * @param {string} gamePhase - The current phase of the game
 * 
 * @returns {JSX Element} The <GameBoard /> component
 */
function GameBoard({ board, gamePhase }) {

    return (
        // The game board container
        <div className="game-board">
            {/* Renders the appropriate game grid (currently for Snakes and Ladders only) */}
            <GameGrid board={board} gamePhase={gamePhase} />
        </div>
    );
}

export default GameBoard;