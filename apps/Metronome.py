from time import ticks_ms, ticks_diff

from core import PiconApp
from core.input import KEY_B, DPAD_UP, DPAD_DOWN, DPAD_LEFT, DPAD_RIGHT

MIN_BPM = 1
MAX_BPM = 240
BPM_SMALL_STEP = 1
BPM_LARGE_STEP = 5


class Main(PiconApp):
    bpm = 120
    current_beat = 0

    last_beat_ms = -1
    init_beat_ms = -1
    beat_gap_ms = (60 * 1000) / bpm

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)
        self.last_beat_ms = self.current_tick
        self.init_beat_ms = self.last_beat_ms
        self.sound.tone(1000)

    def inputs(self):
        if self.input.is_pressed(KEY_B):
            self.quit()

        if self.input.is_pressed(DPAD_UP):
            self.increase_bpm(BPM_SMALL_STEP)
        elif self.input.is_pressed(DPAD_DOWN):
            self.decrease_bpm(BPM_SMALL_STEP)
        elif self.input.is_pressed(DPAD_RIGHT):
            self.increase_bpm(BPM_LARGE_STEP)
        elif self.input.is_pressed(DPAD_LEFT):
            self.decrease_bpm(BPM_LARGE_STEP)

    def update(self):
        beat_delta = ticks_diff(ticks_ms(), self.last_beat_ms)

        self.calculate_beat_gap()

        if beat_delta >= self.beat_gap_ms:
            self.last_beat_ms = self.current_tick
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
