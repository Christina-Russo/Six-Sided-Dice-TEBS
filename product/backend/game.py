from __future__ import annotations
from enum import Enum
import random
import json
from typing import List, Dict

from backend.game_components import * 
from . import minigames
from . import utils


# A dict from Position -> Number, used for snakes and ladders code sometimes.
POSITION_TO_NUM = {(0, 0): 100, (0, 1): 99, (0, 2): 98, (0, 3): 97, (0, 4): 96, (0, 5): 95, (0, 6): 94, (0, 7): 93, (0, 8): 92, (0, 9): 91, (1, 9): 90, (1, 8): 89, (1, 7): 88, (1, 6): 87, (1, 5): 86, (1, 4): 85, (1, 3): 84, (1, 2): 83, (1, 1): 82, (1, 0): 81, (2, 0): 80, (2, 1): 79, (2, 2): 78, (2, 3): 77, (2, 4): 76, (2, 5): 75, (2, 6): 74, (2, 7): 73, (2, 8): 72, (2, 9): 71, (3, 9): 70, (3, 8): 69, (3, 7): 68, (3, 6): 67, (3, 5): 66, (3, 4): 65, (3, 3): 64, (3, 2): 63, (3, 1): 62, (3, 0): 61, (4, 0): 60, (4, 1): 59, (4, 2): 58, (4, 3): 57, (4, 4): 56, (4, 5): 55, (4, 6): 54, (4, 7): 53, (4, 8): 52, (4, 9): 51, (5, 9): 50, (5, 8): 49, (5, 7): 48, (5, 6): 47, (5, 5): 46, (5, 4): 45, (5, 3): 44, (5, 2): 43, (5, 1): 42, (5, 0): 41, (6, 0): 40, (6, 1): 39, (6, 2): 38, (6, 3): 37, (6, 4): 36, (6, 5): 35, (6, 6): 34, (6, 7): 33, (6, 8): 32, (6, 9): 31, (7, 9): 30, (7, 8): 29, (7, 7): 28, (7, 6): 27, (7, 5): 26, (7, 4): 25, (7, 3): 24, (7, 2): 23, (7, 1): 22, (7, 0): 21, (8, 0): 20, (8, 1): 19, (8, 2): 18, (8, 3): 17, (8, 4): 16, (8, 5): 15, (8, 6): 14, (8, 7): 13, (8, 8): 12, (8, 9): 11, (9, 9): 10, (9, 8): 9, (9, 7): 8, (9, 6): 7, (9, 5): 6, (9, 4): 5, (9, 3): 4, (9, 2): 3, (9, 1): 2, (9, 0): 1}

# List of possible snake (head,tail) positions in (r,c) format.
SNAKES = [
    ((0,1),(4,1)),
    ((2,3),(5,4)),
    ((1,8),(3,6)),
    ((8,2),(9,1)),
    ((3,8),(6,9)),
    ((5,7),(7,6)),
    ((0,6),(2,5)),
    ((2,0),(3,3)),
    ((5,3),(8,5)),
    ((8,7),(9,6)),
    ((0,3),(4,7))
]

# List of possible ladder (bottom,top) positions in (r,c) format.
LADDERS = [
    ((9,4),(8,3)),
    ((4,5),(2,4)),
    ((7,2),(5,6)),
    ((3,7),(1,7)),
    ((9,9),(6,7)),
    ((7,1),(5,1)),
    ((8,4),(7,5)),
    ((4,2),(1,2)),
    ((2,9),(1,9)),
    ((8,6),(7,9))
]

# SnL Game States to identify which actions to take in update_game
class SnakesLaddersGameState(Enum):
    SETUP = 0
    GAMEPLAY = 1
    DRAWCARD = 2
    INCORRECT_SQUARE = 3
    MINIGAME = 4
    GAME_OVER = 5

# List of gamestates that are given through the json
GAMEPHASES = [
    'setup',
    'gameplay',
    'drawcard',
    'incorrect-square',
    'minigame',
    'gameover'
    ]

# Positions used during 'setup' gamestate to assign player colours and directions.
# Elements are given in clockwise order, starting from direction 0.
SETUP_POSITIONS = [
    [(9,2), (2,0), (0,7), (7,9)], # CYAN
    [(9,3), (3,0), (0,6), (6,9)], # YELLOW
    [(9,4), (4,0), (0,5), (5,9)], # GREEN
    [(9,5), (5,0), (0,4), (4,9)], # BLACK
    [(9,6), (6,0), (0,3), (3,9)], # PINK
    [(9,7), (7,0), (0,2), (2,9)]  # BLUE
]

