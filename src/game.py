import sys
import pygame
import time

from src.area import Area
from src.bomberman import Bomberman
from src.camera import Camera, camera_func


class Game:
    def __init__(self, width=800, height=625):
        self.area = Area()
        self.bomberman = Bomberman()
        self.camera = Camera(camera_func, self.area.width, self.area.height)
        self.width = width
        self.height = height
        self.size = (width, height)
        self.game_over = False
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        ####
        self.player = Player_Score()  # This part must be here? Or it won't work... But you can try to make it different...
        ####

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == 97 or event.key == 276 or event.key == 160:
                    self.bomberman.shift_x = -self.bomberman.speed
                elif event.key == 100 or event.key == 275 or event.key == 162:
                    self.bomberman.shift_x = self.bomberman.speed
                elif event.key == 115 or event.key == 274 or event.key == 161:
                    self.bomberman.shift_y = self.bomberman.speed
                elif event.key == 119 or event.key == 273 or event.key == 172:
                    self.bomberman.shift_y = -self.bomberman.speed
            if event.type == pygame.KEYUP:
                self.bomberman.shift_x = 0
                self.bomberman.shift_y = 0

    def process_collisions(self):
        self.bomberman.can_move_Right = True
        self.bomberman.can_move_Left = True
        self.bomberman.can_move_Up = True
        self.bomberman.can_move_Down = True
        # Collisions
        for objects in self.area.objects:
            if objects.type != 'Grass':
                if objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x + self.bomberman.speed, self.bomberman.rect.y)):
                    self.bomberman.can_move_Right = False
                elif objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x - self.bomberman.speed, self.bomberman.rect.y)):
                    self.bomberman.can_move_Left = False
                elif objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x, self.bomberman.rect.y + self.bomberman.speed)):
                    self.bomberman.can_move_Down = False
                elif objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x, self.bomberman.rect.y - self.bomberman.speed)):
                    self.bomberman.can_move_Up = False

    def process_move(self):
        self.bomberman.move()

    def process_draw(self):
        self.screen.fill((75, 100, 150))
        self.camera.update(self.bomberman)
        self.area.process_draw(self.screen, self.camera, self.bomberman.speed)
        ####
        self.player.refresh_area(self.screen)
        # Add score: self.player.add_score(<how_much_score>)
        # Add time:  self.player.add_time(<how_much_time>)
        # Add life:  self.player.add_life(<how_much_time>)
        ####

    def main_loop(self):
        while not self.game_over:
            self.process_event()
            self.process_collisions()
            self.process_move()
            self.process_draw()
            self.bomberman.process_draw(self.screen, self.camera)
            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()


class Player_Score:
    def __init__(self, name='New player', score=0, time_left=200, lifes=3):
        self.name = name  # Player name
        self.score = score  # Player score
        self.start_time = time.time()
        self.end_time = self.start_time + 200
        self.time_left = time_left  # How much time left
        self.lifes = lifes  # How much life left
        self.lost = False  # Have you lost?
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
        screen.blit(self.text_time, (610, 2))
        screen.blit(self.text_score, (200, 43))

    def add_time(self, time_add=-1):  # How much time you want to add? Or you want to set it less?
        self.time_left += time_add
        if self.time_left <= 0:
            self.lost = True

    def add_life(self, lifes_add=-1):  # How much lifes you want to give? Or you want to kill him?
        self.lifes += lifes_add;
        if self.lifes <= 0:
            self.lost = True

    def add_score(self, score_add=0):  # How much score you want to add?
        self.score += score_add

    def get_time_left(self):
        now_time = self.time_left - (time.time() - self.start_time)
        if now_time <= 0:
            print("GameOver")
            return "{0:.0f}".format(0)
        return "{0:.0f}".format(now_time)
