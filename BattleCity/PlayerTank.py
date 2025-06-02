import framebuf
from time import ticks_diff, ticks_ms
from BattleCity.Tank import Direction, Tank
from PicoGame import PicoGame

NORTH = framebuf.FrameBuffer(
    bytearray([
        0b00011000,
        0b00011000,
        0b11111111,
        0b11111111,
        0b11111111,
        0b11111111,
        0b11111111,
        0b11111111,
    ]),
    8, 8, framebuf.MONO_HLSB
)
EAST = framebuf.FrameBuffer(
    bytearray([
        0b11111100,
        0b11111100,
        0b11111100,
        0b11111111,
        0b11111111,
        0b11111100,
        0b11111100,
        0b11111100,
    ]),
    8, 8, framebuf.MONO_HLSB
)
SOUTH = framebuf.FrameBuffer(
    bytearray([
        0b11111111,
        0b11111111,
        0b11111111,
        0b11111111,
        0b11111111,
        0b11111111,
        0b00011000,
        0b00011000,
    ]),
    8, 8, framebuf.MONO_HLSB
)
WEST = framebuf.FrameBuffer(
    bytearray([
        0b00111111,
        0b00111111,
        0b00111111,
        0b11111111,
        0b11111111,
        0b00111111,
        0b00111111,
        0b00111111,
    ]),
    8, 8, framebuf.MONO_HLSB
)


class PlayerTank(Tank):
    
    sprites = [ NORTH, EAST, SOUTH, WEST ]
    
    def __init__(self, x, y, direction = Direction.NORTH):
        super().__init__(x, y, direction)
        
    def move(self, direction, enemy_tanks):
        self.direction = direction
        
        # enemy tanks collision check
        for e in enemy_tanks:
            if self.will_collide(e.x, e.y, 8, 8):
                return
            
        if direction == Direction.NORTH and self.y-4 > 0:
            self.y -= 1
        elif direction == Direction.EAST and self.x+4 < PicoGame.SCREEN_WIDTH:
            self.x += 1
        elif direction == Direction.SOUTH and self.y+4 < PicoGame.SCREEN_HEIGHT:
            self.y += 1
        elif direction == Direction.WEST and self.x-4 > 0:
            self.x -= 1
    
    
if __name__ == '__main__':
    from PicoBattleCity import battle_city
    battle_city()
        