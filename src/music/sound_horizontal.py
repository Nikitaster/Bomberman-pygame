from src.music.base_sound import Sound


class SoundRightLeft(Sound):
    sound_file = '.././sounds/in_field/right-left.ogg'

    def __init__(self):
        super().__init__()
        self.len = 0.25
