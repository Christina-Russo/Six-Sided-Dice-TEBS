"""
Board reader module.

Erik & Stu.
"""

import time
import threading

# if unable to import library (prob cause it isn't on a pi) load a pretend
# bitstream for testing
try:
    from RPi import GPIO
    print("RPi pin library successfully loaded.")
except ModuleNotFoundError:
    print("Error importing GPIO Library!  This is probably because you either "
          "tried to run it from something other than a Raspberry Pi, or you "
          "need superuser privileges.")
    print("Try running the program with 'sudo' from a Pi")
    print("This error can be ignored while testing.")
    from . import substitute_gpio_lib as GPIO
    print("Loaded virtual GPIO/shift register lib")

# GPIO.setmode(GPIO.BCM)
PIN_MODE = GPIO.BCM
MIN_TICK_SPD = 0.0001
MIN_PL_SPD = 100 * MIN_TICK_SPD

class BoardReader():
    """
    Class to handle reading bits from the board hardware, then translate it intoW
    something usable.
    Pin constants are contained in here, along with handling the interface with
    hardware pins.

    Usage:
        board = BoardReader()
        board.read_positions()
    """
    # Pins to read from the board hardware
    CLOCK_PIN = 17
    LATCH_PIN = 27
    SERIAL_INPUT = 4

    # Board Size
    ROWS = 10
    COLUMNS = 10
    BITS_PER_ROW = 16

    # Constants for pin states
    PARALLEL_LOAD = GPIO.LOW
    SERIAL_SHIFT = GPIO.HIGH

    def __init__(self) -> None:
        # Sets pin references to standard RPi mode
        GPIO.setmode(PIN_MODE)

        # Initialise pins
        GPIO.setup(BoardReader.CLOCK_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(BoardReader.LATCH_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(BoardReader.SERIAL_INPUT, GPIO.IN) #, pull_up_down=GPIO.PUD_DOWN)

        # initialize board
        self._board = [[0 for _ in range(10)] for _ in range(10)]
        self._positions = []
        self._board_changed = False
        self._on_change_func = None
        self._on_change_lock = False
        self._thread = None
        self._reader_active_lock = False
        self._halt_thread_loop = False
        self._halt_on_first = False

    def read_positions(self, trigger_on_change: bool=True) -> list[tuple[int, int]]:
        """
        Reads the state from the board hardware.
        stores the boardstate from the hardware to the BoardReader().
        If board state has changed, trigger the on_change function if set.
        Params:
            trigger_on_change:  triggers the on change function
        Returns:    
            A list of (row, column) coordinates of locations containing a piece
        """
        # self._positions = self.get_positions()
        self._read_sensors()
        if trigger_on_change:
            if self._board_changed and not self._on_change_lock:
                if self._on_change_func is not None:
                    print("test function")
                    self._on_change_func() # this function is set by backend
                if self._halt_on_first:
                    self._halt_thread_loop = True
            self._board_changed = False
        # print("tick")
        return self._positions[:]

    def get_positions(self) -> list[tuple[int, int]]:
        """
        Returns the currently saved list of positions as list[(row, column)].
        """
        return self._positions[:]

    def _clock_tick(self) -> None:
        """
        Cycles the clock state for one clock tick to the hardware.
        Params:     None
        Returns:    None
        """
        GPIO.output(BoardReader.CLOCK_PIN, GPIO.HIGH)
        time.sleep(MIN_TICK_SPD) # enforce minimum tick speed
        GPIO.output(BoardReader.CLOCK_PIN, GPIO.LOW)
        time.sleep(MIN_TICK_SPD) # enforce minimum tick speed

    def _set_latch(self, new_state: int) -> None:
        """
        Sets the latch pin to the new state to allow for changing the shift 
        register's mode between load from parallel and send to serial
        """
        GPIO.output(BoardReader.LATCH_PIN, new_state)

    def _read_sensors(self) -> None:
        """
        Reads the bits from the sensor array and stores a tuple of (row, column) where
        a bit has been set by the sensor.
        Returns: None
        If the board state has changed since last check, sets the board_changed
        flag.
        """

        board = [[0 for _ in range(10)] for _ in range(10)]
        positions = []

        # TODO: Change this if statement to a lock and change _reader_active to a lock.
        while self._reader_active_lock:
            time.sleep(0.001)

        #self._reader_active_lock = True
        self._set_latch(BoardReader.PARALLEL_LOAD)
        time.sleep(0.001)
        # uncomment all of the below when hardware is implemented
        self._clock_tick() # to load the shift registers
        self._set_latch(BoardReader.SERIAL_SHIFT)
        time.sleep(0.001)
        for row in range(BoardReader.ROWS):
            for _ in range(6): # skip first 6 bits per row
                self._clock_tick()
            for column in reversed(range(BoardReader.COLUMNS)):
                board[row][column] = not GPIO.input(BoardReader.SERIAL_INPUT)
                if self._board[row][column] != board[row][column]:
                    self._board_changed = True
                if board[row][column]:
                    positions.append((row, column))
                self._clock_tick() 

        self._board = board[:]
        self._positions = positions[:]
        #self._reader_active_lock = False

    def get_board(self) -> list[list[int]]:
        """
        Returns the currently saved board state as a list of lists accessable as
        list[row][column].
        """
        return self._board[:]

    def read_board(self, trigger_on_change: bool=False) -> list[list[int]]:
        """
        Reads the board state from the sensor array and returns the entire board
        as a list of lists of bits (ints).
        Sets the self._board_changed flag if board state is different.
        """
        self.read_positions(trigger_on_change)
        return self._board[:]

    def start_board_reader(self, func: callable=None, halt_on_first: bool=False,
                           trigger_on_change: bool=True) -> None:
        """
        A function that is used to start the thread used for continuously
        reading the board.
        
        Usage:
            With new function to continuously check:
                board.start_board_reader(function_to_be_called, False)
            With new function to halt after first change detected:
                board.start_board_reader(function_pointer)
            Start with no update to function (will not start if func not set 
            previously):
                board.start_thread()

        Params: 
            func: a function to be called when there is a change in the board
                If no function pointer is passed, uses currently set on_change 
                function
            halt_on_first: will read board once then stop the thread if True
            trigger_on_change: if true will cause func to be called when there
            is a change in the boardstate
        Returns: None
        will kick off the boardReading thread
        """
        if func:
            self._on_change_func = func
        elif not self._on_change_func:
            print("No function set, thread not started.")
            return

        self._halt_thread_loop = False
        self._halt_on_first = halt_on_first
        self._thread = threading.Thread(target=self._threading_func, args=(trigger_on_change,))
        self._thread.start()

    def set_on_change(self, new_on_change_function: callable=None):
        """
        Updates the function called when a new board state is detected.
        If no parameter passed, assigns a None value. (resets the function)
        """
        # TODO: change to thread.lock()
        #self._on_change_lock = True
        self._on_change_func = new_on_change_function
        #self._on_change_lock = False

    def _threading_func(self, trigger_on_change: bool=True):
        """
        the function to continously read the board state
        it will be called by start_board_thread(func)
        """
        while not self._halt_thread_loop:
            time.sleep(1/100)
            self.read_positions(trigger_on_change)
            if self._halt_on_first: # to end the loop after first read if requested
                self._halt_thread_loop = True
            # print("read tick")

    def halt_reader(self) -> None:
        """
        Ends the thread associated with the boardreading.  Does not require
        setting any flags.
        """
        if self._thread is not None:
            self._halt_thread_loop = True
            self._thread.join()
        else:
            return

class Buttons():
    """
    buttons class for managing the buttons attached to the gameboard
    """

    # the two pins used for buttons
    BLUE_BUTTON = 6
    RED_BUTTON = 5

    def __init__(self):
        GPIO.setmode(PIN_MODE)

        # initializing  all the member variables
        self._btn_func_lock = False
        self._blue_button_func = None
        self._red_button_func = None
        self._button_pressed = 0
        self._halt_loop = False
        self._halt_after_first = False
        self._thread = None
        GPIO.setup(self.BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.RED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def await_button_press(
            self,
            blue_func: callable,
            red_func: callable) -> int:
        """
        Activates the button reader, but will block program function until a 
        press is detected.
        
        Params:
            blue_func:  function to be triggered on blue button press
            red_func:  function to be triggered on red button press
        Returns:
            Which button was pressed as a class const Button.BLUE_BUTTON or 
            Button.RED_BUTTON
        """
        self._halt_loop = False
        self._halt_after_first = True
        self._blue_button_func = blue_func
        self._red_button_func = red_func
        
        return self._button_func

    def _button_func(self) -> int:
        """
        the function that will be run by the button thread
        it will loop through until a button is pressed, then it will 
        check which button has been pressed and execute the function specified
        in self.button_thread_start(func1, func2)
        
        Params: None
        Returns: None
        """
        which = None
        while not self._halt_loop:
            which = None
            time.sleep(1/500)
            if not GPIO.input(Buttons.BLUE_BUTTON):
                which = Buttons.BLUE_BUTTON
            elif not GPIO.input(Buttons.RED_BUTTON):
                which = Buttons.RED_BUTTON
            if which:
                self._trigger_button(which)
                while not GPIO.input(which):
                    # print(f"btn {which} held")
                    time.sleep(0.01)
                    

        return which

    def _trigger_button(self, which: int) -> None:
        """
        Triggers the set function depending on which button is pressed.
        which == 1: trigger blue_func
        which == 2: trigger red_func
        Does nothing on any other value.
        """
        if not self._blue_button_func or not self._red_button_func:
            print("Cannot trigger a null function")
            print("Can haz func plz? :3")
            return
        if which == Buttons.BLUE_BUTTON:
            self._blue_button_func()
        elif which == Buttons.RED_BUTTON:
            self._red_button_func()

        if self._halt_after_first:
            self._halt_loop = True

    def set_button_on_press(
            self,
            which_btn: int,
            btn_func: callable = None) -> None:
        """
        will specify which function will be used when a button is pressed
        Params: 
                which button: which button you want the function to be changed for.
                btn_func: the function to change the button press to.
        Returns: None
        """
        if which_btn != self.BLUE_BUTTON or which_btn != self.RED_BUTTON:
            print("Please select a button")
            return
        self._btn_func_lock = True
        if which_btn == Buttons.BLUE_BUTTON:
            self._blue_button_func = btn_func
        elif which_btn == Buttons.RED_BUTTON:
            self._red_button_func = btn_func
        self._btn_func_lock = False
        return which_btn

    def start_button_reader(
            self,
            blue_func: callable,
            red_func: callable,
            halt_after_first: bool = False) -> None:
        """
        will kick off the thread and specify the functions to be called
        Params: blue_func        :: function for blue button
                red_func        :: function for red button
                halt_after_first :: halt loop immediately after press is detected
    
        """
        # TODO: add check for none functions
        self._blue_button_func = blue_func
        self._red_button_func = red_func
        self._halt_loop = False
        self._halt_after_first = halt_after_first
        self._thread = threading.Thread(target=self._button_func, args=())
        self._thread.start()


    def halt_reader(self) -> None:
        """
        will wait for thread associated with the buttons to end (if needed)
        """
        self._halt_loop = True
        self._thread.join()
