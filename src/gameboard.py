WHITE = 'white'
BLACK = 'black'


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
    def board(self):
        return self.__board.copy()

    def draw(self, player):
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

    def reverse(self):
        self.__board = [-number for number in reversed(self.board)]

    def make_move(self, position_old, width, color, possible_moves, is_ai=False):
        from game import display

        def is_position_inside_board(position):
            return 0 <= position < len(self.board)

        def is_position_outside_board(position):
            return not is_position_inside_board(position)

        def is_own_color_on_position(position):
            return is_position_inside_board(position) and self.board[position] > 0

        def are_all_tokens_in_last_section():
            return max(self.board[:18]) <= 0

        def is_single_opponent_token_on_new_position():
            return is_position_inside_board(position_new) and self.board[position_new] == -1

        def is_new_position_empty():
            return is_position_inside_board(position_new) and self.board[position_new] == 0

        def verify_old_position() -> bool:
            if is_position_outside_board(position_old):
                return False

            if not is_own_color_on_position(position_old):
                return False

            if self.beaten[color] and position_old != 0:
                return False

            return True

        def verify_new_position():
            if is_position_outside_board(position_new):
                if are_all_tokens_in_last_section():
                    return True
                else:  # not are_all_tokens_in_last_section():
                    return False

            if is_own_color_on_position(position_new):
                return True

            if is_single_opponent_token_on_new_position():
                return True

            if is_new_position_empty():
                return True

            return False

        def do_move():
            self.__board[position_old] -= 1

            if is_position_inside_board(position_new):
                if is_single_opponent_token_on_new_position():
                    self.__board[position_new] = 1
                    self.beaten[color_opponent] += 1

                else:  # is_correct_color_on_position(position_new) or is_new_position_empty()
                    self.__board[position_new] += 1

            else:  # is_new_position_outside_board()
                self.finished[color] += 1

        color_opponent = BLACK if color is WHITE else WHITE
        position_new = position_old + width

        if not verify_old_position():
            return False

        if not verify_new_position():
            return False

        do_move()

        print(f"Player {color}: Moved from {position_old + 1} to {position_new + 1}")
        possible_moves.remove(width)
        display(self, possible_moves, color)

        if is_ai:
            input("(ai made it's turn. [Enter] to continue)")

        return True
