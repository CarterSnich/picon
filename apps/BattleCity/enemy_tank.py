from random import choice

from apps.BattleCity.direction import Direction, DIRECTIONS
from apps.BattleCity.resources import ENEMY_TANK_N, ENEMY_TANK_E, ENEMY_TANK_S, ENEMY_TANK_W
from apps.BattleCity.tank import Tank
from core import randbool


class EnemyTank(Tank):

    def __init__(self, x, y, direction, speed=1):
        self.last_move_ms = 0
        sprites = {Direction.NORTH: ENEMY_TANK_N,
                   Direction.EAST: ENEMY_TANK_E,
                   Direction.SOUTH: ENEMY_TANK_S,
                   Direction.WEST: ENEMY_TANK_W}
        super().__init__(sprites, x, y, direction, speed)


    def update(self, current_ms, obstacles):
        will_change_direction = randbool()
        if will_change_direction:
            self.move(choice(DIRECTIONS), obstacles)
        else:
            self.move(self.direction, obstacles)
        self.last_move_ms = current_ms
