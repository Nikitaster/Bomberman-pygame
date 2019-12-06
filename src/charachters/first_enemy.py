import pygame

from src.charachters.enemy import Enemy


class FirstLevelEnemy(Enemy):
    image = pygame.image.load("img/enemy/first_enemy/enemy_move.png")
    animation_enemy = ['./img/enemy/first_enemy/enemy_start.png',
                       './img/enemy/first_enemy/enemy_stand.png',
                       './img/enemy/first_enemy/enemy_move.png']

    def __init__(self, x=100, y=125):
        super().__init__(x, y)
        self.speed = 4
