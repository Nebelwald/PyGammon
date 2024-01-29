import re
from os.path import abspath, basename
from random import randint

from PyScreen.screen import Screen
from gameboard import GameBoard
from computer_opponent import computer_move

SCREEN = None

PLAYER_TOKEN = 1
AI_TOKEN = -1


def main():
    gameboard = GameBoard()

    while True:
        possible_moves_player = roll_dices()
        player_move(gameboard, possible_moves_player)

        possible_moves_computer = [1, 1, 1, 1]  # roll_dices()
        computer_move(gameboard, possible_moves_computer)


def roll_dices():
    possible_moves = [randint(1, 6), randint(1, 6)]
    if possible_moves[0] == possible_moves[1]:
        possible_moves *= 2

    return possible_moves


def player_move(gameboard, possible_moves):
    message = ""

    while True:
        databinding = {
            "gameboard": str(gameboard),
            "possible_moves": f"Possible moves: {[str(move) for move in sorted(possible_moves)]}",
            "message": message
        }

        if not possible_moves:
            _ = SCREEN.display(databinding, prompt="(paused to verify) [Enter]")
            break
        else:
            user_input = SCREEN.display(databinding)

            match = re.search("^[1-2]?[0-9],[0-9]$", user_input)
            if not match:
                message = "Input is invalid."
                continue

            position_width_tuple = match.string.split(",")
            position = int(position_width_tuple[0]) - 1
            width = int(position_width_tuple[1])

            if width not in possible_moves:
                message = f"You cannot move {width} tiles."
                continue

            if not gameboard.make_move(position, width, PLAYER_TOKEN):
                message = "Move is invalid."
            else:
                message = ""
                possible_moves.remove(width)


if __name__ == "__main__":
    SCREEN = Screen("game_view.yaml")

    Screen.set_size(39, 10)
    Screen.set_view_paths(abspath(__file__).replace(basename(__file__), ""))
    Screen.set_title("PyGammon")
    Screen.set_prompt("<pos>,<with>=")

    main()
