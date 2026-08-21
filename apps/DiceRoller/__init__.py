__NAME__ = "Dice Roller"
__CATEGORY__ = "tools"

from random import randrange

from apps.DiceRoller.assets import *
from core import PiconApp
from core.helper import has_elapsed, elapsed
from core.input import Key

ROLL_DURATION_MS = 10_000
ROLL_INTERVAL_MS = 100
ROLL_FINAL_INTERVAL_MS = 800
ROLL_SLOWDOWN_MS = 5_000
TONE_DURATION_MS = 50

FINISH_BEEP_INTERVAL_MS = 120
FINISH_BEEP_COUNT = 2


class Main(PiconApp):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)
        self.sprites = (ONE, TWO, THREE, FOUR, FIVE, SIX)

        self.dice_count = 3
        self.numbers = []
        self.is_rolled = False
        self.roll_start_ms = self.current_ms
        self.last_roll_ms = self.current_ms
        self.last_tone_ms = self.current_ms

        self.finish_beeps = 0
        self.last_finish_beep_ms = 0

        self.randomize()


    def inputs(self):
        if self.input.is_pressed(Key.B):
            self.quit()

        if self.is_rolled:
            return

        if self.input.is_pressed(Key.A):
            self.is_rolled = True
            self.roll_start_ms = self.current_ms
            self.last_roll_ms = self.current_ms

            self.randomize()
            self.sound.tone()
            self.last_tone_ms = self.current_ms
        elif self.input.is_pressed(Key.X):
            self.dice_count = (self.dice_count % 3) + 1


    def update(self):
        # Finish beep sequence
        if self.finish_beeps:
            if has_elapsed(self.current_ms, self.last_tone_ms, TONE_DURATION_MS):
                self.sound.stop()

            if has_elapsed(self.current_ms, self.last_finish_beep_ms, FINISH_BEEP_INTERVAL_MS):
                self.finish_beeps -= 1

                if self.finish_beeps:
                    self.sound.tone()
                    self.last_tone_ms = self.current_ms
                    self.last_finish_beep_ms = self.current_ms

        if not self.is_rolled:
            return

        # Stop roll sound
        if has_elapsed(self.current_ms, self.last_tone_ms, TONE_DURATION_MS):
            self.sound.stop()

        # Roll finished
        if has_elapsed(self.current_ms, self.roll_start_ms, ROLL_DURATION_MS):
            self.is_rolled = False

            self.sound.tone()
            self.last_tone_ms = self.current_ms
            self.last_finish_beep_ms = self.current_ms
            self.finish_beeps = 2

            return

        # Roll animation
        if has_elapsed(self.current_ms, self.last_roll_ms, self.get_roll_interval()):
            self.randomize()
            self.sound.tone()

            self.last_roll_ms = self.current_ms
            self.last_tone_ms = self.current_ms


    def render(self):
        if self.dice_count == 1:
            # Second dice
            self.sprites[self.numbers[1] - 1].draw(self.display, 48, 16)

        elif self.dice_count == 2:
            # First dice
            self.sprites[self.numbers[0] - 1].draw(self.display, 23, 16)

            # Third dice
            self.sprites[self.numbers[2] - 1].draw(self.display, 73, 16)

        else:
            # First dice
            self.sprites[self.numbers[0] - 1].draw(self.display, 8, 16)

            # Second dice
            self.sprites[self.numbers[1] - 1].draw(self.display, 48, 16)

            # Third dice
            self.sprites[self.numbers[2] - 1].draw(self.display, 88, 16)


    def randomize(self):
        self.numbers = [randrange(1, 7) for _ in range(3)]


    def get_roll_interval(self):
        elapsed_ms = elapsed(self.current_ms, self.roll_start_ms)

        if elapsed_ms < ROLL_SLOWDOWN_MS:
            return ROLL_INTERVAL_MS

        progress = (elapsed_ms - ROLL_SLOWDOWN_MS) / (ROLL_DURATION_MS - ROLL_SLOWDOWN_MS)

        # Ease-out
        progress *= progress

        return int(ROLL_INTERVAL_MS + (ROLL_FINAL_INTERVAL_MS - ROLL_INTERVAL_MS) * progress)


if __name__ == '__main__':
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
