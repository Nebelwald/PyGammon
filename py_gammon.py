#!/usr/bin/env python3
from argparse import ArgumentParser

from src.game import Game


def main():
    parser = ArgumentParser(prog='py_gammon.py',
                            description='Python implementation of Backgammon to create and test AI models.')
    parser.add_argument('-w', '--white', default='human', choices=('human', 'ai'), required=True)
    parser.add_argument('-b', '--black', default='ai', choices=('human', 'ai'), required=True)
    parser.add_argument('-i', '--interactive', action='store_true', default=False)
    args = parser.parse_args()

    Game(args.white, args.black, args.interactive).start_game()


if __name__ == "__main__":
    main()
