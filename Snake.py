
class Snake:

    def __init__(self):
        self.segments = [[52, 50], [56, 50], [60, 50]]
        self.direction = Direction.EAST
        
    def head(self):
        s = self.segments[-1]
        return s[0], s[1]
        
    def grow(self):
        x, y = self.head()
        
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
        self.grow()
        self.segments.pop(0)
    
    def set_direction(self, direction):
        self.direction = direction
        
            
        
        
            
    