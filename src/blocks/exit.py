import time
import pygame

from src.blocks.cell import Cell


class Exit(Cell):
    image = pygame.image.load("img/blocks/exit.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Exit"
        self.status = 'Hidden'
        self.time_of_open = None

    def set_open_status(self):
        if self.status == 'Hidden':
            self.time_of_open = time.time()

    def process_logic(self):
        if time.time() - self.time_of_open > 3 and self.status == 'Hidden' and self.time_of_open is not None:
            self.status = 'Open'
