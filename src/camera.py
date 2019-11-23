from pygame.rect import Rect


class Camera:
    def __init__(self, camera_funcs, width, height):
        self.camera_func = camera_funcs
        self.state = Rect(0, 0, width, height)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def apply(self, target, speed):
        return target.rect.move((self.state.x * speed / 4, self.state.y))


def camera_func(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + 800 / 2, -t + 650 / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - 950), l)       # Не движемся дальше правой границы
    t = max(-(camera.height-650), t)        # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы
    return Rect(l, t, w, h)
