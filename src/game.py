import logging
from random import randint

from src.gameboard import GameBoard, BLACK, WHITE
from src.players import AI_AlwaysMoveLastPossibleToken, HumanPlayer

PAUSE = False


class Game:
    def __init__(self, white_player: str, black_player: str, interactive: bool):
        def create_player(name_string, color):
            match name_string:
                case 'human':
                    logging.info(f'Player {color} will be a human.')
                    return HumanPlayer(color)
                case 'ai':
                    logging.info(f'Player {color} will be an AI.')
                    return AI_AlwaysMoveLastPossibleToken(color)

        self.game_board = GameBoard(self)

        self.players = [
            create_player(white_player, WHITE),
            create_player(black_player, BLACK)
        ]

        self.interactive = interactive

    def start_game(self):
        def roll_dices() -> list:
            possible_moves = [randint(1, 6), randint(1, 6)]
            possible_moves = sorted(possible_moves * 2
                                    if possible_moves[0] == possible_moves[1]
                                    else possible_moves)
            logging.info(f"Possible moves: {possible_moves}")
            return possible_moves

        logging.info("\nInitial game board:")
        logging.info(str(self.game_board))
        logging.info("")

        game_round = 1

        while True:
            for player in self.players:
                logging.info(f"\nRound {game_round}, player {player.color}'s turn ({type(player)})")

                moves_player = roll_dices()
                player.make_move(self.game_board, moves_player)

                if not type(player) is HumanPlayer and self.interactive:
                    input("(ai made it's turn. [Enter] to continue)")

            game_round += 1

    def finish(self, color) -> None:
        logging.info(f"\nPlayer {color} has won!")
        exit()
