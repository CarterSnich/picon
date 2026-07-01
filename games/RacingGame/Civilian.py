from games.RacingGame.Resources import CIVILIAN

class Civilian:
    SPRITE = CIVILIAN
    WIDTH = 20
    HEIGHT = 12
    
    def __init__(self, x, y, speed=1):
        self.x = x
        self.y = y
        self.speed = speed
        
    def move(self):
        self.x -= self.speed
        

if __name__ == '__main__':
    from games.RacingGame.__init__ import RacingGame
    RacingGame().run()