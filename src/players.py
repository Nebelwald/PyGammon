import re
from abc import ABC, abstractmethod


class PlayerInterface(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def make_move(self, gameboard, possible_moves):
        pass


class HumanPlayer(PlayerInterface):
    INPUT_REGEX_STRING = "^[1-2]?[0-9],[0-9]$"

    def make_move(self, gameboard, possible_moves):
        while possible_moves:
            user_input = input("pos,width=")
            match = re.search(HumanPlayer.INPUT_REGEX_STRING, user_input)

            if not match:
                print("Input is invalid.")
                continue

            position_width_tuple = match.string.split(",")
            position = int(position_width_tuple[0]) - 1
            width = int(position_width_tuple[1])

            if width not in possible_moves:
                print(f"You cannot move {width} tiles.")
                continue

            if not gameboard.make_move(position, width, self.color, possible_moves.copy()):
                print("Move is invalid.")
            else:
                possible_moves.remove(width)


class AI_AlwaysMoveLastPossibleToken(PlayerInterface):
    def make_move(self, gameboard, possible_moves):
        while possible_moves:
            move = possible_moves[0]

            for i, value in enumerate(gameboard.board):
                if value <= 0:
                    continue

                if gameboard.make_move(i, move, self.color, possible_moves.copy(), True):
                    possible_moves.remove(move)
                    break
