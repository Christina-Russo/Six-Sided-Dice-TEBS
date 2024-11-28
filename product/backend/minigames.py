from __future__ import annotations
from typing import List, Callable
from abc import ABC, abstractmethod
from enum import Enum

from random import randrange, choice
from time import sleep
import json
from . import utils

from pynput import keyboard

# Represents status of a minigame
class MinigameStatus(Enum):
    START = 0
    PLAY = 1
    WIN = 2
    LOSE = 3

# for json to send to frontend
minigameStatus = [
    "start",
    "play",
    "win",
    "lose"
]

def gen_rand_pos() -> tuple[int, int]:
    """
    Generates a random position on a 10x10 board
    """
    return (randrange(0, 10), randrange(0, 10))

class Minigame(ABC):
    """
    Controls the logic and gameplay of a minigame
    """
    TICK = 0.1
    DURATION = 100 # ticks

    def __init__(self, 
                 player: "Player", 
                 posPtr: PosPtr, 
                 exclusions: List[(int, int)], 
                 get_board_state: Callable,
                 board_reader: "BoardReader",
                 get_btns_pressed: callable,
                 debug: bool) -> None:
        super().__init__()
        self._player = player
        self._posPtr = posPtr
        self._exclusions = exclusions
        self._get_board_state = get_board_state
        self.debug = debug

        self._board_reader = board_reader
        self._current_state: list[tuple[int,int]] = self._board_reader.get_positions()
        self.changes: list[tuple[int,int]] = [(-1,-1)]
        self._get_btns_pressed: callable = get_btns_pressed
        self.button_one_pressed: bool = False
        self.button_two_pressed: bool = False
        self._state_lock: bool = False

        self._timer = self.DURATION
        self.status = MinigameStatus.START
        self.phase = "minigame"

    @abstractmethod
    def play(self) -> bool:
        """Executes the gameplay loop"""
        return False
    
    @abstractmethod
    def get_board_data(self) -> dict:
        """Formats relevant data to send to frontend"""
        data = self._get_board_state()
        data['gamePhase'] = self.phase
        data['minigameData'] = {
            'status': minigameStatus[self.status.value],
            'timer': {
                'total': self.DURATION,
                'curr': self._timer
            },
            'squares': []
        }
        return data

    def get_json(self) -> str:
        """Transforms minigame data into JSON."""
        return json.dumps(self.get_board_data(), indent=4)
    
    def is_timeup(self) -> bool:
        """Returns true if the internal minigame timer reached 0 else false."""
        return self._timer <= 0
    
    def gen_rand_pos(self) -> tuple[int, int]:
        """Generates a random position on a 10x10 board, excluding exclusions"""
        pos = gen_rand_pos()
        while pos in self._exclusions:
            pos = gen_rand_pos()
        return pos
    
    def on_pos(self, pos: tuple[int, int]) -> bool:
        """Returns true if the physical position of the player piece matches pos else false."""
        if self.debug:
            return pos == self._posPtr.get_phys_pos()
        
        changes = self.get_board_changes()
        if len(changes) > 0:
            return pos == changes[0]
        
        return False
    
    def decrementTimer(self) -> None:
        """Decrements the internal timer"""
        self._timer -= 1

    def get_buttons_pressed(self) -> tuple[bool, bool]:
        """
        Returns a tuple containing the state of the hardware buttons.
        """
        return self._get_btns_pressed()

    def on_board_change(self):
        """Updates changes & current_state if the board detects a change in piece position."""
        board_state = self._board_reader.get_positions()
        if len(board_state) > 0:
            self.changes = [pos for pos in board_state if pos not in self._current_state]
            self._current_state = board_state
        else:
            self._current_state = [(-1,-1)]

    def update_state(self, func: callable):
        """Claims a state lock then calls the given func."""
        while self._state_lock:
            pass
        self._state_lock = True
        func()
        self._state_lock = False

    def reset_on_changes(self):
        """
        Set board_changed, button_one_pressed, and button_two_pressed = False.
        Uses locks to avoid race conditions. 
        Waits for previous lock to be released before modifying variable
        """
        # Wait for values to unlock
        while self._state_lock:
            pass
        # Lock values
        self._state_lock = True
        # Change values
        self.board_changed = False
        self.button_one_pressed = False
        self.button_two_pressed = False
        # Unlock values
        self._state_lock = False
    
