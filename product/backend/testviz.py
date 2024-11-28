import tkinter as tk
from game import SnakesAndLadders, Snake, Ladder, GameTypes

## SO SCUFFED IT'S INSANE. The black numbers on the board are WRONG. dont worry about it..
# Testviz for just rough checking stuff

class SnakesAndLaddersGUI:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.board_size = 10  # 10x10 board
        self.cell_size = 40
        self.canvas = tk.Canvas(master, width=self.board_size * self.cell_size, height=self.board_size * self.cell_size)
        self.canvas.pack()
        self.draw_board()
        self.draw_snakes_and_ladders()
        self.update_positions()
        self.turn_label = tk.Label(master, text=f"Current turn: {self.game.get_current_turn()}")
        self.turn_label.pack()
        self.roll_button = tk.Button(master, text="Roll Dice", command=self.move_player)
        self.roll_button.pack()

    def draw_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                x1 = i * self.cell_size
                y1 = j * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                position = self.board_size * (self.board_size - 1 - j) + (i + 1) if j % 2 == 0 else self.board_size * (self.board_size - 1 - j) + (self.board_size - i)
                self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2, text=str(position), tags="board")

    def draw_snakes_and_ladders(self):
        for idx, snake in enumerate(self.game.snakes):
            self.mark_position(snake.head, f"S{idx+1}", offset_y=-10)
            self.mark_position(snake.tail, f"S{idx+1}", offset_y=10)
            self.mark_line(snake.head, snake.tail, "Red")

        for idx, ladder in enumerate(self.game.ladders):
            self.mark_position(ladder.bottom, f"L{idx+1}", offset_y=-10)
            self.mark_position(ladder.top, f"L{idx+1}", offset_y=10)
            self.mark_line(ladder.bottom, ladder.top, "Green")

    def mark_position(self, position, text, offset_y=0):
        row = (position - 1) // self.board_size
        col = (position - 1) % self.board_size
        x = col * self.cell_size + self.cell_size / 2
        y = (self.board_size - row - 1) * self.cell_size + self.cell_size / 2 + offset_y
        self.canvas.create_text(x, y, text=text, fill="blue", tags="snake_ladder")

    def mark_line(self, start, end, colour, offset_y=0):
        start_row, start_col = (start - 1) // self.board_size, (start - 1) % self.board_size
        end_row, end_col = (end - 1) // self.board_size, (end - 1) % self.board_size
        x0, y0 = start_col * self.cell_size + self.cell_size / 2, (self.board_size - start_row - 1) * self.cell_size + self.cell_size / 2 + offset_y
        x1, y1 = end_col * self.cell_size + self.cell_size / 2, (self.board_size - end_row - 1) * self.cell_size + self.cell_size / 2 + offset_y
        self.canvas.create_line(x0, y0, x1, y1, arrow='last', fill=colour, tags="snake_ladder")

    def update_positions(self):
        self.canvas.delete("player")
        for player in self.game.players:
            position = player.position
            row = (position - 1) // self.board_size
            col = (position - 1) % self.board_size
            x = col * self.cell_size + self.cell_size / 2
            y = (self.board_size - row - 1) * self.cell_size + self.cell_size / 2
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red", tags="player")
            self.canvas.create_text(x, y, text=player.name[0], fill="white", tags="player")

    def move_player(self):
        result = self.game.move_player()
        self.update_positions()
        self.turn_label.config(text=f"Current turn: {self.game.get_current_turn()}")
        if "wins" in result:
            self.roll_button.config(state=tk.DISABLED)
            self.turn_label.config(text=result)

if __name__ == "__main__":
    game = SnakesAndLadders(10, 10, players=["Alice", "Bob", "Charlie"])
    root = tk.Tk()
    gui = SnakesAndLaddersGUI(root, game)
    root.mainloop()
