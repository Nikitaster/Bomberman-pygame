import sys
import pygame
from random import randint

class Area:
    def __init__(self):
        self.area_data = []
        self.width = 1550
        self.height = 650
        self.size_block = 50
        self.rgb = [
            (150, 0, 0),
            (0, 150, 0),
            (0, 0, 150)
        ]
        self.area_data = []
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
        n = randint(50, 70)
        for i in range(13):
            for j in range(31):
                if i % 2 == 1 and j % 2 == 1 and i != 1 and i != 2 and j != 1 and j != 2 and count <= n:
                    if randint(0, 1):
                        self.area_data[i][j] = 2
                        count += 1

    def process_draw(self, screen):
        # for h in range(75, self.height + 75, self.size_block):
        #     for w in range(0, self.width, self.size_block):
        #         pygame.draw.rect(screen, self.rgb[(w + h) % 3], (w, h, self.size_block, self.size_block))
        for i in range(13):
            print(self.area_data[i])

    def process_logic(self):
        pass


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
        self.area.process_draw(self.screen)

    def main_loop(self):
        while not self.game_over:
            self.process_event()
            self.screen.fill((75, 100, 150))


            # if self.down_left and x < size_screen[0] - 25 - 12.5:
            #     x += 2.5

            # pygame.draw.rect(screen, (0, 0, 0), (x + 12.5, 75 + 12.5, 25, 25))
            # x += 10
            # pygame.draw.rect(screen, (0, 150, 0), (50, 50, 50, 50))
            # pygame.draw.rect(screen, (0, 0, 150), (0, 100, 50, 50))

            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()


def main():
    # x = 0

    game = Game(800, 725)
    game.main_loop()


if __name__ == '__main__':
    main()