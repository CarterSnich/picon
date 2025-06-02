import framebuf

PLAYER_TANK_N = framebuf.FrameBuffer(
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
PLAYER_TANK_E = framebuf.FrameBuffer(
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
PLAYER_TANK_S = framebuf.FrameBuffer(
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
PLAYER_TANK_W = framebuf.FrameBuffer(
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

ENEMY_TANK_N = framebuf.FrameBuffer(
    bytearray([
        0b00011000,
        0b00011000,
        0b11111111,
        0b11111111,
        0b11111111,
        0b11100111,
        0b11100111,
        0b11100111,
    ]),
    8, 8, framebuf.MONO_HLSB
)
ENEMY_TANK_E = framebuf.FrameBuffer(
    bytearray([
        0b11111100,
        0b11111100,
        0b11111100,
        0b00011111,
        0b00011111,
        0b11111100,
        0b11111100,
        0b11111100,
    ]),
    8, 8, framebuf.MONO_HLSB
)
ENEMY_TANK_S = framebuf.FrameBuffer(
    bytearray([
        0b11100111,
        0b11100111,
        0b11100111,
        0b11111111,
        0b11111111,
        0b11111111,
        0b00011000,
        0b00011000,
    ]),
    8, 8, framebuf.MONO_HLSB
)
ENEMY_TANK_W = framebuf.FrameBuffer(
    bytearray([
        0b00111111,
        0b00111111,
        0b00111111,
        0b11111000,
        0b11111000,
        0b00111111,
        0b00111111,
        0b00111111,
    ]),
    8, 8, framebuf.MONO_HLSB
)

BULLET = framebuf.FrameBuffer(
    bytearray([
        0b11,
        0b11,
    ]),
    2, 2, framebuf.MONO_VLSB
)
