from apps.BattleCity.direction import Direction
from apps.BattleCity.resources import PLAYER_TANK_N, PLAYER_TANK_E, PLAYER_TANK_S, PLAYER_TANK_W
from apps.BattleCity.tank import Tank


class PlayerTank(Tank):

    def __init__(self, x, y, direction=Direction.NORTH, speed=1):
        sprites = {Direction.NORTH: PLAYER_TANK_N,
                   Direction.EAST: PLAYER_TANK_E,
                   Direction.SOUTH: PLAYER_TANK_S,
                   Direction.WEST: PLAYER_TANK_W}

        super().__init__(sprites, x, y, direction, speed)