class GooseChase(Minigame):
    """Minigame where the player slides a piece to catch geesee."""
    TICK = 0.3
    DURATION = 50
    class Goose():
        """Handles movement and boundary checking for a goose."""
        DIRECTIONS = [
            (1, 0), #down
            (-1, 0), #up
            (0, 1), #right
            (0, -1), #left
            (1, 1), #down-right
            (1, -1), #down-left
            (-1, 1), #up-right
            (-1, -1) #up-left
        ]

        CHANGE_GAP = 5

        def __init__(self) -> None:
            self.pos = gen_rand_pos()
            self.direction = choice(self.DIRECTIONS)
            self.timer = self.CHANGE_GAP
            self.caught = False

        def move(self):
            """Moves the goose."""
            # change opposite dir if wall hit
            if self.hit_wall():
                self.direction = self.get_opposite_direction(self.pos)
            elif self.timer <= 0:
                self.direction = choice(self.DIRECTIONS)
                self.timer = self.CHANGE_GAP
            
            # move in direction
            self.pos = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])

            # teleport if offscreen
            while not self.is_onscreen():
                self.pos = gen_rand_pos()
                self.direction = choice(self.DIRECTIONS)
            
            self.timer -= 1

        def hit_wall(self) -> bool:
            """Returns true if the goose is on a board boundary else false."""
            return (self.pos[0] == 0 or 
                    self.pos[0] == 9 or 
                    self.pos[1] == 0 or 
                    self.pos[1] == 9)

        def is_onscreen(self) -> bool:
            """Returns true if the goose is on a valid position within the board else false"""
            return (0 <= self.pos[0] < 10) and (0 <= self.pos[1] < 10)

        def get_opposite_vertical(self, row: int) -> int:
            """Returns the row direction delta opposite to row.

            Random direction chosen if row is not at a board boundary.
            """
            if row == 0:
                return 1
            elif row == 9:
                return -1
            else:
                return choice([-1, 0, 1])

        def get_opposite_horizontal(self, col: int) -> int:
            """Returns the col direction delta opposite to the col.

            Random direction chosen if col is not at a board boundary.
            """
            if col == 0:
                return 1
            elif col == 9:
                return -1
            else:
                return choice([-1, 0, 1])
            
        def get_opposite_direction(self, pos: tuple[int, int]) -> tuple[int, int]:
            """Returns the direction vector opposite to pos."""
            return (self.get_opposite_vertical(pos[0]), self.get_opposite_horizontal(pos[1]))

    def __init__(self, player: "Player", posPtr: PosPtr, exclusions: List[int], get_board_state: Callable, board_reader: "BoardReader", get_btns_pressed: callable, debug: bool) -> None:
        super().__init__(player, posPtr, exclusions, get_board_state, board_reader, get_btns_pressed, debug)
        self._posPtr.debug_mode(None, "hit")
        self._geese = [self.Goose() for _ in range(5)]
        self.phase = self.phase + "-gooseChase"

    def on_board_change(self):
        super().on_board_change()

        # remove caught geese
        while self._state_lock:
            continue
        self._state_lock = True
        self._geese = [g for g in self._geese if g.pos not in self.changes]
        self._state_lock = False

    def update_geese(self):
        """Moves geese."""
        for g in self._geese:
            g.move()

    def play(self) -> bool:

        # Store board func
        old_board_func = self._board_reader._on_change_func
        self._board_reader.set_on_change(self.on_board_change)

        # Reset the on_board_change flag
        self.reset_on_changes()

        self.status = MinigameStatus.PLAY

        while not self.is_timeup():

            self.update_state(self.update_geese)
            
            utils.send_json(self.get_json())

            sleep(self.TICK)
            
            if self.debug:
                # check for caught geese
                for goose in self._geese:
                    if self.on_pos(goose.pos) or self.on_pos((-1, -1)): # goose caught
                        goose.caught = True
                
                # remove caught geese
                self._geese = [g for g in self._geese if not g.caught]

            # check if all geese caught
            if not self._geese:
                break

            self.decrementTimer()

        # lose if time is up
        self.status = MinigameStatus.WIN if not self._geese else MinigameStatus.LOSE
        # Set board func to previously stored func
        self._board_reader.set_on_change(old_board_func)
        return self.status == MinigameStatus.WIN
    
    def get_board_data(self) -> dict:
        data = super().get_board_data()
        data["minigameData"]["squares"] = [
            ({
                "colour": "black",
                "name": "goose",
                "position": goose.pos
            }) for goose in self._geese
        ]
        return data

