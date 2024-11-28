# A Readme for using the hardware API spec

## BoardReader

Importing BoardReader will throw an import error message, which currently can be ignored.<br>

### BoardReader functions

#### read_positions(self, trigger_on_change: bool=False): returns list[tuple[int,int]]<br>

**Params:**<ul>
 <li>trigger_on_change = True: will execute the function set by _on_change_func if there is a change since last read</li>
    <li>Otherwise: reads boardstate and returns positions without executing any function </li>
</ul>
Reads the board from the hardware, saving the positions and board to the class.

**Returns:** The list of tuple positions as [(row,column)] that are stored from previous read

#### get_positions(): returns list[tuple[int,int]]<br>

Will return the list of player positions currently stored by the class: [(row,column)] (DOES NOT DO A NEW BOARDSTATE READ)

#### get_board(): returns list[tuple[int,int]]<br>

- Will return the previously read boardstate saved by the class as a 10*10 grid of integers (DOES NOT DO A NEW BOARDSTATE READ)

#### read_board(self, trigger_on_change: bool = False): returns list[list[int]]<br>

Will read the board from the hardware and update positions/board saved to the class.

**Params:**<ul>
<li>trigger_on_change = True: will execute the function set by _on_change_func if there is a change since last board read and returns board.</li>
 <li>Otherwise: does not execute _on_change_func but reads and returns board (default = False)</li>
</ul>

**Returns:** a 10*10 grid of integers

#### start_board_reader(self, func: callable = None, halt_on_first: bool = False): returns None<br>
    Usage:
        With new function to continuously check:
                board.start_board_reader(function_to_be_called, False)
            With new function to halt after first change detected:
                board.start_thread(function_pointer, True)
            Start with no update to function (will not start if func not set 
            previously):
                board.start_board_reader()

**Params:**<ul>
<li>func: a function to be called when there is a change in the board. </li>

<li>halt_on_first: True to only have the board read once and execute func if changed</li>
</ul>

**Returns:** None


#### set_on_change(self, new_on_change_function: callable=None)

- Updates the function called when a new board state is detected.
- If no parameter passed, assigns a None value

#### halt_reader()
- Ends the thread associated with the boardreading.  Does not require setting any flags.

## Buttons
usage: buttons = Buttons() this will initialize the button reader class for managing button inputs

### Button Functions

#### await_button_press(self, btn1_func: callable, btn2_func: callable): Returns: int

Activates the button reader, but will block program function until a press is detected.

**Params:**<ul>
        <li>btn1_func:  function to be triggered on button 1 press</li>
        <li>btn2_func:  function to be triggered on button 2 press</li>
        </ul>

**Returns:**
Which button was pressed as a class const Button.BUTTON_ONE or Button.BUTTON_TWO

#### set_button_on_press(self, which_btn: int, btn_func: callable = None): Returns None
will specify which function will be used when a button is pressed.

Params:<ul>
<li>which_btn: which button to set the function for</li>  
<li>btn_func: the function to be executed when the button is pressed. (default = None)</li>
</ul>

**Returns:** None

#### start_button_reader(self, btn1_func :callable, btn2_func: callable, halt_after_first: bool = False):

will kick off the thread and specify the functions to be called
Params: <ul>
<li>btn1_func :: function for button 1</li>
<li>btn2_func :: function for button 2</li>
<li>halt_after_first :: halt loop immediately after press is detected</li>
</ul>

#### halt_reader(self):
will halt the button thread (if needed)

# TODO:
IMPLEMENT THREADING LOCKS



