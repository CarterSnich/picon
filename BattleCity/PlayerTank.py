import framebuf
from BattleCity.Tank import Direction, Tank

NORTH = framebuf.FrameBuffer(
    bytearray([
        0b00011000,
        0b00011000,
        0b11111111,
        0b11011011,
        0b11111111,
        0b11011011,
        0b11100111,
        0b11111111,
    ]),
    8, 8, framebuf.MONO_HLSB
)
EAST = framebuf.FrameBuffer(
    bytearray([
        0b11111100,
        0b11111100,
        0b11010100,
        0b10111111,
        0b10111111,
        0b11010100,
        0b11111100,
        0b11111100,
    ]),
    8, 8, framebuf.MONO_HLSB
)
SOUTH = framebuf.FrameBuffer(
    bytearray([
        0b11111111,
        0b11100111,
        0b11011011,
        0b11111111,
        0b11011011,
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
        0b00101011,
        0b11111101,
        0b11111101,
        0b00101011,
        0b00111111,
        0b00111111,
    ]),
    8, 8, framebuf.MONO_HLSB
)


class PlayerTank(Tank):
    
    sprites = [ NORTH, EAST, SOUTH, WEST ]
    direction = Direction.NORTH
    
    def __init__(self, x, y):
        super().__init__(x, y)
 
        
        
        
        