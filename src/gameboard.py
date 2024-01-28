class GameBoard:
    def __init__(self):
        self.board = [
            2, 0, 0, 0, 0, -5,
            0, -3, 0, 0, 0, 5,
            -5, 0, 0, 0, 3, 0,
            5, 0, 0, 0, 0, -2
        ]

        self.beaten_white = 0
        self.beaten_black = 0

        self.finished_white = 0
        self.finished_black = 0

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
        line += f"║"
        line += f" {str(self.finished_black).rjust(1)}B"

        line += "\n"

        line += (
                "╠" +
                (f" {self.beaten_white}W ".center(17, "═")) +
                "╬" +
                (f" {self.beaten_black}B ".center(17, "═")) +
                "╣")

        line += "\n"

        line += "║"
        lower_left = self.board[12:18]
        line += (draw_quarter(lower_left))
        line += "║"
        lower_right = self.board[18:]
        line += (draw_quarter(lower_right))
        line += f"║"
        line += f" {str(self.finished_white).rjust(1)}W"

        line += "\n"

        line += ("╚" +
                 (">".join([f"{i}" for i in range(13, 19)])) +
                 "╩" +
                 (">".join([f"{i}" for i in range(19, 25)])) +
                 "╝")

        return line

    def make_move(self, position, width):
        def are_all_white_tokens_in_last_section():
            return max(self.board[6:]) > 0

        # there are no of the players tokens on the field
        if not self.board[position] > 0:
            return False

        # move would move token outside of board but player cannot clear the field yet
        if position - 1 + width >= len(self.board) and not are_all_white_tokens_in_last_section():
            return False

        # on the field to move, there are already tokens of the other player
        if self.board[position + width] < 0:
            return False

        self.board[position] -= 1
        self.board[position + width] += 1
        return True
