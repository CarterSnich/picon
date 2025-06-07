from PicoGame import PicoGame
from tools.keypad_test.Sprites import KEYPAD_UP, KEYPAD_UP_INVERT, KEYPAD_RIGHT, KEYPAD_RIGHT_INVERT, KEYPAD_DOWN, KEYPAD_DOWN_INVERT, KEYPAD_LEFT, KEYPAD_LEFT_INVERT, KEYPAD_A, KEYPAD_A_INVERT, KEYPAD_B, KEYPAD_B_INVERT


class KeypadTest(PicoGame):
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            self.text("Press UP and B", 8, 0, 1)
            self.text("to EXIT", 36, 8, 1)
            
            if self.button_up() and self.button_B():
                return
            
            if self.button_A():
                self.blit(KEYPAD_A_INVERT, 90, 26)
            else:
                self.blit(KEYPAD_A, 90, 26)
            if self.button_B():
                self.blit(KEYPAD_B_INVERT, 78, 42)
            else:
                self.blit(KEYPAD_B, 78, 42)
            
            x, y = 18, 22
            if self.button_up():
                self.blit(KEYPAD_UP_INVERT, x+16, y)
            else:
                self.blit(KEYPAD_UP, x+16, y)
            if self.button_right():
                self.blit(KEYPAD_RIGHT_INVERT, x+30, y+12)
            else:
                self.blit(KEYPAD_RIGHT, x+30, y+12)
            if self.button_down():
                self.blit(KEYPAD_DOWN_INVERT, x+16, y+24)
            else:
                self.blit(KEYPAD_DOWN, x+16, y+24)
            if self.button_left():
                self.blit(KEYPAD_LEFT_INVERT, x+2, y+12)
            else:
                self.blit(KEYPAD_LEFT, x+2, y+12)
            
            self.show()
        

if __name__ == '__main__':
    KeypadTest().run()