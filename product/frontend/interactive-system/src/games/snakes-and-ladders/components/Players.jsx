import React from 'react';
import Player from './Player';
import '../styles/game-styles.css';

/**
 * Displays information relating to all players playing the current Snakes and Ladders game, 
 * including each player's colour/names (ie. BLUE) and all effects currently applying to each 
 * player eg. missing a turn, antivenom. 
 * 
 * @param {Array} players - The players currently playing the game
 * @returns {JSX Elements} The <Players /> component
 */
function Players({ players }) {

    return (
        <div>
            <div>
                <h3 className="players-heading">PLAYERS</h3>
            </div>
            <div className="players-container">
                {/* Renders a box for each player */}
                {players.map((player) => (
                    <div 
                        key={player.id}
                        className={`players-box player-${player.name.toLowerCase()}`}
                    >
                        {/* Player Name */}
                        <Player name={player.name} color={`player-${player.name.toLowerCase()}`} />
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Players;