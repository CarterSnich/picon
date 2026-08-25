__NAME__ = "Resistor Color Code"
__CATEGORY__ = "tools"

from apps.ResistorColorCode.assets import *
from apps.ResistorColorCode.values import *
from assets.menu_sprites import ARROW_LEFT, ARROW_RIGHT, ARROW_UP, ARROW_DOWN
from core import PiconApp
from core.input import Key


class Main(PiconApp):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

        self.num_of_bands = 4
        self.bands = [0, 0, 0, 0, 0]

        self.current_band_index = 1

        self.is_changed = True
        self.output = None


    def inputs(self):
        if self.input.is_pressed(Key.A):
            self.num_of_bands = 9 - self.num_of_bands
            self.current_band_index = 1 if self.num_of_bands == 4 else 0
            self.bands = [0, 0, 0, 0, 0]
            self.is_changed = True
        elif self.input.is_pressed(Key.LEFT):
            n = (self.current_band_index - 1) % 5
            if self.num_of_bands == 4 and n == 0:
                n = 4
            self.current_band_index = n
            self.is_changed = True
        elif self.input.is_pressed(Key.RIGHT):
            n = (self.current_band_index + 1) % 5
            if self.num_of_bands == 4 and n == 0:
                n = 1
            self.current_band_index = n
            self.is_changed = True
        elif self.input.is_pressed(Key.UP):
            if self.current_band_index == 4:
                self.bands[4] = (self.bands[4] - 1) % 8
            else:
                self.bands[self.current_band_index] = (self.bands[self.current_band_index] - 1) % 10
            self.is_changed = True
        elif self.input.is_pressed(Key.DOWN):
            if self.current_band_index == 4:
                self.bands[4] = (self.bands[4] + 1) % 8
            else:
                self.bands[self.current_band_index] = (self.bands[self.current_band_index] + 1) % 10
            self.is_changed = True
        elif self.input.is_pressed(Key.B):
            self.quit()


    def update(self):
        if self.is_changed:
            band_value = 0
            if self.num_of_bands == 5:
                band_value = self.bands[0] * 100
            band_value += self.bands[1] * 10
            band_value += self.bands[2]

            # multiplier
            multiplier = 10 ** MULTIPLIER_VALUES[self.bands[3]]
            band_value = band_value * multiplier

            if band_value >= 1_000_000:
                value = f"{band_value / 1_000_000:g}M"
            elif band_value >= 1000:
                value = f"{band_value / 1000:g}K"
            else:
                value = f"{band_value:g}"
            tolerance = f"{TOLERANCE_VALUES[self.bands[4]]}%"

            self.output = (value, tolerance)

            self.is_changed = False


    def render(self):
        y = 8
        # Number of bands
        self.display.text(f"{self.num_of_bands} Band", 40, y, 1)

        # Bands
        if self.num_of_bands == 4:
            i = 1
            text_x = 13
            arrow_x = 21
        else:
            i = 0
            text_x = 0
            arrow_x = 8

        x = 0
        y = 28
        for _ in range(2 if self.num_of_bands == 4 else 3):
            self.display.text(BAND_COLORS[self.bands[i]], text_x + 26 * x, y, 1)
            if self.current_band_index == i:
                ARROW_UP.draw(self.display, arrow_x + 26 * x, y - 9)
                ARROW_DOWN.draw(self.display, arrow_x + 26 * x, y + 8)
            i += 1
            x += 1

        # Multiplier
        i += 1
        self.display.text(MULTIPLIER_COLORS[self.bands[3]], text_x + 26 * x, y, 1)
        if self.current_band_index == 3:
            ARROW_UP.draw(self.display, arrow_x + 26 * x, y - 9)
            ARROW_DOWN.draw(self.display, arrow_x + 26 * x, y + 8)

        #  Tolerance
        i += 1
        x += 1
        self.display.text(TOLERANCE_COLORS[self.bands[4]], text_x + 26 * x, y, 1)
        if self.current_band_index == 4:
            ARROW_UP.draw(self.display, arrow_x + 26 * x, y - 9)
            ARROW_DOWN.draw(self.display, arrow_x + 26 * x, y + 8)

        self.display.center_text(f"{self.output[0]} Ohms", offset_y=18)
        x, y = self.display.center_text(self.output[1], offset_x=4, offset_y=27)
        PLUS_MINUS.draw(self.display, x - 8, y)


if __name__ == '__main__':
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
