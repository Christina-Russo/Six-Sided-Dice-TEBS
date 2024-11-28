import React from 'react';

/**
 * Displays instructions for the player when they end their turn whilst positioned on an incorrect 
 * grid square.
 * 
 * @param {string} currentPlayer - The player whose turn is ending 
 * @returns {JSX Elements} React Fragment returning  incorrect location instructions to the player
 */
function IncorrectSquareInstructions({ currentPlayer }) {

    // Displays player's name in their own colour
    const playerColour = `player-${currentPlayer.name.toLowerCase()}-text`;

    return (
        <>
            {/* Title */}
            <p className="incorrect-square-instructions-title">
                Incorrect Location
            </p>
            {/* Incorrect Location Instructions */}
            <div className="incorrect-square-instructions-text">
                <p><b className={playerColour}>{currentPlayer.name.toUpperCase()} player: </b>
                    You are not in the correct location.  Please move to the correct square.
                </p>
                <p>Then press the <b className="blue-button-text"> BLUE button </b> or 
                    <b className="red-button-text"> RED button </b> 
                    to end your turn.
                </p>
            </div>
        </>
    )
}

export default IncorrectSquareInstructions;