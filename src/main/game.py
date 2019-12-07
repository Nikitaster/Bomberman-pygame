import sys
import time
from random import randint
from random import randrange

import pygame

from src.blocks.exit import Exit
from src.blocks.grass import Grass
from src.bomb.bomb import Bomb
from src.bomb.fires.firehoriz import FireHorizontal
from src.bomb.fires.firemid import FireMiddle
from src.bomb.fires.firevert import FireVertical
from src.bonus.bonuscalled import BonusCalled
from src.charachters.bomberman import Bomberman
from src.charachters.first_enemy import FirstLevelEnemy
from src.charachters.second_enemy import SecondLevelEnemy
from src.field.area import Area
from src.field.camera import Camera, camera_func
from src.field.score import Player_Score
from src.music.main_theme import Music
from src.music.sound_horizontal import SoundRightLeft
from src.music.sound_vertical import SoundUpDown


class Game:
    def __init__(self, width=800, height=625):
        pygame.mixer.pre_init(44100, -16, 2, 64)
        pygame.mixer.init()
        self.area = Area()
        self.bomberman = Bomberman()
        self.bomb = Bomb()
        self.camera = Camera(camera_func, self.area.width, self.area.height)
        self.width = width
        self.height = height
        self.size = (width, height)
        self.bomb_x_in_area = 0
        self.bomb_y_in_area = 0
        self.exit_num = None
        self.bonus_num = dict(
            BombBonus=None,
            FlamePassBonus=None,
            FlamesBonus=None,
            SpeedBonus=None)
        self.bonus_key_list = list(self.bonus_num.keys())
        self.bonus_num_list = list(self.bonus_num.values())
        self.game_over = False
        self.is_bomb = False
        self.is_pressed_up = False
        self.is_pressed_left = False
        self.is_pressed_down = False
        self.is_pressed_right = False
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        self.music = Music()
        self.bombs = []
        self.fires = []
        self.enemies = []
        self.player = Player_Score()
        self.sounds = dict(
            RightLeft=SoundRightLeft(),
            UpDown=SoundUpDown())
        self.time_start = None

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
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
                    self.bomberman.animation_left(self.is_pressed_left)
                elif event.key == 100 or event.key == 275 or event.key == 162:
                    self.is_pressed_right = False
                    self.bomberman.shift_x_right = 0
                    self.bomberman.animation_right(self.is_pressed_right)
                elif event.key == 115 or event.key == 274 or event.key == 161:
                    self.is_pressed_down = False
                    self.bomberman.shift_y_down = 0
                    self.bomberman.animation_down(self.is_pressed_down)
                elif event.key == 119 or event.key == 273 or event.key == 172:
                    self.is_pressed_up = False
                    self.bomberman.shift_y_up = 0
                    self.bomberman.animation_up(self.is_pressed_up)
                self.bomberman.shift_x = self.bomberman.shift_x_left + self.bomberman.shift_x_right
                self.bomberman.shift_y = self.bomberman.shift_y_up + self.bomberman.shift_y_down

    def process_collisions(self):
        self.bomberman.can_move_Right = True
        self.bomberman.can_move_Left = True
        self.bomberman.can_move_Up = True
        self.bomberman.can_move_Down = True
        # Collisions
        all_objects = self.area.objects + self.bombs + self.fires + self.enemies  # Список всех объектов поля, для
        # обработки коллизии
        for objects in all_objects:
            if objects.type == "Bomb" and objects.rect.colliderect(self.bomberman):
                return
            if (objects.type == "Fire" or objects.type == "Enemy") and objects.rect.colliderect(self.bomberman):
                self.game_over = True
                return
            if objects.type == "Exit" and objects.rect.colliderect(self.bomberman) and len(self.enemies) == 0:
                self.game_over = True
                self.player.stage += 1
                return
            # результат получения бонуса
            if objects.type == "BombBonus" and objects.rect.colliderect(self.bomberman):
                self.bomberman.max_count_bombs += 1
            if objects.type == "FlamePassBonus" and objects.rect.colliderect(self.bomberman):
                self.bomberman.flame_pass = True
            if objects.type == "FlamesBonus" and objects.rect.colliderect(self.bomberman):
                self.bomberman.long_fire += 1
            if objects.type == "SpeedBonus" and objects.rect.colliderect(self.bomberman):
                self.bomberman.speed *= 2
                self.bonus_num.pop('SpeedBonus')
            if objects.type != 'Grass' and objects.type != 'Fire' and objects.type != 'Exit' \
                    and objects.type not in self.bonus_key_list and objects.type != 'Enemy':
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
                if self.area.objects[i].type == 'Brick' and (i == self.exit_num) and \
                        self.area.objects[i].rect.colliderect(fire):
                    self.area.objects[i] = Exit(fire.rect.x, fire.rect.y)
                    self.area.objects[i].set_open_status()
                for bonus in self.bonus_num.keys():
                    if self.area.objects[i].type == 'Brick' and i == self.bonus_num[bonus] and \
                            self.area.objects[i].rect.colliderect(fire):
                        self.area.objects[i] = BonusCalled(fire.rect.x, fire.rect.y, bonus)
                        self.area.objects[i].set_open_status()
                if self.area.objects[i].type == 'Brick' and self.area.objects[i].rect.colliderect(fire):
                    self.area.objects[i] = Grass(fire.rect.x, fire.rect.y)
                if self.area.objects[i].type == 'Exit' and self.area.objects[i].status == 'Open':
                    self.fires.clear()
                    for number in range(randint(5, 10)):
                        self.enemies.append(SecondLevelEnemy(self.area.objects[i].rect.x, self.area.objects[i].rect.y))
                    self.area.objects[i] = Grass(self.area.objects[i].rect.x, self.area.objects[i].rect.y)
            if self.area.objects[i].rect.colliderect(
                    Bomberman(self.bomberman.rect.x, self.bomberman.rect.y)) \
                    and (self.area.objects[i].type in self.bonus_key_list):
                self.area.objects[i] = Grass(self.area.objects[i].rect.x, self.area.objects[i].rect.y)
        for enemy in range(len(self.enemies)):
            for fire in self.fires:
                if self.enemies[enemy].rect.colliderect(fire):
                    self.player.score += 100
                    self.enemies.pop(enemy)
                    return

    def generate_exit_num(self):
        rnd = randint(34, len(self.area.objects) - 31)
        while self.area.objects[rnd].type != 'Brick':
            rnd = randint(34, len(self.area.objects) - 31)
        self.exit_num = rnd

    def generate_bonus_num(self):
        counter = 0
        for bonus in self.bonus_num.keys():
            if randint(0, 4) == 1:
                rnd = randint(34, len(self.area.objects) - 31)
                while self.area.objects[rnd].type != 'Brick':
                    rnd = randint(34, len(self.area.objects) - 31)
                self.bonus_num[bonus] = rnd
                self.bonus_num_list[counter] = rnd
                counter += 1
                return

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

    def process_draw_enemies(self):
        for enemy in self.enemies:
            enemy.process_draw(self.screen, self.camera)

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
        self.check_fire_horizontal_right(x, y, FireHorizontal, can_generate)
        self.check_fire_vertical_up(x, y, FireVertical, can_generate)
        self.check_fire_horizontal_left(x, y, FireHorizontal, can_generate)
        self.check_fire_vertical_down(x, y, FireVertical, can_generate)

    def check_fire_horizontal_right(self, x, y, types, can_generate):
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(types(x + 50 * i, y))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(types(x, y + 50 * (i - 1)))

    def check_fire_vertical_up(self, x, y, types, can_generate):
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(types(x, y + 50 * i))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(types(x, y + 50 * (i - 1)))

    def check_fire_horizontal_left(self, x, y, types, can_generate):
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(types(x - 50 * i, y))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(types(x - 50 * (i - 1), y))

    def check_fire_vertical_down(self, x, y, types, can_generate):
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(types(x, y - 50 * i))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(types(x, y - 50 * (i - 1)))

    def check_fire_gen(self):
        for i in self.fires:
            for obj in self.area.objects:
                if obj.type == 'Block' and obj.rect.colliderect(i):
                    return False
        return True

    def generate_enemies(self):
        for i in range(self.player.max_enemies):
            self.enemies.append(FirstLevelEnemy(randrange(50, 1400, 50), randrange(125, 625, 50)))
            while self.enemies[i].process_collision(self.area.objects):
                self.enemies[i].rect.x = randrange(50, 1500, 50)
                self.enemies[i].rect.y = randrange(125, 625, 50)
            while self.enemies[i].rect.x == 50 and self.enemies[i].rect.y == 125 or \
                    self.enemies[i].rect.x == 100 and self.enemies[i].rect.y == 125 or \
                    self.enemies[i].rect.x == 50 and self.enemies[i].rect.y == 175:
                self.enemies[i].rect.x = randrange(50, 1500, 50)
                self.enemies[i].rect.y = randrange(125, 625, 50)

    def process_logic_enemies(self):
        for enemy in self.enemies:
            enemy.process_logic(self.area.objects + self.bombs)

    def process_collision_enemies(self):
        for enemy in self.enemies:
            enemy.process_collision(self.area.objects + self.fires + self.bombs)

    def reset(self):
        self.area = Area()
        self.game_over = False
        self.bomberman.rect.x = 50
        self.bomberman.rect.y = 125
        self.is_pressed_up = False
        self.is_pressed_left = False
        self.is_pressed_down = False
        self.is_pressed_right = False
        self.bomberman.stop()
        self.bomb.is_bomb = False
        self.fires.clear()
        self.bombs.clear()
        self.player.time_reset()
        self.generate_exit_num()
        self.enemies.clear()
        self.generate_enemies()
        self.generate_bonus_num()
        self.player.timeout = False
        self.player.lost = False
        self.music = Music()

    def play_sounds(self):
        if self.bomberman.shift_x > 0 and self.bomberman.can_move_Right or \
                self.bomberman.shift_x < 0 and self.bomberman.can_move_Left:
            self.sounds['RightLeft'].play()

        if self.bomberman.shift_y > 0 and self.bomberman.can_move_Down or \
                self.bomberman.shift_y < 0 and self.bomberman.can_move_Up:
            self.sounds['UpDown'].play()

    def process_logic_sounds(self):
        for sound in self.sounds.keys():
            self.sounds[sound].process_logic()

    def main_loop(self):
        self.reset()
        self.music.play()
        while not self.game_over:
            self.process_event()
            self.process_collisions()
            self.process_move()
            self.process_draw()
            self.process_logic_bombs()
            self.process_logic_fires()
            self.process_logic_enemies()
            self.process_draw_enemies()
            if self.area.objects[self.exit_num].type == 'Exit':
                self.area.objects[self.exit_num].process_logic()
            self.bomberman.process_logic()
            self.play_sounds()
            self.process_logic_sounds()
            if self.player.timeout:
                self.game_over = True
            pygame.display.flip()
            pygame.time.wait(10)

        self.player.update()
        self.time_start = time.time()
        self.bomberman.start_anim_time = None
        while time.time() - self.time_start < 3:
            self.process_event()
            self.process_logic_fires()
            self.process_logic_enemies()
            self.bomberman.death()
            self.process_draw()
            self.process_draw_enemies()
            pygame.display.flip()
            pygame.time.wait(10)
