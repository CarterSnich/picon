from games.Racing.Resources import RACER
from games.Racing.Lanes import LANES


class Racer:
    SPRITE = RACER
    WIDTH = 20
    HEIGHT = 10
    
    def __init__(self, lane = 1):
        self.lane = lane
        self.x = 0
        self.y = LANES[lane]
    
    def is_colliding(self, obj_x, obj_y, obj_w, obj_h):
        return (
            self.x < obj_x + obj_w and
            self.x + self.WIDTH > obj_x and
            self.y < obj_y + obj_h and
            self.y + self.HEIGHT > obj_y
        )
    
    def up(self):
        self.lane -= 1
        self.y = LANES[self.lane]
        
    def down(self):
        self.lane += 1
        self.y = LANES[self.lane]
        

if __name__ == '__main__':
    from games.RacingGame import RacingGame
    RacingGame().run()