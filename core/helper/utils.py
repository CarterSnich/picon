from random import getrandbits
from time import ticks_diff

from core.config import SCREEN_HEIGHT, SCREEN_WIDTH


def get_center_x(width: int):
    return (SCREEN_WIDTH - width) // 2


def get_center_y(height: int):
    return (SCREEN_HEIGHT - height) // 2


def get_center(width, height):
    return get_center_x(width), get_center_y(height)


def ms_to_hms(milliseconds: int):
    seconds = milliseconds // 1000
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return h, m, s


def randbool():
    return bool(getrandbits(1))


def elapsed(current, last):
    return ticks_diff(current, last)


def has_elapsed(current, last, interval):
    return ticks_diff(current, last) >= interval


def has_not_elapsed(current, last, interval):
    return ticks_diff(current, last) < interval
