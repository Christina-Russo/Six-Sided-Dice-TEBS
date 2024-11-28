import React, { useState, useEffect } from 'react';
import { cards } from '../assets/cardsData.js';

/**
 * Displays instructions for a specific card number only for the draw card game phase.
 * 
 * @param {string} currentPlayer - The player whose turn it currently is
 * @param {integer} cardId - The card number of the card that is drawn by the player
 * @param {string} gamePhase - The drawcard gamephase
 * @returns {JSX Element} The <CardInstructions /> component
 * 
 * Code in amendedCard constant adapted from the following articles relating to the use of .split()
 * and regex to replace placeholder text with dynamic content in imported JSON strings.
// REF: https://stackoverflow.com/questions/71779450/how-to-break-line-in-jsx-from-javascript-string
// REF: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/split
// REF: https://bobbyhadz.com/blog/javascript-split-string-multiple-separators#split-a-string-with-multiple-separators-in-javascript
// REF: https://stackoverflow.com/questions/15986187/or-condition-in-regex
 */
function CardInstructions({ currentPlayer, cardId, gamePhase }) {

    // State to manage card animation
    const [animate, setAnimate] = useState(false);

    // Finds the card details based on the card id number
    const cardReveal = cards.find(card => card.id === cardId);

    // Toggles the card animation based on the game phase
    useEffect(() => {
        if (gamePhase === 'drawcard') {
            setAnimate(false);
            setTimeout(() => {
                setAnimate(true);
            }, 50);
        } else {
            setAnimate(false);
        }
    }, [gamePhase]);

    // Displays a message if the card details are not correct
    if (!cardReveal) {
        return <p>Card not found</p>;
    }

    // Formats the current player's name with the appropriate colour
    const currentPlayerName = <b className={`player-${currentPlayer.name.toLowerCase()}-text`}>
        {currentPlayer.name.toUpperCase()} player</b>;

    /**
     * Returns the appropriate button colour based on the coloured button closest to the current
     * player
     * @param {integer} direction - Rotation value that equates to the side of the board on which
     *      the player is sitting, and the button closest to the player
     * @returns {JSX Element} The button colour.
     */
    const getButtonColour = (direction) => {
        switch(direction) {
            case 180:
            case 270:
                return <b className="red-button-text">RED button</b>;
            case 90:
            case 0:
            default:
                return <b className="blue-button-text">BLUE button</b>;
        }
    };

    /**
     * Replaces placeholders in the card text with dynamic content based on the current player's
     * colour or button colour.
     * 
     * @param {string} text - The text to be displayed as the card instruction, containing 
     *      placeholder text for dynamic content
     * @returns {JSX Element} An Array of JSX elements, with placeholder text replaced with 
     *      dynamic content.
     * 
     * REF: See above for references used to replace placeholder text in strings with .split() and 
     *      regex instead of the dangerouslySetInnerHTML React component.
     */
    const amendedCard = (text) => {
        return text
            // Uses regex to split on placeholder text 'currentPlayer' and 'COLOUR button'
            .split(/(currentPlayer|COLOUR button)/)
            .map((section, index) => {
                // Replaces 'currentPlayer' text with coloured player's name
                if (section === 'currentPlayer') {
                    return <span key={index}>{currentPlayerName} </span>;
                // Replaces 'COLOUR button' text with coloured button name
                } else if (section === 'COLOUR button') {
                    return <span key={index}>{getButtonColour(currentPlayer.direction)}</span>;
                // Unmodified text
                } else {
                    return <span key={index}>{section}</span>
                }
            })
    }

    return (
        <div className={`card-instruction ${animate ? 'animate' : ''}`}>
            <p className="card-instructions-title">{cardReveal.heading}</p>
            <div className="card-instructions-text">
                {/* Renders the body of the card instruction with the dynamically replaced content */}
                {cardReveal.body.map((line, index) => (
                    <p key={index}>{amendedCard(line)}</p>
                ))}
            </div>
        </div>
    )
}

export default CardInstructions;
