import framebuf
from time import ticks_diff, ticks_ms, sleep_ms
from random import randint, choice

from PicoGame import PicoGame
from BattleCity.PlayerTank import PlayerTank
from BattleCity.EnemyTank import EnemyTank
from BattleCity.Tank import Direction


def battle_city():
    game = PicoGame()

    score = 0
    
    x, y = game.get_center(0, 0)
    player = PlayerTank(x, y)
    last_player_shoot_ms = -1
    
    enemy_tanks = [EnemyTank(randint(0, 3))]
    last_enemy_deploy_ms = ticks_ms()
    last_enemy_hit_ms = -1
    
    while True:
        # exit game loop
        if game.button_B():
            break
        
        
        # clear sound
        tick = ticks_ms()
        shoot_delta = ticks_diff(tick, last_player_shoot_ms) >= 10
        enemy_delta = ticks_diff(tick, last_enemy_hit_ms) >= 10
        if shoot_delta and enemy_delta:
            game.sound(0)
        
        # collision checks
        for e in enemy_tanks[:]:
            # enemy hits on player
            for eb in e.bullets:
                if eb.is_colliding(player.x-4, player.y-4, 9, 9):
                    game.sound(560)
                    sleep_ms(50)
                    game.sound(0)
                    game.over()
                    return
                
            # player hits enemies
            for pb in player.bullets[:]:
                # this are just manually adjusted values
                # i don't get the calculations
                # at this point
                if pb.is_colliding(e.x-4, e.y-4, 9, 9):
                    score += 1
                    enemy_tanks.remove(e)
                    player.bullets.remove(pb)
                    game.sound(560)
                    last_enemy_hit_ms = ticks_ms()
        
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
        game.top_right_corner_text(str(score))
        game.show()
        
        # inputs
        if game.button_A() and ticks_diff(ticks_ms(), last_player_shoot_ms) >= 300:
            last_player_shoot_ms = ticks_ms()
            player.shoot()
            game.sound(880)
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