import React, { useState, useEffect } from 'react';

/**
 * Displays an animation effect to show a card being drawn from the card pile on entering the draw 
 * card game phase
 * 
 * @param {string} gamePhase - The draw card game phase
 * @returns {JSX Element} The <Cards /> component
 */
function Cards({ gamePhase }) {

    // Manages the animation state
    const [animate, setAnimate] = useState(false);

    // Toggles the draw card animation on and off, dependant on the current game phase
    useEffect(() => {
        if (gamePhase === 'drawcard') {
            setAnimate(true);
        } else {
            setAnimate(false);
        }
    }, [gamePhase]);

    return (
        <div className="cards-container">
            {/* Renders the card pile (underneath the top card) */}
            <div className="cards-pile">
                <div className="cards-contents">
                    <p>CARD</p>
                </div>
            </div>
            {/* Renders the top card being drawn */}
            <div className={`cards-top ${animate ? 'animate' : ''}`}>
                <div className="cards-contents">
                    <p>CARD</p>
                </div>
            </div>
        </div>   
    )
}

export default Cards;
