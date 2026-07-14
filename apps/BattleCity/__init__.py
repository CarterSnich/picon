from core import PiconGame

from .tank import Direction
from .player_tank import PlayerTank
from .enemy_tank import EnemyTank

MAX_ENEMY_COUNT = 4
ENEMY_SPAWN_INTERVAL = 1500


class Main(PiconGame):
    bullets = []

    player = None

    enemy_tanks = []
    last_enemy_spawn_ms = 0
    last_enemy_hit_ms = 0


    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)


    def inputs(self):
        ...


    def update(self):
        ...


    def render(self):
        ...


if __name__ == "__main__":
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
