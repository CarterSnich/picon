from PicoGame import PicoGame
from time import ticks_ms, ticks_diff



def notepad():
    game = PicoGame()
    
    characters = [chr(i) for i in range(65, 91)]
    characters += [ " ", "." ]
    
    text = ""
    
    keyboard_page = False
    selection = 0
    
    last_debounce_ms = 0
    
    while True:
        game.fill(0)
        
        # print text
        for i in range(len(text)):
            game.text(text[i], i * 8, 0, 1)
        
        # print keyboard
        game.hline(0, game.SCREEN_HEIGHT-12, game.SCREEN_WIDTH, 1)
        
        if keyboard_page == 0:
            chars = characters[0:16]
        else:
            chars = characters[16:28]
         
        for i in range(0, 16 if keyboard_page == 0 else 12):
            x = 8 * i
            c = chars[i]
            
            if selection == i:
                game.fill_rect(x, game.SCREEN_HEIGHT-10, 8, 8, 1)
                game.text(c, x, game.SCREEN_HEIGHT-10, 0)
            else:
                game.text(c, x, game.SCREEN_HEIGHT-10, 1)
                
        game.hline(0, game.SCREEN_HEIGHT-1, game.SCREEN_WIDTH, 1)
        
        
        # input handlings
        if ticks_diff(ticks_ms(), last_debounce_ms) >= 200:
            if game.button_A():
                last_debounce_ms = ticks_ms()
                text += chars[selection]
            elif game.button_B() and len(text):
                last_debounce_ms = ticks_ms()
                text = text[:-1]
            elif game.button_right():
                last_debounce_ms = ticks_ms()
                if selection >= (15 if keyboard_page == 0 else 11):
                    selection = 0
                else:
                    selection += 1
            elif game.button_left():
                last_debounce_ms = ticks_ms()
                if selection <= 0:
                    selection = 15 if keyboard_page == 0 else 11
                else:
                    selection -= 1
            elif game.button_up() or game.button_down():
                last_debounce_ms = ticks_ms()
                selection = 0
                keyboard_page = not keyboard_page
        
        game.show()
    
    
if __name__ == '__main__':
    notepad()