import pytest

from ..field import Field
from ..point import Point
from ..ship import Ship



class TestFieldPutShips:
    def setup(self):
        self.ship = Ship(3)
        self.big_ship = Ship(4)
        self.small_ship = Ship(1)
        self.field = Field(10, 10)

        self.field.add_ship(self.ship)
        self.field.add_ship(self.small_ship)
        self.field.add_ship(self.big_ship)

    @pytest.mark.parametrize("x, y",
                             [(1, 5),
                              (5, 5),
                              (2, 4),
                              (2, 6)])
    def test_shoot_to_miss_return(self, x, y):
        self.field.put_ship(self.ship, Point(2, 5))
        shoot_point = Point(x, y)
        assert self.field.shoot_to(shoot_point) == 'miss'

    @pytest.mark.parametrize("x, y",
                             [(1, 5),
                              (5, 5),
                              (2, 4),
                              (2, 6)])
    def test_shoot_to_miss_to_shoots(self, x, y):
        self.field.put_ship(self.ship, Point(2, 5))
        shoot_point = Point(x, y)
        self.field.shoot_to(shoot_point)
        assert self.field.get_shoots() == {shoot_point}

    @pytest.mark.parametrize("x, y",
                             [(1, 5),
                              (5, 5),
                              (2, 4),
                              (2, 6)])
    def test_shoot_to_miss_to_shoots_not_duplicate(self, x, y):
        self.field.put_ship(self.ship, Point(2, 5))
        shoot_point = Point(x, y)
        self.field.shoot_to(shoot_point)
        self.field.shoot_to(shoot_point)
        assert self.field.get_shoots() == {shoot_point}

    @pytest.mark.parametrize("x, y",
                             [(2, 5),
                              (3, 5),
                              (4, 5)])
    def test_shoot_to_hit_return(self, x, y):
        self.field.put_ship(self.ship, Point(2, 5))
        shoot_point = Point(x, y)
        assert self.field.shoot_to(shoot_point) == 'hit'

    @pytest.mark.parametrize("x, y",
                             [(2, 5),
                              (3, 5),
                              (4, 5)])
    def test_shoot_to_hit_to_shoots(self, x, y):
        self.field.put_ship(self.ship, Point(2, 5))
        shoot_point = Point(x, y)
        self.field.shoot_to(shoot_point)
        assert self.field.get_shoots() == {shoot_point}

    @pytest.mark.parametrize("x, y",
                             [(2, 5),
                              (3, 5),
                              (4, 5)])
    def test_shoot_to_hit_to_shoots_not_duplicate(self, x, y):
        self.field.put_ship(self.ship, Point(2, 5))
        shoot_point = Point(x, y)
        self.field.shoot_to(shoot_point)
        self.field.shoot_to(shoot_point)
        assert self.field.get_shoots() == {shoot_point}

    @pytest.mark.parametrize("x, y",
                             [(2, 5),
                              (3, 5),
                              (4, 5)])
    def test_shoot_to_hit_return_cancel_when_hit_again(self, x, y):
        self.field.put_ship(self.ship, Point(2, 5))
        shoot_point = Point(x, y)
        self.field.shoot_to(shoot_point)
        assert self.field.shoot_to(shoot_point) == 'cancel'

    def test_shoot_to_not_blow_when_last_needed(self):
        self.field.put_ship(self.ship, Point(2, 5))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(3, 5))
        assert self.field.get_shoots() == {Point(2, 5), Point(3, 5)}

    def test_shoot_to_hit_when_blow(self):
        self.field.put_ship(self.ship, Point(2, 5))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(3, 5))
        assert self.field.shoot_to(Point(4,5)) == 'hit'\

    def test_shoot_to_blow_up_shoots(self):
        self.field.put_ship(self.ship, Point(2, 5))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(3, 5))
        self.field.shoot_to(Point(4, 5))
        assert self.field.get_shoots() ==  {Point(1,4), Point(2,4),Point(3,4),Point(4,4),Point(5,4),
                                            Point(1,5), Point(2,5),Point(3,5),Point(4,5),Point(5,5),
                                            Point(1,6), Point(2,6),Point(3,6),Point(4,6),Point(5,6)}
    @pytest.mark.parametrize("x, y",
                             [(1,4), (2,4),(3,4),(4,4),(5,4),
                                (1,5), (2,5),(3,5),(4,5),(5,5),
                                (1,6), (2,6),(3,6),(4,6),(5,6)])
    def test_shoot_to_cancel_after_blow_up(self, x, y):
        self.field.put_ship(self.ship, Point(2, 5))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(3, 5))
        self.field.shoot_to(Point(4, 5))
        assert self.field.shoot_to(Point(x,y)) == 'cancel'

    @pytest.mark.parametrize("x, y",
                             [(1,4), (2,4),(3,4),(4,4),(5,4),
                                (1,5), (2,5),(3,5),(4,5),(5,5),
                                (1,6), (2,6),(3,6),(4,6),(5,6)])
    def test_shoot_to_not_duplicate_after_blow_up(self, x, y):
        self.field.put_ship(self.ship, Point(2, 5))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(3, 5))
        self.field.shoot_to(Point(4, 5))
        shoot_to = Point(x, y)
        self.field.shoot_to(shoot_to)
        assert self.field.get_shoots() == {Point(1, 4), Point(2, 4), Point(3, 4), Point(4, 4), Point(5, 4),
                                           Point(1, 5), Point(2, 5), Point(3, 5), Point(4, 5), Point(5, 5),
                                           Point(1, 6), Point(2, 6), Point(3, 6), Point(4, 6), Point(5, 6)}

    def test_shoot_to_blow_up_top_left_corner(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(0, 0))
        self.field.shoot_to(Point(0, 0))
        self.field.shoot_to(Point(1, 0))
        self.field.shoot_to(Point(2, 0))
        assert self.field.get_shoots() == {Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0),
                                           Point(0, 1), Point(1, 1), Point(2, 1), Point(3, 1)}

    def test_shoot_to_blow_up_top_right_corner(self):
        self.ship.direction = 'vertical'
        self.field.put_ship(self.ship, Point(9, 0))
        self.field.shoot_to(Point(9, 0))
        self.field.shoot_to(Point(9, 1))
        self.field.shoot_to(Point(9, 2))
        assert self.field.get_shoots() == {Point(8, 0), Point(9, 0), Point(8, 1), Point(9, 1),
                                           Point(8, 2), Point(9, 2), Point(8, 3), Point(9, 3)}

    def test_shoot_to_blow_up_bottom_left_corner(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(7, 9))
        self.field.shoot_to(Point(7, 9))
        self.field.shoot_to(Point(8, 9))
        self.field.shoot_to(Point(9, 9))
        assert self.field.get_shoots() == {Point(6, 8), Point(7, 8), Point(8, 8), Point(9, 8),
                                           Point(6, 9), Point(7, 9), Point(8, 9), Point(9, 9)}

    def test_shoot_to_blow_up_bottom_right_corner(self):
        self.ship.direction = 'vertical'
        self.field.put_ship(self.ship, Point(0, 7))
        self.field.shoot_to(Point(0, 7))
        self.field.shoot_to(Point(0, 8))
        self.field.shoot_to(Point(0, 9))
        assert self.field.get_shoots() == {Point(0, 6), Point(1, 6), Point(0, 7), Point(1, 7),
                                           Point(0, 8), Point(1, 8), Point(0, 9), Point(1, 9)}

    def test_get_shoots_when_two_ships_hit(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(2, 5))
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.big_ship, Point(8, 3))
        self.field.shoot_to(Point(3, 5))
        self.field.shoot_to(Point(8, 5))
        assert self.field.get_shoots() == {Point(3, 5), Point(8, 5)}

    def test_get_shoots_when_blow_up_and_miss(self):
        self.field.put_ship(self.small_ship, Point(2, 5))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(8, 5))
        assert self.field.get_shoots() == {Point(1, 4), Point(2, 4), Point(3,4),
                                           Point(1, 5), Point(2, 5), Point(3, 5),
                                           Point(1, 6), Point(2, 6), Point(3, 6),
                                           Point(8, 5)}

    def test_is_alive_raise_when_ship_not_added(self):
        other_ship = Ship(3)
        point = Point(2, 5)
        other_ship.position = point
        with pytest.raises(RuntimeError) as e:
            self.field.is_alive(other_ship)
        assert e.type == RuntimeError

    def test_is_alvie_when_ship_not_hit(self):
        self.field.put_ship(self.ship, Point(2, 5))
        assert self.field.is_alive(self.ship)

    def test_is_alive_when_ship_has_alive_point(self):
        self.field.put_ship(self.ship, Point(2, 5))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(4, 5))
        assert self.field.is_alive(self.ship)

    def test_is_alive_when_ship_blow_up(self):
        self.field.put_ship(self.ship, Point(2, 5))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(3, 5))
        self.field.shoot_to(Point(4, 5))
        assert not self.field.is_alive(self.ship)

    def test_has_alive_ships_when_no_ships(self):
        assert not self.field.has_alive_ship()

    def test_has_alive_ships_two_ships_hit_first(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(2, 5))
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.big_ship, Point(8, 3))
        self.field.shoot_to(Point(3, 5))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(4, 5))

        self.field.shoot_to(Point(8, 5))
        self.field.shoot_to(Point(8, 3))
        self.field.shoot_to(Point(8, 4))
        assert self.field.has_alive_ship()

    def test_has_alive_ships_two_ships_hit_last(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(2, 5))
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.big_ship, Point(8, 3))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(4, 5))

        self.field.shoot_to(Point(8, 5))
        self.field.shoot_to(Point(8, 3))
        self.field.shoot_to(Point(8, 4))
        self.field.shoot_to(Point(8, 6))
        assert self.field.has_alive_ship()

    def test_has_alive_ships_two_ships_was_blow_up(self):
        self.ship.direction = 'horizontal'
        self.field.put_ship(self.ship, Point(2, 5))
        self.big_ship.direction = 'vertical'
        self.field.put_ship(self.big_ship, Point(8, 3))
        self.field.shoot_to(Point(3, 5))
        self.field.shoot_to(Point(2, 5))
        self.field.shoot_to(Point(4, 5))
        self.field.shoot_to(Point(8, 5))
        self.field.shoot_to(Point(8, 3))
        self.field.shoot_to(Point(8, 4))
        self.field.shoot_to(Point(8, 6))
        assert not self.field.has_alive_ship()


