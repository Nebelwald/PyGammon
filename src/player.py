import re

from ai import PlayerInterface


class HumanPlayer(PlayerInterface):
    def make_move(self, gameboard, possible_moves):
        while True:
            if not possible_moves:
                break

            user_input = input("pos,width=")

            match = re.search("^[1-2]?[0-9],[0-9]$", user_input)
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
