from core import GameObject
from apps.DinoGame.assets import TREES, BIG_TREE


class Trees(GameObject):

    def __init__(self, x=128, y=41):
        super().__init__(TREES, x, y)


class BigTree(GameObject):

    def __init__(self, x=128, y=37):
        super().__init__(BIG_TREE, x, y)
