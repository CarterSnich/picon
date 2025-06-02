from time import ticks_diff, ticks_ms

from PicoGame import PicoGame
from BattleCity.Tank import Direction, Tank
from BattleCity.Resources import PLAYER_TANK_N, PLAYER_TANK_E, PLAYER_TANK_S, PLAYER_TANK_W


class PlayerTank(Tank):
    sprites = [
        PLAYER_TANK_N,
        PLAYER_TANK_E,
        PLAYER_TANK_S,
        PLAYER_TANK_W
    ]
    
    def __init__(self, x, y, direction = Direction.NORTH):
        super().__init__(x, y, direction)
        
    def move(self, direction, enemy_tanks):
        self.direction = direction
        
        # enemy tanks collision check
        for e in enemy_tanks:
            if self.will_collide(e.x, e.y, 8, 8):
                return
            
        if direction == Direction.NORTH and self.y-4 > 0:
            self.y -= 1
        elif direction == Direction.EAST and self.x+4 < PicoGame.SCREEN_WIDTH:
            self.x += 1
        elif direction == Direction.SOUTH and self.y+4 < PicoGame.SCREEN_HEIGHT:
            self.y += 1
        elif direction == Direction.WEST and self.x-4 > 0:
            self.x -= 1
    
    
if __name__ == '__main__':
    from PicoBattleCity import battle_city
    battle_city()
        