from PicoGame import PicoGame
from games.BattleCity.Tank import Direction
from games.BattleCity.Resources import BULLET

class Bullet:
    sprite = BULLET
    bullet_speed = 2
    
    def __init__(self, x, y, direction, from_player = False):
        self.x = x
        self.y = y
        self.direction = direction
        self.from_player = from_player
    
    def get_sprite(self):
        return self.sprite
    
    # returns True if out of bounds on the screen
    def update(self):
        if self.direction == Direction.NORTH:
            if self.y <= 0:
                return True
            self.y -= self.bullet_speed
        elif self.direction == Direction.EAST:
            if self.x >= PicoGame.SCREEN_WIDTH:
                return True
            self.x += self.bullet_speed
        elif self.direction == Direction.SOUTH:
            if self.y >= PicoGame.SCREEN_HEIGHT:
                return True
            self.y += self.bullet_speed
        elif self.direction == Direction.WEST:
            if self.x <= 0:
                return True
            self.x -= self.bullet_speed
        return False
    
    def is_colliding(self, tank_x, tank_y, tank_w, tank_h):
        return (
            self.x < tank_x + tank_w and
            self.x + 2 > tank_x and
            self.y < tank_y + tank_h and
            self.y + 2 > tank_y
        )
    
    
if __name__ == '__main__':
    from games.PicoBattleCity import BattleCity
    BattleCity().run()
    
    
if __name__ == '__main__':
    from games.PicoBattleCity import BattleCity
    BattleCity().run()
