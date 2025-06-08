from time import ticks_ms, ticks_diff, sleep_ms
from random import choice

from PicoGame import PicoGame
from games.Racing.Racer import Racer
from games.Racing.Civilian import Civilian
from games.Racing.Lanes import LANES


class RacingGame(PicoGame):
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        
        speed = 1
        is_start = True
        is_transition = False
        transiton_start = 0
        
        last_beep_ms = 0
        beep = True
        
        last_press_ms = 0
        
        racer = Racer()
        
        traffic = [
            Civilian(self.SCREEN_WIDTH, choice(LANES))
        ]
        road_lines = [10, 52, 94]
        traffic_added = len(traffic)
        
        while True:
            # sound
            if not is_start and ticks_diff(ticks_ms(), last_beep_ms) >= 30:
                last_beep_ms = ticks_ms()
                if beep:
                    self.sound(220)
                else:
                    self.sound(0)
            
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
            self.blit(racer.SPRITE, racer.x, LANES[racer.lane])
            
            if is_transition:
                # transition
                self.fill_rect(0, int(self.SCREEN_HEIGHT/2)-5, self.SCREEN_WIDTH, 9, 1)
                t = f"LEVEL {speed+1}"
                self.text(t, int(self.SCREEN_WIDTH/2)-int((len(t)/2) * 8), int(self.SCREEN_HEIGHT/2)-4, 0)            
            else:
                # traffic
                for c in traffic:
                    self.blit(c.SPRITE, c.x, c.y)
            self.show()
            
            # starting animation
            if is_start:
                is_start = False
                for i, t in enumerate(["READY", "3", "2", "1", "GO"]):
                    self.fill_rect(0, int(self.SCREEN_HEIGHT/2)-5, self.SCREEN_WIDTH, 9, 1)
                    self.text(t, int(self.SCREEN_WIDTH/2)-int((len(t)/2) * 8), int(self.SCREEN_HEIGHT/2)-4, 0)
                    self.show()
                    if i == 4:
                        self.sound(880)
                    elif i > 0:
                        self.sound(440)
                    sleep_ms(300)
                    self.sound(0)
                    sleep_ms(700)
            
            # check for collisions
            for c in traffic:
                if racer.is_colliding(c.x, c.y, c.WIDTH, c.HEIGHT):
                    self.over()
                    return
            
            # Inputs
            if ticks_diff(ticks_ms(), last_press_ms) >= 150:
                if self.button_up() and racer.lane > 0:
                    last_press_ms = ticks_ms()
                    racer.up()
                elif self.button_down() and racer.lane < 2:
                    last_press_ms = ticks_ms()
                    racer.down()
                    
            # State updates
            # road lines
            for i in range(len(road_lines)):
                road_lines[i] -= speed
            if road_lines[0] <= 0 and len(road_lines) < 4:
                road_lines.append(self.SCREEN_WIDTH)
            if road_lines[0] <= -20:
                road_lines.remove(road_lines[0])
                
            # traffic
            for civilian in traffic:
                civilian.move()
            if len(traffic) and traffic[0].x <= -32:
                traffic.remove(traffic[0])
            if is_transition:
                if ticks_diff(ticks_ms(), transition_start) >= 3000:
                    is_transition = False
                    speed += 1
                    x = self.SCREEN_WIDTH
                    y = choice(LANES)
                    traffic.append(Civilian(x, y, speed))
                    traffic_added = 1
            else:
                if traffic_added >= 10 and len(traffic) == 0:
                    is_transition = True
                    transition_start = ticks_ms()
                elif traffic_added < 10 and len(traffic) < 3 and traffic[-1].x < self.SCREEN_WIDTH-84:
                    x = self.SCREEN_WIDTH
                    y = choice(LANES)
                    traffic.append(Civilian(x, y, speed))
                    traffic_added += 1
                
                    

if __name__ == '__main__':
    RacingGame().run()