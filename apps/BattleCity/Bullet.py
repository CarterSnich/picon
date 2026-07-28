from apps.BattleCity.direction import Direction
from apps.BattleCity.resources import BULLET
from apps.BattleCity.tank import Tank
from core import GameObject


class Bullet(GameObject):

    def __init__(self, owner: Tank, speed=2):
        self.owner = owner
        self.direction = owner.direction
        self.speed = speed
        self.last_move_ms = 0

        tw = owner.sprite.width
        th = owner.sprite.height
        bw = BULLET.width
        bh = BULLET.height

        if self.direction == Direction.NORTH:
            x = owner.x + (tw - bw) // 2
            y = owner.y - bh
        elif self.direction == Direction.EAST:
            x = owner.x + tw
            y = owner.y + (th - bh) // 2
        elif self.direction == Direction.SOUTH:
            x = owner.x + (tw - bw) // 2
            y = owner.y + th
        else:  # Direction.WEST
            x = owner.x - bw
            y = owner.y + (th - bh) // 2

        super().__init__(BULLET, x, y)


    def move(self):
        x, y = self.direction
        self.x += x
        self.y += y


    def update(self):
        self.move()
