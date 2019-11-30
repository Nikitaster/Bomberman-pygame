import pygame
import time

from src.blocks.cell import Cell


class Bomberman(Cell):
    animation_gap = 2
    animation_bomberman_down_s = ['././img/bomberman/stand/Front.png',
                                  '././img/bomberman/stand/Front1.png']
    animation_bomberman_down_a = ['././img/bomberman/run/Runs_down.png',
                                  '././img/bomberman/run/Runs_down1.png']
    animation_bomberman_up_s = ['././img/bomberman/stand/Back.png']
    animation_bomberman_up_a = ['././img/bomberman/run/Running_back.png',
                                '././img/bomberman/run/Running_back1.png']
    animation_bomberman_left_s = ['././img/bomberman/stand/Side_stands.png']
    animation_bomberman_left_a = ['././img/bomberman/run/Runs_left.png',
                                  '././img/bomberman/run/Runs_left1.png']
    animation_bomberman_right_s = ['././img/bomberman/stand/Side_stoin1.png']
    animation_bomberman_right_a = ['././img/bomberman/run/Runs_right.png',
                                   '././img/bomberman/run/Runs_right1.png']
    image = pygame.image.load(animation_bomberman_down_s[0])

    def __init__(self, x=50, y=125):
        super().__init__(x, y)
        self.shift_x_left = 0
        self.shift_x_right = 0
        self.shift_y_up = 0
        self.shift_y_down = 0
        self.shift_x = 0
        self.shift_y = 0
        self.speed = 5
        self.can_move_Right = True
        self.can_move_Left = True
        self.can_move_Up = True
        self.can_move_Down = True
        # for bonus:
        self.max_count_bombs = 1
        self.long_fire = 2
        # for animation
        self.start_anim_time = None
        self.num_sprite = 0
        self.last_moving_down = True

    def prepare_for_anim(self):
        if self.start_anim_time is None:
            self.start_anim_time = time.time()
            self.num_sprite = 0
        elif self.start_anim_time is not None:
            if time.time() - self.start_anim_time > 0.3:
                self.start_anim_time = time.time()
                self.num_sprite = (self.num_sprite + 1) % 2

    def animation_right(self, flag):
        if flag:
            self.last_moving_down = False
            self.prepare_for_anim()
            self.image = pygame.image.load(self.animation_bomberman_right_a[self.num_sprite])
        else:
            self.image = pygame.image.load(self.animation_bomberman_right_s[0])
            self.start_anim_time = None
            self.num_sprite = 0

    def animation_left(self, flag):
        if flag:
            self.last_moving_down = False
            self.prepare_for_anim()
            self.image = pygame.image.load(self.animation_bomberman_left_a[self.num_sprite])
        else:
            self.image = pygame.image.load(self.animation_bomberman_left_s[0])
            self.start_anim_time = None
            self.num_sprite = 0

    def animation_up(self, flag):
        if flag:
            self.last_moving_down = False
            self.prepare_for_anim()
            self.image = pygame.image.load(self.animation_bomberman_up_a[self.num_sprite])
        else:
            self.image = pygame.image.load(self.animation_bomberman_up_s[0])
            self.start_anim_time = None
            self.num_sprite = 0

    def animation_down(self, flag):
        if flag:
            self.last_moving_down = False
            self.prepare_for_anim()
            self.image = pygame.image.load(self.animation_bomberman_down_a[self.num_sprite])
        else:
            self.image = pygame.image.load(self.animation_bomberman_down_s[0])
            self.start_anim_time = None
            self.num_sprite = 0
            self.last_moving_down = True

    def dancing(self):
        self.prepare_for_anim()
        self.image = pygame.image.load(self.animation_bomberman_down_s[self.num_sprite])

    def process_draw(self, screen, camera, x=0, y=75):
        screen.blit(self.image, camera.apply(self))

    def process_logic(self):
        if self.last_moving_down:
            self.dancing()

    def stop(self):
        self.shift_x = 0
        self.shift_y = 0
        self.can_move_Up = False
        self.can_move_Left = False
        self.can_move_Right = False
        self.can_move_Down = False
        self.last_moving_down = True

    def move(self):
        if self.shift_x > 0 and self.can_move_Right:
            self.rect.move_ip(self.shift_x, 0)
            self.animation_right(True)
        if self.shift_x < 0 and self.can_move_Left:
            self.rect.move_ip(self.shift_x, 0)
            self.animation_left(True)
        if self.shift_y > 0 and self.can_move_Down:
            self.rect.move_ip(0, self.shift_y)
            self.animation_down(True)
        if self.shift_y < 0 and self.can_move_Up:
            self.rect.move_ip(0, self.shift_y)
            self.animation_up(True)
