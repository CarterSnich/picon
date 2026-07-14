from time import ticks_diff, ticks_ms

from core.config import SCREEN_WIDTH, SCREEN_HEIGHT

from .tank import Direction, Tank
from .bullet import Bullet
from .resources import PLAYER_TANK_N, PLAYER_TANK_E, PLAYER_TANK_S, PLAYER_TANK_W

SHOOT_INTERVAL_MS = 300


class PlayerTank(Tank):
    sprites = [
        PLAYER_TANK_N,
        PLAYER_TANK_E,
        PLAYER_TANK_S,
        PLAYER_TANK_W
    ]

    direction = Direction.NORTH
    last_shot_ms = -1
    shots = 0


    def __init__(self, x, y, direction=Direction.NORTH):
        super().__init__(x, y, direction)


    def move(self, direction, enemy_tanks):
        self.direction = direction

        # enemy tanks collision check
        for e in enemy_tanks:
            if self.will_collide(e.x, e.y, 8, 8):
                return

        if direction == Direction.NORTH and self.y - 4 > 0:
            self.y -= 1
        elif direction == Direction.EAST and self.x + 4 < SCREEN_WIDTH:
            self.x += 1
        elif direction == Direction.SOUTH and self.y + 4 < SCREEN_HEIGHT:
            self.y += 1
        elif direction == Direction.WEST and self.x - 4 > 0:
            self.x -= 1


    def can_shoot(self, ms):
        delta = ticks_diff(ms, self.last_shot_ms)
        return self.shots < 3 and delta >= self.shoot_cooldown_ms


    def shoot(self):
        if self.can_shoot():
            self.shots += 1
            self.last_shot_ms = ticks_ms()
            return Bullet(self.x, self.y, self.direction, True)
        return False


    def update(self):
        ...
