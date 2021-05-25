from ..ship import Ship
from ..point import Point


def test_create_not_placed_horizontal_ship():
    ship = Ship(3)
    assert ship.size == 3
    assert ship.direction == 'horizontal'
    assert ship.position is None


def test_get_position_points_return_nothing_when_not_placed():
    ship = Ship(3)
    ship.position = None
    assert list(ship.get_position_points()) == [ ]


def test_get_position_points_when_horizontal():
    ship = Ship(3)
    ship.position = Point(2, 5)
    ship.direction = 'horizontal'
    assert list(ship.get_position_points()) == [
        Point(2, 5),
        Point(3, 5),
        Point(4, 5)
    ]


def test_get_position_points_when_vertical():
    ship = Ship(3)
    ship.position = Point(2, 5)
    ship.direction = 'vertical'
    assert list(ship.get_position_points()) == [
        Point(2, 5),
        Point(2, 6),
        Point(2, 7)
    ]
