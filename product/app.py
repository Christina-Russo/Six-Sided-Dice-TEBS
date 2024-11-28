from backend import game, board_reader, utils
from random import randrange
from time import sleep
import sys
import signal

DEBUG = False
KEYBOARD = False
FORCE_MINIGAME = 0

# Run in debug mode if not on Raspberry Pi
try:
    import RPi.GPIO

except (ImportError):
    DEBUG = True
    from pynput import keyboard

# Enable debug mode if on Pi
if "-d" in sys.argv:
    DEBUG = True

# Force start a minigame at launch
if "-m" in sys.argv:
    if "1" in sys.argv:
        FORCE_MINIGAME = 1
    elif "2" in sys.argv:
        FORCE_MINIGAME = 2
    elif "3" in sys.argv:
        FORCE_MINIGAME = 3
    else:
        FORCE_MINIGAME = randrange(1, 3)

class App:
    """
    Basic application to run the prototype.
    Runs a game of Snakes and Ladders using hardware or software (debug) inputs.
    """

    def __init__(self) -> None:
        # Initialise Server connection to frontend

        # Initialise hardware
        self.board = board_reader.BoardReader()
        self.board_changed: bool = False

        self.buttons = board_reader.Buttons()
        self.button_one_pressed: bool = False
        self.button_two_pressed: bool = False

        self._state_lock: bool = False

        #Initialise signal handling to end threads on exit
        signal.signal(signal.SIGINT, self.signal_handler)

        # initalise game
        self.game = game.SnakesAndLadders(10, 10, [], self.board, self.get_buttons_pressed, DEBUG)

        if FORCE_MINIGAME:
            self.game = game.SnakesAndLadders(10, 10, [game.Player("Blue", 0)], self.board, self.get_buttons_pressed, DEBUG)
            self.game.players[0].position = self.game.ladders[0].bottom
            self.game.minigame_trigger = self.game.ladders[0]
            self.game.minigame = self.game.minigame_manager.new_minigame(self.game.get_current_player(), [], game.minigames.MINIGAMES[FORCE_MINIGAME - 1])
            self.game.state = game.SnakesLaddersGameState.MINIGAME

        if not DEBUG:
            # Start hardware listeners
            self.board.start_board_reader(self.on_board_change, False)
            self.board.set_on_change(self.on_board_change)
            self.buttons.start_button_reader(self.on_button_one_press, self.on_button_two_press, False)
        
        else:
            # Start keyboard listeners
            def on_press_space(key):
                if key == keyboard.Key.space:
                    self.on_board_change()
            self.space = keyboard.Listener(on_press=on_press_space)
            self.space.start()

            def on_press_1(key):
                if key == keyboard.Key.left:
                    self.on_button_one_press()
            self.button_one = keyboard.Listener(on_press=on_press_1)
            self.button_one.start()

            def on_press_2(key):
                if key == keyboard.Key.right:
                    self.on_button_two_press()
            self.button_two = keyboard.Listener(on_press=on_press_2)
            self.button_two.start()

    def on_board_change(self):
        """
        Sets board_changed = True. Uses locks to avoid race conditions. 
        Waits for previous lock to be released before modifying variable
        """
        # Wait for values to unlock
        while self._state_lock:
            pass
        # Lock values
        self._state_lock = True 
        # Change values
        self.board_changed = True
        # Unlock values
        self._state_lock = False
        
    def on_button_one_press(self):
        """
        Set button_one_pressed = True. Uses locks to avoid race conditions.
        Waits for previous lock to be released before modifying variable
        """
        # Wait for values to unlock
        while self._state_lock:
            pass
        # Lock values
        self._state_lock = True 
        # Change values
        self.button_one_pressed = True
        # Unlock values
        self._state_lock = False
        
    def on_button_two_press(self):
        """
        Set button_two_pressed = True. Uses locks to avoid race conditions. 
        Waits for previous lock to be released before modifying variable
        """
        # Wait for values to unlock
        while self._state_lock:
            pass
        # Lock values
        self._state_lock = True 
        # Change values
        self.button_two_pressed = True
        # Unlock values
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

    def get_buttons_pressed(self) -> tuple[bool, bool]:
        """
        Returns which buttons have been pressed, then resets both button states.
        Returned format is (bool, bool) where the first bool value is btn1's status and 
        the second bool value is btn2's status.
        """
        while self._state_lock:
            pass
        self._state_lock = True

        (b1, b2) = self.button_one_pressed, self.button_two_pressed

        self._state_lock = False
        self.reset_on_changes()

        return b1, b2

    def get_hardware_state(self) -> tuple[list[tuple[int,int]], bool, bool, bool]:
        """
        Returns the current state of the hardware. Used for minigame implementations.
        First value is the current board state reading in the form: list[tuple[int,int]] where only the values present are the pieces detected.
        Second value is whether the current board state has changed.
        Third value is whether button 1 (blue button) has been pressed.
        Fourth value is whether button 2 (red button) has been pressed.
        Recommended to call reset_on_changes to reset bool values returned from this function.
        """
        return self.board.get_positions(), self.board_changed, self.button_one_pressed, self.button_two_pressed
    
    def signal_handler(self, sig, frame):
        """
        Handles the SIGINT signal being received. Stops running threads, then exits.
        """
        if KEYBOARD:
            self.button_one.stop()
            self.button_two.stop()
        if not DEBUG:
            self.board.halt_reader()
            self.buttons.halt_reader()
        
        sys.exit(0)

    def run(self):
        """
        Sends the inital state of the game then enters gameplay loop.
        This function encompasses the entire gameplay logic of the prototype and should
        only be modified with care.
        If not DEBUG, the loop is as follows:
            1. wait until the board changes or either button 1 or button 2 is pressed.
            2. Update game with board state and button status.
            3. retreive game data as a JSON file.
            4. Send game data to server for displaying.
            repeat

        If DEBUG, the loop is as follows:
            1. Prompt user for input through the command line.
            2. Update game with board state and button status.
            3. Retreive game data as a JSON file.
            3a. Save game data as game_data.json.
            4. Send game data to server for displaying.
            repeat
        """
        data = self.game.get_json()
        utils.send_json(data)

        in_file = "in_state.txt"
        out_file = "out_state.txt"
        
        # TODO implement main loop logic
        while True:
            
            sleep(0.001)
            
            current_board = self.game.get_player_positions()

            if DEBUG:
                # Iterate through loop once each enter press. for debugging
                user_input = input(f"========= {self.game.state}\n"
                                "Enter a '1' to simulate pressing button 1.\n"
                                "Enter a '2' to simulate pressing button 2.\n"
                                "Enter an 'f' to simulate a custom board state, loaded from \"in_state.txt\"\n"
                                "Type 'reset' to restart the game in setup state\n"
                                "Type 'load' to load a test game\n")

                if '1' in user_input:
                    self.button_one_pressed = True

                if '2' in user_input:
                    self.button_two_pressed = True

                if "reset" == user_input:
                    ### Type "reset", and then press enter after so frontend knows to update to a clear state again
                    self.game = game.SnakesAndLadders(10, 10, [], self.board, self.get_buttons_pressed, DEBUG)

                elif "load" == user_input:
                    game_players = [game.Player(name, direction) for (name, direction) in [("Blue", 0), ("Yellow", 90), ("Green", 180), ("Pink", 270)]]
                    self.game = game.SnakesAndLadders(10, 10, game_players, self.board, self.get_buttons_pressed, DEBUG)

                elif 'f' in user_input:
                    current_board = state_from_file(in_file)

            else:
                # No change.
                if not (self.board_changed or self.button_one_pressed or self.button_two_pressed):
                    continue
            
            if not DEBUG:
                current_board = self.board.get_positions()

            print("In state:", current_board)

            # Send hardware to backend logic
            self.game.update_game(current_board, self.button_one_pressed, self.button_two_pressed)

            # Reset board_changed, btn1, and btn2
            self.reset_on_changes()

            # Store game piece positions for debugging
            state_to_file(out_file, self.game.get_player_positions())

            # Retrieve game data
            data = self.game.get_json()

            if DEBUG:
                # Store most recent game data, replacing last game_data file
                with open("game_data.json", 'w+') as file:
                    file.write(data)

            # Send game state to server to distribute to clients
            utils.send_json(data)
    
def state_from_file(file_name: str) -> list[tuple[int,int]]:
    """
    Reads and returns a stored board state from given file if file exists.
    Used in debugging only.
    """
    state: list[tuple[int,int]] = []
    try:
        with open(file_name) as file:
            data = file.readline()
            nmbrs = [int(s) for s in data if s.isdigit()]
            for i in (range(len(nmbrs) // 2)):
                state.append((nmbrs[2*i], nmbrs[2*i+1]))

    except ValueError:
        return []
    except FileNotFoundError:
        print("File not found")

    return state

def state_to_file(file_name: str, state: list[tuple[int,int]]) -> None:
    """
    Write the given state to given file, truncating file if it exists. Creates file if it doesn't exist.
    Used in debugging only.
    """
    with open(file_name, 'w+') as file:
        file.write(str(state))

# Begin game when running this file
if __name__ == "__main__":
    app = App()
    app.run()
