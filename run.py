import sys

from fail import Fail
from src.main.game import Game


def loop(game, fail):
    fail.fail_loop()
    if game.player.lost is True:
        return
    game.main_loop()
    loop(game, fail)


def main():
    game = Game(800, 725)
    fail = Fail(game.player)
    loop(game, fail)
    sys.exit()


if __name__ == '__main__':
    main()
