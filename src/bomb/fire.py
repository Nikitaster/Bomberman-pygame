import time

from src.blocks.cell import Cell


class Fire(Cell):

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.type = "Fire"
        self.start_time = time.time()
        self.end_time = time.time() + 2

    def process_draw(self, screen, camera, x=0, y=75):
        screen.blit(self.image, camera.apply(self))

    def try_blow(self):  # Попытка взрыва по счетчику кадров
        return False if (time.time() - self.start_time) <= self.end_time - time.time() else True