# Colours corresponding to SETUP_POSITIONS coordinates
SETUP_COLOURS = [
    "Cyan",
    "Yellow",
    "Green",
    "Black",
    "Pink",
    "Blue"

]

# Player Class
class Player:
    """
    Object representing player. Stores the position, intermediate positions, and direction.
    """
    def __init__(self, colour: str, direction: int = 0, position: tuple[int,int] = None) -> None:
        self.name = colour
        self.position = position
        self.intermediate_positions = []
        self.direction = direction  # Direction is an angle 0-360

# Base Game Class
class Game:
    """
    Base Game class that parents SnakesAndLadders. 
    Stores the number of rows and columns, list of players, and current turn.
    """
    def __init__(self, n_rows: int, n_cols: int, players: List[Player] = []) -> None:
        self.n_rows: int = n_rows
        self.n_cols: int = n_cols
        self.players: list[Player] = players
        self.current_turn: int = 0
        #self.button_one_pressed: bool = False
        #self.button_two_pressed: bool = False

    def get_current_player(self) -> Player | None:
        """
        Gets the player whose turn it currently is.
        Returns the current player's Player object if len(self.players) > 0,
        returns None otherwise.
        """
        if len(self.players) > 0:
            return self.players[self.current_turn % len(self.players)]
        return None
    
    def get_player_positions(self) -> list[tuple[int,int]]:
        """
        Return a list of (r,c) positions of all players currently on the game board.
        """
        return [p.position for p in self.players if p.position is not None]
    
    def print_all_players_positions(self) -> None:
        """
        Pretty print of all player positions whether on the board or not.
        """
        for player in self.players:
            print(f"Player {player.name} is at position {player.position}")

# Entities
class Snake():
    """
    Snake class for SnakesAndLadders Game.
    Stores the head (r,c) position, tail (r,c) position, and id integer.
    """
    def __init__(self, head: tuple[int, int], tail: tuple[int, int], id: int) -> None:
        self.head = head
        self.tail = tail
        self.id = id

    def __str__(self) -> str:
        return f"Snake {self.id}: Head at {self.head}, Tail at {self.tail}"

    def __repr__(self) -> str:
        return f"Snake(id={self.id}, head={self.head}, tail={self.tail})"


class Ladder():
    """
    Ladder class for SnakesAndLadders Game.
    Stores the bottom (r,c) position, top (r,c) position, and id integer.
    """
    def __init__(self, bottom: tuple[int, int], top: tuple[int, int], id: int) -> None:
        self.bottom = bottom
        self.top = top
        self.id = id 

    def __str__(self) -> str:
        return f"Ladder {self.id}: Bottom at {self.bottom}, Top at {self.top}"

    def __repr__(self) -> str:
        return f"Ladder(id={self.id}, bottom={self.bottom}, top={self.top})"

