import React, { useState, useEffect } from 'react';
import CardInstructions from './CardInstructions';
import GamePlayInstructions from './GamePlayInstructions';
import GameOverInstructions from './GameOverInstructions';
import IncorrectSquareInstructions from './IncorrectSquareInstructions';
import MinigameFallingFruitsInstructions from './MinigameFallingFruitsInstructions';
import MinigameGooseChaseInstructions from './MinigameGooseChaseInstructions';
import MinigamePestControlInstructions from './MinigamePestControlInstructions';
import SetupInstructions from './SetupInstructions';
import '../styles/game-styles.css';


/**
 * Displays a variety of instructions based on the current game phase.  Different styles and 
 * animations are also applied depending on the game phase, player colours and position of each 
 * player around the physical game board.
 * 
 * @param {string} gamePhase - The current game phase
 * @param {string} currentPlayer - The player whose turn it is
 * @param {integer} card - The current card that is drawn by the player
 * @returns {JSX Element} The <DynamicInstructions /> component.
 */
function DynamicInstructions({ gamePhase, currentPlayer, card, minigameData }) {

    // The current on/off state of the instruction container's border animation
    const [glowBorder, setGlowBorder] = useState(false);

    // Applies different colours to the border animation depending on game phase
    const getBorderColor = (phase) => {
        switch(phase) {
            case 'setup':
                return 'dynamic-border-setup';
            case 'gameplay':
                return 'dynamic-border-gameplay';
            case 'drawcard':
                return 'dynamic-border-drawcard';
            case 'incorrect-square':
                return 'dynamic-border-incorrect-square';
            case 'minigame-gooseChase':
            case 'minigame-fallingFruits':
            case 'minigame-pestControl':
                return 'dynamic-border-minigame';
            case 'gameover':
                return 'dynamic-border-game-over';
            default: 
                return '';
        }       
    };

    // Retrieves the appropriate component to display relevant instructions based on the game phase
    const displayInstructions = () => {
        switch(gamePhase) {
            case 'setup': 
                return <SetupInstructions />;
            case 'drawcard':
                return (
                    <CardInstructions 
                        className="card-instruction" 
                        currentPlayer={currentPlayer} 
                        cardId={card} 
                        gamePhase={gamePhase} 
                    />
                );
            case 'incorrect-square':
                return (
                    <IncorrectSquareInstructions 
                        currentPlayer={currentPlayer} 
                    />
                );
            case 'minigame-gooseChase':
                return (
                    <MinigameGooseChaseInstructions 
                        currentPlayer={currentPlayer}
                        minigameData={minigameData}
                    />
                );
            case 'minigame-fallingFruits':
                return (
                    <MinigameFallingFruitsInstructions 
                        currentPlayer={currentPlayer}
                        minigameData={minigameData}
                    />
                );
            case 'minigame-pestControl':
                return (
                    <MinigamePestControlInstructions 
                        currentPlayer={currentPlayer}
                        minigameData={minigameData}
                    />
                );
            case 'gameover':
                return (
                    <GameOverInstructions 
                        currentPlayer={currentPlayer} 
                    />
                );
            default:  // normal gameplay or undefined phase
                return (
                    <GamePlayInstructions 
                        currentPlayer={currentPlayer} 
                    />
                );
        }
    };

    // Rotates the instruction text based on each player's position around the game board 
    const getRotation = (gamePhase, direction) => {
        // Rotation is not applied during the setup phase
        if (gamePhase === 'setup') {
            return 'rotate-0';
        } 
        // Rotation applied during other game phases
        switch(direction) {
            case 90:
                return 'rotate-90';
            case 180: 
                return 'rotate-180';
            case 270:
                return 'rotate-270';
            default:
                return 'rotate-0';
        }
    };

    // Turns the border animations on and off depending on game phase
    useEffect(() => {
        if (gamePhase === 'gameplay' || gamePhase === 'incorrect-square') {
            setGlowBorder(true);
        } else {
            setGlowBorder(false);
        }
    }, [gamePhase]);

    // Chooses the glow effect class based on the game phase
    const getGlowEffect = (gamePhase) => {
        switch(gamePhase) {
            case 'gameplay':
                return 'glow-border-animation-gameplay';
            case 'incorrect-square':
                return 'glow-border-animation-incorrect-square';
            default:
                return '';
        }
    }

    return (
        // Renders the appropriate instructions band animations ased on the game phase
        <div className={`
                dynamic-instructions-box 
                ${getBorderColor(gamePhase)} 
                ${getGlowEffect(gamePhase)} 
                ${getRotation(gamePhase, currentPlayer.direction)}
            `}
        >
            {displayInstructions()}
        </div>
    );
}

export default DynamicInstructions;
