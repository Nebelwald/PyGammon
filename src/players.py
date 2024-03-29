import re
from abc import ABC, abstractmethod

from src.gameboard import normalise_position


class PlayerInterface(ABC):
    def __init__(self, color):
        self.color = color

    def make_move(self, gameboard, possible_moves) -> None:
        self._make_move(gameboard, possible_moves)

    @abstractmethod
    def _make_move(self, gameboard, possible_moves) -> None:
        pass


class HumanPlayer(PlayerInterface):
    INPUT_REGEX_STRING = "^[1-2]?[0-9],[0-9]$"

    def _make_move(self, gameboard, possible_moves) -> None:
        while possible_moves and gameboard.get_possible_positions(possible_moves, self.color):
            user_input = input("pos,width=")
            match = re.search(HumanPlayer.INPUT_REGEX_STRING, user_input)

            if not match:
                print("Input is invalid.")
                continue

            position_width_tuple = match.string.split(",")
            position = normalise_position(int(position_width_tuple[0]), self.color) - 1
            width = int(position_width_tuple[1])

            if width not in possible_moves:
                print(f"You cannot move {width} tiles.")
                continue

            if not gameboard.make_move(position, width, self.color, possible_moves):
                print("Move is invalid.")


class AI_AlwaysMoveLastPossibleToken(PlayerInterface):
    def _make_move(self, gameboard, possible_moves) -> None:
        while possible_moves and gameboard.get_possible_positions(possible_moves, self.color):
            move = possible_moves[0]

            if gameboard.make_move(-1, move, self.color, possible_moves):
                continue

            for i, value in enumerate(gameboard.board):
                if gameboard.make_move(i, move, self.color, possible_moves):
                    break
