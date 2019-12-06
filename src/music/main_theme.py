from random import randint
import pygame


class Music:
    themes = ['./sounds/themes/theme_1.ogg',
              './sounds/themes/theme_2.ogg',
              './sounds/themes/theme_3.ogg',
              './sounds/themes/theme_4.ogg',
              './sounds/themes/theme_5.ogg',
              './sounds/themes/theme_6.ogg',
              './sounds/themes/theme_7.ogg',
              './sounds/themes/theme_8.ogg',
              './sounds/themes/theme_9.ogg']

    def __init__(self):
        index = randint(0, len(self.themes) - 1)
        pygame.mixer.music.load(self.themes[index])
        pygame.mixer.music.set_volume(0.18)

    @staticmethod
    def play():
        pygame.mixer.music.play(-1)

    @staticmethod
    def stop():
        pygame.mixer.music.stop()
