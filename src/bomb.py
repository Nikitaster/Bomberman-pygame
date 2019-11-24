import pygame
import pyganim
from src.cell import Cell

black = 0, 0, 0

animation_delay = 1000  # скорость смены кадров
animation_bomb = ['img/Bomb1.png',
                  'img/Bomb2.png',
                  'img/Bomb3.png',
                  'img/Bomb4.png',
                  'img/grass.jpg']


class Bomb(Cell):
    image = pygame.image.load("img/Bomb1.png")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = 'Bomb'
        self.alive = 0  # Количество кадров, которое бомба существует
        self.bomb_x_in_area = 0
        self.bomb_y_in_area = 0
        self.is_bomb = False
        self.boltAnim = []
        for anim in animation_bomb:
            self.boltAnim.append((anim, animation_delay))
        self.boltAnimBomb = pyganim.PygAnimation(self.boltAnim)
        self.boltAnimBomb.play()

    def process_draw(self, screen, camera, x=0, y=75):
        self.rect.x = x
        self.rect.y = y
        self.boltAnimBomb.blit(self.image)
        screen.blit(self.image, self.rect)

    def try_blow(self):  # Попытка взрыва по счетчику кадров
        if self.alive < 60:
            self.alive += 1
            return False  # Вернуть False, если счетчик времени не достиг значения взрыва
        else:
            return True  # Вернуть True, как только счетчик времени достиг значения взрыва
