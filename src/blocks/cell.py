class Cell:
    image = None

    def __init__(self, x=0, y=75):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def process_draw(self, screen, camera, x=0, y=75):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, camera.apply(self))
