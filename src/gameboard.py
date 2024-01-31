WHITE = 'WHITE'
BLACK = 'BLACK'

COUNT_TOKENS_PER_COLOR = 15


class GameBoard:
    def __init__(self):
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

    def draw(self, player) -> str:
        opponent = BLACK if player == WHITE else WHITE
        char_player = "W" if player == WHITE else "B"
        char_opponent = "B" if player == WHITE else "W"

        def draw_quarter(fields):
            elements = [f"{abs(element) if element != 0 else ' '}"
                        f"{char_player if element > 0 else (char_opponent if element < 0 else ' ')}"
                        for element in fields]
            return "│".join(elements)

        line = " ↙12←11←10← 9← 8← 7← 6← 5← 4← 3← 2← 1"
        line += "\n"
        line += "↓╔" + ("═" * 17) + "╦" + ("═" * 17) + "╗"
        line += "\n"
        line += "↓"
        line += f"║{draw_quarter(reversed(self.board[6:12]))}"
        line += f"║{draw_quarter(reversed(self.board[:6]))}"
        line += f"║ {str(self.finished[opponent]).rjust(1)}{char_opponent}"
        line += "\n"
        line += "↓"
        line += (f"╠" + f" {self.beaten[player]}{char_player} ".center(17, "═") +
                 f"╬" + f" {self.beaten[opponent]}{char_opponent} ".center(17, "═") +
                 f"╣")
        line += "\n"
        line += "↓"
        line += f"║{draw_quarter(self.board[12:18])}"
        line += f"║{draw_quarter(self.board[18:])}"
        line += f"║ {str(self.finished[player]).rjust(1)}{char_player}"
        line += "\n"
        line += "↓╚" + ("═" * 17) + "╩" + ("═" * 17) + "╝"
        line += "\n"
        line += " ↘13→14→15→16→17→18→19→20→21→22→23→24"
        return line

    def reverse(self) -> None:
        self.__board = [-number for number in reversed(self.board)]

    def get_possible_positions(self, possible_moves, color):
        if self.beaten[color]:
            for move in possible_moves:
                if self.test_move(-1, move, color):
                    return [-1]
            return []

        possible_positions = []
        for i in range(len(self.board)):
            for move in possible_moves:
                if self.test_move(i, move, color):
                    possible_positions.append(i)
        return possible_positions

    def test_move(self, position_old, width, color):
        position_new = position_old + width

        def is_beaten_tokens_field(position):
            return position == -1

        def is_position_inside_board(position):
            return 0 <= position < len(self.board)

        def is_own_color_on_position(position):
            return is_position_inside_board(position) and self.board[position] > 0

        def are_all_tokens_in_last_section():
            return max(self.board[:18]) <= 0

        def is_single_opponent_token_on_new_position():
            return is_position_inside_board(position_new) and self.board[position_new] == -1

        def is_new_position_empty():
            return is_position_inside_board(position_new) and self.board[position_new] == 0

        def verify_old_position() -> bool:
            if is_beaten_tokens_field(position_old) and self.beaten[color]:
                return True

            if not is_position_inside_board(position_old):
                return False

            if not is_own_color_on_position(position_old):
                return False

            return True

        def verify_new_position():
            if not is_position_inside_board(position_new):
                return True if are_all_tokens_in_last_section() else False

            if is_own_color_on_position(position_new):
                return True

            if is_single_opponent_token_on_new_position():
                return True

            if is_new_position_empty():
                return True

            return False

        return verify_old_position() and verify_new_position()

    def make_move(self, position_old, width, color, possible_moves):
        from game import display, finish

        def is_beaten_tokens_field(position):
            return position == -1

        def is_position_inside_board(position):
            return 0 <= position < len(self.board)

        def is_single_opponent_token_on_new_position():
            return is_position_inside_board(position_new) and self.board[position_new] == -1

        color_opponent = BLACK if color is WHITE else WHITE
        position_new = position_old + width

        if not self.test_move(position_old, width, color):
            return False

        if is_beaten_tokens_field(position_old):
            self.beaten[color] -= 1
        else:
            self.__board[position_old] -= 1

        if not is_position_inside_board(position_new):
            self.finished[color] += 1

        elif is_single_opponent_token_on_new_position():
            self.__board[position_new] = 1
            self.beaten[color_opponent] += 1

        else:
            self.__board[position_new] += 1

        possible_moves.remove(width)

        print(f"Player {color} moved a token from {position_old + 1} to {position_new + 1}")
        display(self, possible_moves, color)

        if self.finished[color] == COUNT_TOKENS_PER_COLOR:
            finish(color)

        return True
