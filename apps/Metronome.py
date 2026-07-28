from time import ticks_ms, ticks_diff

from core import PiconApp
from core.input import Key

DEFAULT_BPM = 120
MIN_BPM = 1
MAX_BPM = 240
BPM_SMALL_STEP = 1
BPM_LARGE_STEP = 5

SIXTY_SECONDS = 60
ONE_K_MILLISECONDS = 1000


class Main(PiconApp):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

        self.bpm = DEFAULT_BPM
        self.current_beat = 0

        self.last_beat_ms = self.current_ms
        self.init_beat_ms = self.last_beat_ms
        self.beat_gap_ms = (SIXTY_SECONDS * ONE_K_MILLISECONDS) / self.bpm

        self.sound.tone(1000)


    def inputs(self):
        if self.input.is_pressed(Key.B):
            self.quit()

        if self.input.is_pressed(Key.UP):
            self.increase_bpm(BPM_SMALL_STEP)
        elif self.input.is_pressed(Key.DOWN):
            self.decrease_bpm(BPM_SMALL_STEP)
        elif self.input.is_pressed(Key.RIGHT):
            self.increase_bpm(BPM_LARGE_STEP)
        elif self.input.is_pressed(Key.LEFT):
            self.decrease_bpm(BPM_LARGE_STEP)


    def update(self):
        beat_delta = ticks_diff(ticks_ms(), self.last_beat_ms)

        self.calculate_beat_gap()

        if beat_delta >= self.beat_gap_ms:
            self.last_beat_ms = self.current_ms
            self.current_beat = (self.current_beat + 1) % 4
            if self.current_beat == 0:
                self.sound.tone(1000)
            else:
                self.sound.tone(880)
        elif beat_delta >= 100:
            self.sound.stop()


    def render(self):
        self.display.center_text(str(self.bpm))

        for i in range(4):
            if self.current_beat == i:
                self.display.ellipse((20 * i) + 34, 44, 5, 5, 1, [True])
            else:
                self.display.ellipse((20 * i) + 34, 44, 5, 5, 1)


    def increase_bpm(self, amount):
        if self.bpm + amount >= MAX_BPM:
            self.bpm = MAX_BPM
        else:
            self.bpm += amount


    def decrease_bpm(self, amount):
        if self.bpm - amount <= MIN_BPM:
            self.bpm = MIN_BPM
        else:
            self.bpm -= amount


    def calculate_beat_gap(self):
        self.beat_gap_ms = (60 * 1000) / self.bpm
