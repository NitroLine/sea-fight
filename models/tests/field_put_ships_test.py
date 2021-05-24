from ..ship import Ship
from ..field import Field
from ..point import Point
import pytest

class TestFieldPutShips:
    def setup(self):
        self.ship = Ship(3)
        self.big_ship = Ship(4)
        self.small_ship = Ship(1)
        self.field = Field(10,10)

        self.field.add_ship(self.ship)
        self.field.add_ship(self.small_ship)
        self.field.add_ship(self.big_ship)

    def test_get_first_to_put_ship_return_biggest_first(self):
        assert self.field.get_first_to_put_ship() == self.big_ship

    def test_get_first_to_put_ship_return_second_biggest_ship(self):
        self.big_ship.position = Point(0,0)
        assert self.field.get_first_to_put_ship() == self.ship

    def test_get_first_to_put_ship_none_when_no_ships(self):
        self.field = Field(10, 10)
        assert self.field.get_first_to_put_ship() is None

    def test_get_first_to_put_ship_none_when_no_ships_to_put(self):
        self.big_ship.position = Point(0, 0)
        self.ship.position = Point(0, 0)
        self.small_ship.position = Point(0, 0)
        assert self.field.get_first_to_put_ship() is None

    def test_put_ship_change_position(self):
        point = Point(2, 5)
        self.field.put_ship(self.ship,point)
        assert self.ship.position == point

    def test_put_ship_raise_when_ship_not_added(self):
        other_ship = Ship(3)
        point = Point(2, 5)
        with pytest.raises(RuntimeError) as e:
            self.field.put_ship(other_ship,point)
        assert e.type == RuntimeError

    @pytest.mark.parametrize("before_direction, after_direction", [('horizontal', 'vertical'), ('vertical', 'horizontal')])
    def test_change_ship_direction(self,before_direction, after_direction):
        point = Point(2, 5)
        self.ship.direction = before_direction
        self.field.put_ship(self.ship,point)

        self.field.change_ship_direction(self.ship)
        assert self.ship.direction == after_direction
        assert self.ship.position == point

    @pytest.mark.parametrize("x, y, direction,new_x,new_y",
                             [(9, 5, 'vertical', 7, 5),
                              (8, 5, 'vertical', 7, 5),
                              (2, 9, 'horizontal', 2, 7),
                              (2, 8, 'horizontal', 2, 7)])
    def test_change_ship_direction_move_ship_when_no_space(self,x,y,direction,new_x,new_y):
        point = Point(x,y)
        self.ship.direction = direction
        self.field.put_ship(self.ship, point)

        assert self.field.change_ship_direction(self.ship) == True
        assert self.ship.position == Point(new_x, new_y)

    def test_change_ship_direction_remove_ship_when_can_not_move_horizontal(self):
        field = Field(3,2)
        ship = Ship(3)
        field.add_ship(ship)
        ship.direction = 'horizontal'
        field.put_ship(ship, Point(0,0))
        assert field.change_ship_direction(ship) == False
        assert ship.position is None

    def test_change_ship_direction_remove_ship_when_can_not_move_vertical(self):
        field = Field(2,3)
        ship = Ship(3)
        field.add_ship(ship)
        ship.direction = 'vertical'
        field.put_ship(ship, Point(0,0))
        assert field.change_ship_direction(ship) == False
        assert ship.position is None

    def test_get_conflicted_points_no_ships(self):
        assert list(self.field.get_conflicted_points()) == []








