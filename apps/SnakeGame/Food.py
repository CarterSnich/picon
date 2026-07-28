from core import has_elapsed

BLINK_INTERVAL = 100


class Food:

    def __init__(self, x, y, last_blink_ms):
        self.x, self.y = x, y
        self.blink_state = True
        self.last_blink_ms = last_blink_ms


    def is_intersecting(self, x, y):
        return self.x == x and self.y == y


    def set_coordinates(self, x, y):
        self.x = x
        self.y = y


    def update(self, tick):
        if has_elapsed(tick, self.last_blink_ms, BLINK_INTERVAL):
            self.last_blink_ms = tick
            self.blink_state = not self.blink_state
