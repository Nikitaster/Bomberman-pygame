from tkinter import *
import pygame


class MainMenu:

    def __init__(self, width=800, height=725):
        self.image = pygame.image.load("../img/menu/img_name.png")
        self.width = width
        self.height = height
        self.game_over = False
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        self.rect = self.image.get_rect()
        pygame.init()

    def process_draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, self.rect)

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

    def main_loop(self):
        while not self.game_over:
            self.process_event()
            self.process_draw()
            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()


menu = MainMenu()
menu.main_loop()
