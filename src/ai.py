from abc import ABC, abstractmethod


class PlayerInterface(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def make_move(self, gameboard, possible_moves):
        pass


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
