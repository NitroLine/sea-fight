from .ship import Ship
from .point import Point
from .model import EventEmitter


class Field(EventEmitter):
    def __init__(self, width, height, game=None):
        super().__init__(game)
        self.width = width
        self.height = height
        self._shots = set()
        self._ships = set()

    def add_ship(self, ship):
        self._ships.add(ship)
        self.emit('updated')

    def get_ships(self):
        return list(self._ships)

    def get_first_to_put_ship(self):
        return next(filter(lambda x: x.position is not None, sorted(self._ships, key=lambda x: x.size)), None)

    def put_ship(self, ship, point):
        if not isinstance(ship, Ship):
            raise TypeError
        if ship not in self._ships:
            raise ReferenceError
        if ship.position is not None:
            return False
        if ship.direction == "horizontal":
            dx = ship.size
            dy = 1
        else:
            dx = 1
            dy = ship.size
        if (0 <= point.x and point.x + dx <= self.width
                and 0 <= point.y and point.y + dy <= self.height):
            ship.position = point
            self.emit('updated')
            return True
        ship.position = None
        self.emit('updated')
        return False

    def get_ships_at(self, point):
        return filter(lambda ship: point in ship.get_position_points(), sorted(self._ships, key=lambda x: x.size))

    def shoot_to(self, point):
        pass

    def change_ship_direction(self, ship):
        if not isinstance(ship, Ship):
            raise TypeError
        if ship not in self._ships:
            raise ReferenceError
        if ship.position is not None:
            return False
        pos = ship.position
        if ship.direction == "horizontal":
            overflow = pos.y + ship.size - self.height
            if overflow > 0:
                new_pos = Point(pos.x, pos.y - overflow)
                if new_pos.y < 0:
                    ship.position = None
                    self.emit('updated')
                    return False
                ship.position = new_pos
            ship.direction = "vertical"
        else:
            overflow = pos.x + ship.size - self.width
            if overflow > 0:
                new_pos = Point(pos.x - overflow, pos.y)
                if new_pos.x < 0:
                    ship.position = None
                    self.emit('updated')
                    return False
                ship.position = new_pos
            ship.direction = "horizontal"
        self.emit('updated')
        return True

    def get_conflicted_points(self):
        pass

    def is_alive(self, ship):
        if ship not in self._ships:
            raise ReferenceError
        return

    def has_alive_ship(self):
        pass

    def get_shoots(self):
        return self._shots
