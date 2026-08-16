__NAME__ = "Dino Game"
__CATEGORY__ = "games"

from random import randrange

from apps.DinoGame.assets import REPEAT_ICON
from apps.DinoGame.dino import Dino
from apps.DinoGame.obstacles import Trees, BigTree
from core import PiconGame, has_not_elapsed, elapsed, has_elapsed, GameObject
from core.input import Key

INITIAL_INTERVAL_MS = 10
MIN_INTERVAL_MS = 1
DINO_UPDATE_INTERVAL_MS = 50

OBSTACLE_START_X = 128
OBSTACLES = (Trees(OBSTACLE_START_X), BigTree(OBSTACLE_START_X))


class Main(PiconGame):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

        self.dino = Dino(2, 36)
        self.current_obstacle: GameObject = OBSTACLES[randrange(2)]

        self.start_ms = self.current_ms
        self.last_interval_ms = self.current_ms
        self.dino_last_update_ms = self.current_ms

        self.randomize_obstacle()


    def inputs(self):
        if self.dino.is_dead:
            if self.input.is_pressed(Key.A):
                self.reset()
            elif self.input.is_pressed(Key.B):
                self.quit()
        elif not self.dino.is_jumping:
            if self.input.is_pressed(Key.A) or self.input.is_pressed(Key.UP):
                self.dino.jump()


    def update(self):
        # Skip update if game is over
        if self.dino.is_dead:
            return

        # Check Dino collision
        if self.dino.is_colliding(self.current_obstacle):
            self.dino.die()
            return

        # Dino update
        if has_elapsed(self.current_ms, self.dino_last_update_ms, DINO_UPDATE_INTERVAL_MS):
            self.dino.update(self.current_ms)
            self.dino_last_update_ms = self.current_ms

        # Obstacle update
        elapsed_minutes = elapsed(self.current_ms, self.start_ms) // 60_000
        interval = max(INITIAL_INTERVAL_MS - elapsed_minutes, MIN_INTERVAL_MS)
        if has_not_elapsed(self.current_ms, self.last_interval_ms, interval):
            return
        self.last_interval_ms = self.current_ms

        if self.current_obstacle.is_offscreen_left():
            self.randomize_obstacle()
        self.current_obstacle.x -= 1


    def render(self):
        self.display.line(0, 58, 128, 58, 1)
        self.dino.draw(self.display)
        self.current_obstacle.draw(self.display, key=0)

        if self.dino.is_dead:
            self.display.center_text("GAME OVER", 28, 6)
            REPEAT_ICON.draw(self.display, 46, 21)


    def randomize_obstacle(self):
        self.current_obstacle = OBSTACLES[randrange(2)]
        self.current_obstacle.x = OBSTACLE_START_X


    def reset(self):
        self.randomize_obstacle()
        self.dino.reset()
        self.start_ms = self.current_ms


if __name__ == '__main__':
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
