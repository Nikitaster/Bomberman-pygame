import pygame

from src.bomb.fire import Fire


class FireHorizontal(Fire):
    image = pygame.image.load('./img/bomb/Bomb_horiz.png')

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
