import pygame

from src.cell import Cell


class Brick(Cell):
    image = pygame.image.load("img/blocks/brick.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Brick"
