from time import ticks_ms, ticks_diff, sleep
from random import choice

from PicoGame import PicoGame
from Racing.Racer import Racer
from Racing.Civilian import Civilian
from Racing.Resources import BUICK


class RacingGame(PicoGame):
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        racer = Racer(0, 5)
        traffic = [
            Civilian(self.SCREEN_WIDTH, choice([7, 27, 47]))
        ]
        road_lines = [10, 52, 94]
        traffic_added = 1
        
        last_beep_ms = 0
        beep = True
        bg_music_on = True
        
        last_pass_ms = 0
        
        while True:
            # sound
            if bg_music_on and ticks_diff(ticks_ms(), last_beep_ms) >= 30:
                last_beep_ms = ticks_ms()
                if beep:
                    self.sound(220)
                else:
                    self.sound(0)
                beep = not beep
            elif not bg_music_on and ticks_diff(ticks_ms(), last_pass_ms) >= 500:
                self.sound(0)
                beep = False
                bg_music_on = True
            
            # Render
            self.fill(0)
            # top and bottom lines
            self.fill_rect(0, 0, self.SCREEN_WIDTH, 4, 1)
            self.fill_rect(0, self.SCREEN_HEIGHT-4, self.SCREEN_WIDTH, 4, 1)
            # road lines
            for rl_x in road_lines:
                self.fill_rect(rl_x, 20, 21, 4, 1)
                self.fill_rect(rl_x, 40, 21, 4, 1)
            # racer
            self.blit(racer.SPRITE, racer.x, racer.y)
            for c in traffic:
                self.blit(c.SPRITE, c.x, c.y)
            self.show()
            
            # Inputs
            if self.button_up() and racer.y > 5:
                racer.y -= 2
            elif self.button_down() and racer.y < self.SCREEN_HEIGHT-15:
                racer.y += 2
                    
            # State updates
            # road lines
            for i in range(len(road_lines)):
                road_lines[i] -= 1
            if road_lines[0] <= 0 and len(road_lines) < 4:
                road_lines.append(self.SCREEN_WIDTH)
            if road_lines[0] <= -20:
                road_lines.remove(road_lines[0])
                
            # traffic
            for civilian in traffic:
                civilian.move()
            if traffic[0].x <= -32:
                traffic.remove(traffic[0])
                last_pass_ms = ticks_ms()
                self.sound(880)
                bg_music_on = False
                
            if len(traffic) < 3 and traffic[-1].x < self.SCREEN_WIDTH-84:
                x = self.SCREEN_WIDTH
                y = choice([7, 27, 47])
                traffic.append(Civilian(x, y, (traffic_added // 10) + 1))
                traffic_added += 1
                
            # check for collisions
            for c in traffic:
                if racer.is_colliding(c.x, c.y, c.WIDTH, c.HEIGHT):
                    self.over()
                    return
                    

if __name__ == '__main__':
    RacingGame().run()