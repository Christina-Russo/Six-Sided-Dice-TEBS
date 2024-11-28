# game_components.py

from abc import ABC, abstractmethod
import random
POSITION_TO_NUM = {(0, 0): 100, (0, 1): 99, (0, 2): 98, (0, 3): 97, (0, 4): 96, (0, 5): 95, (0, 6): 94, (0, 7): 93, (0, 8): 92, (0, 9): 91, (1, 9): 90, (1, 8): 89, (1, 7): 88, (1, 6): 87, (1, 5): 86, (1, 4): 85, (1, 3): 84, (1, 2): 83, (1, 1): 82, (1, 0): 81, (2, 0): 80, (2, 1): 79, (2, 2): 78, (2, 3): 77, (2, 4): 76, (2, 5): 75, (2, 6): 74, (2, 7): 73, (2, 8): 72, (2, 9): 71, (3, 9): 70, (3, 8): 69, (3, 7): 68, (3, 6): 67, (3, 5): 66, (3, 4): 65, (3, 3): 64, (3, 2): 63, (3, 1): 62, (3, 0): 61, (4, 0): 60, (4, 1): 59, (4, 2): 58, (4, 3): 57, (4, 4): 56, (4, 5): 55, (4, 6): 54, (4, 7): 53, (4, 8): 52, (4, 9): 51, (5, 9): 50, (5, 8): 49, (5, 7): 48, (5, 6): 47, (5, 5): 46, (5, 4): 45, (5, 3): 44, (5, 2): 43, (5, 1): 42, (5, 0): 41, (6, 0): 40, (6, 1): 39, (6, 2): 38, (6, 3): 37, (6, 4): 36, (6, 5): 35, (6, 6): 34, (6, 7): 33, (6, 8): 32, (6, 9): 31, (7, 9): 30, (7, 8): 29, (7, 7): 28, (7, 6): 27, (7, 5): 26, (7, 4): 25, (7, 3): 24, (7, 2): 23, (7, 1): 22, (7, 0): 21, (8, 0): 20, (8, 1): 19, (8, 2): 18, (8, 3): 17, (8, 4): 16, (8, 5): 15, (8, 6): 14, (8, 7): 13, (8, 8): 12, (8, 9): 11, (9, 9): 10, (9, 8): 9, (9, 7): 8, (9, 6): 7, (9, 5): 6, (9, 4): 5, (9, 3): 4, (9, 2): 3, (9, 1): 2, (9, 0): 1}
# Abstract Card Class
class Card(ABC):
    """
    Abstract card superclass
    """
    def __init__(self, name: str, description: str, card_id: int):
        self.name = name
        self.description = description
        self.card_id = card_id

    @abstractmethod
    def apply(self, game, player) -> None:
        """
        Apply card effects. Might need to add current_board, btn1, and btn2 for expanded functionality
        """
        pass

# Card Implementations
class RollDiceCard(Card):
    """
    Simple and most common card in deck. Moves player position forward by 1-6 spaces when applied.
    """
    def __init__(self):
        super().__init__("Roll Dice", "Roll a dice and move forward.", 0)
        self.card_id = 22 + random.randint(1,6)

    def apply(self, game, player):
        roll = self.card_id - 22
        print(f"{player.name} rolled a {roll}.")
        game.move_player(player, roll)

class OversleepCard(Card):
    """
    "Do Nothing" card. This card does nothing. Effectively skips the player's turn.
    """
    def __init__(self):
        super().__init__("Oversleep", "Do nothing this turn.", 2)

    def apply(self, game, player):
        print(f"{player.name} overslept and does nothing this turn.")

class SwapWithLeadCard(Card):
    """
    Swaps the current player with the player in the lead. No effect if the current player is already in the lead.
    """
    def __init__(self):
        super().__init__("Swap with Leader", "Swap positions with the current leader.", 29)

    def apply(self, game, player):
        leader = game.get_leader()
        if leader != player:
            print(f"{player.name} swaps with {leader.name}.")
            player.position, leader.position = leader.position, player.position
        else:
            print(f"{player.name} is already the leader.")

class DiceRollDuelCard(Card):
    """
    Initiate a duel between the current player and the player in the lead. No effect if the current player is already the leader. DEPRECATED
    """
    def __init__(self):
        super().__init__("Dice Roll Duel", "Trigger a dice roll duel with the leader.", 1)
        self.first_roll = None
        self.second_roll = None

    def apply(self, game, player):
        pass

class DescendSnakeCard(Card):
    """
    If a snake is ahead of the current player, move that player to the snake's tail.
    """
    def __init__(self):
        super().__init__("Descend the Next Snake", "Move forward to the head of the next snake, then slide to its tail.", 5)

    def apply(self, game, player):
        print(f"{player.name} is descending the next snake.")
        
        # Current player position in (row, col) format
        player_position = player.position
        player_num = POSITION_TO_NUM[player_position]

        # Find all snakes with head above the player's current number
        snakes_ahead = [snake for snake in game.snakes if POSITION_TO_NUM[snake.head] > player_num]

        if snakes_ahead:
            # Find the nearest snake head by the difference in numbers
            nearest_snake = min(snakes_ahead, key=lambda snake: POSITION_TO_NUM[snake.head] - player_num)
            snake_head_num = POSITION_TO_NUM[nearest_snake.head]
            num_spaces_to_move = snake_head_num - player_num
            
            print(f"{player.name} will move {num_spaces_to_move} spaces to reach Snake {nearest_snake.id} at {nearest_snake.head}.")
            #game.move_player(player, num_spaces_to_move, minigames_enabled=False)
            
            # Collect intermediate_positions
            game._move_spaces(player, num_spaces_to_move, collect_intermediates=True)
            player.intermediate_positions.append(player.position)
            # Set position to snake tail
            player.position = nearest_snake.tail
            # Move position if on top of another player
            game.move_player(player, 0, False)
        else:
            print("No snakes found ahead of player.")

