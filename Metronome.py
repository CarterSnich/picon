from PicoGame import PicoGame
from time import ticks_ms, ticks_diff, sleep_ms


def metronome():
    game = PicoGame()
    bpm = 120
    beat = 0
    
    game.sound(1000)
    last_beat_ms = ticks_ms()
    last_pressed_ms = last_beat_ms
    init_beat_ms = last_beat_ms
    
    while True:
        if game.button_B():
            game.sound(0)
            break
        
        game.fill(0)
        button_delta = ticks_diff(ticks_ms(), last_pressed_ms)
        
        if button_delta >= 100:
            if game.button_up() and bpm < 240:
                last_pressed_ms = ticks_ms()
                bpm += 1
            elif game.button_down() and bpm > 1:
                last_pressed_ms = ticks_ms()
                bpm -= 1
            elif game.button_right():
                last_pressed_ms = ticks_ms()
                if bpm >= 235:
                    bpm = 240
                else:
                    bpm += 5
            elif game.button_left():
                last_pressed_ms = ticks_ms()
                if bpm <= 5:
                    bpm = 1
                else:
                    bpm -= 5
        
        game.center_text(str(bpm))
        
        beat_delta = ticks_diff(ticks_ms(), last_beat_ms)
        gap_ms = (60 * 1000) / bpm
        
        for i in range(4):
            if beat == i:
                game.fill_rect((20 * i)+29, 40, 10, 10, 1)
            else:
                game.rect((20 * i)+29, 40, 10, 10, 1)

        if beat_delta >= gap_ms:
            last_beat_ms = ticks_ms()
            beat = (beat + 1) % 4
            
            if beat == 0:
                game.sound(1000)
            else:
                game.sound(880)
                
        elif beat_delta >= 100:
            game.sound(0)
            
        game.show()
        
        
        
    
if __name__ == '__main__':
    metronome()


