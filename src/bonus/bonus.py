from src.blocks.cell import Cell


class Bonus(Cell):
    image = None  # в дочерних: image = pygame.image.load("PATH")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Bonus"  # для каждого бонуса моенять type
        self.status = 'Hidden'  # Open, Taken

    def process_logic(self):
        # тут должна происходить логика бомбы в зависимости от ее текущего статуса
        # с последующей сменой этого статуса на следущий.
        pass
