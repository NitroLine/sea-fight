import random

from models.point import Point


class BaseAI:
    def __init__(self):
        self.field = None

    def setup(self, field):
        self.field = field

    def generate_shot(self):
        pass

    def put_ship_automatic(self):
        pass


class AutomaticPutShip(BaseAI):
    def try_put_ships(self, try_count):
        for i in range(try_count):
            ship = self.field.get_first_to_put_ship()
            if ship is None:
                break
            x = random.randint(0, self.field.width - 1)
            y = random.randint(0, self.field.height - 1)
            p = Point(x, y)
            self.field.put_ship(ship, p)
            if ship.position is None:
                return
            if random.randint(0, 1):
                self.field.change_ship_direction(ship)
            if any(self.field.get_conflicted_points()):
                self.field.put_ship(ship, Point(-1, -1))
        return self.field.get_first_to_put_ship() is None and not any(self.field.get_conflicted_points())

    def remove_all_ships(self):
        for ship in filter(lambda s: s.position is not None, self.field.get_ships()):
            self.field.put_ship(ship, Point(-1, -1))

    def put_ship_automatic(self):
        for i in range(1000):
            self.remove_all_ships()
            if self.try_put_ships(1000):
                return True
        return False



class SimpleRandomAI(AutomaticPutShip):
    def generate_shot(self):
        shots = self.field.get_shoots()
        for i in range(1000):
            x = random.randint(0, self.field.width - 1)
            y = random.randint(0, self.field.height - 1)
            p = Point(x, y)
            if p not in shots:
                return p
        for y in range(self.field.height):
            for x in range(self.field.width):
                p = Point(x, y)
                if p not in shots:
                    return p
        return Point(0, 0)

