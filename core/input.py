from time import ticks_ms

from machine import Pin

from core import config
from core.helper import has_elapsed
from lib.keypad import Keypad

BUTTON_DEBOUNCE_MS = 200


class Key:
    SELECT = "SELECT"
    START = "START"
    X = "X"
    Y = "Y"
    A = "A"
    B = "B"
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    UP = "UP"
    DOWN = "DOWN"


class Input:

    def __init__(self):
        self.__KEY_SELECT = Pin(config.KEY_SELECT, Pin.IN, Pin.PULL_UP)
        self.__KEY_START = Pin(config.KEY_START, Pin.IN, Pin.PULL_UP)
        self.__KEY_X = Pin(config.KEY_X, Pin.IN, Pin.PULL_UP)
        self.__KEY_Y = Pin(config.KEY_Y, Pin.IN, Pin.PULL_UP)
        self.__KEY_A = Pin(config.KEY_A, Pin.IN, Pin.PULL_UP)
        self.__KEY_B = Pin(config.KEY_B, Pin.IN, Pin.PULL_UP)
        self.__DPAD = Keypad(
            [Pin(config.DPAD_ROWS[0]), Pin(config.DPAD_ROWS[1])],
            [Pin(config.DPAD_COLS[0]), Pin(config.DPAD_COLS[1])],
            [config.DPAD_ROWS, config.DPAD_COLS]  # RT, LT, UP, DN
        )

        self.__key_states = {
            Key.SELECT: lambda: self.__KEY_SELECT.value() == False,
            Key.START: lambda: self.__KEY_START.value() == False,
            Key.X: lambda: self.__KEY_X.value() == False,
            Key.Y: lambda: self.__KEY_Y.value() == False,
            Key.A: lambda: self.__KEY_A.value() == False,
            Key.B: lambda: self.__KEY_B.value() == False,
            Key.RIGHT: lambda: self.__DPAD.read_keypad() == config.DPAD_ROWS[0],
            Key.LEFT: lambda: self.__DPAD.read_keypad() == config.DPAD_ROWS[1],
            Key.UP: lambda: self.__DPAD.read_keypad() == config.DPAD_COLS[0],
            Key.DOWN: lambda: self.__DPAD.read_keypad() == config.DPAD_COLS[1]
        }

        self.last_pressed_ms = 0
        self.button_debounce_ms = BUTTON_DEBOUNCE_MS


    def __update_tick(self):
        self.last_pressed_ms = ticks_ms()


    def is_ready(self, tick):
        return has_elapsed(tick, self.last_pressed_ms, self.button_debounce_ms)


    def is_pressed(self, key):
        state = self.__key_states[key]()
        if state:
            self.__update_tick()
        return state


    def any_pressed_key(self):
        for key, state in self.__key_states.items():
            if state():
                self.__update_tick()
                return key
        return None


    def set_debounce(self, ms):
        self.button_debounce_ms = ms


    def restore_debounce(self):
        self.button_debounce_ms = BUTTON_DEBOUNCE_MS
