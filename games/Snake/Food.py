from time import ticks_ms, ticks_diff

class Food:
    
    BLINK_INTERVAL = 100
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blink_state = True
        self.last_blink_ms = ticks_ms()
    
    def is_intersecting(self, x, y):
        return self.x == x and self.y == y
    
    def set_coordinates(self, x, y):
        self.x = x
        self.y = y
    
    def update(self):
        tick = ticks_ms()
        if ticks_diff(tick, self.last_blink_ms) >= self.BLINK_INTERVAL:
            self.last_blink_ms = tick
            self.blink_state = not self.blink_state
                        
if __name__ == '__main__':
    from games.SnakeGame import SnakeGame
    SnakeGame().run()