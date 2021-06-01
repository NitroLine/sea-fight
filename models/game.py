from .model import EventEmitter
from .options import Options
from .player import Player


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

    def end_putting_current_player_ships(self):
        if not self.is_current_can_end_putting():
            return
        if not self.is_can_begin_battle():
            self.move_to_next_player()
            return
        self.move_to_next_player()
        self.change_stage('battle')

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
        return player.field.get_first_to_put_ship() is None and not any(
            player.field.get_conflicted_points())

    def move_to_next_player(self):
        self.current_turn = not self.current_turn
        self.emit({'name': 'player_changed', 'player': self.current_player})

    def create_player(self, name):
        field = self.settings.create_field(self.game)
        for ship in self.settings.create_fleet():
            field.add_ship(ship)
        return Player(name, field)

    def change_stage(self, stage):
        self.stage = stage
        self.emit({'name': 'state_changed', 'new_stage': stage})

    def shoot_to(self, point):
        if self.stage != "battle":
            raise RuntimeError("Can't shoot while not battle")
        status = False
        shot_result = self.next_player.field.shoot_to(point)
        if shot_result == "hit":
            status = True
            if self.is_current_player_win():
                self.change_stage('finished')
            else:
                self.emit({'name': 'ready_to_shoot'})
        elif shot_result == "miss":
            self.move_to_next_player()
            self.emit({'name': 'ready_to_shoot'})
        elif shot_result != 'cancel':
            raise RuntimeError("Unknown shot result")

        return {'point': point, 'status': status}

    def is_can_begin_battle(self):
        return self.stage == 'putting_ships' \
               and self.is_ready_for_battle(self.first_player) \
               and self.is_ready_for_battle(self.second_player)

    def is_current_can_end_putting(self):
        return self.stage == 'putting_ships' \
               and self.is_ready_for_battle(self.current_player)
