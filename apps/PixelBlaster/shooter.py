from apps.PixelBlaster.utils import get_row_y
from core import GameObject

from apps.PixelBlaster.assets import SHOOTER


class Shooter(GameObject):

    def __init__(self, row):
        self.row = row

        super().__init__(SHOOTER, 0, get_row_y(row) - 4)


    def up(self):
        if self.row == 0:
            return

        self.row -= 1
        self.y -= 4


    def down(self):
        if self.row == 15:
            return

        self.row += 1
        self.y += 4
