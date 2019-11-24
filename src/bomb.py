import pygame
import pyganim
import time
from src.cell import Cell


class Bomb(Cell):
    animation_delay = 1000  # скорость смены кадров
    animation_bomb = ['img/Bomb1.png',
                      'img/Bomb2.png',
                      'img/Bomb3.png']
    image = pygame.image.load(animation_bomb[0])

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = 'Bomb'
        self.start_time = time.time()
        self.end_time = self.start_time + len(self.animation_bomb) * 2
        self.is_bomb = False
        self.boltAnim = []
        for anim in self.animation_bomb:
            self.boltAnim.append((anim, self.animation_delay))
        self.boltAnimBomb = pyganim.PygAnimation(self.boltAnim)
        self.boltAnimBomb.play()

    def process_draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
        self.boltAnimBomb.blit(self.image)

    def try_blow(self):  # Попытка взрыва по счетчику кадров
        if (time.time() - self.start_time) <= self.end_time - time.time():
            return False  # Вернуть False, если счетчик времени не достиг значения взрыва
        else:
            self.boltAnimBomb.stop()
            return True  # Вернуть True, как только счетчик времени достиг значения взрыва


class Fire(Cell):
    image_left = pygame.image.load('img/Bomb4.png')
    image_right = pygame.image.load('img/Bomb3.png')
    image_up = pygame.image.load('img/Bomb4.png')
    image_down = pygame.image.load('img/Bomb4.png')
    image_middle = pygame.image.load('img/Bomb4.png')
    image_horizontal = pygame.image.load('img/Bomb4.png')
    image_vertical = pygame.image.load('img/Bomb4.png')

    image = image_middle

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.type = "Fire"
        self.start_time = time.time()
        self.end_time = time.time() + 2

    def process_draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    def try_blow(self):  # Попытка взрыва по счетчику кадров
        if (time.time() - self.start_time) <= self.end_time - time.time():
            return False  # Вернуть False, если счетчик времени не достиг значения взрыва
        else:
            return True  # Вернуть True, как только счетчик времени достиг значения взрыва


class FireMiddle(Fire):
    image = Fire.image_middle

    def __init__(self, x=0, y=0):
        super().__init__(x, y)


class FireLeft(Fire):
    image = Fire.image_left

    def __init__(self, x=0, y=0):
        super().__init__(x, y)


class FireRight(Fire):
    image = Fire.image_right

    def __init__(self, x=0, y=0):
        super().__init__(x, y)


class FireUp(Fire):
    image = Fire.image_up

    def __init__(self, x=0, y=0):
        super().__init__(x, y)


class FireDown(Fire):
    image = Fire.image_down

    def __init__(self, x=0, y=0):
        super().__init__(x, y)


class FireHorizontal(Fire):
    image = Fire.image_horizontal

    def __init__(self, x=0, y=0):
        super().__init__(x, y)


class FireVertical(Fire):
    image = Fire.image_vertical

    def __init__(self, x=0, y=0):
        super().__init__(x, y)