class FallingFruits(Minigame):
    """Minigame where the player slides their piece to move a basket and catch fruit."""
    class Fruit():
        """Handles movement, boundary, and catch checking for a fruit."""
        def __init__(self, pos) -> None:
            self.pos = pos
            self.rotten = False
            self.caught = False

            if randrange(0, 100) < 25:
                self.rotten = True
        
        def fall(self):
            """Move a fruit downwards."""
            (r, c) = self.pos
            self.pos = (r + 1, c)

        def on_bottom_row(self) -> bool:
            """Returns true if fruit is on the bottom row (9) else false."""
            (r, c) = self.pos
            return r == 9
        
        def near_bottom_row(self) -> bool:
            """Returns true if fruit is on the second-bottom row (8) else false."""
            (r, c) = self.pos
            return r == 8

        def is_offscreen(self) -> bool:
            """Returns true if fruit is offscreen else false"""
            (r, c) = self.pos
            return r > 9

    DURATION = 100

    def __init__(self, player: "Player", posPtr: PosPtr, exclusions: List[int], get_board_state: Callable, board_reader: "BoardReader", get_buttons_pressed: callable, debug: bool) -> None:
        super().__init__(player, posPtr, exclusions, get_board_state, board_reader, get_buttons_pressed, debug)
        self._posPtr.debug_mode((9, 0), 'left-right')
        self.fruits = []
        self.phase = self.phase + "-fallingFruits"

    def play(self) -> bool:
        self.status = MinigameStatus.PLAY
        SPAWN_GAP = 10
        spawn_timer = SPAWN_GAP  #ticks
        FALL_GAP = 3
        fall_timer = FALL_GAP

        # Store board func
        old_board_func = self._board_reader._on_change_func
        self._board_reader.set_on_change(self.on_board_change)

        self.fruits.append(self.Fruit((0, randrange(0, 10))))
        while self.fruits:
            if fall_timer <= 0:
                for fruit in self.fruits:
                    fruit.fall()
                fall_timer = FALL_GAP
            
            # get rid of any off-screen and caught fruits
            self.fruits = [f for f in self.fruits if not (f.caught or f.is_offscreen())]
            
            # gen new fruit when spawn_timer is over
            if spawn_timer <= 0 and not self.is_timeup():
                self.fruits.append(self.Fruit((0, randrange(0, 10))))
                spawn_timer = SPAWN_GAP
            
            utils.send_json(self.get_json())
            sleep(self.TICK)

            # check for caught fruits and losing conitions
            for fruit in self.fruits:
                if (fruit.on_bottom_row() or fruit.near_bottom_row()) and not fruit.rotten and self._on_col(fruit.pos):
                    fruit.caught = True # disappears next tick
                elif ((fruit.on_bottom_row() and not fruit.rotten and not self._on_col(fruit.pos)) or 
                      (fruit.on_bottom_row() and fruit.rotten and self._on_col(fruit.pos))):
                    self.status = MinigameStatus.LOSE
                    break
                
            if self.status == MinigameStatus.LOSE:
                break
            
            spawn_timer -= 1
            fall_timer -= 1
            self.decrementTimer()

        # win if time is up
        self.status = MinigameStatus.WIN if self.status is not MinigameStatus.LOSE else MinigameStatus.LOSE

        # Set board func to previously stored func
        self._board_reader.set_on_change(old_board_func)

        return True if self.status == MinigameStatus.WIN else False
    
    def _on_col(self, pos: tuple[int, int]):
        if self.debug:
            (r, c) = self._posPtr.get_phys_pos()
            return c == pos[1]
        
        return (9, pos[1]) == (self.changes[0]) if len(self.changes) > 0 else False
    
    def get_pos(self):
        if self.debug:
            return self._posPtr.get_phys_pos()[1]
        return None
            
    def get_board_data(self) -> dict:
        data = super().get_board_data()
        data["minigameData"]["timer"] = {}
        data["minigameData"]["squares"] = [
            {
                "position": f.pos, 
                "colour": ("black" if f.rotten else "pink"),
                "name": ("fruitRotten" if f.rotten else "fruit")
            } for f in self.fruits
        ] + [
            {
                "position": (9, self._posPtr.get_phys_pos()[1] if self.debug else self.changes[0][1] if len(self.changes) > 0 else (-1, -1)), 
                "colour": self._player.name, 
                "name": "basket"
            }
        ]
        return data

