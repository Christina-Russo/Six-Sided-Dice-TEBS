import React from 'react';

/**
 * Displays instructions for the player during the Goose Chase minigame. 
 * 
 * @param {string} currentPlayer - The player playing the minigame.
 * @returns {JSX Elements} React Fragment returning the minigame instructions. 
 */
function MinigameFallingFruitsInstructions({ currentPlayer, minigameData }) {

    // Displays player's name in their own colour
    const playerColour = `player-${currentPlayer.name.toLowerCase()}-text`;

    return (
        <>
            {/* Title */}
            <p className="minigame-instructions-title">
                Falling Fruits
            </p>
            {/* Minigame Instructions */}
            <div className="minigame-instructions-text">

                {/* Renders initial instructions */}
                {(minigameData.status === 'start' || minigameData.status === 'play') && (
                    <p>
                        <b className={playerColour}>{currentPlayer.name.toUpperCase()} player: </b>
                        Slide your piece left and right to move your basket and catch the falling fruits. 
                        <br></br>
                        Catch all the ripe fruits but avoid the rotten ones!<br></br>
                        A fruit is caught when your basket is immediately below the fruit, 
                        just before the fruit reaches the bottom row.
                    </p>
                )}

                {/* Renders instructions to start the minigame */}
                {minigameData.status === 'start' && (
                    <p>
                        <br></br> Press the <b className="blue-button-text"> BLUE button </b> or 
                        <b className="red-button-text"> RED button </b> 
                        to start the minigame.
                    </p>
                )}
                {/* Renders statement if minigame is won */}
                {minigameData.status === 'win' && (
                    <>
                        <p>
                            <br></br>Congratulations, you caught all the fruit!
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
                            <br></br>Sorry, better luck next time!
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

export default MinigameFallingFruitsInstructions;