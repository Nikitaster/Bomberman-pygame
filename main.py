import sys
import pygame
from random import randint

from pygame.rect import Rect


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def apply(self, target):
        # return target.rect.move(self.state.topleft)
          return target.rect.move((self.state.x, self.state.y))


def camera_func(camera, target_rect):
    l = -target_rect.x + 800 / 2
    t = -target_rect.y + 650 / 2
    # w, h = camera.width, camera.height
    w, h = 800, 650
    l = min(0, l)
    l = max(-(800 - 800 / 2), l)
    t = max(-(650 - 650 / 2), t)
    t - min(0, t)
    return Rect(l, t, w, h)


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
    image = pygame.image.load("blocker.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)


class Grass(Cell):
    image = pygame.image.load("grass.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)


class Brick(Cell):
    image = pygame.image.load("brick.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)


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
        self.block = Block()
        self.grass = Grass()
        self.brick = Brick()
        self.create_area()

    def create_area(self):
        h = self.height // 50
        w = self.width // 50
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
        count = 0
        n = randint(50, 75)
        for i in range(h):
            for j in range(w):
                if i % 2 == 1 and j % 2 == 1 and i != 1 and i != 2 and j != 1 and j != 2 and count <= n:
                    if randint(0, 1):
                        self.area_data[i][j] = 2
                        count += 1

        for i in range(h):
            print(self.area_data[i])

    # def process_draw(self, screen, speed):
    #     for w in range(self.width // 50):
    #         for h in range(self.height // 50):
    #             if self.area_data[h][w] == 0:
    #                 self.block.process_draw(screen, w * 50 + self.shift_area * speed / 2, h * 50 + 75)
    #             elif self.area_data[h][w] == 1:
    #                 self.grass.process_draw(screen, w * 50 + self.shift_area * speed / 2, h * 50 + 75)
    #             elif self.area_data[h][w] == 2:
    #                 self.brick.process_draw(screen, w * 50 + self.shift_area * speed / 2, h * 50 + 75)


class Bomberman(Cell):
    image = pygame.image.load("bomberman.png")

    def __init__(self, x=50, y=125):
        super().__init__(x, y)
        self.shift_x = 0
        self.shift_y = 0
        self.speed = 5

    def process_draw(self, screen, camera):
        screen.blit(self.image, self.rect)

    def process_logic(self, width, height, area):
        if self.rect.x + self.shift_x < 50:
            self.shift_x = 0

        if self.rect.y + self.shift_y < 125:
            self.shift_y = 0
        if self.rect.y + self.shift_y > height - 25:
            self.shift_y = 0

        print(self.rect.x + self.speed, end=' ')
        print(self.rect.y)

        if self.rect.left < 50:
            self.rect.left = 50
        if self.rect.top < 125:
            self.rect.top = 125

    # def move(self):
    #     if self.rect.x <= 800 / 2:
    #         self.rect.x += self.shift_x
    #     else:
    #         self.rect.x += self.shift_x / 2
    #     self.rect.y += self.shift_y

    def move(self):
        self.rect.x += self.shift_x
        self.rect.y += self.shift_y

    def get_shift_area(self, screen_width, area_width):
        if self.rect.x > screen_width / 2:
            return screen_width / 2 - self.rect.x
        return 0


class Game:
    def __init__(self, width=800, height=625):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.game_over = False
        self.down_left = False
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        self.create_objects()

    def create_objects(self):
        self.area = Area()
        self.bomberman = Bomberman()
        self.camera = Camera(camera_func, 1550, 650)
        self.objects = []

        for i in range(13):
            for j in range(31):
                if self.area.area_data[i][j] == 0:
                    self.objects.append(Block(j * 50, i * 50 - 125))
                elif self.area.area_data[i][j] == 1:
                    self.objects.append(Grass(j * 50, i * 50 - 125))
                elif self.area.area_data[i][j] == 2:
                    self.objects.append(Brick(j * 50, i * 50 - 125))

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == 97 or event.key == 276:
                    self.bomberman.shift_x = -self.bomberman.speed
                    self.area.shift_x = -self.bomberman.speed
                elif event.key == 100 or event.key == 275:
                    self.bomberman.shift_x = self.bomberman.speed
                    self.area.shift_x = self.bomberman.speed
                elif event.key == 115 or event.key == 274:
                    self.bomberman.shift_y = self.bomberman.speed
                elif event.key == 119 or event.key == 273:
                    self.bomberman.shift_y = -self.bomberman.speed
                print(event.key)
            if event.type == pygame.KEYUP:
                self.bomberman.shift_x = 0
                self.bomberman.shift_y = 0
                self.area.shift_x = 0

    def process_move(self):
        self.bomberman.move()

    def main_loop(self):
        while not self.game_over:
            self.process_event()
            self.screen.fill((75, 100, 150))

            # self.area.shift_area = self.bomberman.get_shift_area(self.width, self.area.width)
            # print(self.area.shift_area)
            # self.area.process_draw(self.screen, self.bomberman.speed)

            self.camera.update(self.bomberman)
            for i in self.objects:
                self.screen.blit(i.image, self.camera.apply(i))

            self.bomberman.process_logic(self.area.width, self.area.height, self.area)
            self.process_move()
            self.bomberman.process_draw(self.screen, self.camera)

            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()


def main():
    game = Game(800, 725)
    game.main_loop()


if __name__ == '__main__':
    main()
