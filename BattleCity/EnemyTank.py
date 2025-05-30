import framebuf

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