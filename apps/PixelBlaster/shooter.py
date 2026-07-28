from apps.PixelBlaster.utils import get_row_y
from core import GameObject

from apps.PixelBlaster.assets import SHOOTER


class Shooter(GameObject):

    def __init__(self, row):
        self.row = row

        super().__init__(SHOOTER, 0, get_row_y(row) - 4)


    def move(self, n: int):
        if (n == -1 and self.row == 0) or (n == 1 and self.row == 15):
            return

        self.row += n
        self.y = get_row_y(self.row) - 4
