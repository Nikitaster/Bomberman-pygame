import time
import pygame


class Sound:
    sound_file = None

    def __init__(self):
        self.sound = pygame.mixer.Sound(self.sound_file)
        self.sound.set_volume(0.1)
        self.start_time = None
        self.len = 0.25

    def play(self):
        if self.start_time is None:
            self.sound.play()
            self.start_time = time.time()

    def stop(self):
        self.sound.stop()

    def process_logic(self):
        if self.start_time is not None:
            if time.time() - self.start_time > self.len:
                self.stop()
                self.start_time = None
