from time import ticks_ms, ticks_diff
from random import choice

from PicoGame import PicoGame
from games.BattleCity.Resources import BULLET


class Direction:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Tank:
    
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        
    def get_sprite(self):
        return self.sprites[self.direction]
    
    def is_colliding(self, obj_x, obj_y, obj_w, obj_h):
        return (
            self.x < obj_x + obj_w and
            self.x + 8 > obj_x and
            self.y < obj_y + obj_h and
            self.y + 8 > obj_y
        )
    
    def will_collide(self, obj_x, obj_y, obj_w, obj_h):
        self_x = self.x
        self_y = self.y
        
        if self.direction == Direction.NORTH:
            self_y -= 1
        elif self.direction == Direction.EAST:
            self_x += 1
        elif self.direction == Direction.SOUTH:
            self_y += 1
        elif self.direction == Direction.WEST:
            self_x -= 1
            
        return (
            self_x < obj_x + obj_w and
            self_x + 8 > obj_x and
            self_y < obj_y + obj_h and
            self_y + 8 > obj_y
        )
    
    
if __name__ == '__main__':
    from games.PicoBattleCity import BattleCity
    BattleCity().run()