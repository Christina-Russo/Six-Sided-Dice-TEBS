import React, {useState} from 'react';
import GridSquare from './GridSquare';
import Entity from './Entity';
import MinigameTimer from './MinigameTimer';
import '../styles/game-styles.css';

/**
 * Renders the game board for Snakes and Ladders with the current game data including the 
 * positions of players, snakes and ladders, and the current game phase.
 * 
 * @param {object} board - The current state of the game board
 * @param {string} gamePhase - The current game phase
 * @returns {JSX Element} The <GameGrid /> component
 */
function GameGrid({ board, gamePhase }) {
    
    // Creates a game grid based on the current state of the board
    const entities = board.entities || [];
    const minigameData = board.minigameData || [];
    const grid = (gamePhase.startsWith('minigame') ? genMinigameGrid() : genGrid());

    // Retrieve all players who have joined a game (for grey setup squares)
    const joinedPlayers = ((players) => {
        return players.map(player => player.name);
    })(board.players);

    /**
     * Creates a game grid of numbered squares for a Snakes and Ladders game, that also includes 
     * all players' current positions and grid squares required for the current player's movement
     * @returns {Array} A 10 x 10 array of numbered grid squares with player data
     */
    function genGrid() {
        const grid = genEmptyGrid();
        const players = board.players || []; //convenience alias
        
        if (players.length > 0) {
            for (let i = 0; i < players.length; ++i) {
                // Update grid with player positions (when available) 
                const [r, c] = players[i].position || [];
                if (r != null && c != null && grid[r] && grid[r][c]) {  
                    grid[r][c].player = players[i].name.toLowerCase();
                } 
                // Update grid with grid squares needed for player movement (when available)
                if (players[i].intermediatePositions) {
                    players[i].intermediatePositions.forEach(([x,y]) => {
                        if (x != null && y != null && grid[x] && grid[x][y]) {
                            grid[x][y].playerIntermediate = players[[i]].name.toLowerCase();
                        }
                    })
                }
            }
        }
        return grid;
    }

    function genMinigameGrid() {
        const grid = genEmptyGrid();
        const squares = board.minigameData.squares || []

        for (let i = 0; i < squares.length; ++i) {
            // Update grid with square positions (if present)
            const [r, c] = squares[i].position || [];
            if (r != null && c != null && grid[r] && grid[r][c]) { 
                // border around square images (except Falling Fruits minigame) 
                if (gamePhase !== 'minigame-fallingFruits') {
                    grid[r][c].player = squares[i].colour ?? null;
                }
                // square images identified by name
                grid[r][c].imageName = squares[i].name ?? null;
                grid[r][c].isImage = true;
            }
        }
        return grid
    }

    /**
     * Creates a 10 x 10 grid with each grid square numbered according to a Snakes and Ladders
     * game board, with square 100 in the top left corner and square 1 in the bottom left corner.
     * @returns {Array} A game grid containing numbered grid squares.
     */
    function genEmptyGrid() {
        const grid = [];
        let count = 100;  
        for (let r = 0; r < 10; ++r) {
            const row = [];
            for (let c = 0; c < 10; ++c) {
                row.push({num: count, player: null});
                // Manipulate count to make the board numbers snake around and upwards
                if (c === 9) { // end of row
                    count -= 10;
                } else if (r % 2 === 0) { // even row
                    count -= 1;
                } else { // odd row
                    count += 1;
                }
            }
            grid.push(row);
        }
        return grid;
    }

    return (
        <div className="grid">
            <div className="board">
                {/* Renders grid squares on each row */}
                {grid.map((row, rowIndex) => (
                    <div key={`row-${rowIndex}`} className="board-row">
                        {row.map(square => (
                            <GridSquare 
                                key={square.num} 
                                num={square.num} 
                                player={square.player} 
                                playerIntermediate={square.playerIntermediate} 
                                gamePhase={gamePhase}
                                joinedPlayers={joinedPlayers}
                                imageName={square.imageName} 
                                isImage={square.isImage}
                            />
                        ))}
                    </div>
                ))}
            </div>
            {/* Renders entities (snakes or ladders) except in the setup or minigame game phase */}
            {gamePhase !== 'setup' && !(gamePhase.startsWith('minigame')) && entities.map((entity) => (
                <Entity 
                    key={entity.id} 
                    type={entity.type} 
                    start={entity.start} 
                    end={entity.end}
                />
            ))}
            {/* Renders timer bar during Goose Chase and Pest Control minigames */}
            {(gamePhase === 'minigame-gooseChase' || gamePhase === 'minigame-pestControl') && minigameData &&
                <MinigameTimer total={minigameData.timer.total} curr={minigameData.timer.curr}/>
            }
        </div>
    );
}

export default GameGrid;