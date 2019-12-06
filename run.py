import sys


from src.main.loop import loop
from src.screens.fail import Fail
from src.main.game import Game
from src.screens.menu import Menu


def main():
    menu = Menu()
    if menu.main_menu():
        game = Game(800, 725)
        fail = Fail(game.player)
        loop(game, fail)
    sys.exit()


if __name__ == '__main__':
    main()
