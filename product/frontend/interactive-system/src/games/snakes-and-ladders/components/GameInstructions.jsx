import React from 'react';
import SetupInstructions from './SetupInstructions';
import '../styles/game-styles.css';

/**
 * Displays the permanent "how to play" game instructions for the Snakes and Ladders game.
 * 
 * @returns {JSX Element} The <GameInstructions /> component
 */
function GameInstructions() {

    return (
        <div className="game-instructions-box">
            {/* Game Title */}
            <p className="game-instructions-title">
                Snakes and Ladders Game Rules
            </p>
            {/* Snakes and Ladders Game Rules */}
            <div className="game-instructions-text">
                <p>All players start in the 
                    <b className="start-box-text"> START box </b> 
                    beside the grid.</p>
                <p>On their turn, each player presses the
                    <b className="blue-button-text"> BLUE button </b> or 
                    <b className="red-button-text"> RED button </b> 
                    to draw a card and follow the instructions.</p>
                <p>When landing on a square already OCCUPIED by a player, move to the first 
                    unoccupied square ahead.</p>
                <p>
                    A SNAKE's head does not automatically take effect, 
                    but if a minigame is activated, win it to avoid 
                    sliding down the snake's tail.
                </p>
                <p>
                    A LADDER's bottom rung does not automatically 
                    take effect, but if a minigame is activated, win it to 
                    climb to the top.
                </p>
                <p>The first player who lands on or passes square 100 wins the game.</p>
            </div>
        </div>
    )
}

export default GameInstructions;