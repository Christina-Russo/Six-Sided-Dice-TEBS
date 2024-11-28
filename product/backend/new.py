import board_reader as br
import game as gm
import time

game = gm.SnakesAndLadders()
board = br.BoardReader()
buttons = br.Buttons()

board.start_board_thread(game.pretty_print_board(), game.pretty_print_board())
time.sleep(3)
buttons._button_pressed = 1
board.finish_board_thread()