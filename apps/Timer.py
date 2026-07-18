from core import PiconApp, ms_to_hms
from core.input import DPAD_LEFT, DPAD_RIGHT, DPAD_UP, DPAD_DOWN, KEY_A, KEY_B
from core.helper.countdown import *

from assets.menu_sprites import ARROW_UP, ARROW_DOWN

BLINK_INTERVAL_MS = 1_000


class Main(PiconApp):
    cursor: int
    delta: int
    hour: int
    minute: int
    seconds: int
    countdown: Countdown

    last_blink_ms: int
    blink: bool


    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)
        self.cursor = 0
        self.delta = 0
        self.hour = 0
        self.minute = 1
        self.seconds = 0

        self.countdown = Countdown(0)

        self.last_blink_ms = self.current_ms
        self.blink = False


    def inputs(self):
        if self.input.is_pressed(DPAD_LEFT):
            self.cursor = (self.cursor - 1) % 3
        elif self.input.is_pressed(DPAD_RIGHT):
            self.cursor = (self.cursor + 1) % 3
        elif self.input.is_pressed(DPAD_UP):
            self.delta = 1
        elif self.input.is_pressed(DPAD_DOWN):
            self.delta = -1
        elif self.input.is_pressed(KEY_A):
            if self.countdown.state == STATE_TICKING:
                self.countdown.pause()
            elif self.countdown.state == STATE_PAUSED:
                self.countdown.unpause()
            elif self.countdown.state == STATE_FINISHED:
                self.countdown.stop()
                self.blink = False
                self.sound.stop()
            else:
                self.start_timer()
        elif self.input.is_pressed(KEY_B):
            if self.countdown.state in (STATE_TICKING, STATE_PAUSED):
                self.countdown.stop()
            else:
                self.quit()


    def update(self):
        if self.countdown.state == STATE_IDLE and self.delta:
            if self.cursor == 0:
                self.hour = (self.hour + self.delta) % 100
            elif self.cursor == 1:
                self.minute = (self.minute + self.delta) % 60
            elif self.cursor == 2:
                self.seconds = (self.seconds + self.delta) % 60
            self.delta = 0
        else:
            self.countdown.update(self.current_ms)

            if ticks_diff(self.current_ms, self.last_blink_ms) >= BLINK_INTERVAL_MS:
                self.blink = not self.blink
                self.last_blink_ms = self.current_ms

            if self.countdown.state == STATE_FINISHED:
                if self.blink:
                    self.sound.tone(550)
                else:
                    self.sound.stop()


    def render(self):
        if self.countdown.state == STATE_IDLE:
            self.display.text(f"{self.hour:02d}:{self.minute:02d}:{self.seconds:02d}", 32, 28)
            x = 24 * self.cursor
            self.display.blit(ARROW_UP.framebuffer, 36 + x, 18)
            self.display.blit(ARROW_DOWN.framebuffer, 36 + x, 37)
        elif self.countdown.state == STATE_TICKING or self.countdown.state in (STATE_PAUSED,
                                                                               STATE_FINISHED) and self.blink:
            h, m, s = ms_to_hms(((self.countdown.remaining_ms + 999) // 1000) * 1000)
            self.display.text(f"{h:02d}:{m:02d}:{s:02d}", 32, 28)


    def start_timer(self):
        total_ms = (self.hour * 3600 + self.minute * 60 + self.seconds) * 1000
        if total_ms:
            self.countdown.set(total_ms)
            self.countdown.start(self.current_ms)


if __name__ == '__main__':
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
