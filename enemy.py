import time
from random import randint, randrange, choice

import sys
import pygame


class Enemy:

    animation_enemy = ['./img/enemy/first_enemy/enemy_start.png',
                       './img/enemy/first_enemy/enemy_stand.png',
                       './img/enemy/first_enemy/enemy_move.png']

    image = pygame.image.load(animation_enemy[0])
    type = 'Enemy'

    def __init__(self, x=100, y=125):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0
        self.direction = None
        self.can_move_Right = True
        self.can_move_Left = True
        self.can_move_Up = True
        self.can_move_Down = True
        self.directions = ['Up', 'Left', 'Right', 'Down']
        self.choose_direction(self.directions)
        # for animation
        self.start_anim_time = None
        self.num_sprite = 0

    def choose_direction(self, data_can_move):
        data = []
        if self.can_move_Left:
            data.append('Left')
        if self.can_move_Right:
            data.append('Right')
        if self.can_move_Up:
            data.append('Up')
        if self.can_move_Down:
            data.append('Down')

        if len(data) == 0:
            data = ['Right', 'Left', 'Up', 'Down']
            self.can_move_Right = True
            self.can_move_Left = True
            self.can_move_Up = True
            self.can_move_Down = True

        self.direction = choice(data)

    def prepare_for_anim(self):
        if self.start_anim_time is None:
            self.start_anim_time = time.time()
            self.num_sprite = 0
        elif self.start_anim_time is not None:
            if time.time() - self.start_anim_time > 0.3:
                self.start_anim_time = time.time()
                self.num_sprite = (self.num_sprite + 1) % 2

    def dancing(self):
        self.prepare_for_anim()
        self.image = pygame.image.load(self.animation_enemy[self.num_sprite])

    def process_move(self):
        if not self.can_move_Up and not self.can_move_Right and not self.can_move_Left and not self.can_move_Down:
            return
        if self.direction == 'Right':
            self.rect.move_ip(self.speed, 0)
        if self.direction == 'Left':
            self.rect.move_ip(-self.speed, 0)
        if self.direction == 'Up':
            self.rect.move_ip(0, -self.speed)
        if self.direction == 'Down':
            self.rect.move_ip(0, self.speed)

    def unexpected_move(self):
        pass

    def process_logic(self, objects):
        while self.process_collision(objects):
            self.choose_direction(['Up', 'Left', 'Right', 'Down'])
        self.process_move()
        self.dancing()

    def process_draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    def detect_collision_right(self, object):
        if self.direction == 'Right' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                Enemy(self.rect.x + self.speed, self.rect.y)):
            return True
        return False

    def detect_collision_left(self, object):
        if self.direction == 'Left' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                Enemy(self.rect.x - self.speed, self.rect.y)):
            return True
        return False

    def detect_collision_down(self, object):
        if self.direction == 'Down' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                Enemy(self.rect.x, self.rect.y + self.speed)):
            return True
        return False

    def detect_collision_up(self, object):
        if self.direction == 'Up' and object.type != 'Grass' and object.type != 'Fire' and object.rect.colliderect(
                Enemy(self.rect.x, self.rect.y - self.speed)):
            return True
        return False

    def process_collision(self, objects):
        for object in objects:
            if self.detect_collision_down(object):
                self.can_move_Down = False
                return True
            if self.detect_collision_up(object):
                self.can_move_Up = False
                return True
            if self.detect_collision_right(object):
                self.can_move_Right = False
                return True
            if self.detect_collision_left(object):
                self.can_move_Left = False
                return True
        return False


class FirstLevelEnemy(Enemy):
    image = pygame.image.load("img/enemy/first_enemy/enemy_move.png")

    def __init__(self, x=100, y=125):
        super().__init__(x, y)
        self.speed = 4


class SecondLevelEnemy(Enemy):
    image = pygame.image.load("img/enemy/second_enemy/enemy_move.png")

    def __init__(self, x=100, y=125):
        super().__init__(x, y)
        self.speed = 6
