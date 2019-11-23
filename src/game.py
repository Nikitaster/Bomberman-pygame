import sys
import pygame

from src.area import Area
from src.bomberman import Bomberman
from src.camera import Camera, camera_func


class Game:
    def __init__(self, width=800, height=625):
        self.area = Area()
        self.bomberman = Bomberman()
        self.camera = Camera(camera_func, self.area.width, self.area.height)
        self.width = width
        self.height = height
        self.size = (width, height)
        self.game_over = False
        self.screen = pygame.display.set_mode(self.size)
        self.is_pressed_up = False
        self.is_pressed_left = False
        self.is_pressed_down = False
        self.is_pressed_right = False
        pygame.init()

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == 97 or event.key == 276 or event.key == 160:
                    self.is_pressed_left = True
                    self.bomberman.shift_xl = -self.bomberman.speed
                elif event.key == 100 or event.key == 275 or event.key == 162:
                    self.is_pressed_right = True
                    self.bomberman.shift_xr = self.bomberman.speed
                elif event.key == 115 or event.key == 274 or event.key == 161:
                    self.is_pressed_down = True
                    self.bomberman.shift_yd = self.bomberman.speed
                elif event.key == 119 or event.key == 273 or event.key == 172:
                    self.is_pressed_up = True
                    self.bomberman.shift_yu = -self.bomberman.speed
                self.bomberman.shift_x = self.bomberman.shift_xl + self.bomberman.shift_xr
                self.bomberman.shift_y = self.bomberman.shift_yu + self.bomberman.shift_yd
            if event.type == pygame.KEYUP:
                if event.key == 97 or event.key == 276 or event.key == 160:
                    self.is_pressed_left = False
                    self.bomberman.shift_xl = 0
                elif event.key == 100 or event.key == 275 or event.key == 162:
                    self.is_pressed_right = False
                    self.bomberman.shift_xr = 0
                elif event.key == 115 or event.key == 274 or event.key == 161:
                    self.is_pressed_down = False
                    self.bomberman.shift_yd = 0
                elif event.key == 119 or event.key == 273 or event.key == 172:
                    self.is_pressed_up = False
                    self.bomberman.shift_yu = 0
                self.bomberman.shift_x = self.bomberman.shift_xl + self.bomberman.shift_xr
                self.bomberman.shift_y = self.bomberman.shift_yu + self.bomberman.shift_yd



    def process_collisions(self):
        self.bomberman.can_move_Right = True
        self.bomberman.can_move_Left = True
        self.bomberman.can_move_Up = True
        self.bomberman.can_move_Down = True
        # Collisions
        for objects in self.area.objects:
            if objects.type != 'Grass':
                if objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x + self.bomberman.speed, self.bomberman.rect.y)):
                    self.bomberman.can_move_Right = False
                elif objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x - self.bomberman.speed, self.bomberman.rect.y)):
                    self.bomberman.can_move_Left = False
                elif objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x, self.bomberman.rect.y + self.bomberman.speed)):
                    self.bomberman.can_move_Down = False
                elif objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x, self.bomberman.rect.y - self.bomberman.speed)):
                    self.bomberman.can_move_Up = False

    def process_move(self):
        self.bomberman.move()

    def process_draw(self):

        self.screen.fill((75, 100, 150))
        self.camera.update(self.bomberman)
        self.area.process_draw(self.screen, self.camera)

    def main_loop(self):
        while not self.game_over:
            self.process_event()
            self.process_collisions()
            self.process_move()
            self.process_draw()
            self.bomberman.process_draw(self.screen, self.camera)
            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()
