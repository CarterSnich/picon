import framebuf
from time import ticks_diff, ticks_ms
from random import randint, choice

from PicoGame import PicoGame
from BattleCity.PlayerTank import PlayerTank
from BattleCity.EnemyTank import EnemyTank
from BattleCity.Tank import Direction


def battle_city():
    game = PicoGame()

    score = 0    
    button_delay = 300
    last_button_debounce = -1
    
    x, y = game.get_center(0, 0)
    player = PlayerTank(x, y)
    
    enemy_tanks = [EnemyTank(randint(0, 3))]
    last_enemy_deploy_ms = ticks_ms()
    last_enemy_hit_ms = -1
    
    while True:
        # exit game loop
        if game.button_B():
            break
        
        # collision checks
        
        for e in enemy_tanks[:]:
            # enemy tanks' bullet check
            for eb in e.bullets:
                if player.will_collide(eb.x, eb.y, 8, 8):
                    game.over()
                    return
                
            for pb in player.bullets[:]:
                if pb.is_colliding(e.x, e.y, 8, 8):
                    enemy_tanks.remove(e)
                    player.bullets.remove(pb)
                    last_enemy_hit_ms = ticks_ms()
                    continue
        
        tick = ticks_ms()
        new_enemy = ticks_diff(tick, last_enemy_hit_ms) >= 1000 and \
            ticks_diff(tick, last_enemy_deploy_ms) >= 1000
        if len(enemy_tanks) < 3 and new_enemy:
            last_enemy_deploy_ms = tick
            enemy_tanks.append(EnemyTank(randint(0, 3)))
            
            
        
        # render and update states
        game.fill(0)
        player.update()
        player.render(game)
        for enemy in enemy_tanks:
            enemy.update(player)
            enemy.render(game)
        game.show()
        
        # inputs
        debounce_delta = ticks_diff(ticks_ms(), last_button_debounce)
        if game.button_A() and debounce_delta >= button_delay:
            last_button_debounce = ticks_ms()
            player.shoot()    
        if game.button_up():
            player.move(Direction.NORTH, enemy_tanks)
        elif game.button_right():
            player.move(Direction.EAST, enemy_tanks)
        elif game.button_down():
            player.move(Direction.SOUTH, enemy_tanks)
        elif game.button_left():
            player.move(Direction.WEST, enemy_tanks)
                


if __name__ == '__main__':
    battle_city()