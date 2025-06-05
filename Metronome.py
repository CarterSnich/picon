from PicoGame import PicoGame
from time import ticks_ms, ticks_diff, sleep_ms


class Metronome(PicoGame):
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        bpm = 120
        beat = 0
        
        self.sound(1000)
        last_beat_ms = ticks_ms()
        last_pressed_ms = last_beat_ms
        init_beat_ms = last_beat_ms
        
        while True:
            if self.button_B():
                self.sound(0)
                break
            
            self.fill(0)
            button_delta = ticks_diff(ticks_ms(), last_pressed_ms)
            
            if button_delta >= 100:
                if self.button_up() and bpm < 240:
                    last_pressed_ms = ticks_ms()
                    bpm += 1
                elif self.button_down() and bpm > 1:
                    last_pressed_ms = ticks_ms()
                    bpm -= 1
                elif self.button_right():
                    last_pressed_ms = ticks_ms()
                    if bpm >= 235:
                        bpm = 240
                    else:
                        bpm += 5
                elif self.button_left():
                    last_pressed_ms = ticks_ms()
                    if bpm <= 5:
                        bpm = 1
                    else:
                        bpm -= 5
            
            self.center_text(str(bpm))
            
            beat_delta = ticks_diff(ticks_ms(), last_beat_ms)
            gap_ms = (60 * 1000) / bpm
            
            for i in range(4):
                if beat == i:
                    self.fill_rect((20 * i)+29, 40, 10, 10, 1)
                else:
                    self.rect((20 * i)+29, 40, 10, 10, 1)

            if beat_delta >= gap_ms:
                last_beat_ms = ticks_ms()
                beat = (beat + 1) % 4
                
                if beat == 0:
                    self.sound(1000)
                else:
                    self.sound(880)
                    
            elif beat_delta >= 100:
                self.sound(0)
                
            self.show()
        
        
if __name__ == '__main__':
    Metronome().run()


