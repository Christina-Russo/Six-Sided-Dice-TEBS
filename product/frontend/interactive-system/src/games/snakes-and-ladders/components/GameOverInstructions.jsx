import React from 'react';

/**
 * Displays instructions for the player when they win the game.
 * 
 * @param {string} currentPlayer - The player who wins the game.
 * @returns {JSX Elements} React Fragment returning the game over instructions to the player.
 */
function GameOverInstructions({ currentPlayer }) {

    // Displays player's name in their own colour
    const playerColour = `player-${currentPlayer.name.toLowerCase()}-text`;

    return (
        <>
            {/* Title */}
            <p className="game-over-instructions-title">
                GAME OVER
            </p>
            {/* Game Over Instructions */}
            <div className="game-over-instructions-text">
                <p>
                    CONGRATULATIONS, 
                    <b className={playerColour}> {currentPlayer.name.toUpperCase()} PLAYER </b> 
                    WINS!
                </p>
                <p>
                    Please press the <b className="red-button-text"> RED button </b> to play again.
                </p>
            </div>
        </>
    )
}

export default GameOverInstructions;