from random import randint

from gameboard import GameBoard, BLACK, WHITE
from ai import AI_AlwaysMoveLastPossibleToken
from player import HumanPlayer


def main():
    gameboard = GameBoard()

    human_player = HumanPlayer(WHITE)
    ai = AI_AlwaysMoveLastPossibleToken(BLACK)

    players = [human_player, ai]

    while True:
        for player in players:
            moves_player = roll_dices()
            display(gameboard, moves_player, player.color)

            if not type(player) is HumanPlayer:
                input("[Enter] to continue")

            player.make_move(gameboard, moves_player)

            print(f"Switching view to {BLACK if player.color == WHITE else WHITE} player's pov...")
            input()

            gameboard.reverse()


def roll_dices():
    possible_moves = [randint(1, 6), randint(1, 6)]
    if possible_moves[0] == possible_moves[1]:
        possible_moves *= 2

    return sorted(possible_moves)


def display(gameboard, possible_moves, color):
    print(f"\n--- ({color} player's point of view) ---")
    print(f"↓ {(BLACK if color == WHITE else WHITE).upper()} player ↓".center(37))
    print(gameboard.draw(color))
    print(f"↑ {(WHITE if color == WHITE else BLACK).upper()} player ↑".center(37))
    print(f"Possible moves: {[str(move) for move in possible_moves]}")


if __name__ == "__main__":
    main()
