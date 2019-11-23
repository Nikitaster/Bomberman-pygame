import sys
import pygame

from src.area import Area, Bomb
from src.blocks.grass import Grass
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
        pygame.init()
        self.is_bomb = False

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == 97 or event.key == 276 or event.key == 160:
                    self.bomberman.shift_x = -self.bomberman.speed
                elif event.key == 100 or event.key == 275 or event.key == 162:
                    self.bomberman.shift_x = self.bomberman.speed
                elif event.key == 115 or event.key == 274 or event.key == 161:
                    self.bomberman.shift_y = self.bomberman.speed
                elif event.key == 119 or event.key == 273 or event.key == 172:
                    self.bomberman.shift_y = -self.bomberman.speed
                elif event.key == 101 and not(self.is_bomb):
                    #print("Bomberman: ", self.bomberman.rect.x, self.bomberman.rect.y)
                    self.bomb_x_in_area = int((self.bomberman.rect.x - (self.bomberman.rect.x % 50)) // 50)
                    self.bomb_y_in_area = int((self.bomberman.rect.y - 75 - ((self.bomberman.rect.y - 75) % 50)) // 50)
                    #print("Bomb: ", self.bomb_x_in_area, self.bomb_y_in_area)
                    self.area.area_data[self.bomb_x_in_area][self.bomb_y_in_area] = Bomb(self.bomb_x_in_area * 50, self.bomb_y_in_area * 50 + 75)
                    self.is_bomb = True

            if event.type == pygame.KEYUP:
                self.bomberman.shift_x = 0
                self.bomberman.shift_y = 0

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
        self.area.process_draw(self.screen, self.camera, self.bomberman.speed)
        if self.is_bomb:
            self.area.area_data[self.bomb_x_in_area][self.bomb_y_in_area].process_draw(self.screen, self.camera, int(self.bomb_x_in_area * 50), int(self.bomb_y_in_area * 50 + 75))

    def main_loop(self):
        while not self.game_over:
            self.process_event()
            self.process_collisions()
            self.process_move()
            self.process_draw()
            self.bomberman.process_draw(self.screen, self.camera)
            if self.is_bomb:
                if self.area.area_data[self.bomb_x_in_area][self.bomb_y_in_area].try_blow():
                    self.area.area_data[self.bomb_x_in_area][self.bomb_y_in_area] = Grass(self.bomb_x_in_area * 50, self.bomb_y_in_area * 50 + 75)
                    self.is_bomb = False
            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()
