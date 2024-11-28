import React from 'react';
import ArrowDown from '../assets/arrow-down.png';
import ArrowUp from '../assets/arrow-up.png';
import ArrowLeft from '../assets/arrow-left.png';
import ArrowRight from '../assets/arrow-right.png';
import gooseImage from '../assets/goose.png';
import fruitImage from '../assets/fruit.png';
import rottenFruitImage from '../assets/rotten-fruit.png';
import basketImage from '../assets/basket.png';
import flyImage from '../assets/fly.png';
import '../styles/game-styles.css';

/**
 * Renders each individual square for the Snakes and Ladders game grid.  It displays numbers,
 * colours and styles based on the grid square number, player positions and game phases.
 * 
 * @param {integer} num - The number of the grid square visible on the game grid.
 * @param {string} player - The name (ie. colour) of the player on the grid square  
 * @param {Array} playerIntermediate - The grid square coordinates over which the player will be
 *      moving on their current turn
 * @param {string} gamePhase - The current game phase
 * @returns {JSX Element} The <GridSquare /> component
 */
function GridSquare({ num, player, playerIntermediate, gamePhase, joinedPlayers, imageName, isImage }) {

    // List of coloured squares on which each player colour can join the game during setup phase
    const colouredSquares = {
        Cyan: new Set([3, 30, 80, 93]),
        Yellow: new Set([4, 61, 94, 31]),
        Green: new Set([5, 60, 95, 50]),
        Black: new Set([6, 41, 96, 51]),
        Pink: new Set([7, 40, 97, 70]),
        Blue: new Set([8, 21, 98, 71]),
    }; 

    // Checks which player colours have joined the game
    const isGrayedOut = () => {
        return Object.keys(colouredSquares).some(colour => {
            return (
                colouredSquares[colour].has(num) && joinedPlayers.includes(colour)
            );
        });
    };

    // Applies coloured squares to the game grid to allow players to join the game during setup
    const getColour = () => {
        // Once player joins game, setup coloured square is grayed out
        if (isGrayedOut()) {
            return 'board-square-player player-joined-game';
        }
        // Otherwise setup coloured squares displayed
        for (const [colour, squares] of Object.entries(colouredSquares)) {
            if (squares.has(num)) {
                return `board-square-player player-${colour.toLowerCase()}`;
            }
        }
        return '';
    };

    // Applies the coloured squares to the game grid during the setup phase only
    const setupSquare = gamePhase === 'setup' ? `board-square ${getColour()}` : 'board-square';

    // Applies player position colours to grid squares in the game phases except during setup 
    const playerBorder = gamePhase !== 'setup' && player 
        ? `board-square board-square-player player-${player.toLowerCase()}` 
        : setupSquare;

    // Applies background colour for player's intermediate positions, except during setup phase
    const squareStyle = gamePhase !== 'setup' && playerIntermediate 
        ? `board-square board-square-intermediate player-${playerIntermediate}` 
        : playerBorder;

    // Shows or hides the grid squares numbers depending on game phases
    const gridNumbers = (gamePhase === 'setup' || isImage) ? 'grid-number-hidden' : 'grid-number';

    // List of curved arrow images displayed during the setup phase
    const arrows = [ArrowUp, ArrowLeft, ArrowDown, ArrowRight];

    // Applies the clockwise curved arrow images to specific grid squares
    // Clockwise arrows in setup gamegrid display adapted from Flaticon upward arrow free icon
    // https://www.flaticon.com/free-icon/upward-arrow_2268143?term=curved+arrow&page=1&position=12&origin=search&related_id=2268143 
    const getArrowImage = (num) => {
        switch(num) {
            case 45:
                return arrows[0]; 
            case 46:
                return arrows[1]; 
            case 55:
                return arrows[2];
            case 56: 
                return arrows[3];
            default:
                return null;
        }
    }

    // Applies the clockwise curved arrow images to the game grid only during the setup phase
    const arrowImage = gamePhase === 'setup' ? getArrowImage(num) : null;

    // Shows appropriate images on grid during minigames
    const showGoose = isImage && gamePhase === 'minigame-gooseChase';
    const showFruit = isImage && (imageName === 'fruit') && gamePhase === 'minigame-fallingFruits';
    const showRottenFruit = isImage && (imageName === 'fruitRotten') && gamePhase === 'minigame-fallingFruits';
    const showBasket = isImage && (imageName === 'basket') && gamePhase === 'minigame-fallingFruits';
    const showFly = isImage && (imageName === 'pest') && gamePhase === 'minigame-pestControl';

    return (
        <div className={squareStyle}> 
            {/* Displays grid numbers */}
            {(!showGoose && !showFruit && !showRottenFruit && !showBasket) && (
                <div className={gridNumbers}>{num}</div>
            )}

            {/* Centre clockwise symbol of curved arrows */}
            {arrowImage && (
                <img 
                    src={arrowImage} 
                    alt="Clockwise Symbol Quadrant" 
                    className="clockwise-icon" 
                />
            )}

            {/* Show Goose Image during Wild Goose Chase minigame.  Goose icon created by Freepik - Flaticon:  
            https://www.flaticon.com/free-icon/goose_2707763?term=goose&page=1&position=21&origin=search&related_id=2707763*/}
            {showGoose && (
                <img 
                    src={gooseImage}
                    alt="Goose"
                    className="goose-icon"
                />
            )}

            {/* Show Fruit Image during Falling Fruits minigame.  Fruit icon created by Freepik - Flaticon: 
            https://www.flaticon.com/free-icon/fruits_1625048?term=fruit&page=2&position=32&origin=style&related_id=1625048 */}
            {showFruit && (
                <img 
                    src={fruitImage}
                    alt="Fruit"
                    className="fruit-icon"
                />
            )}

            {/* Show Rotten Fruit Image during Falling Fruits minigame.  Rotten Fruit icon adapted from 
            icons by Freepik - Flaticon:
            https://www.flaticon.com/free-icon/apple_2847460?term=rotten+fruit&page=1&position=60&origin=search&related_id=2847460 
            https://www.flaticon.com/free-icon/rotten_4114810?page=2&position=2&term=rotten+fruit&origin=style-search&related_id=4114810 
            https://www.flaticon.com/free-icon/banana_2494112?page=1&position=4&term=banana&origin=style-search&related_id=2494112 */}
            {showRottenFruit && (
                <img 
                    src={rottenFruitImage}
                    alt="Rotten Fruit"
                    className="rotten-fruit-icon"
                />
            )}

            {/* Show Basket Image during Falling Fruits minigame.  Basket icon created by Freepik - Flaticon:
            https://www.flaticon.com/free-icon/basket_3649105?term=food+basket&page=1&position=31&origin=style&related_id=3649105 */}
            {showBasket && (
                <img 
                    src={basketImage}
                    alt="basket"
                    className="basket-icon"
                />
            )}

            {/* Show Fly image during Pest Control minigame. Fly icon created by Freepik - Flaticon
            https://www.flaticon.com/free-icon/fly_1198077?term=fly+insect&page=1&position=4&origin=search&related_id=1198077*/}
            {showFly && (
                <img 
                    src={flyImage}
                    alt="fly"
                    className="fly-icon"
                />
            )}
        </div>
    );
}

export default GridSquare;


