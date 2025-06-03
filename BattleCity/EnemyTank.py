from random import choice, randint
from time import ticks_diff, ticks_ms

from PicoGame import PicoGame
from BattleCity.Tank import Tank, Direction
from BattleCity.Bullet import Bullet
from BattleCity.Resources import ENEMY_TANK_N, ENEMY_TANK_E, ENEMY_TANK_S, ENEMY_TANK_W

class EnemyTank(Tank):
    sprites = [
        ENEMY_TANK_N,
        ENEMY_TANK_E,
        ENEMY_TANK_S,
        ENEMY_TANK_W
    ]
    
    movement_delay_ms = 100
    min_shot_interval_ms = 750
    max_shot_interval_ms = 1000
    
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.displacement = 0
        self.displacement_length = 8
        self.next_shot_ms = randint(self.min_shot_interval_ms, self.max_shot_interval_ms)
        self.last_shot_ms = ticks_ms()
        self.last_move_ms = ticks_ms()
        
    
    def update(self):
        self.move()
    
    def move(self):
        if ticks_diff(ticks_ms(), self.last_move_ms) < self.movement_delay_ms:
            return
        
        if self.displacement >= self.displacement_length:
            self.change_direction()
            
        if self.direction == Direction.NORTH:
            if self.y-4 > 0:
                self.displacement += 1
                self.y -= 1
                self.last_move_ms = ticks_ms()
            else:
                self.change_direction()
        elif self.direction == Direction.EAST:
            if self.x+4 < PicoGame.SCREEN_WIDTH:
                self.displacement += 1
                self.x += 1
                self.last_move_ms = ticks_ms()
            else:
                self.change_direction()
        elif self.direction == Direction.SOUTH:
            if self.y+4 < PicoGame.SCREEN_HEIGHT:
                self.displacement += 1
                self.y += 1
                self.last_move_ms = ticks_ms()
            else:
                self.change_direction()
        elif self.direction == Direction.WEST:
            if self.x-4 > 0:
                self.displacement += 1
                self.x -= 1
                self.last_move_ms = ticks_ms()
            else:
                self.change_direction()
     
    def change_direction(self, exclude_current = True):
        directions = [
            Direction.NORTH, Direction.EAST,
            Direction.SOUTH, Direction. WEST
        ]
        if exclude_current:
            directions.remove(self.direction)
        self.displacement = 0
        self.displacement_length = randint(8, 32)
        self.direction = choice(directions)
    
    def can_shoot(self):
        if ticks_diff(ticks_ms(), self.last_shot_ms) >= self.next_shot_ms:
            return True
        return False
    
    def shoot(self):
        if self.can_shoot():        
            self.last_shot_ms = ticks_ms()
            self.next_shot_ms = randint(self.min_shot_interval_ms, self.max_shot_interval_ms)
            return Bullet(self.x, self.y, self.direction)
        return False


if __name__ == '__main__':
    from PicoBattleCity import battle_city
    battle_city()