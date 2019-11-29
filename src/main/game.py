import sys
import pygame

from fail import Fail
from src.blocks.grass import Grass
from src.bomb.bomb import Bomb
from src.bomb.fires.firehoriz import FireHorizontal
from src.bomb.fires.firemid import FireMiddle
from src.bomb.fires.firevert import FireVertical
from src.charachters.bomberman import Bomberman
from src.field.area import Area
from src.field.camera import Camera, camera_func
from src.field.score import Player_Score


class Game:
    def __init__(self, width=800, height=625):
        self.area = Area()
        self.bomberman = Bomberman()
        self.bomb = Bomb()
        self.camera = Camera(camera_func, self.area.width, self.area.height)
        self.width = width
        self.height = height
        self.size = (width, height)
        self.bomb_x_in_area = 0
        self.bomb_y_in_area = 0
        self.game_over = False
        self.is_bomb = False
        self.is_pressed_up = False
        self.is_pressed_left = False
        self.is_pressed_down = False
        self.is_pressed_right = False
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        self.bombs = []
        self.fires = []
        self.player = Player_Score()

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
                # self.game_over = True
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 97 or event.key == 276 or event.key == 160:
                    self.is_pressed_left = True
                    self.bomberman.shift_x_left = -self.bomberman.speed
                elif event.key == 100 or event.key == 275 or event.key == 162:
                    self.is_pressed_right = True
                    self.bomberman.shift_x_right = self.bomberman.speed
                elif event.key == 115 or event.key == 274 or event.key == 161:
                    self.is_pressed_down = True
                    self.bomberman.shift_y_down = self.bomberman.speed
                elif event.key == 119 or event.key == 273 or event.key == 172:
                    self.is_pressed_up = True
                    self.bomberman.shift_y_up = -self.bomberman.speed
                # Обработка нажатия клавиши E (для взрыва)
                elif (event.key == 101 or event.key == 173) and not self.bomb.is_bomb:
                    self.bomb.bomb_larger_middle_x = self.bomb_place_x()
                    self.bomb.bomb_larger_middle_y = self.bomb_place_y()
                    if self.bomb.bomb_larger_middle_x:
                        self.bomb.bomb_x_in_area = int((self.bomberman.rect.x - (
                                self.bomberman.rect.x % 50)) // 50)
                    elif not self.bomb.bomb_larger_middle_x:
                        self.bomb.bomb_x_in_area = int((self.bomberman.rect.x - (
                                self.bomberman.rect.x % 50)) // 50) + 1
                    if self.bomb.bomb_larger_middle_y:
                        self.bomb.bomb_y_in_area = int((self.bomberman.rect.y - 75 - (
                                (self.bomberman.rect.y - 75) % 50)) // 50)
                    elif not self.bomb.bomb_larger_middle_y:
                        self.bomb.bomb_y_in_area = int((self.bomberman.rect.y - 75 - (
                                (self.bomberman.rect.y - 75) % 50)) // 50) + 1
                    self.bombs.append(Bomb(self.bomb.bomb_x_in_area * 50, self.bomb.bomb_y_in_area * 50 + 75))
                    if len(self.bombs) == self.bomberman.max_count_bombs:
                        self.bomb.is_bomb = True
                self.bomberman.shift_x = self.bomberman.shift_x_left + self.bomberman.shift_x_right
                self.bomberman.shift_y = self.bomberman.shift_y_up + self.bomberman.shift_y_down
            if event.type == pygame.KEYUP:
                if event.key == 97 or event.key == 276 or event.key == 160:
                    self.is_pressed_left = False
                    self.bomberman.shift_x_left = 0
                elif event.key == 100 or event.key == 275 or event.key == 162:
                    self.is_pressed_right = False
                    self.bomberman.shift_x_right = 0
                elif event.key == 115 or event.key == 274 or event.key == 161:
                    self.is_pressed_down = False
                    self.bomberman.shift_y_down = 0
                elif event.key == 119 or event.key == 273 or event.key == 172:
                    self.is_pressed_up = False
                    self.bomberman.shift_y_up = 0
                self.bomberman.shift_x = self.bomberman.shift_x_left + self.bomberman.shift_x_right
                self.bomberman.shift_y = self.bomberman.shift_y_up + self.bomberman.shift_y_down

    def process_collisions(self):
        self.bomberman.can_move_Right = True
        self.bomberman.can_move_Left = True
        self.bomberman.can_move_Up = True
        self.bomberman.can_move_Down = True
        # Collisions
        all_objects = self.area.objects + self.bombs + self.fires  # Список всех объектов поля, для обработки коллизии
        for objects in all_objects:
            if objects.type == "Bomb" and objects.rect.colliderect(self.bomberman):
                return
            if objects.type == "Fire" and objects.rect.colliderect(self.bomberman):
                print("Game Over")
                self.game_over = True
                return
            if objects.type != 'Grass' and objects.type != 'Fire':
                if objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x + self.bomberman.speed, self.bomberman.rect.y)):
                    self.bomberman.can_move_Right = False
                if objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x - self.bomberman.speed, self.bomberman.rect.y)):
                    self.bomberman.can_move_Left = False
                if objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x, self.bomberman.rect.y + self.bomberman.speed)):
                    self.bomberman.can_move_Down = False
                if objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x, self.bomberman.rect.y - self.bomberman.speed)):
                    self.bomberman.can_move_Up = False
        for i in range(len(self.area.objects)):
            for fire in self.fires:
                if self.area.objects[i].type == 'Brick' and self.area.objects[i].rect.colliderect(fire):
                    self.area.objects[i] = Grass(fire.rect.x, fire.rect.y)

    def process_move(self):
        self.bomberman.move()

    def process_draw(self):
        self.screen.fill((75, 100, 150))
        self.camera.update(self.bomberman)
        self.area.process_draw(self.screen, self.camera)
        # Score
        self.player.refresh_area(self.screen)
        self.process_draw_bomb()
        self.process_draw_fires()
        self.bomberman.process_draw(self.screen, self.camera)

    def process_draw_fires(self):
        for fire in self.fires:
            fire.process_draw(self.screen, self.camera)

    def process_logic_fires(self):
        if len(self.fires):
            if self.fires[0].try_blow():
                self.fires.clear()

    def process_logic_bombs(self):
        for i in range(len(self.bombs)):
            if self.bombs[i].try_blow():
                self.generate_fires(self.bombs[i].rect.x, self.bombs[i].rect.y)
                self.bombs.pop(i)
                self.bomb.is_bomb = False
                break

    def process_draw_bomb(self):
        for bomb in self.bombs:
            bomb.process_draw(self.screen, self.camera)

    def bomb_place_x(self):
        if self.bomberman.rect.x <= int((self.bomberman.rect.x - (
                self.bomberman.rect.x % 50)) // 50) * 50 + 25:
            return True

        if self.bomberman.rect.x > int((self.bomberman.rect.x - (
                self.bomberman.rect.x % 50)) // 50) * 50 + 25:
            return False

    def bomb_place_y(self):
        if self.bomberman.rect.y < int(((self.bomberman.rect.y - 75 - (
                (self.bomberman.rect.y - 75) % 50)) // 50) * 50 + 75) + 25:
            return True

        if self.bomberman.rect.y >= int(((self.bomberman.rect.y - 75 - (
                (self.bomberman.rect.y - 75) % 50)) // 50) * 50 + 75) + 25:
            return False

    def generate_fires(self, x, y):
        if len(self.fires) == 0:
            self.fires.append(FireMiddle(x, y))
        can_generate = True
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(FireHorizontal(x + 50 * i, y))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(FireHorizontal(x, y + 50 * (i - 1)))

        can_generate = True
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(FireVertical(x, y + 50 * i))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(FireVertical(x, y + 50 * (i - 1)))

        can_generate = True
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(FireHorizontal(x - 50 * i, y))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(FireHorizontal(x - 50 * (i - 1), y))

        can_generate = True
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(FireVertical(x, y - 50 * i))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(FireVertical(x, y - 50 * (i - 1)))

    def check_fire_gen(self):
        for i in self.fires:
            for obj in self.area.objects:
                if obj.type == 'Block' and obj.rect.colliderect(i):
                    print("COLLIDE")
                    return False
        return True

    def reset(self):
        self.area = Area()
        self.game_over = False
        self.bomberman.rect.x = 50
        self.bomberman.rect.y = 125
        self.fires.clear()
        self.bombs.clear()
        self.player.time_reset()

    def main_loop(self):
        self.reset()
        while not self.game_over:
            self.process_event()
            self.process_collisions()
            self.process_move()
            self.process_draw()
            self.process_logic_bombs()
            self.process_logic_fires()

            pygame.display.flip()
            pygame.time.wait(10)

        self.player.update()

