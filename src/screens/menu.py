import os
import pygame


class Menu:
    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (50, 50, 50)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    # Game Fonts
    font = "fonts/pixel.ttf"
    # Game Framerate
    clock = pygame.time.Clock()
    FPS = 30
    # Center the Game Application
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    def __init__(self):
        pygame.init()
        # Game Resolution
        self.screen_width = 800
        self.screen_height = 725
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    # Text Renderer
    def text_format(self, message, textfont, textsize, textcolor):
        newfont = pygame.font.Font(textfont, textsize)
        newtext = newfont.render(message, 0, textcolor)
        return newtext

    def main_menu(self):
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
                            return True
                        if selected == "quit":
                            return False
            # Main Menu UI
            self.screen.fill(self.black)
            title = self.text_format("BOMBERMAN", self.font, 90, self.yellow)
            if selected == "start":
                text_start = self.text_format("START", self.font, 55, self.white)
            else:
                text_start = self.text_format("START", self.font, 45, self.red)
            if selected == "quit":
                text_quit = self.text_format("QUIT", self.font, 55, self.white)
            else:
                text_quit = self.text_format("QUIT", self.font, 45, self.red)
            title_rect = title.get_rect()
            start_rect = text_start.get_rect()
            quit_rect = text_quit.get_rect()
            self.screen.blit(title, (self.screen_width / 2 - (title_rect[2] / 2), 80))
            self.screen.blit(text_start, (self.screen_width / 2 - (start_rect[2] / 2), 300))
            self.screen.blit(text_quit, (self.screen_width / 2 - (quit_rect[2] / 2), 370))
            pygame.display.update()
            self.clock.tick(self.FPS)
