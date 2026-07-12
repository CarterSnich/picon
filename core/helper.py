from time import ticks_ms, ticks_diff

from core.config import SCREEN_HEIGHT, SCREEN_WIDTH

def get_center(x=0, y=0):
    center_x = (SCREEN_WIDTH / 2) + x
    center_y = (SCREEN_HEIGHT / 2) + y
    return center_x, center_y

class Countdown:
    def __init__(self, seconds):
        self.remaining = seconds
        self.last_tick = ticks_ms()

    def update(self, now):
        self.remaining -= ticks_diff(now, self.last_tick)
        self.last_tick = now

    def finished(self):
        return self.remaining <= 0
