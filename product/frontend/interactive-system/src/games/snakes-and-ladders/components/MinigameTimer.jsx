import React from 'react';
import '../styles/game-styles.css';

/**
 *  A timer to control the length of a minigame. 
 */
export default function MinigameTimer({total, curr}) {
    return (
        <div className='timer-bar'>
            <div className='timer-progress' style={{height: `${curr / total * 100}%`}}></div>
        </div>
    );
}