import sys
import pygame

from src.area import Area
from src.camera import Camera, camera_func
from src.cell import Cell


class Bomberman(Cell):
    image = pygame.image.load("img/bomberman.png")

    def __init__(self, x=50, y=125):
        super().__init__(x, y)
        self.shift_x = 0
        self.shift_y = 0
        self.speed = 5
        self.can_move_Right = True
        self.can_move_Left = True
        self.can_move_Up = True
        self.can_move_Down = True

    def process_draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self, 5))

    def process_logic(self, width, height, area):
        if self.rect.x + self.shift_x < 50:
            self.shift_x = 0
        if self.rect.y + self.shift_y < 125:
            self.shift_y = 0
        if self.rect.y + self.shift_y > height - 25:
            self.shift_y = 0
        if self.rect.left < 50:
            self.rect.left = 50
        if self.rect.top < 125:
            self.rect.top = 125
        if self.rect.left < 50:
            self.rect.right = 50

    def move(self):
        if self.shift_x > 0 and self.can_move_Right:
            self.rect.move_ip(self.shift_x, 0)
        if self.shift_x < 0 and self.can_move_Left:
            self.rect.move_ip(self.shift_x, 0)
        if self.shift_y > 0 and self.can_move_Down:
            self.rect.move_ip(0, self.shift_y)
        if self.shift_y < 0 and self.can_move_Up:
            self.rect.move_ip(0, self.shift_y)


class Game:
    def __init__(self, width=800, height=625):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.game_over = False
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        self.create_objects()

    def create_objects(self):
        self.area = Area()
        self.bomberman = Bomberman()
        self.camera = Camera(camera_func, self.area.width, self.area.height)

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

    def main_loop(self):
        while not self.game_over:
            self.process_event()
            self.screen.fill((75, 100, 150))
            self.camera.update(self.bomberman)
            self.area.process_draw(self.screen, self.camera, self.bomberman.speed)
            self.bomberman.process_logic(self.area.width, self.area.height, self.area)
            self.process_collisions()
            self.process_move()
            self.bomberman.process_draw(self.screen, self.camera)
            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()