from random import randrange
from time import ticks_diff

from core.app import PiconGame
from core.config import SCREEN_HEIGHT, SCREEN_WIDTH
from core.input import DPAD_UP, DPAD_DOWN, KEY_A

from apps.RacingGame.racer import Racer
from apps.RacingGame.civilian import Civilian

ROAD_LINES_Y = (10, 52, 94)
STARTING_INTERVAL = 50
MAX_CIVILLIANS = 3


class Main(PiconGame):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

        self.racer = Racer()
        self.civillians = (
            Civilian(128, randrange(3)),
            Civilian(182, randrange(3)),
            Civilian(236, randrange(3))
        )
        self.interval = STARTING_INTERVAL
        self.nos_on = False

        self.last_update_ms = self.current_ms


    def inputs(self):
        if self.input.is_pressed(DPAD_UP):
            self.racer.up()
        if self.input.is_pressed(DPAD_DOWN):
            self.racer.down()
        if self.input.is_pressed(KEY_A):
            self.nos_on = True
        else:
            self.nos_on = False


    def update(self):
        if ticks_diff(self.current_ms, self.last_update_ms) < self.interval and self.nos_on is False:
            return

        for c in self.civillians:
            c.move()
            if c.is_colliding(self.racer):
                self.game_over()
                return

            if c.is_offscreen():
                c.x = 148
                c.set_lane(randrange(3))
                if self.interval:
                    self.interval -= 1

        self.last_update_ms = self.current_ms


    def render(self):
        # Top and bottom lines
        self.display.fill_rect(0, 0, SCREEN_WIDTH, 4, 1)
        self.display.fill_rect(0, SCREEN_HEIGHT - 4, SCREEN_WIDTH, 4, 1)

        # Road lines
        for rl_x in ROAD_LINES_Y:
            self.display.fill_rect(rl_x, 20, 21, 4, 1)
            self.display.fill_rect(rl_x, 40, 21, 4, 1)

        # Racer
        self.racer.draw(self.display, self.racer.x, self.racer.y)

        # Civillians
        for c in self.civillians:
            c.draw(self.display, c.x, c.y)


if __name__ == '__main__':
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
