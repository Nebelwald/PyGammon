#!/usr/bin/env python3
import logging
from argparse import ArgumentParser
import datetime
from os import mkdir
from os.path import abspath, basename, exists

from src.game import Game

LOG_DIR_PATH = abspath(__file__).replace(basename(__file__), "logs")
LOG_FILE_PATH = f'logs/py_gammon_{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log'


def main():
    parser = ArgumentParser(prog='py_gammon.py',
                            description='Python implementation of Backgammon to create and test AI models.',
                            epilog='\'Interactive\' mode will pause the game after each move of an AI to follow its '
                                   'strategy.')
    parser.add_argument('-w', '--white', default='human', choices=('human', 'ai'), required=True)
    parser.add_argument('-b', '--black', default='ai', choices=('human', 'ai'), required=True)
    parser.add_argument('-i', '--interactive', action='store_true', default=False)
    args = parser.parse_args()

    if not exists(LOG_DIR_PATH):
        mkdir(LOG_DIR_PATH)

    logging.basicConfig(format="", encoding='utf-8', level=logging.INFO,
                        handlers=[logging.FileHandler(LOG_FILE_PATH),
                                  logging.StreamHandler()])

    logging.info(f'Called with parameters: --white {args.white} --black {args.black} --interactive {args.interactive}')

    Game(args.white, args.black, args.interactive).start_game()


if __name__ == "__main__":
    main()
