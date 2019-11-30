import pygame
import time
from random import randrange


class Player_Score:
    def __init__(self, name='New player', score=0, time_left=200, lifes=3):
        self.name = name  # Player name
        self.score = score  # Player score
        self.start_time = time.time()
        self.end_time = self.start_time + 200
        self.time_left = time_left  # How much time left
        self.lifes = lifes  # How much life left
        self.lost = False  # Have you lost?
        self.max_enemies = 1
        pygame.font.init()  # Start fonts
        self.scores_font = pygame.font.Font('./fonts/pixel.ttf', 30)  # Create a font
        self.text_name = self.scores_font.render('', 0, (255, 255, 255))  # declaration
        self.text_time = self.scores_font.render('', 0, (255, 255, 255))  # declaration
        self.text_life = self.scores_font.render('', 0, (255, 255, 255))  # declaration
        self.text_score = self.scores_font.render('', 0, (255, 255, 255))  # declaration

    def refresh_area(self, screen):
        pygame.draw.rect(screen, (100, 110, 100), (0, 0, 800, 75), 0)
        self.text_name = self.scores_font.render('Name:{}'.format(self.name), 0, (255, 255, 255))
        self.text_time = self.scores_font.render('Time:{}'.format(self.get_time_left()), 0, (255, 255, 255))
        self.text_life = self.scores_font.render('Lifes:{}'.format(self.lifes), 0, (255, 255, 255))
        self.text_score = self.scores_font.render('Score:{}'.format(self.score), 0, (255, 255, 255))
        screen.blit(self.text_name, (10, 2))
        screen.blit(self.text_life, (10, 43))
        screen.blit(self.text_time, (610, 22))
        screen.blit(self.text_score, (200, 43))

    def add_time(self, time_add=-1):  # How much time you want to add? Or you want to set it less?
        self.time_left += time_add
        if self.time_left <= 0:
            self.lost = True

    def add_life(self, lifes_add=-1):  # How much lifes you want to give? Or you want to kill him?
        self.lifes += lifes_add
        if self.lifes <= 0:
            self.lost = True

    def add_score(self, score_add=0):  # How much score you want to add?
        self.score += score_add

    def get_time_left(self):
        now_time = self.time_left - (time.time() - self.start_time)
        if now_time <= 0:
            self.lost = True
            print("GameOver")
            return "{0:.0f}".format(0)
        return "{0:.0f}".format(now_time)