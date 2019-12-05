import time

import pygame

from src.blocks.cell import Cell


class Bonus(Cell):
    image = None  # в дочерних: image = pygame.image.load("PATH")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Bonus"  # для каждого бонуса моенять type
        self.status = 'Hidden'  # Open, Taken

    def process_logic(self):
        # тут должна происходить логика бомбы в зависимости от ее текущего статуса
        # с последующей сменой этого статуса на следущий.
        pass


class BombBonus(Bonus):
    image = pygame.image.load('././img/bonus/bonus2.png')
    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = 'BombBonus'
        self.status = 'Hidden'

    def set_open_status(self):
        if self.status == 'Hidden':
            self.time_of_open = time.time()

    def process_logic(self):
        if time.time() - self.time_of_open > 3 and self.status == 'Hidden' and self.time_of_open is not None:
            self.status = 'Open'