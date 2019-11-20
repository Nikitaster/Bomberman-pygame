import sys
import pygame
from random import randint


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
        for i in range(13):
            self.area_data.append([])
        for i in range(13):
            for j in range(31):
                self.area_data[i].append(1)
        for i in range(13):
            self.area_data[i][0] = 0
            self.area_data[i][30] = 0
        for i in range(31):
            self.area_data[0][i] = 0
            self.area_data[12][i] = 0
        for i in range(2, 12, 2):
            for j in range(2, 30, 2):
                self.area_data[i][j] = 0
        count = 0
        n = randint(50, 75)
        for i in range(13):
            for j in range(31):
                if i % 2 == 1 and j % 2 == 1 and i != 1 and i != 2 and j != 1 and j != 2 and count <= n:
                    if randint(0, 1):
                        self.area_data[i][j] = 2
                        count += 1

        for i in range(13):
            print(self.area_data[i])

    def process_draw(self, screen):
        for w in range(31):
            for h in range(13):
                if self.area_data[h][w] == 0:
                    self.block.process_draw(screen, w * 50, h * 50 + 75)
                elif self.area_data[h][w] == 1:
                    self.grass.process_draw(screen, w * 50, h * 50 + 75)
                elif self.area_data[h][w] == 2:
                    self.brick.process_draw(screen, w * 50, h * 50 + 75)


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

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == 275 or event.key == 100:
                    self.down_left = True
            elif event.type == pygame.KEYUP:
                if event.key == 275 or event.key == 100:
                    self.down_left = False
                print(event.key)

    def create_objects(self):
        self.area = Area()

    def main_loop(self):
        while not self.game_over:
            self.process_event()
            self.screen.fill((75, 100, 150))
            self.area.process_draw(self.screen)

            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()


def main():
    game = Game(800, 725)
    game.main_loop()


if __name__ == '__main__':
    main()
