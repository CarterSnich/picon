from Racing.Resources import SPORTS_CAR


class Racer:
    SPRITE = SPORTS_CAR
    WIDTH = 32
    HEIGHT = 10
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def is_colliding(self, obj_x, obj_y, obj_w, obj_h):
        return (
            self.x < obj_x + obj_w and
            self.x + self.WIDTH > obj_x and
            self.y < obj_y + obj_h and
            self.y + self.HEIGHT > obj_y
        )
        

if __name__ == '__main__':
    from RacingGame import RacingGame
    RacingGame().run()