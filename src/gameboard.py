class GameBoard:
    def __init__(self):
        self.board = [
            2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5,
            -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2
        ]

        self.beaten = {
            1: 0,
            -1: 0
        }

        self.finished = {
            1: 0,
            -1: 0
        }

    def __str__(self):
        line = ""

        def draw_quarter(fields):
            elements = [
                f"{abs(element) if element != 0 else ' '}"
                f"{'W' if element > 0 else ('B' if element < 0 else ' ')}"
                for element in fields

            ]
            return "│".join(elements)

        line += ("╔" +
                 ("<".join(reversed([f"{i}".rjust(2, " ") for i in range(7, 13)]))) +
                 "╦" +
                 ("<".join(reversed([f"{i}".rjust(2, " ") for i in range(1, 7)]))) +
                 "╗")

        line += "\n"

        line += "║"
        upper_left = reversed(self.board[6:12])
        line += (draw_quarter(upper_left))
        line += "║"
        upper_right = reversed(self.board[:6])
        line += (draw_quarter(upper_right))
        line += "║"
        line += f" {str(self.finished[-1]).rjust(1)}B"

        line += "\n"

        line += (
                "╠" +
                f" {self.beaten[1]}W ".center(17, "═") +
                "╬" +
                f" {self.beaten[-1]}B ".center(17, "═") +
                "╣")

        line += "\n"

        line += "║"
        lower_left = self.board[12:18]
        line += (draw_quarter(lower_left))
        line += "║"
        lower_right = self.board[18:]
        line += (draw_quarter(lower_right))
        line += "║"
        line += f" {str(self.finished[1]).rjust(1)}W"

        line += "\n"

        line += ("╚" +
                 ">".join([f"{i}" for i in range(13, 19)]) +
                 "╩" +
                 ">".join([f"{i}" for i in range(19, 25)]) +
                 "╝")

        return line

    def make_move(self, position_old, width, token):
        def is_old_position_inside_board():
            return 0 <= position_old < len(self.board)

        def is_old_position_outside_board():
            return not is_old_position_inside_board()

        def get_normalized_number_of_tokens_on_position(position):
            return self.board[position] * token

        def is_correct_color_on_position(position):
            return get_normalized_number_of_tokens_on_position(position) > 0

        def is_new_position_inside_board():
            return 0 <= position_new < len(self.board)

        def is_new_position_outside_board():
            return not is_new_position_inside_board()

        def are_all_tokens_in_last_section():
            return max(self.board[:18]) > 0

        def is_single_opponent_token_on_new_position():
            return self.board[position_new] == -token

        def is_new_position_empty():
            return self.board[position_new] == 0

        def is_new_position_movable_to():
            return (is_correct_color_on_position(position_new) or
                    is_single_opponent_token_on_new_position() or
                    is_new_position_empty())

        position_new = position_old + width

        if is_old_position_outside_board():
            return False

        if not is_correct_color_on_position(position_old):
            return False

        if is_new_position_outside_board and not are_all_tokens_in_last_section:
            return False

        if not is_new_position_movable_to:
            return False

        self.board[position_old] -= token

        if is_new_position_inside_board():
            if is_single_opponent_token_on_new_position():
                self.board[position_new] = token
                self.beaten[-token] += 1
            else:  # is_correct_color_on_position(position_new) or is_new_position_empty()
                self.board[position_new] += token
        else:  # is_new_position_outside_board()
            self.finished[token] += 1

        return True