class PestControl(Minigame):
    """Minigame where the player presses a button to exterminate a pest when it is on a certain column."""
    class Pest():
        """Handles movement and boundary checking for a pest."""
        DIRECTIONS = [
            (0, 1), #right
            (0, -1), #left
            (1, 1), #down-right
            (1, -1), #down-left
            (-1, 1), #up-right
            (-1, -1) #up-left
        ]

        def __init__(self) -> None:
            self.pos = gen_rand_pos()
            self.direction = choice(self.DIRECTIONS)
            self.caught = False

        def move(self):
            """Moves the pest."""
            # change opposite dir if wall hit
            if self.hit_horizontal_wall():
                self.direction = self.get_opposite_direction(self.pos)
            elif self.hit_vertical_wall():
                self.direction = (self.get_opposite_vertical(self.direction[0]), self.direction[1])
            
            # move in direction
            self.pos = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])

            # teleport if offscreen
            while not self.is_onscreen():
                self.pos = gen_rand_pos()
                self.direction = choice(self.DIRECTIONS)
        
        def hit_vertical_wall(self) -> bool:
            """Returns true if the pest is on a row boundary else false."""
            return self.pos[0] == 0 or self.pos[0] == 9
        
        def hit_horizontal_wall(self) -> bool:
            """Returns true if the pest is on a col boundary else false."""
            return self.pos[1] == 0 or self.pos[1] == 9

        def is_onscreen(self) -> bool:
            """Returns true if the pest is on a valid position within the board else false"""
            return (0 <= self.pos[0] < 10) and (0 <= self.pos[1] < 10)

        def get_opposite_vertical(self, row: int) -> int:
            """Returns the row direction delta opposite to row.

            Random direction chosen if row is not at a board boundary.
            """
            if row == 0:
                return choice([1, 0])
            elif row == 9:
                return choice([-1, 0])
            else:
                return choice([-1, 0, 1])

        def get_opposite_horizontal(self, col: int) -> int:
            """Returns the col direction delta opposite to the col.

            Random direction chosen if col is not at a board boundary.
            """
            if col == 0:
                return 1
            elif col == 9:
                return -1
            else:
                return choice([-1, 1])
            
        def get_opposite_direction(self, pos: tuple[int, int]) -> tuple[int, int]:
            """Returns the direction vector opposite to pos."""
            return (self.get_opposite_vertical(pos[0]), self.get_opposite_horizontal(pos[1]))

    TICK = 0.2

    def __init__(self, player: "Player", posPtr: PosPtr, exclusions: List[int], get_board_state: Callable, board_reader: "BoardReader", get_buttons_pressed: callable, debug: bool) -> None:
        super().__init__(player, posPtr, exclusions, get_board_state, board_reader, get_buttons_pressed, debug)
        self._pest = None
        self._judgment_line = player.position[1]
        self._posPtr.debug_mode(None, "hit")
        self.phase = self.phase + "-pestControl"

    def play(self) -> bool:
        self.status = MinigameStatus.PLAY
        self._pest = self.Pest()

        # Reset button pressed flags
        self.get_buttons_pressed()

        while not self.is_timeup():
            
            # extra generous so another check before moving
            btn1, btn2 = self.get_buttons_pressed()

            if btn1 or btn2:
                if self._pest.pos[1] == self._judgment_line:
                    self.status = MinigameStatus.WIN
                    return True
                else:
                    self.status = MinigameStatus.LOSE
                    return False

            self._pest.move()
            utils.send_json(self.get_json())
            sleep(self.TICK)
            
            ## check if pest caught
            #btn1, btn2 = self.get_buttons_pressed()
            #
            #if btn1 or btn2:
            #    if self._pest.pos[1] == self._judgment_line:
            #        self.status = MinigameStatus.WIN
            #        return True
            #    else:
            #        self.status = MinigameStatus.LOSE
            #        return False

            self.decrementTimer()

        # lose if time is up
        self.status = MinigameStatus.LOSE
        return False

    def get_board_data(self) -> dict:
        data = super().get_board_data()
        data["minigameData"]["squares"] = [
            ({
                "colour": self._player.name,
                "name": "line",
                "position": (row, self._judgment_line)
            }) for row in range(10)
        ]
        if self._pest:
            data["minigameData"]["squares"].append(
                {
                    "colour": "black",
                    "name": "pest",
                    "position": self._pest.pos
                }
            )
        return data

