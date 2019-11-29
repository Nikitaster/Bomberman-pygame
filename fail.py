import pygame
import sys
import random
import string
import time
from src.field.score import Player_Score


class Fail:

    def __init__(self, player_score, width=800, height=725):
        self.width = width
        self.height = height
        self.game_over = False
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        pygame.font.init
        self.text_font = pygame.font.Font('fonts/pixel.ttf', 35)
        self.text_game_over = self.text_font.render('GAME OVER', 0, (255, 255, 255))
        self.token = ''.join(random.choice(string.ascii_uppercase) for x in range(20))
        self.text_token = self.text_font.render(self.token, 0, (255, 255, 255))
        self.player_score = player_score
        self.text_stage = self.text_font.render('STAGE 1', 0, (255, 255, 255))
        '''позже добавлю форматирование строки для смены уровня'''
        self.start_time = None

    def process_draw(self):
        self.screen.fill((0, 0, 0))
        if self.player_score.lost:
            self.screen.blit(self.text_game_over, (280, 340))
            self.screen.blit(self.text_token, (140, 600))
        else:
            self.screen.blit(self.text_stage, (310, 340))
            # print(self.player_score.lost)

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
                sys.exit()
            if event.type == pygame.KEYDOWN and self.player_score.lost:
                '''if event.key == 13:
                Переход к главному меню'''
                sys.exit()

    def fail_loop(self):
        self.text_stage = self.text_font.render('STAGE {}'.format(self.player_score.stage), 0, (255, 255, 255))
        self.start_time = time.time()
        while time.time() - self.start_time < 2 or self.player_score.lost:
            self.process_event()
            self.process_draw()
            pygame.display.flip()
            pygame.time.wait(10)