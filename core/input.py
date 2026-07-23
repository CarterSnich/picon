from machine import Pin
from time import ticks_ms, ticks_diff

from lib.keypad import Keypad
from core import config

KEY_SELECT = "KEYPAD_SELECT"
KEY_START = "KEYPAD_START"
KEY_X = "KEY_X"
KEY_Y = "KEY_Y"
KEY_A = "KEY_A"
KEY_B = "KEY_B"
DPAD_RIGHT = "DPAD_RIGHT"
DPAD_LEFT = "DPAD_LEFT"
DPAD_UP = "DPAD_UP"
DPAD_DOWN = "DPAD_DOWN"

BUTTON_DEBOUNCE_MS = 200


class Input:
    last_pressed_ms = 0
    button_debounce_ms = BUTTON_DEBOUNCE_MS


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

        self.key_states = {
            KEY_SELECT: lambda: self.__KEY_SELECT.value() == False,
            KEY_START: lambda: self.__KEY_START.value() == False,
            KEY_X: lambda: self.__KEY_X.value() == False,
            KEY_Y: lambda: self.__KEY_Y.value() == False,
            KEY_A: lambda: self.__KEY_A.value() == False,
            KEY_B: lambda: self.__KEY_B.value() == False,
            DPAD_RIGHT: lambda: self.__DPAD.read_keypad() == config.DPAD_ROWS[0],
            DPAD_LEFT: lambda: self.__DPAD.read_keypad() == config.DPAD_ROWS[1],
            DPAD_UP: lambda: self.__DPAD.read_keypad() == config.DPAD_COLS[0],
            DPAD_DOWN: lambda: self.__DPAD.read_keypad() == config.DPAD_COLS[1]
        }


    def __update_tick(self):
        self.last_pressed_ms = ticks_ms()


    def is_ready(self, tick):
        return ticks_diff(tick, self.last_pressed_ms) >= self.button_debounce_ms


    def is_pressed(self, key):
        state = self.key_states[key]()
        if state:
            self.__update_tick()
        return state


    def any_pressed_key(self):
        for key, state in self.key_states.items():
            if state():
                self.__update_tick()
                return key
        return None


    def set_debounce(self, ms):
        self.button_debounce_ms = ms


    def restore_debounce(self):
        self.button_debounce_ms = BUTTON_DEBOUNCE_MS
