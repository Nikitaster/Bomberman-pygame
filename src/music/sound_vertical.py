from src.music.base_sound import Sound


class SoundUpDown(Sound):
    sound_file = '.././sounds/in_field/up-down.ogg'

    def __init__(self):
        super().__init__()
        self.len = 0.25
