import framebuf

ARROW_UP = framebuf.FrameBuffer(
    bytearray([
        0b00000000,
        0b00000000,
        0b00000000,
        0b00011000,
        0b00111100,
        0b01111110,
        0b00000000,
        0b00000000,
    ]),
    8, 8, framebuf.MONO_HLSB
)

ARROW_RIGHT = framebuf.FrameBuffer(
    bytearray([
        0b00000000,
        0b00100000,
        0b00110000,
        0b00111000,
        0b00111000,
        0b00110000,
        0b00100000,
        0b00000000,
    ]),
    8, 8, framebuf.MONO_HLSB
)

ARROW_DOWN = framebuf.FrameBuffer(
    bytearray([
        0b00000000,
        0b00000000,
        0b01111110,
        0b00111100,
        0b00011000,
        0b00000000,
        0b00000000,
        0b00000000,
    ]),
    8, 8, framebuf.MONO_HLSB
)

ARROW_LEFT = framebuf.FrameBuffer(
    bytearray([
        0b00000000,
        0b00000100,
        0b00001100,
        0b00011100,
        0b00011100,
        0b00001100,
        0b00000100,
        0b00000000,
    ]),
    8, 8, framebuf.MONO_HLSB
)