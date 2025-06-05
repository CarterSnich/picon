from PicoGame import PicoGame
from time import ticks_ms, ticks_diff



class Notepad(PicoGame):
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        characters = [chr(i) for i in range(65, 91)]
        characters += [" ", "."]
        
        text = ""
        
        keyboard_page = False
        selection = 0
        
        last_debounce_ms = 0
        
        while True:
            self.fill(0)
            
            # print text
            for i in range(len(text)):
                self.text(text[i], i * 8, 0, 1)
            
            # print keyboard
            self.hline(0, self.SCREEN_HEIGHT-12, self.SCREEN_WIDTH, 1)
            
            if keyboard_page == 0:
                chars = characters[0:16]
            else:
                chars = characters[16:28]
             
            for i in range(0, 16 if keyboard_page == 0 else 12):
                x = 8 * i
                c = chars[i]
                
                if selection == i:
                    self.fill_rect(x, self.SCREEN_HEIGHT-10, 8, 8, 1)
                    self.text(c, x, self.SCREEN_HEIGHT-10, 0)
                else:
                    self.text(c, x, self.SCREEN_HEIGHT-10, 1)
                    
            self.hline(0, self.SCREEN_HEIGHT-1, self.SCREEN_WIDTH, 1)
            
            
            # input handlings
            if ticks_diff(ticks_ms(), last_debounce_ms) >= 200:
                if self.button_A():
                    last_debounce_ms = ticks_ms()
                    text += chars[selection]
                elif self.button_B() and len(text):
                    last_debounce_ms = ticks_ms()
                    text = text[:-1]
                elif self.button_right():
                    last_debounce_ms = ticks_ms()
                    if selection >= (15 if keyboard_page == 0 else 11):
                        selection = 0
                    else:
                        selection += 1
                elif self.button_left():
                    last_debounce_ms = ticks_ms()
                    if selection <= 0:
                        selection = 15 if keyboard_page == 0 else 11
                    else:
                        selection -= 1
                elif self.button_up() or self.button_down():
                    last_debounce_ms = ticks_ms()
                    selection = 0
                    keyboard_page = not keyboard_page
            
            self.show()
    
    
if __name__ == '__main__':
    Notepad().run()