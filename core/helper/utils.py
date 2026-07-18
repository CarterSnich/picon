
from core.config import SCREEN_HEIGHT, SCREEN_WIDTH


def get_center_x(off_set):
    return (SCREEN_WIDTH / 2) + off_set


def get_center_y(off_set):
    return (SCREEN_HEIGHT / 2) + off_set


def get_center(x_offset=0, y_offset=0):
    return get_center_x(x_offset), get_center_y(y_offset)


def ms_to_hms(milliseconds: int):
    seconds = milliseconds // 1000
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return h, m, s
