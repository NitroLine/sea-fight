class Game:
    first_player = None
    second_player = None
    current_turn = None

    def __init__(self,settings=None):
        self.stage = "not_started"
        if settings is not None:
            self.settings = settings
        else:
            self.settings = Options()

    def start(self,first_player_name,second_player_name):
        self.first_player = self.create_player(first_player_name)
        self.second_player = self.create_player(second_player_name)
        self.current_turn = 1
        self.change_stage('putting_ships')


    @property
    def current_player(self):
        if self.current_turn is None:
            return None
        if self.current_turn:
            return self.first_player
        else:
            return self.second_player

    def is_current_player_win(self):
        pass

    def is_ready_for_battle(self):
        pass

    def create_player(self,name):
        field = self.settings.create_field()
        for ship in self.settings.create_fleet():
            field.add_ship(ship)
        return Player(name,field)

    def change_stage(self,stage):
        self.stage = stage


class Options:
    def __init__(self,width=10,height=10):
        self.width = width
        self.height = height
        self.fleet_sizes = [1,1,1,1,2,2,2,3,3,4]

    def set_fleet(self,*fleet):
        self.fleet_sizes = fleet

    def create_field(self):
        return Field(self.width,self.height)

    def create_fleet(self):
        for size in self.fleet_sizes:
            yield Ship(size)


class Field:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self._shots = set()
        self._ships = set()

    def add_ship(self,ship):
        self._ships.add(ship)

    def get_ships(self):
        return list(self._ships)

    def get_first_to_put_ship(self):
        return next(filter(lambda x:x.position is not None, sorted(self._ships,key=lambda x:x.size)),None)

    def put_ship(self,ship,point):
        if not isinstance(ship,Ship):
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
            return True
        ship.position = None
        return False

    def get_ships_at(self,point):
        return filter(lambda ship:point in ship.get_position_points(), sorted(self._ships,key=lambda x:x.size))


    def shoot_to(self,point):
        pass

    def change_ship_direction(self,ship):
        if not isinstance(ship, Ship):
            raise TypeError
        if ship not in self._ships:
            raise ReferenceError
        if ship.position is not None:
            return False
        pos = ship.position
        if ship.direction == "horizontal":
            overflow =pos.y +ship.size - self.height
            if overflow > 0:
                new_pos = Point(pos.x,pos.y-overflow)
                if new_pos.y < 0:
                    ship.position = None
                    return False
                ship.position = new_pos
            ship.direction = "vertical"
        else:
            overflow = pos.x + ship.size - self.width
            if overflow > 0:
                new_pos = Point(pos.x - overflow, pos.y)
                if new_pos.x < 0:
                    ship.position = None
                    return False
                ship.position = new_pos
            ship.direction = "horizontal"
        return True

    def get_conflicted_points(self):
        pass

    def is_alive(self,ship):
        if ship not in self._ships:
            raise ReferenceError
        return

    def has_alive_ship(self):
        pass

    def get_shoots(self):
        return self._shots





class Player:
    def __init__(self,name,field):
        self.name = name
        self.field = field


class Ship:
    def __init__(self,size):
        self.size = size
        self.direction = None
        self.position = None

    def get_position_points(self):
        ans = []
        if self.position:
            for i in range(self.size):
                if self.position == 'horizontal':
                    ans.append(Point(self.position.x + i,self.position.y))
                else:
                    ans.append(Point(self.position.x, self.position.y + i))
        return ans

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x} {self.y})'