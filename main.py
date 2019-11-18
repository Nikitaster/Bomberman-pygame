import sys
import pygame
import random


class BomberMan:
    filename = 'bomberman.png'

    def __init__(self, x=10, y=90):
        self.image = pygame.image.load(self.filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shift_x = 0
        self.shift_y = 0

    def beginning_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.shift_x = -10
            elif event.key == pygame.K_d:
                self.shift_x = 10
            elif event.key == pygame.K_w:
                self.shift_y = 10
            elif event.key == pygame.K_s:
                self.shift_y = -10

    def process_logic(self, width, height):
        if self.rect.left < 0 or self.rect.right > width:
            self.shift_x = 0
        elif self.rect.bottom < 0 or self.rect.top > height:
            self.shift_y = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.bottom < 0:
            self.rect.bottom = 0
        if self.rect.top > height:
            self.rect.top = height

    def move(self):
        self.rect.x += self.shift_x
        self.rect.y += self.shift_y

    def process_draw(self, screen):
        screen.blit(self.image, self.rect)


def main():
    rgb = [
        (150, 0, 0),
        (0, 150, 0),
        (0, 0, 150)
    ]
    size_block = 50
    size_screen = (800, 625)
    pygame.init()
    screen = pygame.display.set_mode(size_screen)
    x = 0
    game_over = False
    bomberman = BomberMan(50, 125)
    while not game_over:
        for event in pygame.event.get():
            bomberman.process_event(event)
            if event.type == pygame.QUIT:
                game_over = True
        screen.fill((75, 100, 150))
        for h in range(75, size_screen[1] - 25, size_block):
            for i in range(0, size_screen[0], size_block):
                pygame.draw.rect(screen, rgb[(i + h) % 3], (i, h, size_block, size_block))
        bomberman.process_draw(screen)
        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit()


if __name__ == '__main__':
    main()