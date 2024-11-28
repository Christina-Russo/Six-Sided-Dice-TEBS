import React from 'react';
import Title from '../../games/snakes-and-ladders/components/GameTitle';
import '../styles/styles.css';

/**
 * Displays the appropriate game title.  
 * Currently only one game title of Snakes and Ladders is available for display
 * 
 * @returns {JSX Element} The <GameTitle /> component
 */
function GameTitle() {

    const title = Title();

    return (
        <div className="game-title">
            <h1 className="title">{title}</h1>
        </div>
    );
}

export default GameTitle;