class SnakesAndLadders(Game):
    """
    Implementation of the game Snakes and Ladders.

    Position (0,0) is the top left tile (tile 100).
    Start position will be (9, 0) (tile 1).
    At (9, 9), a move of +1 will move it to (8,9). Moves will then go backwards until (8,0), and a +1 
    results in (7,0), and then it moves forward again.
    """
    def __init__(self, 
                n_rows: int,
                n_cols: int,
                players: List[Player],
                board_reader: "BoardReader",
                get_btns_pressed: callable,
                debug: bool) -> None:
        
        super().__init__(n_rows, n_cols, players)
        # Setup card manager
        self.card_manager = CardManager()
        self.current_card_id: int = 0
        # Populate the snakes and ladders for the game
        self.snakes = self._make_snakes()
        self.ladders = self._make_ladders()
        # Start in GAMEPLAY state if players arg was not empty, otherwise start in SETUP state
        self.state = SnakesLaddersGameState.GAMEPLAY if len(players) > 0 else SnakesLaddersGameState.SETUP
        # Setup minigame manager for the game
        self.minigame_manager = minigames.MinigameManager(self.get_board_state, board_reader, get_btns_pressed, debug)
        self.minigame_trigger = None
        self.minigame = None

    def _make_snakes(self, num_snakes: int = 7) -> List[Snake]:
        """
        Selects num_snakes from the predefined SNAKES list. 
        If num_snakes > len(SNAKES) or < 0, ALL snakes will be generated from SNAKES.
        """
        if num_snakes < 0 or num_snakes > len(SNAKES):
            num_snakes = len(SNAKES)
        return [Snake(h, t, i) for i, (h,t) in enumerate(random.sample(SNAKES, k=num_snakes))]

    def _make_ladders(self, num_ladders: int = 7) -> List[Ladder]:
        """
        Selects num_ladders from the predefined LADDERS list.
        If num_ladders > len(LADDERS) or < 0, ALL ladders will be generated from LADDERS.
        """
        if num_ladders < 0 or num_ladders > len(LADDERS):
            num_ladders = len(LADDERS)
        return [Ladder(h, t, i) for i, (h,t) in enumerate(random.sample(LADDERS, k=num_ladders))]

    def _roll_dice(self) -> int:
        """
        Return a random integer in the range [1, 6]
        """
        return random.randint(1, 6)
    
    def get_leader(self) -> Player | None:
        """
        Returns the player in the position closest to the finish.
        In this instance, the player on the row closest to the top is returned.
        If multiple players are in this row, the player closest to moving to the 
        next row is returned.
        """
        if not len(self.players) > 1:
            return self.players[0]
        leader = self.players[0]
        
        for p in self.players:
            if p.position is not None:
                # compare row coords
                if (p.position[0] < leader.position[0]):
                    leader = p
                # compare col coords
                elif (p.position[0] == leader.position[0]):
                    # odd row. Higher col number is ahead
                    if (p.position[0] % 2 == 1) and (p.position[1] > leader.position[1]):
                        leader = p
                    # even row. Lower is ahead
                    if (p.position[0] % 2 == 0) and (p.position[1] < leader.position[1]):
                        leader = p
        return leader
    
    def move_player(self, player: Player, num_spaces: int, minigames_enabled=True) -> tuple[int, int]:
        """
        Moves the given player forward by num_spaces, adhering to the 'snaking' pattern of Snakes and Ladders. 
        Sets the player's position to the first free space after num_spaces moves. 
        Appends player's intermediate_positions with up to num_spaces + 1 (r,c) positions.
        Checks for any snakes or ladders and sets the minigame_trigger flag when minigames_enabled is true.
        """
        # player.position == None, so start off board
        if player.position is None:
            player.position = (9, -1)

        # Move forward by num_spaces, collecting intermediate_positions
        (r, c) = self._move_spaces(player, num_spaces, True)

        pos_occupied = any(p.position == (r, c) for p in self.players if p != player)
        entity = self._get_entity((r, c))

        # (Current (r,c) is occupied by another player) OR (player is on a snake head / ladder bottom)
        while pos_occupied or entity is not None:

            if pos_occupied:
                print(f"{(r, c)} is occupied. Moving {player.name} forward one space.")
                (r,c) = self._move_spaces(player, 1, False)

            else:
            # check for any entities and trigger minigame if enabled
                if minigames_enabled:
                    self.minigame_trigger = entity
                    player.position = (r, c)
                    utils.send_json(self.get_json()) #remove if unecessary
                    break
                elif isinstance(entity, Snake):
                    (r, c) = entity.tail
                elif isinstance(entity, Ladder):
                    (r, c) = entity.top

            pos_occupied = any(p.position == (r, c) for p in self.players if p != player)
            entity = self._get_entity((r, c))

        player.position = (r, c)
        return (r, c)
    
    def _move_spaces(self, player: Player, num_spaces: int, collect_intermediates: bool = False) -> tuple[int, int]:
        """
        Moves player by num_spaces forward and updates player.position. Follows the Snakes and Ladders winding pattern.
        If collect_intermediates is set, append up to num_spaces (r,c) positions to player.intermediate_positions.
        Returns the end (r,c) position player reaches after moving num_spaces.
        DOES NOT check if the space is occupied, use move_player if that functionality is desired.
        """
        (r,c) = player.position
        # Iterate through positions, collecting intermediates if collect_intermediates is set
        for _ in range((num_spaces)):
            # Collect intermediates if set
            if collect_intermediates:
                player.intermediate_positions.append((r, c))
            # End of row. Move ^
            if ((r % 2 == 0) and c <= 0) or ((r % 2 == 1) and c >= self.n_cols - 1):
                r -= 1
            # Odd row. Move ->
            elif r % 2 == 1:
                c += 1
            # Even row. Move <-
            else:       
                c -= 1
        player.position = (r,c)
        return (r, c)
    
    def _get_entity(self, pos: tuple[int, int]) -> Snake | Ladder | None:
        """
        Returns the Snake or Ladder at pos if one exists.
        Otherwise returns None.
        """
        entity = self._get_snake(pos)
        if not entity:
            entity = self._get_ladder(pos)
        return entity

    def _get_snake(self, pos: tuple[int, int]) -> Snake | None:
        """
        Returns the Snake at pos if one exists.
        Otherwise returns None.
        """
        for snake in self.snakes:
                if pos == snake.head:
                    return snake
        return None
    
    def _get_ladder(self, pos: tuple[int, int]) -> Ladder | None:
        """
        Returns the Ladder at pos if one exists.
        Otherwise returns None.
        """
        for ladder in self.ladders:
                if pos == ladder.bottom:
                    return ladder
        return None
    
    def is_expected(self, current_board: list[tuple[int,int]]) -> bool:
        """
        Compares current_board with stored board_positions (i.e. all player posiitons). Order insensitive.
        Returns True if every (r,c) position in current_board matches with a player position.
        Returns False otherwise.
        """
        if sorted(current_board) == sorted(self.get_player_positions()):
            return True
        return False

    def handle_setup_state(self, current_board: list[tuple[int,int]], btn_1_pressed: bool, btn_2_pressed: bool) -> None:
        """
        Handles the SETUP state of the game.
        Will modify the game's data only if either button has been pressed and the board state has changed.
        For Button 1, if a game piece has been correctly placed on the board, that player is added to the game.
            Incorrect board state changes prompt the players of the error and does not update the game.
        For Button 2, if all player pieces are in the correct positions, the state will change to GAMEPLAY 
            and the game will start.
            If no pieces register on the board, and at least one player has been added to the game, all players
            are removed, and the SETUP state resets.
        """
        stored_state = self.get_player_positions()

        # Players confirm one board piece has been added
        if btn_1_pressed:
            
            # A piece that is assigned to a player has been moved
            if len(current_board) < len(stored_state):
                print("A previous player's piece has been moved")
                return
            
            # No pieces were added to board
            elif len(current_board) == len(stored_state):
                print("No board change")
                return

            # Find new position(s) unassigned to a player
            new_positions = [pos for pos in current_board if pos not in stored_state]

            # More than one new position -> return early
            if len(new_positions) > 1:
                print("Only add one piece at a time! Do not move other pieces")
                return
            
            if len(new_positions) < 1:
                print("No new positions!")
                return
            
            # Find colour of position
            new_pos = new_positions[0]
            clr = None
            direction = None
            for i, colour in enumerate(SETUP_POSITIONS):
                if new_pos in colour:
                    clr = SETUP_COLOURS[i]
                    direction = colour.index(new_pos) * 90
                    break

            # Piece has been placed on an invalid tile
            if clr is None or direction is None:
                print("Tile has no colour!")
                return

            # Colour already in use
            if clr in [p.name for p in self.players]:
                print("Colour already in use!")
                return 

            # Player added to game!
            self.players.append(Player(clr, direction, new_pos))
            print("Added", clr, "player with direction", direction)

        # All players added, want to start game
        elif (btn_2_pressed):

            # All pieces have been removed
            if len(current_board) == 0:
                print("Resetting setup state")
                self.players = []
                self.state = SnakesLaddersGameState.SETUP

            # At least one player has been added into game.
            elif len(self.players) > 0:
                
                for p in self.players:
                    p.position = None
                self.state = SnakesLaddersGameState.GAMEPLAY    

        

    def update_game(self, current_board: list[tuple[int,int]], btn_1_pressed: bool, btn_2_pressed: bool) -> None:
        """
        Is called ONCE each time the board changes, or a button is pressed.
        Handles game logic based on given args, stored state, and variables.
        """
        # Handle game over state.
        if self.state == SnakesLaddersGameState.GAME_OVER:
            self.handle_game_over_state(btn_2_pressed)
            return

        # Game over. Change state to 'gameover', then return
        if self.is_game_over():
            self.current_turn = self.players.index(self.get_leader())
            self.state = SnakesLaddersGameState.GAME_OVER
            return

        # Setup game. Should only happen at start of game until all setup is done
        if self.state == SnakesLaddersGameState.SETUP:
            self.handle_setup_state(current_board, btn_1_pressed, btn_2_pressed)
            return

        # Tells current player it's their turn and to draw a card
        if self.state == SnakesLaddersGameState.GAMEPLAY:
            self.handle_gameplay_state(current_board, btn_1_pressed, btn_2_pressed)

        # Handle card drawing and rules. Will be run in the same call the state changes from 'gameplay' to 'drawcard'
        if self.state == SnakesLaddersGameState.DRAWCARD and not self.minigame_trigger:
            self.handle_drawcard_state(current_board, btn_1_pressed, btn_2_pressed)
        
        # Incorrect Board State. Will be run in the same call the state changes from either 'gameplay' or 'drawcard' to 'incorrect-square'
        if self.state == SnakesLaddersGameState.INCORRECT_SQUARE:
            
            for p in self.players:
                p.intermediate_positions = []
            
            if self.is_expected(current_board):
                
                # Card still needs to be resolved, return to 'drawcard' state
                if self.card_manager.current is not None:
                    self.state = SnakesLaddersGameState.DRAWCARD
                # Return to 'gameplay' state
                else:
                    self.state = SnakesLaddersGameState.GAMEPLAY
        

        # Initialise a new minigame
        if self.minigame_trigger is not None and self.minigame is None:
            exclusions = [p for p in self.get_player_positions() if p != self.get_current_player().position]

            self.minigame = self.minigame_manager.new_minigame(self.get_current_player(), exclusions)
            #self.state = SnakesLaddersGameState.MINIGAME

        # Handle minigame
        elif self.minigame is not None:
            self.state = SnakesLaddersGameState.MINIGAME
            self.handle_minigame_state(current_board, btn_1_pressed, btn_2_pressed)

    def handle_gameplay_state(self, current_board: list[tuple[int,int]], btn1: bool, btn2: bool) -> None:
        """
        Handles game logic related to the 'gameplay' state. 
        Sets self.state to INCORRECT_SQUARE if current_board does not match expected board.
        Otherwise, if btn1 or btn2 is True, sets self.state to DRAWCARD
        """
        # Wrong board state
        if not self.is_expected(current_board):
            self.state = SnakesLaddersGameState.INCORRECT_SQUARE
        
        # Either button is pressed
        elif btn1 or btn2:
            self.state = SnakesLaddersGameState.DRAWCARD

    def handle_drawcard_state(self, current_board: list[tuple[int,int]], btn1: bool, btn2: bool) -> None:
        """
        Handles game logic related to the 'drawcard' state.
        Handles a card that needs to be resolved, if one is still active. If the card is resolved, calls self.end_turn().
        Draws a new card if none are active and applies that card's effects if it should be resolved immediately. e.g. DiceRollCard
        """
        card = self.card_manager.current

        # Handle Dice roll duel card
        if isinstance(card, DiceRollDuelCard):
            self.handle_dice_roll_duel(current_board, btn1, btn2, card)

        # Handle Oversleep card
        elif isinstance(card, OversleepCard) or isinstance(card, SwapSnakesAndLaddersCard):
            self.end_turn()
            return
        
        ###
        ### Handle cards that require a board change to process ABOVE here
        ###
        
        # Draw a new card
        elif card is None:
            card = self.card_manager.draw_card()
            self.card_manager.current = card
            # Ensure the first turn for each player is a RollDiceCard
            if self.current_turn < len(self.players):
                card = RollDiceCard()
            
            self.current_card_id = card.card_id
            card.apply(self, self.get_current_player())

        ###
        ### Handle Cards that activate immediately BELOW here
        ###

        # Movement Cards
        elif isinstance(card, RollDiceCard) or isinstance(card, DescendSnakeCard) or isinstance(card, JumpAheadCard) or isinstance(card, HelpingHandCard) or isinstance(card, SwapWithLeadCard):

            if sorted(current_board) == sorted(self.get_player_positions()):
                self.end_turn()
                return
            
            # Wrong positions and either button was pressed
            if btn1 or btn2:
                self.state = SnakesLaddersGameState.INCORRECT_SQUARE



    def handle_dice_roll_duel(self, current_board: list[tuple[int,int]], btn1: bool, btn2: bool, card: DiceRollDuelCard) -> None:
        """
        Handles the functionality of the DiceRollDuelCard. DEPRECATED, DO NOT USE 
        """
        current = self.get_current_player()
        leader = self.get_leader()
        print("Current:", current.name)
        print("Leader:", leader.name)
        if current == leader:
            print(f"{current.name} is already the leader. Card has no effect.")
            self.end_turn()
            return

        # Resolve Player swapping
        if not (btn1 or btn2) and ((card.first_roll is not None) and (card.second_roll is not None)):

            # Both pieces have been picked up off the board for swapping
            if (current.position not in current_board) and (leader.position not in current_board):
                current.position, leader.position = leader.position, current.position
                self.end_turn()
                return
            
        # Current player rolls dice first
        elif (btn1 or btn2) and card.first_roll is None:
            card.first_roll = self._roll_dice()
            print(current.name, "rolled a", card.first_roll)

        # Lead player rolls dice second
        elif (btn1 or btn2) and card.second_roll is None:
            card.second_roll = self._roll_dice()
            print(leader.name, "rolled a", card.second_roll)

        # Both players have rolled dice
        if (card.first_roll is not None) and (card.second_roll is not None):
            if card.first_roll > card.second_roll:
                print(f"{current.name} wins the duel and swaps places with {leader.name}!")
            else:
                print(f"{leader.name} wins the duel. No changes in position.")
                self.end_turn()

    def handle_game_over_state(self, btn2: bool) -> None:
        """
        Handles the game over state logic.
        When btn2 is True, resets all game variables and begins new game in the setup state.
        """
        if btn2:
            # Setup card manager
            self.card_manager = CardManager()
            self.current_card_id: int = 0
            # Populate the snakes and ladders for the game
            self.snakes = self._make_snakes()
            self.ladders = self._make_ladders()
            # Reinitialise variables
            self.players = []
            self.current_turn = 0
            self.minigame_trigger = None
            self.minigame = None
            self.state = SnakesLaddersGameState.SETUP

    def handle_minigame_state(self, current_board: list[tuple[int,int]], btn_1_pressed: bool, btn_2_pressed: bool) -> None:
        """
        Handles the minigame state logic.
        Starts a minigame, then updates game state upon completion.
        """
        print("handling minigame state")
        if not self.minigame:
            # minigame should be init'd in update_game so this is an invalid branch
            print("INTERNAL ERROR: minigame should be initialised in update_game")
        elif self.minigame.status == minigames.MinigameStatus.START and (btn_1_pressed or btn_2_pressed):
            # player pressed btn to confirm start of minigame
            win = self.minigame_manager.play()
            # check for all possible outcomes
            player = self.get_current_player() # convenience alias
            if win and isinstance(self.minigame_trigger, Ladder):
                player.intermediate_positions.append(player.position)
                player.position = self.minigame_trigger.top
                self.move_player(player, 0, False)
                print("Won minigame - climb ladder")
            elif not win and isinstance(self.minigame_trigger, Ladder):
                print("Lost minigame - stay in position")
            elif win and isinstance(self.minigame_trigger, Snake):
                print("Won minigame - stay in position")
            elif not win and isinstance(self.minigame_trigger, Snake):
                player.intermediate_positions.append(player.position)
                player.position = self.minigame_trigger.tail
                self.move_player(player, 0, False)
                print("Lost minigame - slide down snake")
            self.minigame_trigger = None
            print("Enter 1 or 2 to continue: ")
        elif ((self.minigame.status == minigames.MinigameStatus.WIN or 
                self.minigame.status == minigames.MinigameStatus.LOSE) and 
                self.minigame_trigger == None and (btn_1_pressed or btn_2_pressed)):
            # player pressed btn to confirm end of minigame
            self.minigame = None
            self.state = SnakesLaddersGameState.DRAWCARD

    def end_turn(self) -> None:
        """
        Handles the end of a player's turn. 
        Assumes all cards have been resolved and all players are in the correct positions.
        """
        # Clear intermediate_positions for all players
        for p in self.players:
            p.intermediate_positions = []

        # Increment turn count
        self.current_turn += 1
        # Reset current card id for json
        self.current_card_id = 0
        # Reset manager's current card. Assumes it has been resolved
        self.card_manager.current = None
        # Set state back to 'gameplay'
        self.state = SnakesLaddersGameState.GAMEPLAY
        # Printing for terminal. Optional
        self.print_all_players_positions()
        print("Next player's turn.")

    def is_game_over(self) -> bool:
        """
        Returns true if any player has landed on or passed the last tile on the board.
        i.e. Any player's position, (r,c) == (0,0) or r < 0
        """
        for p in self.players:
            if p.position is not None and (p.position == (0,0) or p.position[0] < 0):
                return True
        return False

    def get_board_state(self) -> Dict:
        """
        Returns the game's data as a dict representing JSON format.
        """
        return {
            "gameType": "SnakesLadders",
            "gamePhase": GAMEPHASES[self.state.value],  # Include gamePhase
            "cardID": self.current_card_id,
            "currentPlayer": self.get_current_player().name if self.get_current_player() is not None else "",
            "players": [
                {
                    "id": f"p{i}",
                    "name": player.name,
                    "direction": player.direction,
                    "position": player.position,
                    "intermediatePositions": player.intermediate_positions,
                    # "effects": player.effects
                } for i, player in enumerate(self.players)
            ],
            "entities": [
                {
                    "type": "snake",
                    "id": f"s{i+1}",
                    "start": snake.head,
                    "end": snake.tail
                } for i, snake in enumerate(self.snakes)
            ] + [
                {
                    "type": "ladder",
                    "id": f"l{i+1}",
                    "start": ladder.bottom,
                    "end": ladder.top
                } for i, ladder in enumerate(self.ladders)
            ]
        }

    def get_json(self) -> str:
        """
        Returns the game's data as a str in JSON format.
        """
        board_state = self.get_board_state()
        if self.state == SnakesLaddersGameState.MINIGAME and self.minigame:
            board_state = self.minigame.get_board_data()
        return json.dumps(board_state, indent=4)

    def pretty_print_board(self) -> None:
        """
        Prints the board layout with players, snakes (S1, S2, etc.), and ladders (L1, L2, etc.),
        followed by detailed snake and ladder positions.
        """
        # Initialize the board with empty strings
        board = [[" " for _ in range(self.n_cols)] for _ in range(self.n_rows)]

        # Place snakes on the board with their IDs
        for snake in self.snakes:
            head_row, head_col = snake.head
            tail_row, tail_col = snake.tail
            # Represent snake head and tail with 'S' followed by their ID
            board[head_row][head_col] = f"S{snake.id}"
            board[tail_row][tail_col] = f"S{snake.id}"

        # Place ladders on the board with their IDs
        for ladder in self.ladders:
            bottom_row, bottom_col = ladder.bottom
            top_row, top_col = ladder.top
            # Represent ladder bottom and top with 'L' followed by their ID
            board[bottom_row][bottom_col] = f"L{ladder.id}"
            board[top_row][top_col] = f"L{ladder.id}"

        # Place players on the board
        for player in self.players:
            row, col = player.position
            current_cell = board[row][col]
            player_initial = player.name[0]  # Use the first letter of the player's name
            if current_cell == " ":
                # If the cell is empty, place the player's initial
                board[row][col] = player_initial
            else:
                # If the cell already has an entity or another player, append the player's initial
                # Ensure there's an '&' separator if needed
                if "&" not in current_cell:
                    board[row][col] += f"&{player_initial}"
                else:
                    board[row][col] += f"&{player_initial}"

        # Print the board from top to bottom with snaking pattern
        print("\nCurrent Board State:")
        for r in reversed(range(self.n_rows)):
            if r % 2 == 0:
                # Left to right for even rows
                row_cells = board[r]
            else:
                # Right to left for odd rows (snaking pattern)
                row_cells = list(reversed(board[r]))
            # Format each cell to have a fixed width for alignment
            formatted_cells = [f"{cell:^4}" for cell in row_cells]
            row_str = " | ".join(formatted_cells)
            print(f"Row {r}: {row_str}")
        print("\n")

        # Print detailed snake and ladder positions
        print("Snakes:")
        for snake in self.snakes:
            print(snake)
        print("\nLadders:")
        for ladder in self.ladders:
            print(ladder)
        print("\n")



if __name__ == "__main__":
    print("Do not run this file. Instead, run the run.sh file in /product")
