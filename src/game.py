from random import randint

from gameboard import GameBoard, BLACK, WHITE
from players import AI_AlwaysMoveLastPossibleToken, HumanPlayer


PAUSE = False


def main():
    gameboard = GameBoard()

    human_player = AI_AlwaysMoveLastPossibleToken(WHITE)
    ai = AI_AlwaysMoveLastPossibleToken(BLACK)

    players = [human_player, ai]

    while True:
        for player in players:
            moves_player = roll_dices()
            display(gameboard, moves_player, player.color)

            player.make_move(gameboard, moves_player)

            if not type(player) is HumanPlayer and PAUSE:
                input("(ai made it's turn. [Enter] to continue)")

            print(f"Switching {BLACK if player.color == WHITE else WHITE} player's pov...")

            gameboard.reverse()


def roll_dices() -> list:
    possible_moves = [randint(1, 6), randint(1, 6)]
    if possible_moves[0] == possible_moves[1]:
        possible_moves *= 2
    return sorted(possible_moves)


def display(gameboard: GameBoard, possible_moves: list, color: str) -> None:
    print(f"\n--- ({color} player's point of view) ---")
    print(f"↓ {(BLACK if color == WHITE else WHITE)} player ↓".center(37))
    print(gameboard.draw(color))
    print(f"↑ {(WHITE if color == WHITE else BLACK)} player ↑".center(37))
    print(f"Possible moves: {[str(move) for move in possible_moves] if possible_moves else '-'}")


def finish(color) -> None:
    print(f"\nPlayer {color} has won!")
    exit()


if __name__ == "__main__":
    main()
