import React from 'react';

/**
 * Displays the START box on the game board.  This is the location where players put their 
 * game piece before their first turn and entry to the game grid.
 * @returns {JSX Element} The <Start /> component
 */
function Start() {
    
    return (
        <div className="start-container">
            <div className="start-contents">
                <p>START</p>
            </div>
            
        </div>
        
    )
}

export default Start;