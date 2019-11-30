from random import randint, randrange, choice

import sys
import pygame


class Enemy:
    filename = "img/enemy/first_enemy/enemy_move.png"
    image = pygame.image.load(filename)
    type = 'Enemy'

    def __init__(self, x=100, y=125):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.shift_x = 5
        self.shift_y = 0
        self.direction = None
        self.can_move_Right = True
        self.can_move_Left = True
        self.can_move_Up = True
        self.can_move_Down = True
        self.choose_direction(['Up', 'Left', 'Right', 'Down'])

    def choose_direction(self, data_can_move):
        self.direction = choice(data_can_move)

    def process_move(self):
        if not self.can_move_Up and not self.can_move_Right and not self.can_move_Left and not self.can_move_Down:
            return
        if self.direction == 'Right' and self.can_move_Right:
            self.rect.move_ip(self.speed, 0)
        if self.direction == 'Left' and self.can_move_Left:
            self.rect.move_ip(-self.speed, 0)
        if self.direction == 'Up' and self.can_move_Up:
            self.rect.move_ip(0, -self.speed)
        if self.direction == 'Down' and self.can_move_Down:
            self.rect.move_ip(0, self.speed)

        self.can_move_Right = True
        self.can_move_Left = True
        self.can_move_Up = True
        self.can_move_Down = True

    def unexpected_move(self):
        pass

    def process_logic(self):
        self.process_move()

    def process_draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    def process_collision(self, objects):
        for object in objects:
            if self.direction == 'Right' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                    Enemy(self.rect.x + self.speed, self.rect.y)):
                self.can_move_Right = False
                self.choose_direction(['Left', 'Up', 'Down'])
                print("Right", end=' ')
            elif self.direction == 'Left' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                    Enemy(self.rect.x - self.speed, self.rect.y)):
                self.can_move_Left = False
                self.choose_direction(['Right', 'Up', 'Down'])
                print("Left", end=' ')
            elif self.direction == 'Down' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                    Enemy(self.rect.x, self.rect.y + self.speed)):
                self.can_move_Down = False
                self.choose_direction(['Left', 'Up', 'Right'])
                print("Down", end=' ')
            elif self.direction == 'Up' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                    Enemy(self.rect.x, self.rect.y - self.speed)):
                self.can_move_Up = False
                self.choose_direction(['Left', 'Right', 'Down'])
                print("Up", end=' ')



class FirstLevelEnemy(Enemy):
    def __init__(self, x=100, y=125):
        super().__init__(x, y)
