from time import sleep_ms, ticks_ms, ticks_diff
from sys import print_exception

from core import Sound, Display
from core.input import Input, DPAD_UP, DPAD_DOWN, KEY_A, KEY_B
from assets.MenuSprites import GAMES_OR_TOOLS, ARROW_RIGHT


class Picon:
    display = Display()
    input = Input()
    sound = Sound()

    apps = {}

    is_main_menu = True
    main_menu_selection = "games"

    # item selection
    current_index = 0
    selection_index = 0
    items_stop_index = 0
    max_index = 0
    sub_items = []

    current_tick = ticks_ms()
    last_press_ms = current_tick

    def __init__(self, apps):
        self.apps = apps

    def get_sub_menu_list(self):
        return self.apps[self.main_menu_selection]

    def render(self):
        self.display.fill(0)

        if self.is_main_menu:
            self.display.blit(GAMES_OR_TOOLS, 0, 0)
            if self.main_menu_selection == "games":
                self.display.invert(0)
            else:
                self.display.invert(1)
        else:
            self.display.invert(0)
            self.sub_items = self.sub_items[self.items_stop_index - self.max_index:self.items_stop_index]
            y = 0
            for i, item in enumerate(self.sub_items):
                if i == self.selection_index:
                    self.display.blit(ARROW_RIGHT, 0, y)
                self.display.text(item[0], 8, y)
                y += 8

        self.display.show()

    def inputs(self):
        if ticks_diff(ticks_ms(), self.last_press_ms) < 200:
            return

        if self.is_main_menu:
            if self.input.is_pressed(DPAD_UP):
                self.main_menu_selection = "games"
                self.last_press_ms = self.current_tick
            elif self.input.is_pressed(DPAD_DOWN):
                self.main_menu_selection = "tools"
                self.last_press_ms = self.current_tick
            elif self.input.is_pressed(KEY_A):
                self.is_main_menu = False
                self.sub_items = self.get_sub_menu_list()
                self.max_index = min(len(self.sub_items), 8)
                self.items_stop_index = self.max_index
                self.selection_index = 0
                self.last_press_ms = self.current_tick
        else:
            if self.input.is_pressed(KEY_A) and len(self.sub_items):
                item = self.sub_items[self.current_index]
                try:
                    app = __import__("apps." + item[1], None, None, ("*",))
                    app.Main(self.display, self.input, self.sound).run()
                except BaseException as e:
                    self.modal("Failed to open")
                    print_exception(e)
                sleep_ms(200)
            elif self.input.is_pressed(KEY_B):
                self.is_main_menu = True
                self.last_press_ms = self.current_tick
            elif self.input.is_pressed(DPAD_UP):
                self.last_press_ms = self.current_tick
                if self.selection_index > 0:
                    self.selection_index -= 1
                elif self.items_stop_index > 8:
                    self.items_stop_index -= 1
                self.current_index = self.items_stop_index - (self.max_index - self.selection_index - 1) - 1
            elif self.input.is_pressed(DPAD_DOWN):
                self.last_press_ms = self.current_tick
                if self.selection_index < self.max_index - 1:
                    self.selection_index += 1
                elif self.items_stop_index < len(self.sub_items):
                    self.items_stop_index += 1
                self.current_index = self.items_stop_index - (self.max_index - self.selection_index - 1) - 1

    def run(self):
        while True:
            self.current_tick = ticks_ms()
            self.inputs()
            self.render()

    def modal(self, text):
        self.display.center_text(text, True)
        self.display.show()
        sleep_ms(3000)

if __name__ == '__main__':
    # this delay saves the world
    sleep_ms(200)

    apps = {
        "games": [
            ("SNAKE", "SnakeGame"),
            ("BATTLE CITY", "BattleCity"),
            ("RACING GAME", "RacingGame"),
            ("SLIDING PUZZLE", "SlidingPuzzle")
        ],
        "tools": [
            ("FLASHLIGHT", "Flashlight"),
            ("METRONOME", "Metronome"),
            ("NOTEPAD", "Notepad"),
            ("KEYPAD TEST", "KeypadTest"),
        ]
    }

    Picon(apps).run()
