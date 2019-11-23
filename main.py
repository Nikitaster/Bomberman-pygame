import sys
import pygame
from random import randint
from src.camera import Camera, camera_func


class Cell:
    image = None

    def __init__(self, x=0, y=75):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def process_draw(self, screen, x=0, y=75):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)


class Block(Cell):
    image = pygame.image.load("img/blocker.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Block"


class Grass(Cell):
    image = pygame.image.load("img/grass.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Grass"


class Brick(Cell):
    image = pygame.image.load("img/brick.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Brick"


class Area:
    def __init__(self, width=1550, height=650, size_block=50):
        self.area_data = []
        self.width = width
        self.height = height
        self.size_block = size_block
        self.shift_area = 0
        self.rgb = [
            (150, 0, 0),
            (0, 150, 0),
            (0, 0, 150)
        ]
        self.area_data = []
        self.objects = []
        self.create_area()

    def create_area(self):
        h = self.height // 50
        w = self.width // 50
        # Fill list with grass
        for i in range(h):
            self.area_data.append([])
        for i in range(h):
            for j in range(w):
                self.area_data[i].append(1)
        for i in range(h):
            self.area_data[i][0] = 0
            self.area_data[i][30] = 0
        for i in range(w):
            self.area_data[0][i] = 0
            self.area_data[12][i] = 0
        for i in range(2, 12, 2):
            for j in range(2, 30, 2):
                self.area_data[i][j] = 0
        # Fill list with bricks
        for i in range(randint(50, 75)):
            x = randint(1, 29)
            y = randint(1, 11)
            while self.area_data[y][x] == 0 or self.area_data[y][x] == 2:
                x = randint(1, 29)
                y = randint(1, 11)
            self.area_data[y][x] = 2
        self.area_data[1][1] = 1
        self.area_data[1][2] = 1
        self.area_data[2][1] = 1

        for i in range(h):
            print(self.area_data[i])
        # Fill area with all blocks
        for i in range(13):
            for j in range(31):
                if self.area_data[i][j] == 0:
                    self.objects.append(Block(j * 50, i * 50 + 75))
                elif self.area_data[i][j] == 1:
                    self.objects.append(Grass(j * 50, i * 50 + 75))
                elif self.area_data[i][j] == 2:
                    self.objects.append(Brick(j * 50, i * 50 + 75))

    def process_draw(self, screen, camera, speed):
        for i in self.objects:
            screen.blit(i.image, camera.apply(i, speed))


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