from apps.DVDLogo.assets import DVD_LOGO
from core import PiconApp, has_not_elapsed, SCREEN_WIDTH, SCREEN_HEIGHT
from core.input import Key

DEFAULT_UPDATE_INTERVAL_MS = 250


class Main(PiconApp):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

        self.x = 0
        self.y = 0
        self.velocity = [1, 1]

        self.is_paused = False
        self.is_inverted = False

        self.update_inverval_ms = DEFAULT_UPDATE_INTERVAL_MS
        self.last_update_ms = self.current_ms


    def inputs(self):
        if self.input.is_pressed(Key.A):
            self.is_paused = not self.is_paused
        elif self.input.is_pressed(Key.X):
            self.invert()
        elif self.input.is_pressed(Key.UP):
            self.update_inverval_ms += 50
        elif self.input.is_pressed(Key.DOWN) and self.update_inverval_ms > 0:
            self.update_inverval_ms -= 50
        elif self.input.is_pressed(Key.Y):
            self.update_inverval_ms = DEFAULT_UPDATE_INTERVAL_MS
        elif self.input.is_pressed(Key.B):
            self.quit()


    def update(self):
        if self.is_paused:
            return

        if has_not_elapsed(self.current_ms, self.last_update_ms, self.update_inverval_ms):
            return
        self.last_update_ms = self.current_ms

        if self.x + DVD_LOGO.width >= SCREEN_WIDTH:
            self.velocity[0] = -1
        elif self.x <= 0:
            self.velocity[0] = 1

        if self.y + DVD_LOGO.height >= SCREEN_HEIGHT:
            self.velocity[1] = -1
        elif self.y <= 0:
            self.velocity[1] = 1

        self.x += self.velocity[0]
        self.y += self.velocity[1]


    def render(self):
        DVD_LOGO.draw(self.display, self.x, self.y)


    def invert(self):
        self.is_inverted = not self.is_inverted
        self.display.invert(self.is_inverted)


if __name__ == '__main__':
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
