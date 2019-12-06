import pygame

from src.bonus.bonus import Bonus


class BonusCalled(Bonus):
    def __init__(self, x=0, y=75, type='Bonus'):
        super().__init__(x, y, type)
        self.image = pygame.image.load('././img/bonus/' + type + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def process_draw(self, screen, camera, x=0, y=75):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, camera.apply(self))
