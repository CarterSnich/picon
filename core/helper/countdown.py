from time import ticks_diff

STATE_IDLE = 0
STATE_TICKING = 1
STATE_PAUSED = 2
STATE_FINISHED = 3


class Countdown:
    time_ms: int
    remaining_ms: int
    last_update_ms: int
    state: int


    def __init__(self, ms: int):
        self.time_ms = ms
        self.state = STATE_IDLE


    def update(self, current_ms):
        if self.state == STATE_TICKING:
            self.remaining_ms -= ticks_diff(current_ms, self.last_update_ms)

            if self.remaining_ms <= 0:
                self.finish()

        self.last_update_ms = current_ms


    def set(self, ms: int):
        self.time_ms = ms


    def start(self, current_ms):
        self.remaining_ms = self.time_ms
        self.last_update_ms = current_ms
        self.state = STATE_TICKING


    def stop(self):
        self.remaining_ms = 0
        self.state = STATE_IDLE


    def pause(self):
        self.state = STATE_PAUSED


    def unpause(self):
        self.state = STATE_TICKING


    def finish(self):
        self.state = STATE_FINISHED


    def reset(self):
        self.remaining_ms = self.time_ms


if __name__ == '__main__':
    from time import ticks_ms

    c = Countdown(5000)
    c.start(ticks_ms())

    while c.state == STATE_TICKING:
        c.update(ticks_ms())
        print((c.remaining_ms + 999) // 1000)
