from machine import Pin
from keypad import Keypad
from time import sleep

row_pins = [Pin(8),Pin(9)]
column_pins = [Pin(10), Pin(11)]

# Define keypad layout
keys = [
    ['RIGHT', 'LEFT'],
    ['UP', 'DOWN',]
]

keypad = Keypad(row_pins, column_pins, keys)

while True:
    key_pressed = keypad.read_keypad()
    if key_pressed:
        print("Key pressed:", key_pressed)
    sleep(0.1)  # debounce and delay