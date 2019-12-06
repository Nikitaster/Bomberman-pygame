
import os
import pygame
from pygame.locals import *
from src.game import Game

pygame.init()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width = 800
screen_height = 725
screen = pygame.display.set_mode((screen_width, screen_height))


# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Game Fonts
font = "./fonts/pixels.ttf"

# Game Framerate
clock = pygame.time.Clock()
FPS = 30


def main_menu():
    menu = True
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        exec(open('./run.py').read())
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(black)
        title = text_format("BOMBERMAN", font, 90, yellow)
        if selected == "start":
            text_start = text_format("START", font, 55, white)
        else:
            text_start = text_format("START", font, 45, red)
        if selected == "quit":
            text_quit = text_format("QUIT", font, 55, white)
        else:
            text_quit = text_format("QUIT", font, 45, red)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (screen_width / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (screen_width / 2 - (quit_rect[2] / 2), 370))
        pygame.display.update()
        clock.tick(FPS)


main_menu()
pygame.quit()
quit()
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
