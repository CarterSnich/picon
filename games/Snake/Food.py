class Food:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def is_intersecting(self, x, y):
        return self.x == x and self.y == y
    
    def set_coordinates(self, x, y):
        self.x = x
        self.y = y
        
                        
if __name__ == '__main__':
    from games.SnakeGame import SnakeGame
    SnakeGame().run()