__NAME__ = "Racing Game"
__CATEGORY__ = "games"

from random import randrange

from apps.RacingGame.civilian import Civilian
from apps.RacingGame.racer import Racer
from core.app import PiconGame
from core.config import SCREEN_HEIGHT, SCREEN_WIDTH
from core.helper import has_not_elapsed
from core.input import Key

STARTING_INTERVAL = 50
MAX_CIVILLIANS = 3

ROAD_LINE_WIDTH = 20
ROAD_LINE_COUNT = 4  # 3 visible + 1 off-screen
ROAD_LINE_SPACING = 43  # round(128 / 3)
ROAD_LINE_CYCLE = ROAD_LINE_SPACING * ROAD_LINE_COUNT
ROAD_LINE_X = [11, 53, 96, 139]

NORMAL_SPEED_TONE = 200
NOS_SPEED_TONE = 220


class Main(PiconGame):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)
        self.input.set_debounce(100)

        self.racer = Racer()
        self.civillians = (Civilian(128, randrange(3)),
                           Civilian(182, randrange(3)),
                           Civilian(236, randrange(3)))
        self.interval = STARTING_INTERVAL
        self.nos_on = False

        self.road_lines = ROAD_LINE_X

        self.last_update_ms = self.current_ms


    def inputs(self):
        if self.input.is_pressed(Key.UP):
            self.racer.up()
        if self.input.is_pressed(Key.DOWN):
            self.racer.down()
        if self.input.is_pressed(Key.A):
            self.nos_on = True
        else:
            self.nos_on = False


    def update(self):
        self.sound.tone(NOS_SPEED_TONE if self.nos_on else NORMAL_SPEED_TONE)

        if has_not_elapsed(self.current_ms, self.last_update_ms, self.interval) and self.nos_on is False:
            return

        # Civillians
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

        # Road lines
        for i in range(len(self.road_lines)):
            if self.road_lines[i] <= -ROAD_LINE_WIDTH:
                self.road_lines[i] += ROAD_LINE_CYCLE
            else:
                self.road_lines[i] -= 1

        self.last_update_ms = self.current_ms


    def render(self):
        # Top and bottom lines
        self.display.fill_rect(0, 0, SCREEN_WIDTH, 4, 1)
        self.display.fill_rect(0, SCREEN_HEIGHT - 4, SCREEN_WIDTH, 4, 1)

        # Road lines
        for rl_x in self.road_lines:
            self.display.fill_rect(rl_x, 20, 22, 4, 1)
            self.display.fill_rect(rl_x, 40, 22, 4, 1)

        # Racer
        self.racer.draw(self.display, self.racer.x, self.racer.y)

        # Civillians
        for c in self.civillians:
            c.draw(self.display, c.x, c.y)


if __name__ == '__main__':
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
