import time

import pygame



class Bonus:
    # image = None  # в дочерних: image = pygame.image.load("PATH")

    def __init__(self, x=0, y=75, type='Bonus'):
        self.type = type  # для каждого бонуса моенять type
        self.status = 'Hidden'  # Open, Taken
        self.time_of_open = None

    def set_open_status(self):
        if self.status == 'Hidden':
            self.time_of_open = time.time()

    def process_logic(self):
        if time.time() - self.time_of_open > 3 and self.status == 'Hidden' and self.time_of_open is not None:
            self.status = 'Open'


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



# class BombBonus(Bonus):
#     image = pygame.image.load('././img/bonus/bonus2.png')
#
#     def __init__(self, x=0, y=75):
#         super().__init__(x, y)
#         self.type = 'BombBonus'
#
#
# class FlamePassBonus(Bonus):
#     image = pygame.image.load('././img/bonus/bonus7.png')
#
#     def __init__(self, x=0, y=75):
#         super().__init__(x, y)
#         self.type = 'FlamePassBonus'
#
#
# class FlamesBonus(Bonus):
#     image = pygame.image.load('././img/bonus/bonus1.png')
#
#     def __init__(self, x=0, y=75):
#         super().__init__(x, y)
#         self.type = 'FlamesBonus'
