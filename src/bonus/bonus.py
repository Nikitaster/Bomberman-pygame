import time


class Bonus:
    def __init__(self, x=0, y=75, type='Bonus'):
        self.type = type  # для каждого бонуса моенять type
        self.status = 'Hidden'  # Open, Taken
        self.time_of_open = None

    def set_open_status(self):
        if self.status == 'Hidden':
            self.time_of_open = time.time()

    def process_logic(self):
        if time.time() - self.time_of_open > 3 and self.status == 'Hidden' and self.time_of_open is not None:
            self.status = 'Open'
