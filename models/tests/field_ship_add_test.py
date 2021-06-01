from ..ship import Ship
from ..field import Field


class TestFieldAddShips:
    def setup(self):
        self.ship = Ship(3)
        self.big_ship = Ship(4)
        self.small_ship = Ship(1)
        self.field = Field(10, 10)

    def test_get_ships_when_empty(self):
        assert self.field.get_ships() == []

    def test_get_ships_return_ships(self):
        self.field.add_ship(self.ship)
        self.field.add_ship(self.big_ship)
        self.field.add_ship(self.small_ship)
        assert set(self.field.get_ships()) == {self.ship, self.big_ship, self.small_ship}

    def test_get_ships_not_return_duplicate(self):
        self.field.add_ship(self.ship)
        self.field.add_ship(self.ship)
        assert self.field.get_ships() == [self.ship]

