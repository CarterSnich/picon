import framebuf
from BattleCity.Tank import Tank, SpawnPoint, Direction
from PicoGame import PicoGame
from random import choice, randint
from time import ticks_diff, ticks_ms

NORTH = framebuf.FrameBuffer(
    bytearray([
        0b00011000,
        0b00011000,
        0b11111111,
        0b10111101,
        0b11011011,
        0b11111111,
        0b10000001,
        0b11111111,
    ]),
    8, 8, framebuf.MONO_HLSB
)

EAST = framebuf.FrameBuffer(
    bytearray([
        0b11111100,
        0b10110100,
        0b10101100,
        0b10111111,
        0b10111111,
        0b10101100,
        0b10110100,
        0b11111100,
    ]),
    8, 8, framebuf.MONO_HLSB
)

SOUTH = framebuf.FrameBuffer(
    bytearray([
        0b11111111,
        0b10000001,
        0b11111111,
        0b11011011,
        0b10111101,
        0b11111111,
        0b00011000,
        0b00011000,
    ]),
    8, 8, framebuf.MONO_HLSB
)

WEST = framebuf.FrameBuffer(
    bytearray([
        0b00111111,
        0b00101101,
        0b00110101,
        0b11111101,
        0b11111101,
        0b00110101,
        0b00101101,
        0b00111111,
    ]),
    8, 8, framebuf.MONO_HLSB
)


class EnemyTank(Tank):
    sprites = [NORTH, EAST, SOUTH, WEST]
    
    def __init__(self, spawn_point = -1, x = -1, y = -1, direction = Direction.NORTH):
        self.displacement = 8
        self.delay_next_shot_ms = randint(300, 1000)
        self.last_shot_ms = ticks_ms()
        
        if spawn_point == SpawnPoint.NW:
            x, y = 4, 4
            direction = choice([Direction.EAST, Direction.SOUTH])
        elif spawn_point == SpawnPoint.NE:
            x, y = PicoGame.SCREEN_WIDTH - 8, 8
            direction = choice([Direction.WEST, Direction.SOUTH])
        elif spawn_point == SpawnPoint.SE:
            x, y = PicoGame.SCREEN_WIDTH - 8, PicoGame.SCREEN_HEIGHT - 8
            direction = choice([Direction.NORTH, Direction.WEST])
        elif spawn_point == SpawnPoint.SW:
            x, y = 4, PicoGame.SCREEN_HEIGHT- 8
            direction = choice([Direction.NORTH, Direction.EAST])
            
        super().__init__(x, y, direction)
    
    def change_direction(self, remove_current = True):
        directions = [
            Direction.NORTH, Direction.EAST,
            Direction.SOUTH, Direction. WEST
        ]
        if remove_current:
            directions.remove(self.direction)
        self.direction = choice(directions)
    
    def update(self, player):
        super().update()
        
        delta = ticks_diff(ticks_ms(), self.last_shot_ms)
        if delta >= self.delay_next_shot_ms:
            self.shoot()
            self.last_shot_ms = ticks_ms()
            self.delay_next_shot_ms = randint(300, 1000)
        
        if self.displacement < 8:
            if self.direction == Direction.NORTH:
                if self.y-4 > 0:
                    self.displacement += 1
                    self.y -= 1
                else:
                    self.displacement = 0
                    self.change_direction()
            elif self.direction == Direction.EAST:
                if self.x+4 < PicoGame.SCREEN_WIDTH:
                    self.displacement += 1
                    self.x += 1
                else:
                    self.displacement = 0
                    self.change_direction()
            elif self.direction == Direction.SOUTH:
                if self.y+4 < PicoGame.SCREEN_HEIGHT:
                    self.displacement += 1
                    self.y += 1
                else:
                    self.displacement = 0
                    self.change_direction()
            elif self.direction == Direction.WEST:
                if self.x-4 > 0:
                    self.displacement += 1
                    self.x -= 1
                else:
                    self.displacement = 0
                    self.change_direction()
        else:
            self.displacement = 0
            self.change_direction(False)
            
        

if __name__ == '__main__':
    from PicoBattleCity import battle_city
    battle_city()