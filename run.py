import sys

from src.main.loop import loop
from src.screens.fail import Fail
from src.main.game import Game


def main():
    game = Game(800, 725)
    fail = Fail(game.player)
    loop(game, fail)
    sys.exit()


if __name__ == '__main__':
    main()
