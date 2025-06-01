from PicoGame import PicoGame
import framebuf

class SpawnPoint:
    NW = 0
    NE = 1
    SE = 2
    SW = 3

class Direction:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Bullet:
    sprite = framebuf.FrameBuffer(
        bytearray([
            0b11,
            0b11,
        ]),
        2, 2, framebuf.MONO_VLSB
    )
    bullet_speed = 2
    
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        
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
    
    
class Tank:
    
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.bullets = []
        
    def get_sprite(self):
        return self.sprites[self.direction]
    
    def update(self):
        for b in self.bullets[:]:
            if b.update(): self.bullets.remove(b) 
                
    
    def render(self, game):
        game.blit(self.get_sprite(), self.x-4, self.y-4)
        for b in self.bullets:
            game.blit(b.sprite, b.x, b.y)
            
    def shoot(self):
        if len(self.bullets) < 3:
            if self.direction == Direction.NORTH:
                self.bullets.append(Bullet(self.x-1, self.y-6, self.direction))
            elif self.direction == Direction.EAST:
                self.bullets.append(Bullet(self.x+4, self.y-1, self.direction))
            elif self.direction == Direction.SOUTH:
                self.bullets.append(Bullet(self.x-1, self.y+4, self.direction))
            elif self.direction == Direction.WEST:
                self.bullets.append(Bullet(self.x-6, self.y-1, self.direction))
    
    def will_collide(self, enemy_x, enemy_y, enemy_w, enemy_h):
        self_x = self.x
        self_y = self.y
        
        if self.direction == Direction.NORTH:
            self_y -= 1
        elif self.direction == Direction.EAST:
            self_x += 1
        elif self.direction == Direction.SOUTH:
            self_y += 1
        elif self.direction == Direction.WEST:
            self_x -= 1
            
        return (
            self_x < enemy_x + enemy_w and
            self_x + 8 > enemy_x and
            self_y < enemy_y + enemy_h and
            self_y + 8 > enemy_y
        )
        
        

if __name__ == '__main__':
    from PicoBattleCity import battle_city
    battle_city()