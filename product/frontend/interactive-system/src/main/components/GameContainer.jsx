import React, { useState, useEffect } from 'react';
import useWebSocket, { ReadyState } from "react-use-websocket"
import TeamBanner from './TeamBanner'
import GameTitle from './GameTitle';
import GameInfo from './GameInfo';
import GameBoard from './GameBoard';
import '../styles/styles.css';

/**
 * The main container for the gaming device's display.  It uses WebSockets to receive real-time 
 * updates from the server.  It divides the game display into four containers, and manages the 
 * different game phases. 
 * 
 * data: Contains dynamic game information received from the server ie. players, entities, cardID 
 *      and current player
 * 
 * gamePhase: The current phase of the game:
 *      setup: Allows players to join the game
 *      drawcard: A player draws a card to receive instructions
 *      gameplay: A player is prompted for their turn
 *      incorrect-square:  A player is notified they are on an incorrect square
 *      gameover: The players are notified of the winner at the end of the game.  
 * 
 * @returns {JSX element} The <GameContainer /> component 
 */
function GameContainer() {

    // Stores current game information
    const [data, setData] = useState({
        cardID: null,
        currentPlayer: null,
        players: [],
        entities: [],
        minigameData: []
    });

    // Stores current game phase
    const [gamePhase, setGamePhase] = useState('setup');  

    // Current player object is based on that player's name
    const currentPlayer = data.players.find(player => 
        player.name === data.currentPlayer
    ) || {};

    // WebSocket URL connects to the game server
    // react-use-websocket used to simplify usage of WebSocket API
    const WS_URL = "ws://127.0.0.1:8000/ws";   
    const { lastMessage, readyState } = useWebSocket(
        WS_URL,
        {
        share: true,
        shouldReconnect: () => true,
        },
    )

    /* Leave in here temporarily for debugging */
    /* Run when the connection state (readyState) changes - for debugging
    useEffect(() => {
        console.log("Connection state changed");
        if (readyState === ReadyState.OPEN) {
            console.log("ready");
        } 
    }, [readyState])
    */

    // Parses WebSocket messages and updates game data and game phase
    useEffect(() => {
        const getData = async () => {
            if (lastMessage && lastMessage.data) {
                try {
                    const msg = await lastMessage.data.text();
                    const parsedMsg = JSON.parse(msg);
                    // Update game data
                    setData({
                        cardID: parsedMsg.cardID || 1,
                        currentPlayer: parsedMsg.currentPlayer || null,
                        players: parsedMsg.players || [],
                        entities: parsedMsg.entities || [],
                        minigameData: parsedMsg.minigameData || []
                    });
                    // Update game phase
                    setGamePhase(parsedMsg.gamePhase || 'drawcard');

                } catch (error) {
                    console.log(`entities: ${JSON.stringify(parsedMsg.entities, null, 4)}`);
                }
            }
        };
        getData();
    }, [lastMessage]);

    // TO BE REMOVED - For debugging only
    console.log("Data: ", data);
    console.log("Game Phase: ", gamePhase);

    return (
        <div id="grid">
            {/* Renders the Team Name & Logo container */}
            <TeamBanner />
            {/* Renders the Game Title container */}
            <GameTitle />
            {/* Renders the Game Info container */}
            <GameInfo 
                players={data.players} 
                gamePhase={gamePhase} 
                currentPlayer={currentPlayer} 
                card={data.cardID}
                minigameData={data.minigameData}
            />
            {/* Renders the Gameboard container */}
            <div className="game-board">
                <GameBoard 
                    board={data} 
                    gamePhase={gamePhase}
                />
            </div>
        </div>
    );
}

export default GameContainer;