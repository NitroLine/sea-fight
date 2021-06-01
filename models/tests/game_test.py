from ..point import Point
from ..game import Game
from ..options import Options



class TestGame:
    def test_init_not_started(self):
        game = Game()
        assert game.stage == 'not_started'
        assert game.first_player is None
        assert game.second_player is None
        assert game.current_player is None

    def test_game_play(self):
        setting = Options(10,10)
        setting.set_fleet(3)
        game = Game(settings=setting)
        game.start('first','second')
        assert game.stage == 'putting_ships'
        ship1 = game.current_player.field.get_first_to_put_ship()
        game.current_player.field.put_ship(ship1,Point(2,5))
        game.end_putting_current_player_ships()
        assert game.stage == 'putting_ships'
        ship2 = game.current_player.field.get_first_to_put_ship()
        game.current_player.field.put_ship(ship2,Point(2,5))
        game.end_putting_current_player_ships()
        assert game.stage == 'battle'
        game.shoot_to(Point(2,5))
        game.shoot_to(Point(3,5))
        game.shoot_to(Point(4,5))
        assert game.stage == 'finished'


