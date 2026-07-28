from apps.PixelBlaster.shooter import Shooter
from apps.PixelBlaster.utils import get_row_y
from core import PiconGame, has_not_elapsed, randbool
from core.input import DPAD_UP, DPAD_DOWN, KEY_A

MAX_INTERVAL = 1000
MIN_INTERVAL = 150
MAX_PIXEL_WALL_WIDTH = 31
BULLET_ANIMATION_DURATION = 100
BULLET_SPEED = 8


class Main(PiconGame):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)
        self.input.set_debounce(100)

        self.interval = MAX_INTERVAL
        self.cleared_pixels = 0
        self.last_wall_move_ms = self.current_ms

        self.shooter = Shooter(8)
        self.has_fired = False
        self.last_shot_ms = None
        self.bullet_xy = [8, get_row_y(self.shooter.row)]

        self.pixel_wall = []


    def inputs(self):
        if self.input.is_pressed(KEY_A):
            self.has_fired = True

        if self.input.is_pressed(DPAD_UP):
            self.shooter.move(-1)
        elif self.input.is_pressed(DPAD_DOWN):
            self.shooter.move(1)


    def update(self):
        # Shooting animation
        if self.last_shot_ms:
            if has_not_elapsed(self.current_ms, self.last_shot_ms, BULLET_ANIMATION_DURATION):
                self.bullet_xy[0] += BULLET_SPEED
                self.sound.tone(500 - self.bullet_xy[0])
            else:
                self.sound.stop()
                self.bullet_xy = [8, get_row_y(self.shooter.row)]
                self.last_shot_ms = None

        # Player shoots
        if self.has_fired:
            self.has_fired = False

            self.sound.tone()
            self.bullet_xy = [8, get_row_y(self.shooter.row)]
            self.last_shot_ms = self.current_ms

            # Flip pixel if hit
            for i, row in enumerate(self.pixel_wall):
                if row[self.shooter.row]:
                    self.pixel_wall[i][self.shooter.row] = False
                    break

        # Remove top pixel wall when cleared
        if len(self.pixel_wall) and not any(self.pixel_wall[0]):
            self.pixel_wall.pop(0)
            self.cleared_pixels += 1

        # Update pixel wall
        interval = max(self.interval - self.cleared_pixels, MIN_INTERVAL)
        if has_not_elapsed(self.current_ms, self.last_wall_move_ms, interval):
            return

        # Check if pixel wall collision
        if len(self.pixel_wall) >= MAX_PIXEL_WALL_WIDTH:
            self.sound.stop()
            self.game_over()

        # Grow wall
        new_row = [randbool() for _ in range(16)]
        self.pixel_wall.append(new_row)

        self.last_wall_move_ms = self.current_ms


    def render(self):
        # Pixel wall
        w = len(self.pixel_wall)
        for i in range(w):
            row = self.pixel_wall[i]
            x = 128 - ((w - i) * 4)
            for j in range(16):
                y = j * 4
                self.display.fill_rect(x, y, 4, 4, row[j])

        # Shooting animation
        if self.last_shot_ms:
            self.display.fill_rect(self.bullet_xy[0], self.bullet_xy[1], 4, 4, 1)

        # Shooter
        self.shooter.draw(self.display)


if __name__ == '__main__':
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
