import React from 'react';
import '../styles/game-styles.css';

/**
 * Displays the name of a player in upper case
 * 
 * @param {string} name - The name of the player being displayed
 * @returns {JSX Element} The <Player /> component
 */
function Player({ name }) {

    return (
        <div>
            <p>{name.toUpperCase()}</p>
        </div>
    );
}

export default Player;