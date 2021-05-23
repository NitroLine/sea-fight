from .model import EventEmitter
from .point import Point
from .ship import Ship


class Field(EventEmitter):
    def __init__(self, width, height, game=None):
        super().__init__(game)
        self.width = width
        self.height = height
        self._shots = set()
        self._ships = set()

    def add_ship(self, ship):
        self._ships.add(ship)
        self.emit({'name': 'updated'})

    def get_ships(self):
        return list(self._ships)

    def get_first_to_put_ship(self):
        return next(filter(lambda x: x.position is None, sorted(self._ships, key=lambda x: x.size, reverse=True)), None)

    def put_ship(self, ship, point):
        if not isinstance(ship, Ship):
            raise TypeError
        if ship not in self._ships:
            raise RuntimeError("Cant find ship")
        if ship.direction == "horizontal":
            dx = ship.size
            dy = 1
        else:
            dx = 1
            dy = ship.size

        if (0 <= point.x and point.x + dx <= self.width
                and 0 <= point.y and point.y + dy <= self.height):
            ship.position = point
            self.emit({'name': 'updated'})
            return True
        ship.position = None
        self.emit({'name': 'updated'})
        return False

    def is_inside_field(self,point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def get_ships_at(self, point):
        return filter(lambda ship: point in ship.get_position_points(),
                      sorted(self._ships, key=lambda x: x.size, reverse=True))

    def shoot_to(self, point):
        if point in self._shots:
            return "cancel"
        self._shots.add(point)
        ship = next(self.get_ships_at(point), None)
        if ship is None:
            self.emit({'name': 'updated'})
            return "miss"

        blow = all(map(lambda x: x in self._shots, ship.get_position_points()))
        if blow:
            self._shots = self._shots.union(self.get_ship_rounded_points(ship))
        self.emit({'name': 'updated'})
        return "hit"

    def get_ship_rounded_points(self, ship):
        return set(filter(self.is_inside_field,
                          [p for point in ship.get_position_points() for p in point.get_round_points()]))

    def change_ship_direction(self, ship):
        if not isinstance(ship, Ship):
            raise TypeError
        if ship not in self._ships:
            raise RuntimeError("Cant find ship")
        pos = ship.position
        if ship.direction == "horizontal":
            overflow = pos.y + ship.size - self.height
            if overflow > 0:
                new_pos = Point(pos.x, pos.y - overflow)
                if new_pos.y < 0:
                    ship.position = None
                    self.emit({'name': 'updated'})
                    return False
                ship.position = new_pos
            ship.direction = "vertical"
        else:
            overflow = pos.x + ship.size - self.width
            if overflow > 0:
                new_pos = Point(pos.x - overflow, pos.y)
                if new_pos.x < 0:
                    ship.position = None
                    self.emit({'name': 'updated'})
                    return False
                ship.position = new_pos
            ship.direction = "horizontal"
        self.emit({'name': 'updated'})
        return True

    def get_conflicted_points(self):
        ship_to_round_points = dict([(s, self.get_ship_rounded_points(s)) for s in self._ships])
        res = set()
        for ship in self._ships:
            position_points = ship.get_position_points()
            for point in position_points:
                is_point_in_other_ship = any(
                    map(lambda pair: not pair[0] == ship and point in pair[1], ship_to_round_points.items()))
                if is_point_in_other_ship:
                    res.add(point)
        return res

    def is_alive(self, ship):
        if ship not in self._ships:
            raise RuntimeError("Cant find ship")
        return any(map(lambda point: point not in self._shots, ship.get_position_points()))

    def has_alive_ship(self):
        return any(map(lambda ship: self.is_alive(ship), self._ships))

    def get_shoots(self):
        return self._shots
