import React from 'react';

/**
 * Provides instructions to all players indicating the player whose turn it currently is.
 *  
 * @param {string} currentPlayer - The player whose turn it is
 * @returns {JSX Elements} A React Fragment of JSX elements containing the current game play 
 *      instructions
 */
function GamePlayInstructions({ currentPlayer }) {

    // Displays player's name in their own colour
    const playerColour = `player-${currentPlayer.name.toLowerCase()}-text`;

    return (
        <>
            {/* Gameplay Instructions Title */}
            <p className="gameplay-instructions-title">
                Gameplay Instructions
            </p>
            {/* Dynamic gameplay text including the current player's name and button colours */}
            <div className="gameplay-instructions-text">
                <p>
                    <b className={playerColour}>{currentPlayer.name.toUpperCase()} player: </b> 
                    It's your turn! 
                </p>
                <p>
                    Press the <b className="blue-button-text"> BLUE button </b> or 
                    <b className="red-button-text"> RED button </b>.
                </p>
            </div>
        </>
    )
}

export default GamePlayInstructions;