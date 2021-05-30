from ..ship import Ship
from ..field import Field
from ..point import Point
import pytest

# TODO Change test for new ships rotation

class TestFieldPutShips:
    def setup(self):
        self.ship = Ship(3)
        self.big_ship = Ship(4)
        self.small_ship = Ship(1)
        self.field = Field(10, 10)

        self.field.add_ship(self.ship)
        self.field.add_ship(self.small_ship)
        self.field.add_ship(self.big_ship)

    def test_get_first_to_put_ship_return_biggest_first(self):
        assert self.field.get_first_to_put_ship() == self.big_ship

    def test_get_first_to_put_ship_return_second_biggest_ship(self):
        self.big_ship.position = Point(0, 0)
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
        self.field.put_ship(self.ship, point)
        assert self.ship.position == point

    def test_put_ship_raise_when_ship_not_added(self):
        other_ship = Ship(3)
        point = Point(2, 5)
        with pytest.raises(RuntimeError) as e:
            self.field.put_ship(other_ship, point)
        assert e.type == RuntimeError

    @pytest.mark.parametrize("before_direction, after_direction",
                             [ ('horizontal', 'vertical'), ('vertical', 'horizontal') ])
    def test_change_ship_direction(self, before_direction, after_direction):
        point = Point(2, 5)
        self.ship.direction = before_direction
        self.field.put_ship(self.ship, point)

        self.field.change_ship_direction(self.ship)
        assert self.ship.direction == after_direction
        assert self.ship.position == point

    @pytest.mark.parametrize("x, y, direction,new_x,new_y",
                             [ (9, 5, 'vertical', 7, 5),
                               (8, 5, 'vertical', 7, 5),
                               (2, 9, 'horizontal', 2, 7),
                               (2, 8, 'horizontal', 2, 7) ])
    def test_change_ship_direction_move_ship_when_no_space(self, x, y, direction, new_x, new_y):
        point = Point(x, y)
        self.ship.direction = direction
        self.field.put_ship(self.ship, point)

        assert self.field.change_ship_direction(self.ship) == True
        assert self.ship.position == Point(new_x, new_y)

    def test_change_ship_direction_remove_ship_when_can_not_move_horizontal(self):
        field = Field(3, 2)
        ship = Ship(3)
        field.add_ship(ship)
        ship.direction = 'horizontal'
        field.put_ship(ship, Point(0, 0))
        assert field.change_ship_direction(ship) == False
        assert ship.position is None

    def test_change_ship_direction_remove_ship_when_can_not_move_vertical(self):
        field = Field(2, 3)
        ship = Ship(3)
        field.add_ship(ship)
        ship.direction = 'vertical'
        field.put_ship(ship, Point(0, 0))
        assert field.change_ship_direction(ship) == False
        assert ship.position is None

    def test_get_conflicted_points_no_ships(self):
        assert list(self.field.get_conflicted_points()) == [ ]

    def test_get_conflicted_points_empty_when_one_ship(self):
        point = Point(2, 5)
        self.field.put_ship(self.ship, point)
        assert list(self.field.get_conflicted_points()) == [ ]

    def test_get_conflicted_points_when_main_point_conflict(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(2, 5))
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.big_ship, Point(2, 5))
        assert self.field.get_conflicted_points() == {
            Point(2, 5),
            Point(3, 5),
            Point(2, 6)
        }

    def test_get_conflicted_points_when_back_point_conflict(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(2, 8))
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.big_ship, Point(4, 5))
        assert self.field.get_conflicted_points() == {
            Point(4, 8),
            Point(3, 8),
            Point(4, 7)
        }

    def test_get_conflicted_points_when_main_point_touch(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(3, 5))
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.big_ship, Point(2, 6))
        assert self.field.get_conflicted_points() == {
            Point(3, 5),
            Point(2, 6),
        }

    def test_get_conflicted_points_when_back_point_touch(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(1, 8))
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.big_ship, Point(4, 4))
        assert self.field.get_conflicted_points() == {
            Point(3, 8),
            Point(4, 7),
        }

    def test_get_conflicted_points_return_point_once_when_3_ships_in_conflict(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(2, 5))
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.big_ship, Point(2, 5))
        self.small_ship.direction = 'horizontal'
        self.field.put_ship(self.small_ship, Point(2, 5))
        assert self.field.get_conflicted_points() == {
            Point(3, 5),
            Point(2, 5),
            Point(2, 6)
        }

    def test_get_conflicted_points_when_3_ships_in_conflict(self):
        ship1 = Ship(1)
        ship2 = Ship(2)
        self.field.add_ship(ship1)
        self.field.add_ship(ship2)
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(2, 5))
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.big_ship, Point(2, 5))
        self.field.put_ship(ship1, Point(4, 5))
        self.field.put_ship(ship2, Point(2, 8))
        assert self.field.get_conflicted_points() == {
            Point(2, 5),
            Point(2, 6),
            Point(2, 7),
            Point(2, 8),
            Point(3, 8),
            Point(3, 5),
            Point(4, 5),
        }

    @pytest.mark.parametrize("x, y, direction",
                             [ (0, 5, 'vertical'),
                               (9, 5, 'vertical'),
                               (0, 5, 'horizontal'),
                               (7, 5, 'horizontal'),
                               (2, 0, 'horizontal'),
                               (2, 9, 'horizontal'),
                               (2, 0, 'vertical'),
                               (2, 7, 'vertical') ])
    def test_put_ship_before_out_of_bounds(self, x, y, direction):
        point = Point(x, y)
        self.ship.direction = direction
        assert self.field.put_ship(self.ship, point)
        assert self.ship.position == point

    @pytest.mark.parametrize("x, y, direction",
                             [ (-1, 5, 'vertical'),
                               (10, 5, 'vertical'),
                               (-1, 5, 'horizontal'),
                               (8, 5, 'horizontal'),
                               (2, -1, 'horizontal'),
                               (2, 10, 'horizontal'),
                               (2, -1, 'vertical'),
                               (2, 8, 'vertical') ])
    def test_put_ship_out_of_bounds(self, x, y, direction):
        point = Point(x, y)
        self.ship.direction = direction
        assert not self.field.put_ship(self.ship, point)
        assert self.ship.position is None

    def test_put_ship_reset_when_inside(self):
        point = Point(2, 5)
        self.field.put_ship(self.ship, point)

        second_point = Point(3, 6)
        assert self.field.put_ship(self.ship, second_point)
        assert self.ship.position == second_point

    def test_put_ship_remove_when_outside(self):
        point = Point(2, 5)
        self.field.put_ship(self.ship, point)

        second_point = Point(10, 5)
        assert not self.field.put_ship(self.ship, second_point)
        assert self.ship.position is None

    def test_get_ships_at_when_no_ship(self):
        point = Point(2, 5)
        assert list(self.field.get_ships_at(point)) == [ ]

    @pytest.mark.parametrize("dx, dy, direction",
                             [ (0, 0, 'horizontal'),
                               (1, 0, 'horizontal'),
                               (2, 0, 'horizontal'),
                               (0, 0, 'vertical'),
                               (0, 1, 'vertical'),
                               (0, 2, 'vertical') ])
    def test_get_ships_at_when_point_at_ship(self, dx, dy, direction):
        self.ship.direction = direction
        point = Point(2, 5)
        self.field.put_ship(self.ship, point)
        delta_point = Point(point.x + dx, point.y + dy)
        assert list(self.field.get_ships_at(delta_point)) == [ self.ship ]

    @pytest.mark.parametrize("dx, dy, direction",
                             [ (-1, 0, 'horizontal'),
                               (3, 0, 'horizontal'),
                               (0, -1, 'horizontal'),
                               (0, 1, 'horizontal'),
                               (1, 0, 'vertical'),
                               (-1, 0, 'vertical'),
                               (0, -1, 'vertical'),
                               (0, 3, 'vertical') ])
    def test_get_ships_at_when_point_out_ship(self, dx, dy, direction):
        self.ship.direction = direction
        point = Point(2, 5)
        self.field.put_ship(self.ship, point)
        delta_point = Point(point.x + dx, point.y + dy)
        assert list(self.field.get_ships_at(delta_point)) == [ ]

    def test_get_ships_after_put_fail(self):
        point = Point(8, 5)
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, point)
        assert list(self.field.get_ships_at(point)) == [ ]

    def test_get_ships_after_reset_ship(self):
        point = Point(2, 5)
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, point)

        second_point = Point(3, 6)
        self.field.put_ship(self.ship, second_point)
        assert list(self.field.get_ships_at(second_point)) == [ self.ship ]

    def test_get_ships_after_remove_ship(self):
        point = Point(2, 5)
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, point)

        second_point = Point(10, 6)
        self.field.put_ship(self.ship, second_point)
        assert list(self.field.get_ships_at(point)) == [ ]

    def test_get_ships_return_one_ship_when_double_placed(self):
        point = Point(2, 5)
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, point)
        self.field.put_ship(self.ship, point)
        assert list(self.field.get_ships_at(point)) == [ self.ship ]

    def test_get_ships_return_from_small_to_big(self):
        point = Point(2, 5)
        self.ship.direction = 'horizontal'
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.ship, point)
        self.field.put_ship(self.small_ship, point)
        self.field.put_ship(self.big_ship, point)
        assert list(self.field.get_ships_at(point)) == [
            self.small_ship,
            self.ship,
            self.big_ship
        ]

    def test_change_ship_direction_raise_when_ship_not_added(self):
        other_ship = Ship(3)
        with pytest.raises(RuntimeError) as e:
            self.field.change_ship_direction(other_ship)
        assert e.type == RuntimeError

    def test_change_ship_direction_do_nothing_when_not_put(self):
        self.ship.direction = 'horizontal'
        self.field.change_ship_direction(self.ship)
        assert self.ship.direction == 'horizontal'
