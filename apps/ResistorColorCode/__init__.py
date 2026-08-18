__NAME__ = "Resistor Color Code"
__CATEGORY__ = "tools"

from apps.ResistorColorCode.assets import PLUS_MINUS, OHMS
from apps.ResistorColorCode.values import BAND_COLORS, MULTIPLIER_COLORS, TOLERANCE_COLORS, TOLERANCE_VALUES, \
    MULTIPLIER_VALUES
from assets.menu_sprites import ARROW_LEFT, ARROW_RIGHT, ARROW_UP, ARROW_DOWN
from core import PiconApp
from core.input import Key


class Main(PiconApp):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

        self.num_of_bands = 4
        self.bands = [0, 0, 0, 0, 0]

        # 0 - num of bands selection
        # 1 - band colors selection
        # 2 - showing output
        self.state = 0
        self.current_band_index = 1

        self.output = None


    def inputs(self):

        if self.state == 0:
            if self.input.is_pressed(Key.A):
                self.state = 1
            elif self.input.is_pressed(Key.B):
                self.quit()
            elif self.input.is_pressed(Key.LEFT) or self.input.is_pressed(Key.RIGHT):
                self.num_of_bands = 9 - self.num_of_bands
                self.current_band_index = 1 if self.num_of_bands == 4 else 0
        elif self.state == 1:
            if self.input.is_pressed(Key.A):
                self.state = 2
            elif self.input.is_pressed(Key.B):
                self.state = 0
            elif self.input.is_pressed(Key.LEFT):
                n = (self.current_band_index - 1) % 5
                if self.num_of_bands == 4 and n == 0:
                    n = 4
                self.current_band_index = n
            elif self.input.is_pressed(Key.RIGHT):
                n = (self.current_band_index + 1) % 5
                if self.num_of_bands == 4 and n == 0:
                    n = 1
                self.current_band_index = n
            elif self.input.is_pressed(Key.UP):
                if self.current_band_index == 4:
                    self.bands[4] = (self.bands[4] - 1) % 8
                else:
                    self.bands[self.current_band_index] = (self.bands[self.current_band_index] - 1) % 10
            elif self.input.is_pressed(Key.DOWN):
                if self.current_band_index == 4:
                    self.bands[4] = (self.bands[4] + 1) % 8
                else:
                    self.bands[self.current_band_index] = (self.bands[self.current_band_index] + 1) % 10
        else:
            if self.input.is_pressed(Key.B):
                self.state = 1
                self.output = None


    def update(self):
        if self.state == 2 and self.output is None:
            band_value = 0
            if self.num_of_bands == 5:
                band_value = self.bands[0] * 100
            band_value += self.bands[1] * 10
            band_value += self.bands[2]

            # multiplier
            multiplier = 10 ** MULTIPLIER_VALUES[self.bands[3]]
            band_value = band_value * multiplier

            if band_value >= 1_000_000:
                value = f"{band_value // 1_000_000}M"
            elif band_value >= 1000:
                value = f"{band_value // 1000}K"
            else:
                value = f"{band_value:,}"
            tolerance = f"{TOLERANCE_VALUES[self.bands[4]]}%"

            self.output = (value, tolerance)


    def render(self):
        if self.state == 2:
            self.display.center_text(f"{self.output[0]} Ohms")
            x, y = self.display.center_text(self.output[1], offset_x=4, offset_y=9)
            PLUS_MINUS.draw(self.display, x - 8, y)
        else:
            # Number of bands
            self.display.text(f"{self.num_of_bands} Band", 40, 18, 1)
            if self.state == 0:
                ARROW_LEFT.draw(self.display, 30, 18)
                ARROW_RIGHT.draw(self.display, 90, 18)

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
            for _ in range(2 if self.num_of_bands == 4 else 3):
                self.display.text(BAND_COLORS[self.bands[i]], text_x + 26 * x, 38, 1)
                if self.current_band_index == i and self.state == 1:
                    ARROW_UP.draw(self.display, arrow_x + 26 * x, 29)
                    ARROW_DOWN.draw(self.display, arrow_x + 26 * x, 46)

                i += 1
                x += 1

            # Multiplier
            i += 1
            self.display.text(MULTIPLIER_COLORS[self.bands[3]], text_x + 26 * x, 38, 1)
            if self.current_band_index == 3 and self.state == 1:
                ARROW_UP.draw(self.display, arrow_x + 26 * x, 29)
                ARROW_DOWN.draw(self.display, arrow_x + 26 * x, 46)

            #  Tolerance
            i += 1
            x += 1
            self.display.text(TOLERANCE_COLORS[self.bands[4]], text_x + 26 * x, 38, 1)
            if self.current_band_index == 4 and self.state == 1:
                ARROW_UP.draw(self.display, arrow_x + 26 * x, 29)
                ARROW_DOWN.draw(self.display, arrow_x + 26 * x, 46)


if __name__ == '__main__':
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