class JumpAheadCard(Card):
    """
    All players move ahead by one space, automatically climbing a ladder, or falling down a snake if they land on one.
    """
    def __init__(self):
        super().__init__("Jump Ahead", "All players move one space ahead.", 7)

    def apply(self, game, player):
        print("All players are moving one space ahead.")
        # Iterate through players by their current position on the board
        for p in sorted(game.players, key=lambda p: POSITION_TO_NUM[p.position], reverse=True):
            print(f"{p.name} is moving one space ahead.")
            game.move_player(p, 1, minigames_enabled=False)

class HelpingHandCard(Card):
    """
    The player in the last position moves up to to the square behind the player in the second-last position.
    """
    def __init__(self):
        super().__init__("Helping Hand", "The player in last position moves up to the square behind the next player in front of them.", 9)

    def apply(self, game, player):
        # Sort players by their current position on the board
        sorted_players = sorted(game.players, key=lambda p: POSITION_TO_NUM[p.position])
        
        # Get the player in the last position
        last_player = sorted_players[0]
        last_player_num = POSITION_TO_NUM[last_player.position]
        print(f"{last_player.name} is currently in last position at {last_player.position}.")

        # Find the next player ahead of the last player
        players_ahead = [p for p in sorted_players if POSITION_TO_NUM[p.position] > last_player_num]

        if players_ahead:
            # Find the closest player ahead
            next_player = players_ahead[0]
            next_player_num = POSITION_TO_NUM[next_player.position]
            print(f"{next_player.name} is the next player ahead at position {next_player.position}.")

            # Calculate how many spaces to move the last player
            num_spaces_to_move = next_player_num - last_player_num - 1  # One space behind the next player

            # Move the last player
            if num_spaces_to_move > 0:
                print(f"{last_player.name} will move {num_spaces_to_move} spaces to be behind {next_player.name}.")
                game.move_player(last_player, num_spaces_to_move, minigames_enabled=False)
            else:
                print(f"{last_player.name} cannot move behind {next_player.name}, as they are too close.")
        else:
            print(f"No players are ahead of {last_player.name} to move behind.")


class SwapSnakesAndLaddersCard(Card):
    """
    Replaces all snakes with ladders and all ladders with snakes.
    Players previously on a snake tail or a ladder will move foward one space.
    """
    def __init__(self):
        super().__init__("Swap Snakes and Ladders", "Swap all snakes and ladders on the board. Players on a snake's head or ladder's tail will be moved 1 space forward.", 10)

    def apply(self, game, player):
        print("Swapping all snakes and ladders on the board.")
        
        # Swap all snakes and ladders
        self._swap_snakes_and_ladders(game)
        
        # Move players to avoid landing on snake heads or ladder tails
        self._adjust_player_positions(game)

    def _swap_snakes_and_ladders(self, game):
        """Swap the heads and tails of snakes with the bottoms and tops of ladders."""
        for i in range(min(len(game.snakes), len(game.ladders))):
            # Swap snake head with ladder top
            game.snakes[i].head, game.ladders[i].top = game.ladders[i].top, game.snakes[i].head
            # Swap snake tail with ladder bot
            game.snakes[i].tail, game.ladders[i].bottom = game.ladders[i].bottom, game.snakes[i].tail
        print("Snakes and ladders swapped successfully.")

    def _adjust_player_positions(self, game):
        """Move players 1 space forward if they land on a snake's head or a ladder's tail."""
        for p in game.players:
            player_position = p.position
            
            # Check if player is on a snake's head or ladder's tail
            snake_on_position = next((s for s in game.snakes if s.head == player_position), None)
            ladder_on_position = next((l for l in game.ladders if l.bottom == player_position), None)
            
            if snake_on_position:
                print(f"{p.name} is on a snake's head at {player_position}. Moving 1 space forward.")
                game.move_player(p, 1, minigames_enabled=False)
            
            elif ladder_on_position:
                print(f"{p.name} is on a ladder's tail at {player_position}. Moving 1 space forward.")
                game.move_player(p, 1, minigames_enabled=False)

class CardManager:
    """
    Handles drawing cards from the deck and storing current cards.
    """
    def __init__(self):
        self.deck = [RollDiceCard, OversleepCard, SwapWithLeadCard, DiceRollDuelCard, DescendSnakeCard, JumpAheadCard, HelpingHandCard, SwapSnakesAndLaddersCard]
        self.weights = [0.6, 0.02, 0.05, 0.0, 0.05, 0.05, 0.05, 0.05]
        self.current: Card = None


    def draw_card(self) -> Card:
        """
        Returns a random card using self.weights to simulate multiple identical cards increasing probability.
        """
        return random.choices(self.deck, weights=self.weights, k=1)[0]()
