from Racing.Resources import BUICK

class Civilian:
    SPRITE = BUICK
    WIDTH = 32
    HEIGHT = 10
    
    def __init__(self, x, y, speed=1):
        self.x = x
        self.y = y
        self.speed = speed
        
    def move(self):
        self.x -= self.speed
        

if __name__ == '__main__':
    from RacingGame import RacingGame
    RacingGame().run()