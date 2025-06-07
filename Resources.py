import framebuf

PIXEL = framebuf.FrameBuffer(
    bytearray([
        0b1111,
        0b1111,
        0b1111,
        0b1111,
    ]),
    4, 4, framebuf.MONO_VLSB
)