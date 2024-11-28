def generate_snakes_and_ladders_dict(n_rows=10, n_cols=10):
    board_dict = {}
    num = n_rows * n_cols  # Start with 100 in a 10x10 board

    for r in range(n_rows):
        if r % 2 == 0:
            # Even row, left to right
            for c in range(n_cols):
                board_dict[(r, c)] = num
                num -= 1
        else:
            # Odd row, right to left
            for c in range(n_cols - 1, -1, -1):
                board_dict[(r, c)] = num
                num -= 1
    return board_dict

# Generate the dictionary representation of the board
snakes_and_ladders_dict = generate_snakes_and_ladders_dict()

# Print the dictionary
print(snakes_and_ladders_dict)