class PosPtr():
    """
    Wrapper around an object which is expected to contain the current location
    of the player's physical piece on the board.
    Currently using keyboard input via pynput to emulate hardware.
    """
    def __init__(self, player: "Player") -> None:
        self._player = player
        self.input_pos = None
        self.debug = False

    def debug_mode(self, start_pos: tuple[int, int], input_mode: str) -> None:

        def on_press_lr(key):
            if key == keyboard.Key.left and self.input_pos[1] > 0:
                (r, c) = self.input_pos
                self.input_pos = (r, c - 1)
            elif key == keyboard.Key.right and self.input_pos[1] < 9:
                (r, c) = self.input_pos
                self.input_pos = (r, c + 1)
        
        def on_press_space(key):
            if key == keyboard.Key.space:
                self.input_pos = (-1, -1)
        
        self.debug = True
        self.input_pos = start_pos
        if input_mode == "hit":
            listener = keyboard.Listener(on_press=on_press_space)
            listener.start()
        elif input_mode == "left-right":
            listener = keyboard.Listener(on_press=on_press_lr)
            listener.start()

    def get_phys_pos(self) -> tuple[int, int]:
        if self.debug:
            return self.input_pos
        return self._player.position

MINIGAMES = [GooseChase, FallingFruits, PestControl]
class MinigameManager():
    """Handles selecting and starting a minigame.
    Bridges data from the main game class to the minigame classees."""

    def __init__(self, get_board_state: Callable, board_reader: "BoardReader", get_btns_pressed: callable, debug: bool) -> None:
        
        self._get_board_state = get_board_state
        self._board_reader = board_reader
        self._get_btns_pressed = get_btns_pressed
        self._minigame: Minigame = None
        self.debug: bool = debug

    def new_minigame(self, player: "Player", exclusions: list["Player"], game: Minigame = None) -> Minigame:
        """
        Initialises a new minigame, to be run when play() is called.
        If game is None, initialises a random minigame.
        Returns the minigame.
        """
        if game is None:
            game = MINIGAMES[randrange(0, len(MINIGAMES))]
            
        self._minigame = game(player, PosPtr(player), exclusions, self._get_board_state, self._board_reader, self._get_btns_pressed, self.debug)

        return self._minigame

    def play(self) -> bool:
        """
        Starts a minigame, and after it finishes returns true if the player won else false.
        """

        if self._minigame is None:
            return False

        win = self._minigame.play()
        utils.send_json(self._minigame.get_json())
        return win
    
    def get_status(self) -> MinigameStatus:
        """Returns the minigame's status"""
        return self._minigame.status if self._minigame is not None else None
    
    def get_phase(self) -> str:
        """Returns the minigame's phase"""
        return self._minigame.phase if self._minigame is not None else None
    
    def get_state(self) -> dict:
        """Returns the minigame's data"""
        return self._minigame.get_board_data() if self._minigame is not None else None



