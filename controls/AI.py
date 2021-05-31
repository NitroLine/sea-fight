import random

from models.point import Point
from models.ship import directions_for_size


class BaseAI:
    def __init__(self):
        self.field = None

    def setup(self, field):
        self.field = field

    def generate_shot(self, turns):
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
            for j in range(random.randint(0, len(directions_for_size[ship.size]))):
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
    def generate_shot(self, turns):
        shots = self.field.get_shoots()
        for i in range(len(turns) - 1, -1, -1):
            if turns[i]['status']:
                last_hit = turns[i]['point']
                if not self.is_all_around_points_shots(last_hit, shots):
                    if not self.is_left_point_shot(last_hit, shots):
                        point = Point(last_hit.x - 1, last_hit.y)
                        if self.field.is_inside_field(point):
                            return point
                    if not self.is_right_point_shot(last_hit, shots):
                        point = Point(last_hit.x + 1, last_hit.y)
                        if self.field.is_inside_field(point):
                            return point
                    if  not self.is_up_point_shot(last_hit, shots):
                        point = Point(last_hit.x, last_hit.y + 1)
                        if self.field.is_inside_field(point):
                            return point
                    if not self.is_bottom_point_shot(last_hit, shots):
                        point = Point(last_hit.x, last_hit.y - 1)
                        if self.field.is_inside_field(point):
                            return point
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

    @staticmethod
    def is_all_around_points_shots(point, shots):
        points = point.get_round_points()
        for t in points:
            if t not in shots:
                return False
        return True

    @staticmethod
    def is_any_around_points_hit(point, turns):
        return SimpleRandomAI.is_left_point_hit(point, turns) \
               or SimpleRandomAI.is_right_point_hit(point, turns) \
               or SimpleRandomAI.is_up_point_hit(point, turns) \
               or SimpleRandomAI.is_bottom_point_hit(point, turns)

    @staticmethod
    def is_left_point_hit(point, turns):
        for turn in turns:
            if turn['status'] and turn['point'] == Point(point.x - 1, point.y):
                return True
        return False

    @staticmethod
    def is_right_point_hit(point, turns):
        for turn in turns:
            if turn['status'] and turn['point'] == Point(point.x + 1, point.y):
                return True
        return False

    @staticmethod
    def is_bottom_point_hit(point, turns):
        for turn in turns:
            if turn['status'] and turn['point'] == Point(point.x, point.y - 1):
                return True
        return False

    @staticmethod
    def is_up_point_hit(point, turns):
        for turn in turns:
            if turn['status'] and turn['point'] == Point(point.x, point.y + 1):
                return True
        return False

    @staticmethod
    def is_left_point_shot(point, shots):
        return Point(point.x - 1, point.y) in shots

    @staticmethod
    def is_right_point_shot(point, shots):
        return Point(point.x + 1, point.y) in shots

    @staticmethod
    def is_up_point_shot(point, shots):
        return Point(point.x, point.y + 1) in shots

    @staticmethod
    def is_bottom_point_shot(point, shots):
        return Point(point.x, point.y - 1) in shots
