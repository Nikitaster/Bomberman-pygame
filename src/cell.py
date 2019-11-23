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