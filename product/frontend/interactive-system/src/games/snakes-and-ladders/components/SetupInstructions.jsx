import React from 'react';

/**
 * Displays instructions for setting up the game. These instructions help players to place their 
 * game pieces on the board and join the game, so that player order and seating position is
 * recognised by the game.
 * 
 * @returns {JSX Elements} React fragment containing the instructions for the setup game phase. 
 */
function SetupInstructions() {

    return (
        <>
            {/* Title */}
            <p className="setup-instructions-title">
                Game Setup Instructions
            </p>
            {/* Setup Instructions Text */}
            <div className="setup-instructions-text">
                <p><b>Choose a player to start:</b> This player will place their piece first. </p>
                <p><b>For each player in turn (clockwise):</b></p>
                <ol>
                    <li>Place your game piece on its 
                        <b className="player-cyan-text"> C</b>
                        <b className="player-yellow-text">O</b>
                        <b className="player-green-text">L</b>
                        <b className="player-black-text">O</b>
                        <b className="player-pink-text">U</b>
                        <b className="player-blue-text">R</b>
                        <b className="player-cyan-text">E</b>
                        <b className="player-yellow-text">D </b>
                        <b className="player-green-text">S</b>
                        <b className="player-black-text">Q</b>
                        <b className="player-pink-text">U</b>
                        <b className="player-blue-text">A</b>
                        <b className="player-cyan-text">R</b>
                        <b className="player-yellow-text">E </b> 
                        closest to your side of the board.</li>
                    <li>Press the 
                        <b className="blue-button-text"> BLUE button </b> 
                        to join the game.</li>
                    <li>Repeat these steps in a clockwise direction until all players have 
                        joined the game. </li>
                </ol>
                <p></p>
                <p><b>Once all players have joined:  </b>  
                    Keep your pieces on their coloured squares.  Then press the 
                    <b className="red-button-text"> RED button </b> 
                    to start the game.
                </p>
                <p><b>To reset player colours:  </b>Remove all pieces from the board and press the <b className="red-button-text"> RED button</b>. </p>
            </div>
        </>
    )

}

export default SetupInstructions;