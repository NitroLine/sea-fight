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

    def is_current_player_win(self):
        pass

    def is_ready_for_battle(self):
        pass

    def create_player(self, name):
        field = self.settings.create_field()
        for ship in self.settings.create_fleet():
            field.add_ship(ship)
        return Player(name, field)

    def change_stage(self, stage):
        self.stage = stage
        self.emit('stage_changed')
