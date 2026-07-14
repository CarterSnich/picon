from time import ticks_ms, ticks_diff

BLINK_INTERVAL = 100


class Food:
    x = -1
    y = -1
    blink_state = True
    last_blink_ms = -1


    def __init__(self, x, y):
        self.set_coordinates(x, y)
        self.last_blink_ms = ticks_ms()


    def is_intersecting(self, x, y):
        return self.x == x and self.y == y


    def set_coordinates(self, x, y):
        self.x = x
        self.y = y


    def update(self, tick):
        if ticks_diff(tick, self.last_blink_ms) >= BLINK_INTERVAL:
            self.last_blink_ms = tick
            self.blink_state = not self.blink_state
