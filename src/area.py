from random import randint
from src.blocks.block import Block
from src.blocks.brick import Brick
from src.blocks.grass import Grass


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
