import pygame

from src.cell import Cell


class Block(Cell):
    image = pygame.image.load("img/blocker.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Block"
