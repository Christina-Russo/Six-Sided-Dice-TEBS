import React from 'react';
import Cards from '../../games/snakes-and-ladders/components/Cards';
import DynamicInstructions from '../../games/snakes-and-ladders/components/DynamicInstructions';
import GameInstructions from '../../games/snakes-and-ladders/components/GameInstructions';
import Players from '../../games/snakes-and-ladders/components/Players';
import Start from '../../games/snakes-and-ladders/components/Start';
import '../styles/styles.css';

/**
 * Displays information relevant to the current game on the left side of the game display
 * 
 * @param {object[]} players - All players currently playing this game
 * @param {string} gamePhase - The current phase of the game
 * @param {object} currentPlayer - The player whose turn it currently is
 * @param {integer} card - The number of the card being drawn
 * 
 * @returns {JSX Element} The <GameInfo /> component
 */
function GameInfo({ players, gamePhase, currentPlayer, card, minigameData }) {

    return (
        <div className="game-info">
            {/* Renders information for all current players */}
            <div className="players">
                <Players players={players} />
            </div>
            {/* Renders instructions to play the game, which remain constant */}
            <div className="static-info">
                <GameInstructions />
            </div>
            {/* Renders game and player instructions that change throughout the game */}
            <div className="dynamic-info">
                <DynamicInstructions 
                    gamePhase={gamePhase} 
                    currentPlayer={currentPlayer} 
                    card={card}
                    minigameData={minigameData}
                />
            </div>
            {/* Renders pile of cards waiting to be drawn */}
            <div className="cards">
                <Cards type="cards" gamePhase={gamePhase} />
            </div>
            {/* Renders the start location before players enter the game grid */}
            <div className="start">
                <Start />
            </div>
        </div>
    );
}

export default GameInfo;