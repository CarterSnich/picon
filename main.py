from time import sleep_ms, ticks_ms
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
    sub_items = []
    sub_items_count = 0
    current_index = 0
    split_start_index = 0
    split_end_index = 0
    current_row = 0

    current_ms = 0


    def __init__(self, apps):
        self.apps = apps


    def inputs(self):
        if not self.input.is_ready(self.current_ms):
            return

        if self.is_main_menu:
            if self.input.is_pressed(DPAD_UP):
                self.main_menu_selection = "games"
            elif self.input.is_pressed(DPAD_DOWN):
                self.main_menu_selection = "tools"
            elif self.input.is_pressed(KEY_A):
                self.is_main_menu = False

                self.sub_items = apps[self.main_menu_selection]
                self.sub_items_count = len(self.sub_items)

                self.current_index = 0
                self.current_row = 0
                self.split_start_index = 0
                self.split_end_index = self.sub_items_count

        else:
            if self.input.is_pressed(KEY_A) and len(self.sub_items):
                print(self.current_index)

                # try:
                #     item = self.sub_items[current_index]
                #     app = __import__("apps." + item[1], None, None, ("*",))
                #     app.Main(self.display, self.input, self.sound).run()
                # except BaseException as e:
                #     self.modal("Failed to open")
                #     print_exception(e)
                # sleep_ms(200)
            elif self.input.is_pressed(KEY_B):
                self.is_main_menu = True
            elif self.input.is_pressed(DPAD_UP):
                self.scroll(-1)
            elif self.input.is_pressed(DPAD_DOWN):
                self.scroll(1)


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

            for i, item in enumerate(self.sub_items[self.split_start_index:self.split_end_index]):
                y = i * 8
                if self.current_row == i:
                    self.display.blit(ARROW_RIGHT, 0, y)
                self.display.text(item[1], 8, y)

        self.display.show()


    def run(self):
        while True:
            self.update_ms()
            self.inputs()
            self.render()


    def update_ms(self):
        self.current_ms = ticks_ms()


    def scroll(self, i):
        if i == -1 and self.current_index == 0 and self.current_row == 0:
            self.current_index = self.sub_items_count - 1
            self.current_row = 7 if self.sub_items_count >= 8 else self.current_index
            self.split_start_index = self.sub_items_count - 8 if self.sub_items_count >= 8 else 0
            self.split_end_index = self.sub_items_count
        elif (i == 1 and self.current_index == self.sub_items_count - 1
              and self.current_row == (7 if self.sub_items_count >= 8 else self.sub_items_count - 1)):
            self.current_index = 0
            self.current_row = 0
            self.split_start_index = 0
            self.split_end_index = 8 if self.sub_items_count >= 8 else self.sub_items_count
        else:
            self.current_index += i

            if (self.current_row == 0 and self.split_start_index - 1 == self.current_index
                    or self.current_row == 7 and self.split_end_index == self.current_index):
                self.set_split_range(i)
            else:
                self.current_row = self.current_index - self.split_start_index


    def set_split_range(self, i):
        self.split_start_index += i
        self.split_end_index += i


    def get_selection_index(self):
        return self.split_start_index + self.current_index


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
