from .options import Options
from .player import Player
from .model import EventEmitter


class Game(EventEmitter):
    first_player = None
    second_player = None
    current_turn = None

    def __init__(self, game=None, settings=None):
        super().__init__(game)
        self.stage = "not_started"
        if settings is not None:
            self.settings = settings
        else:
            self.settings = Options()

    def start(self, first_player_name, second_player_name):
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

    @property
    def next_player(self):
        if self.current_turn is None:
            return None
        if self.current_turn:
            return self.second_player
        else:
            return self.first_player

    def is_current_player_win(self):
        next_player = self.next_player
        if next_player is None:
            return False
        return not next_player.field.has_alive_ship()

    @staticmethod
    def is_ready_for_battle(player):
        return player.field.get_first_to_put_ship() is None and not any(player.field.get_conflicted_points())

    def move_to_next_player(self):
        self.current_turn = not self.current_turn
        self.emit({'name':'player_changed','player':self.current_player})

    def create_player(self, name):
        field = self.settings.create_field()
        for ship in self.settings.create_fleet():
            field.add_ship(ship)
        return Player(name, field)

    def change_stage(self, stage):
        self.stage = stage
        self.emit({'name':'state_changed', 'new_stage':stage})

    def shoot_to(self,point):
        if self.stage != "Battle":
            raise RuntimeError("Can't shoot while not battle")

        shot_result = self.next_player.field.shoot_to(point)
        if shot_result == "hit":
            if self.is_current_player_win():
                self.change_stage('finished')
            else:
                self.emit({'name':'ready_to_shoot'})
        elif shot_result == "miss":
            self.move_to_next_player()
            self.emit({'name':'ready_to_shoot'})
        elif shot_result != 'cancel':
            raise RuntimeError("Unknown shot result")

    def is_can_begin_battle(self):
        return self.stage == 'arranging_ships' \
               and self.is_ready_for_battle(self.first_player)\
               and self.is_ready_for_battle(self.second_player)

