from .field import Field
from .ship import Ship


class Options:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.fleet_sizes = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]

    def set_fleet(self, *fleet):

        self.fleet_sizes = fleet

    def create_field(self, game):
        return Field(self.width, self.height, game)

    def create_fleet(self):
        for size in self.fleet_sizes:
            yield Ship(size)
