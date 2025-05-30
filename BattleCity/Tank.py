
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

class Direction:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Tank:
    bullets = []
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get_sprite(self):
        return self.sprites[self.direction]
    
    def update(self):
        for b in self.bullets[:]:
            if b[2] == Direction.NORTH:
                if b[1] <= 0:
                    self.bullets.remove(b)
                else:
                    b[1] -= 1
            elif b[2] == Direction.EAST:
                if b[0] >= SCREEN_WIDTH:
                    self.bullets.remove(b)
                else:
                    b[0] += 1
            elif b[2] == Direction.SOUTH:
                if b[1] >= SCREEN_HEIGHT:
                    self.bullets.remove(b)
                else:
                    b[1] += 1
            elif b[2] == Direction.WEST:
                if b[0] <= 0:
                    self.bullets.remove(b)
                else:
                    b[0] -= 1
                
    
    def up(self):
        if self.y > 0:
            self.y -= 1
        self.direction = Direction.NORTH
    
    def right(self):
        if self.x+8 < SCREEN_WIDTH:
            self.x += 1
        self.direction = Direction.EAST
    
    def down(self):
        if self.y+8 < SCREEN_HEIGHT:
            self.y += 1
        self.direction = Direction.SOUTH
    
    def left(self):
        if self.x > 0:
            self.x -= 1
        self.direction = Direction.WEST
    
    def fire(self):
        if len(self.bullets) < 3:
            if self.direction == Direction.NORTH:
                self.bullets.append([self.x+4, self.y-4, self.direction])
            elif self.direction == Direction.EAST:
                self.bullets.append([self.x+4, self.y+4, self.direction])
            elif self.direction == Direction.SOUTH:
                self.bullets.append([self.x+4, self.y+4, self.direction])
            elif self.direction in (Direction.EAST, Direction.WEST):
                self.bullets.append([self.x-4, self.y+4, self.direction])
                
        