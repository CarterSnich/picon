from time import ticks_ms, ticks_diff

from games.Snake.Direction import Direction

class Snake:
    MOVEMENT_INTERVAL = 100

    def __init__(self, head_x, head_y):
        self.segments = [[head_x, head_y], [head_x-4, head_y], [head_x-8, head_y]]
        self.direction = Direction.EAST
        self.last_move_ms = self.MOVEMENT_INTERVAL
        
    def head(self):
        return self.segments[0]
    
    def tail(self):
        return self.segments[-1]
        
    def grow(self):
        tail = self.tail()
        x, y = tail[0], tail[1]
        
        if self.direction == Direction.NORTH:
            y -= 4
        elif self.direction == Direction.EAST:
            x += 4
        elif self.direction == Direction.SOUTH:
            y += 4
        elif self.direction == Direction.WEST:
            x -= 4
        self.segments.append([x, y])
    
    def move(self):
        head = self.head()
        x, y = head[0], head[1]
        
        if self.direction == Direction.NORTH:
            y -= 4
        elif self.direction == Direction.EAST:
            x += 4
        elif self.direction == Direction.SOUTH:
            y += 4
        elif self.direction == Direction.WEST:
            x -= 4
            
        self.segments.insert(0, [x, y])
        self.segments.pop()
        self.last_move_ms = ticks_ms()
        
    def can_move(self):
        movement_delta = ticks_diff(ticks_ms(), self.last_move_ms)
        return movement_delta >= self.MOVEMENT_INTERVAL
            
    def set_direction(self, direction):
        self.direction = direction
        
    def intersecting_self(self):
        return self.head() in self.segments[1:]
            
                      
if __name__ == '__main__':
    from games.SnakeGame import SnakeGame
    SnakeGame().run()
    
            
    