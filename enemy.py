from random import randint, randrange

import sys
import pygame


class Enemy:
    filename = "img/enemy/first_enemy/enemy_move.png"

    def __init__(self, x=100, y=125, width=1550, height=650):
        self.image = pygame.image.load(Enemy.filename)
        self.rect = self.image.get_rect()
        # self.rect = pygame.Rect(x, y, 50, 50)
        # self.rect.x = randrange(50, width-100, 50)
        # self.rect.y = randrange(125, height-100, 50)
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        # self.shift_x = self.speed if randint(0, 1) == 1 else -1
        self.shift_x = 5
        self.shift_y = 0
        # self.shift_y = self.speed if randint(0, 1) == 1 else -1
        self.direction = None
        self.choose_direction()

        self.can_move_Right = True
        self.can_move_Left = True
        self.can_move_Up = True
        self.can_move_Down = True

    def choose_direction(self):
        i = randint(0, 3)
        if i == 0:
            self.direction = 'Left'
            self.can_move_Right = True
            self.can_move_Up = True
            self.can_move_Down = True
        if i == 1:
            self.direction = 'Up'
            self.can_move_Right = True
            self.can_move_Left = True
            self.can_move_Down = True
        if i == 2:
            self.direction = 'Right'
            self.can_move_Left = True
            self.can_move_Up = True
            self.can_move_Down = True
        if i == 3:
            self.direction = 'Down'
            self.can_move_Right = True
            self.can_move_Up = True
            self.can_move_Left = True

    def process_move(self):
        if self.direction == 'Right' and self.can_move_Right:
            self.rect.move_ip(self.speed, 0)
        if self.direction == 'Left' and self.can_move_Left:
            self.rect.move_ip(-self.speed, 0)
        if self.direction == 'Up' and self.can_move_Up:
            self.rect.move_ip(0, -self.speed)
        if self.direction == 'Down' and self.can_move_Down:
            self.rect.move_ip(0, self.speed)

    def process_logic(self):
        self.process_move()

    def process_draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    def process_collision(self, objects):
        for object in objects:
            if self.direction == 'Right' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                    Enemy(self.rect.x + self.speed, self.rect.y)):
                self.can_move_Right = False
                self.choose_direction()
                print("Right", end=' ')
            elif self.direction == 'Left' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                    Enemy(self.rect.x - self.speed, self.rect.y)):
                self.can_move_Left = False
                self.choose_direction()
                print("Left", end=' ')
            elif self.direction == 'Down' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                    Enemy(self.rect.x, self.rect.y + self.speed)):
                self.can_move_Down = False
                self.choose_direction()
                print("Down", end=' ')
            elif self.direction == 'Up' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                    Enemy(self.rect.x, self.rect.y - self.speed)):
                self.can_move_Up = False
                self.choose_direction()
                print("Up", end=' ')


class FirstLevelEnemy(Enemy):
    def __init__(self, x=100, y=125, width=1550, height=650):
        super().__init__(x, y, width, height)
