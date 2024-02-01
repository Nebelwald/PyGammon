from random import randint

from src.gameboard import GameBoard, BLACK, WHITE
from src.players import AI_AlwaysMoveLastPossibleToken, HumanPlayer

PAUSE = False


class Game:
    def __init__(self, white_player: str, black_player: str, interactive: bool):
        def create_player(name_string, color):
            match name_string:
                case 'human':
                    return HumanPlayer(color)
                case 'ai':
                    return AI_AlwaysMoveLastPossibleToken(color)

        self.game_board = GameBoard(self)

        self.players = [
            create_player(white_player, WHITE),
            create_player(black_player, BLACK)
        ]

        self.interactive = interactive

    def start_game(self):
        def roll_dices() -> list:
            possible_moves = [randint(1, 6), randint(1, 6)]
            if possible_moves[0] == possible_moves[1]:
                possible_moves *= 2
            return sorted(possible_moves)

        while True:
            for player in self.players:
                moves_player = roll_dices()
                self.display(moves_player, player.color)

                player.make_move(self.game_board, moves_player)

                if not type(player) is HumanPlayer and self.interactive:
                    input("(ai made it's turn. [Enter] to continue)")

                print(f"Switching {BLACK if player.color == WHITE else WHITE} player's pov...")

                self.game_board.reverse()

    def display(self, possible_moves: list, color: str) -> None:
        print(f"\n--- ({color} player's point of view) ---")
        print(f"↓ {(BLACK if color == WHITE else WHITE)} player ↓".center(37))
        print(self.game_board.draw(color))
        print(f"↑ {(WHITE if color == WHITE else BLACK)} player ↑".center(37))
        print(f"Possible moves: {[str(move) for move in possible_moves] if possible_moves else '-'}")

    def finish(self, color) -> None:
        print(f"\nPlayer {color} has won!")
        exit()
