from time import ticks_diff
from random import randint

from core import PiconGame
from core.input import KEY_A, DPAD_UP, DPAD_DOWN, DPAD_LEFT, DPAD_RIGHT
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from core.helper import get_center

from apps.BattleCity.Tank import Direction
from apps.BattleCity.PlayerTank import PlayerTank
from apps.BattleCity.EnemyTank import EnemyTank

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
