from core import GameObject

from apps.RacingGame.sprites import CIVILIAN

LANES_Y = (7, 27, 47)


class Civilian(GameObject):

    def __init__(self, x, lane):
        self.x: int = x
        self.y = LANES_Y[lane]
        super().__init__(CIVILIAN, self.x, self.y)


    def move(self):
        self.x -= 1


    def is_offscreen(self):
        return self.x + self.sprite.width <= 0


    def set_lane(self, lane):
        self.y = LANES_Y[lane]
