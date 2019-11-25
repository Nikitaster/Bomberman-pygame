import pygame

from src.bomb.fire import Fire


class FireDown(Fire):
    image = pygame.image.load('img/bomb/blow_under_bomb.png')

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
