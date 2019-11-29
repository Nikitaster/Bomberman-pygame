from random import randint, randrange

import sys
import pygame

class Enemy:
    filename = "/home/prom/bomberman/img/enemy/first_enemy/enemy_move.png"
    def __init__(self, width=1550, height=650):
        self.image = pygame.image.load(Enemy.filename)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(50, width-100, 50)
        self.rect.y = randrange(100, height-100, 50)

    def process_event(self):
        pass

    def process_logic(self):
        pass

    def process_draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))


class FirstLevelEnemy(Enemy):
    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.rect.x = randint(10, self.window_width - self.rect.width-10)
        self.rect.x = randint(10, self.window_height - self.rect.height-10)
        self.shift_x = 1 if randint(0, 1) == 1 else -1
        self.shift_y = 1 if randint(0, 1) == 1 else -1

    def process_logic(self):
        self.rect.x += self.shift_x
        self.rect.y += self.shift_y
        if self.rect.left <= 0 or self.rect.right >= self.window_width:
            self.shift_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= self.window_height:
            self.shift_y *= -1






