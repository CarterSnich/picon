from random import choice, randint
from time import ticks_diff, ticks_ms

from BattleCity.Tank import Tank, SpawnPoint, Direction
from PicoGame import PicoGame
from BattleCity.Resources import ENEMY_TANK_N, ENEMY_TANK_E, ENEMY_TANK_S, ENEMY_TANK_W

class EnemyTank(Tank):
    sprites = [
        ENEMY_TANK_N,
        ENEMY_TANK_E,
        ENEMY_TANK_S,
        ENEMY_TANK_W
    ]
    
    def __init__(self, spawn_point = None, x = 0, y = 0, direction = Direction.NORTH):
        self.displacement = 8
        self.delay_next_shot_ms = randint(500, 1000)
        self.last_shot_ms = ticks_ms()
        self.last_displacement_ms = ticks_ms()
        
        if spawn_point == SpawnPoint.NW:
            x, y = 4, 4
            direction = choice([Direction.EAST, Direction.SOUTH])
        elif spawn_point == SpawnPoint.NE:
            x, y = PicoGame.SCREEN_WIDTH - 8, 8
            direction = choice([Direction.WEST, Direction.SOUTH])
        elif spawn_point == SpawnPoint.SE:
            x, y = PicoGame.SCREEN_WIDTH - 8, PicoGame.SCREEN_HEIGHT - 8
            direction = choice([Direction.NORTH, Direction.WEST])
        elif spawn_point == SpawnPoint.SW:
            x, y = 4, PicoGame.SCREEN_HEIGHT- 8
            direction = choice([Direction.NORTH, Direction.EAST])
        else:
            super().__init__(x, y, direction)
            return
            
        super().__init__(x, y, direction)
    
    def change_direction(self, remove_current = True):
        directions = [
            Direction.NORTH, Direction.EAST,
            Direction.SOUTH, Direction. WEST
        ]
        if remove_current:
            directions.remove(self.direction)
        self.direction = choice(directions)
    
    def update(self, player):
        super().update()
        
        if ticks_diff(ticks_ms(), self.last_shot_ms) >= self.delay_next_shot_ms:
            self.shoot()
            self.last_shot_ms = ticks_ms()
            self.delay_next_shot_ms = randint(300, 1000)
        
        if ticks_diff(ticks_ms(), self.last_displacement_ms) < 300:
            return
        
        if self.will_collide(player.x, player.y, 8, 8):
            self.change_direction(self.direction)
            self.displacement = 0
            self.last_displacement_ms = ticks_ms()
            return
        elif self.displacement < 8:
            self.last_displacement_ms = ticks_ms()
            if self.direction == Direction.NORTH:
                if self.y-4 > 0:
                    self.displacement += 1
                    self.y -= 1
                else:
                    self.displacement = 0
                    self.change_direction()
            elif self.direction == Direction.EAST:
                if self.x+4 < PicoGame.SCREEN_WIDTH:
                    self.displacement += 1
                    self.x += 1
                else:
                    self.displacement = 0
                    self.change_direction()
            elif self.direction == Direction.SOUTH:
                if self.y+4 < PicoGame.SCREEN_HEIGHT:
                    self.displacement += 1
                    self.y += 1
                else:
                    self.displacement = 0
                    self.change_direction()
            elif self.direction == Direction.WEST:
                if self.x-4 > 0:
                    self.displacement += 1
                    self.x -= 1
                else:
                    self.displacement = 0
                    self.change_direction()
        else:
            self.displacement = 0
            self.change_direction(False)
            
        

if __name__ == '__main__':
    from PicoBattleCity import battle_city
    battle_city()