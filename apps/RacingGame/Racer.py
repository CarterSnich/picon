from core.sprite import GameObject

from apps.RacingGame.sprites import RACER

LANES_Y = (8, 28, 48)


class Racer(GameObject):

    def __init__(self, lane=1):
        self.lane = lane
        self.x = 0
        self.y = LANES_Y[lane]
        super().__init__(RACER, self.x, self.y)


    def move(self, n):
        self.lane += n
        self.y = LANES_Y[self.lane]


    def up(self):
        if self.lane > 0:
            self.move(-1)


    def down(self):
        if self.lane < 2:
            self.move(1)


if __name__ == '__main__':
    from core import Display, Input, Sound
    from apps.RacingGame import Main

    Main(Display(), Input(), Sound()).run()
