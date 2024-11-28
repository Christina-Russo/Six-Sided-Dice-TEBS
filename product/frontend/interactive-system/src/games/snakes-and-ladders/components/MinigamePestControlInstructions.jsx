import React from 'react';

/**
 * Displays instructions for the player during the Pest Control minigame. 
 * 
 * @param {string} currentPlayer - The player playing the minigame.
 * @returns {JSX Elements} React Fragment returning the minigame instructions. 
 */
function MinigamePestControlInstructions({ currentPlayer, minigameData }) {

    // Displays player's name in their own colour
    const playerColour = `player-${currentPlayer.name.toLowerCase()}-text`;

    return (
        <>
            {/* Title */}
            <p className="minigame-instructions-title">
                Pest Control
            </p>
            {/* Minigame Instructions */}
            <div className="minigame-instructions-text">

                {/* Renders initial instructions */}
                {(minigameData.status === 'start' || minigameData.status === 'play') && (
                    <p>
                        <b className={playerColour}>{currentPlayer.name.toUpperCase()} player: </b>
                        Press the <b className="blue-button-text"> BLUE button </b> or 
                            <b className="red-button-text"> RED button </b> ONCE 
                            to catch the fly in one of the <b className={playerColour}>{ currentPlayer.name.toUpperCase() }</b> squares.   
                        <br></br>
                        You only get ONE CHANCE to catch the fly before the timer ends.  Make it count!
                    </p>
                )}

                {/* Renders instructions to start the minigame */}
                {minigameData.status === 'start' && (
                    <p>
                        <br></br>Press the <b className="blue-button-text"> BLUE button </b> or 
                        <b className="red-button-text"> RED button </b> 
                        to start the minigame.
                    </p>
                )}

                {/* Renders statement if minigame is won */}
                {minigameData.status === 'win' && (
                    <>
                        <p>
                            <br></br>Congratulations, you caught the fly!
                        </p>
                        <p>
                            Press the <b className="blue-button-text"> BLUE button </b> or 
                            <b className="red-button-text"> RED button </b> 
                            to return to the game.
                        </p>
                        <p>
                            If you were at the bottom of a ladder, <br></br>climb to the top.<br></br>
                            If you were on a snake's head, <br></br>stay where you are.
                        </p>
                    </>
                )} 

                {/* Renders statement if minigame is lost */}
                {minigameData.status === 'lose' && (
                    <>
                        <p>
                            <br></br>Sorry, you didn't catch the fly in time, or you didn't catch it in the 
                            <b className={playerColour}>{ currentPlayer.name.toUpperCase() }</b> square!
                        </p>
                        <p>
                            Press the <b className="blue-button-text"> BLUE button </b> or 
                            <b className="red-button-text"> RED button </b> 
                            to return to the game.
                        </p>
                        <p>
                            If you were at the bottom of a ladder, <br></br>stay where you are.<br></br>
                            If you were on a snake's head, <br></br>slide to its tail.
                        </p>
                    </>
                )}
            </div>
        </>
    )
}

export default MinigamePestControlInstructions;