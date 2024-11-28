import board_reader as br
import substitute_gpio_lib as GPIO
import time


def testfunc2():
    print("this is another test")

def testfunc3():
    print("this is a test function")
    # do something


board = br.BoardReader()
buttons = br.Buttons()
board.set_on_change(testfunc2)
board.read_board()
GPIO.set_at_coord((1,3))
board.start_board_reader(trigger_on_change=True)
#board.set_on_change()

#board._on_change_func = testfunc2
#board.halt_reader()
time.sleep(1)
GPIO.set_at_coord((1,4))
time.sleep(3)
board.halt_reader()

