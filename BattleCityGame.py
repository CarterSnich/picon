from time import ticks_diff, ticks_ms, sleep_ms
from random import randint, choice

from PicoGame import PicoGame
from games.BattleCity.Tank import Direction
from games.BattleCity.PlayerTank import PlayerTank
from games.BattleCity.EnemyTank import EnemyTank

MAX_ENEMY_COUNT = 4
ENEMY_SPAWN_INTERVAL = 1500

class BattleCity(PicoGame):
    
    def __init__(self):
        super().__init__()
        self.score = 0
        self.bullets = []
        
        x, y = self.get_center(0, 0)
        self.player = PlayerTank(x, y)
        
        self.enemy_tanks = []
        self.last_enemy_spawn_ms = 0
        self.last_enemy_hit_ms = 0

    def run(self):
        while True:
            # exit game loop
            if self.button_B():
                break
            
            # mute sounds
            tick = ticks_ms()
            player_shot_delta = ticks_diff(tick, self.player.last_shot_ms)
            enemy_hit_delta = ticks_diff(tick, self.last_enemy_hit_ms)
            if player_shot_delta >= 50 and enemy_hit_delta >= 50:
                self.sound(0)
            
            # bullet state update
            for b in self.bullets:
                # movement
                if b.update():
                    if b.from_player:
                        self.player.shots -= 1
                    self.bullets.remove(b)
                    continue
                # check hits enemy tanks
                if b.from_player:
                    for et in self.enemy_tanks:
                        if b.is_colliding(et.x-2, et.y-2, 9, 9):
                            self.sound(1000)
                            self.last_enemy_hit_ms = ticks_ms()
                            self.enemy_tanks.remove(et)
                            self.bullets.remove(b)
                            self.score += 1
                            self.player.shots -= 1
                            break
                    else:
                        continue
                    break
                else:
                    # check on player tank
                    if b.is_colliding(self.player.x-2, self.player.y-2, 9, 9):
                        self.over()
                        return
            
            # state update of enemy tanks
            for et in self.enemy_tanks:
                if et.can_shoot():
                    self.bullets.append(et.shoot())
                # check collision on player
                if et.will_collide(self.player.x, self.player.y, 8, 8):
                    et.change_direction()
                else:
                    et.update()
                    
                    
            # spawn enemy
            enemy_hit_delta = ticks_diff(ticks_ms(), self.last_enemy_hit_ms) >= ENEMY_SPAWN_INTERVAL
            enemy_spawn_delta = ticks_diff(ticks_ms(), self.last_enemy_spawn_ms) >= ENEMY_SPAWN_INTERVAL
            if len(self.enemy_tanks) < MAX_ENEMY_COUNT and enemy_hit_delta and enemy_spawn_delta:
                self.last_enemy_spawn_ms = ticks_ms()
                
                # loop until coordinates doesn't
                # intersect with the player
                while True:
                    x = randint(4, self.SCREEN_WIDTH-4)
                    y = randint(4, self.SCREEN_HEIGHT-4)
                    
                    is_intersecting = self.sprites_intersection(
                        x, y, 8, 8,
                        self.player.x, self.player.y, 8, 8
                    )
                    
                    if not is_intersecting:
                        break
                self.enemy_tanks.append(EnemyTank(x, y, randint(0, 3)))
            
                
            # render
            self.fill(0)
            self.blit(self.player.get_sprite(), self.player.x-4, self.player.y-4)
            for e in self.enemy_tanks:
                self.blit(e.get_sprite(), e.x-4, e.y-4)
            for b in self.bullets:
                self.blit(b.get_sprite(), b.x-1, b.y-1)
            self.top_right_corner_text(str(self.score))
            self.show()
            
            # inputs
            if self.button_A() and self.player.can_shoot():
                self.sound(880)
                self.bullets.append(self.player.shoot())
            if self.button_up():
                self.player.move(Direction.NORTH, self.enemy_tanks)
            elif self.button_right():
                self.player.move(Direction.EAST, self.enemy_tanks)
            elif self.button_down():
                self.player.move(Direction.SOUTH, self.enemy_tanks)
            elif self.button_left():
                self.player.move(Direction.WEST, self.enemy_tanks)
                    


if __name__ == '__main__':
    BattleCity().run()