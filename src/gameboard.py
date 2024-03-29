import logging

WHITE = 'WHITE'
BLACK = 'BLACK'

COUNT_TOKENS_PER_COLOR = 15


# Utility function
def normalise_position(position_to_normalise, color):
    if color == BLACK:
        position_to_normalise = abs(position_to_normalise - 25)
    return position_to_normalise


class GameBoard:
    def __init__(self, game):
        self.game = game

        self.__board = [
            2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5,
            -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2
        ]

        self.beaten = {
            WHITE: 0,
            BLACK: 0
        }

        self.finished = {
            WHITE: 0,
            BLACK: 0
        }

    @property
    def board(self) -> list:
        return self.__board.copy()

    def __str__(self) -> str:
        def draw_quarter(fields) -> str:
            elements = [f"{abs(element) if element != 0 else ' '}"
                        f"{'W' if element > 0 else ('B' if element < 0 else ' ')}"
                        for element in fields]
            return "│".join(elements)

        line = " ↙12←11←10← 9← 8← 7← 6← 5← 4← 3← 2← 1"
        line += "\n"
        line += "↓╔" + ("═" * 17) + "╦" + ("═" * 17) + "╗"
        line += "\n"
        line += "↓"
        line += f"║{draw_quarter(reversed(self.board[6:12]))}"
        line += f"║{draw_quarter(reversed(self.board[:6]))}"
        line += f"║ {str(self.finished[BLACK]).rjust(1)}B"
        line += "\n"
        line += "↓"
        line += (f"╠" + f" {self.beaten[WHITE]}W ".center(17, "═") +
                 f"╬" + f" {self.beaten[BLACK]}B ".center(17, "═") +
                 f"╣")
        line += "\n"
        line += "↓"
        line += f"║{draw_quarter(self.board[12:18])}"
        line += f"║{draw_quarter(self.board[18:])}"
        line += f"║ {str(self.finished[WHITE]).rjust(1)}W"
        line += "\n"
        line += "↓╚" + ("═" * 17) + "╩" + ("═" * 17) + "╝"
        line += "\n"
        line += " ↘13→14→15→16→17→18→19→20→21→22→23→24"
        return line

    def reverse(self) -> None:
        self.__board = [-number for number in reversed(self.board)]

    def get_possible_positions(self, possible_moves: list, color_player: str):
        if self.beaten[color_player]:
            for move in possible_moves:
                if self.test_move(-1, move, color_player):
                    return [-1]
            return []

        possible_positions = []
        for i in range(len(self.board)):
            for move in possible_moves:
                if self.test_move(i, move, color_player):
                    possible_positions.append(i)
        return possible_positions

    def test_move(self, position_old: int, width: int, color_player: str) -> bool:
        def verify_old_position() -> bool:
            if self.__is_beaten_tokens_field(position_old) and self.beaten[color_player]:
                return True

            if not self.__is_position_inside_board(position_old):
                return False

            if not self.__is_own_color_on_position(position_old):
                return False

            return True

        def verify_new_position() -> bool:
            if not self.__is_position_inside_board(position_new):
                return True if self.__are_all_tokens_in_last_section() else False

            if self.__is_own_color_on_position(position_new):
                return True

            if self.__is_single_opponent_token_on_position(position_new):
                return True

            if self.__is_position_empty(position_new):
                return True

            return False

        if color_player == BLACK:
            self.reverse()

        position_new = position_old + width
        result = verify_old_position() and verify_new_position()

        if color_player == BLACK:
            self.reverse()

        return result

    def make_move(self, position_old: int, width: int, color_player: str, possible_moves: list) -> bool:
        def do_move():
            color_opponent = BLACK if color_player is WHITE else WHITE

            if self.__is_beaten_tokens_field(position_old):
                self.beaten[color_player] -= 1
            else:
                self.__board[position_old] -= 1

            if not self.__is_position_inside_board(position_new):
                self.finished[color_player] += 1

            elif self.__is_single_opponent_token_on_position(position_new):
                self.__board[position_new] = 1
                self.beaten[color_opponent] += 1

            else:
                self.__board[position_new] += 1

            possible_moves.remove(width)

        if not self.test_move(position_old, width, color_player):
            return False

        if color_player == BLACK:
            self.reverse()

        position_new = position_old + width
        do_move()

        if color_player == BLACK:
            self.reverse()

        normalised_old = normalise_position(position_old + 1, color_player)
        normalised_new = normalise_position(position_new + 1, color_player)
        logging.info(f"Player {color_player} moved a token from {normalised_old} "
                     f"to {normalised_new} ({width}):")
        logging.info(str(self))

        if self.finished[color_player] == COUNT_TOKENS_PER_COLOR:
            self.game.finish(color_player)

        return True

    # The following methods are used to check some properties of the game board
    def __is_beaten_tokens_field(self, position: int) -> bool:
        return position == -1

    def __is_position_inside_board(self, position: int) -> bool:
        return 0 <= position < len(self.board)

    def __is_own_color_on_position(self, position: int) -> bool:
        return self.__is_position_inside_board(position) and self.board[position] > 0

    def __are_all_tokens_in_last_section(self) -> bool:
        return max(self.board[:18]) <= 0

    def __is_single_opponent_token_on_position(self, position) -> bool:
        return self.__is_position_inside_board(position) and self.board[position] == -1

    def __is_position_empty(self, position) -> bool:
        return self.__is_position_inside_board(position) and self.board[position] == 0
