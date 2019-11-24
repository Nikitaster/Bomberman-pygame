import sys
import pygame

black = 0, 0, 0

from src.area import Area
# from src.blocks.grass import Grass
from src.bomberman import Bomberman
from src.bomb import Bomb
from src.camera import Camera, camera_func


class Game:
    def __init__(self, width=800, height=625):
        self.area = Area()
        self.bomberman = Bomberman()
        self.bomb = Bomb()
        self.camera = Camera(camera_func, self.area.width, self.area.height)
        self.width = width
        self.height = height
        self.size = (width, height)
        self.game_over = False
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        self.bombs = []

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
                elif event.key == 101 and not self.bomb.is_bomb:  # Обработка нажатия клавиши E (для взрыва)
                    self.bomb.bomb_x_in_area = int((self.bomberman.rect.x - (
                            self.bomberman.rect.x % 50)) // 50)  # Координата x бомбы относительно блоков
                    self.bomb.bomb_y_in_area = int((self.bomberman.rect.y - 75 - (
                            (self.bomberman.rect.y - 75) % 50)) // 50)  # Координата y бомбы относительно блоков
                    self.bombs.append(Bomb(self.bomb.bomb_x_in_area * 50, self.bomb.bomb_y_in_area * 50 + 75))
                    self.bomb.is_bomb = True

            if event.type == pygame.KEYUP:
                self.bomberman.shift_x = 0
                self.bomberman.shift_y = 0

    def process_collisions(self):
        self.bomberman.can_move_Right = True
        self.bomberman.can_move_Left = True
        self.bomberman.can_move_Up = True
        self.bomberman.can_move_Down = True
        # Collisions
        all_objects = self.area.objects + self.bombs  # Список всех объектов поля, для обработки коллизии
        for objects in all_objects:
            if objects.type == "Bomb" and objects.rect.colliderect(self.bomberman):
                return
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
        # self.bomb.image.fill(black)
        # self.bomb.boltAnimBomb.blit(self.bomb.image)
        # for bombs in self.bombs:
        #     self.screen.blit(bombs.image, self.camera.apply(bombs, self.bomberman.speed))

    def main_loop(self):
        while not self.game_over:
            self.process_event()
            self.process_collisions()
            self.process_move()
            self.process_draw()
            self.bomberman.process_draw(self.screen, self.camera)
            self.bomb.process_draw(self.screen, self.camera)

            # if self.bomb.is_bomb:
            #     for i in range(len(self.bombs)):
            #         if self.bombs[i].try_blow():
            #             del self.bombs[i]
            #             self.bomb.is_bomb = False

            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()
