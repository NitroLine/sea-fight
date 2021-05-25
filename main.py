import pygame

from controls.fight_control import Fight2PlayerControl, FightAgainstAIControl
from controls.putting_ships_control import PuttingShipsControl, AIPuttingShipControl
from models.game import Game
from models.options import Options
from settings import *
from views.button import Button
from views.field import FieldView
from views.text import Text
from views.timer import Timer

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption("SEA FIGHT")

GAME_FONT = pygame.font.SysFont('Comic Sans MS', 30)

game_options = Options(10, 10)


class Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = Game(pygame, settings=game_options)
        self.running = True
        self.is_two_player = True
        self.menu = {
            'title': Text("SEA FIGHT", WIDTH / 2 - 90, HEIGHT / 2 - 200, BLACK, GAME_FONT),
            'start_1_player_button': Button((WIDTH / 2 - 100, HEIGHT / 2 - 100, 200, 50), BLUE,
                                            self.start_one_player_game, text="1 Player",
                                            **BUTTON_STYLE),
            'start_2_player_button': Button((WIDTH / 2 - 100, HEIGHT / 2 - 40, 200, 50), BLUE,
                                            self.start_two_player_game, text="2 Players",
                                            **BUTTON_STYLE),
            'exit_button': Button((WIDTH / 2 - 100, HEIGHT / 2 + 20, 200, 50), BLUE, self.exit_from_game, text="Exit",
                                  **BUTTON_STYLE)
        }
        self.two_player_fight = {
            'first_player_field': FieldView(WIDTH / 2 - 500, HEIGHT / 2 - 200, 400, 400),
            'second_player_field': FieldView(WIDTH / 2 + 100, HEIGHT / 2 - 200, 400, 400),
            'fight_controller': Fight2PlayerControl(),
            'first_field_text': Text("First Player Field", WIDTH / 2 - 500, HEIGHT / 2 - 250, BLACK, GAME_FONT),
            'second_field_text': Text("Second Player Field", WIDTH / 2 + 100, HEIGHT / 2 - 250, BLACK, GAME_FONT),
            'which_turn_text': Text("First Player Turn", WIDTH / 2 - 100, HEIGHT / 2 - 350, BLACK, GAME_FONT),
            'timer': Timer(WIDTH / 2 - 50, 50, BLACK, GAME_FONT)
        }
        self.putting_ships_first = {
            'player_field': FieldView(WIDTH / 2 - 200, HEIGHT / 2 - 200, 400, 400),
            'putting_ships_controller': PuttingShipsControl(),
            'go_next_button': Button((100, 100, 200, 50), BLUE, lambda x: x, text="Next", **BUTTON_STYLE, hidden=True),
            'text': Text("First player arranges ships", WIDTH / 2 - 100, HEIGHT / 2 - 350, BLACK, GAME_FONT),
        }
        self.putting_ships_second = {
            'player_field': FieldView(WIDTH / 2 - 200, HEIGHT / 2 - 200, 400, 400),
            'putting_ships_controller': PuttingShipsControl(),
            'go_next_button': Button((100, 100, 200, 50), BLUE, lambda x: x, text="Next", **BUTTON_STYLE, hidden=True),
            'text': Text("Second player arranges ships", WIDTH / 2 - 100, HEIGHT / 2 - 350, BLACK, GAME_FONT),
        }
        self.putting_ships_human = {
            'player_field': FieldView(WIDTH / 2 - 200, HEIGHT / 2 - 200, 400, 400),
            'putting_ships_controller': AIPuttingShipControl(),
            'go_next_button': Button((100, 100, 200, 50), BLUE, lambda x: x, text="Next", **BUTTON_STYLE, hidden=True),
            'text': Text("Arrange your ships", WIDTH / 2 - 100, HEIGHT / 2 - 350, BLACK, GAME_FONT),
        }
        self.against_ai_battle_scene = {
            'player_field': FieldView(WIDTH / 2 - 500, HEIGHT / 2 - 200, 400, 400),
            'ai_field': FieldView(WIDTH / 2 + 100, HEIGHT / 2 - 200, 400, 400),
            'fight_controller': FightAgainstAIControl(),
            'player_text': Text("Human Field", WIDTH / 2 - 500, HEIGHT / 2 - 300, BLACK, GAME_FONT),
            'ai_text': Text("AI Field", WIDTH / 2 + 100, HEIGHT / 2 - 300, BLACK, GAME_FONT),
        }
        self.end_screen = {
            'who_win_text': Text("Wining", WIDTH / 2 - 90, HEIGHT / 2 - 200, BLACK, GAME_FONT),
            'first_player_field': FieldView(WIDTH / 2 - 500, HEIGHT / 2 - 200, 400, 400),
            'second_player_field': FieldView(WIDTH / 2 + 100, HEIGHT / 2 - 200, 400, 400),
            'restart_button': Button((WIDTH / 2 - 100, HEIGHT / 2 + 20, 200, 50), BLUE, self.restart_game,
                                     text="To main menu",
                                     **BUTTON_STYLE)
        }
        self.current_scene = self.menu

    def exit_from_game(self):
        self.running = False

    def start_two_player_game(self):
        self.game.start('First', 'Second')
        self.putting_ships_first['player_field'].setup(self.game.first_player.field, False)
        self.putting_ships_first['putting_ships_controller'].setup(self.game,
                                                                   self.putting_ships_first['go_next_button'],
                                                                   self.putting_ships_first['player_field'])
        self.is_two_player = True
        self.current_scene = self.putting_ships_first

    def start_one_player_game(self):
        self.game.start('Human', 'AI')
        self.putting_ships_human['player_field'].setup(self.game.first_player.field, False)
        self.is_two_player = False
        self.putting_ships_human['putting_ships_controller'].setup(self.game,
                                                                   self.putting_ships_human['go_next_button'],
                                                                   self.putting_ships_human['player_field'])
        self.current_scene = self.putting_ships_human

    def restart_game(self):
        self.game = Game(pygame, game_options)
        self.current_scene = self.menu

    def main_loop(self):
        while self.running:
            # Держим цикл на правильной скорости
            self.clock.tick(FPS)
            # Ввод процесса (события)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.exit_from_game()
                if event.type == pygame.USEREVENT:
                    if event.data['name'] == 'player_changed' \
                            and self.game.stage == "putting_ships" \
                            and self.is_two_player:
                        self.putting_ships_second['player_field'].setup(self.game.second_player.field, False)
                        self.putting_ships_second['putting_ships_controller'].setup(self.game,
                                                                                    self.putting_ships_second[
                                                                                        'go_next_button'],
                                                                                    self.putting_ships_second[
                                                                                        'player_field'])
                        self.current_scene = self.putting_ships_second
                    if event.data['name'] == 'state_changed' \
                            and event.data['new_stage'] == 'battle':
                        if self.is_two_player:
                            self.two_player_fight['fight_controller'].setup(self.game,
                                                                            self.two_player_fight['first_player_field'],
                                                                            self.two_player_fight[
                                                                                'second_player_field'])
                            self.two_player_fight['timer'].setup(pygame, 60, self.game.move_to_next_player)
                            self.current_scene = self.two_player_fight
                        else:
                            self.against_ai_battle_scene['fight_controller'].setup(self.game,
                                                                                   self.against_ai_battle_scene[
                                                                                       'player_field'],
                                                                                   self.against_ai_battle_scene[
                                                                                       'ai_field'])
                            self.current_scene = self.against_ai_battle_scene
                    if event.data['name'] == 'state_changed' \
                            and event.data['new_stage'] == 'finished':
                        self.end_screen['who_win_text'].text = self.game.current_player.name + " WIN"
                        self.end_screen['first_player_field'].setup(self.game.first_player.field, False)
                        self.end_screen['second_player_field'].setup(self.game.second_player.field, False)
                        self.current_scene = self.end_screen
                    if event.data['name'] == 'player_changed' \
                            and self.game.stage == "battle" \
                            and self.is_two_player:
                        self.two_player_fight['which_turn_text'].text = event.data['player'].name + " Turn"
                        self.two_player_fight['timer'].reset()
                for element in self.current_scene.values():
                    element.check_event(event)

            # Обновление
            self.screen.fill(WHITE)
            for element in self.current_scene.values():
                element.update(self.screen)
            pygame.display.update()


# Цикл игры
window = Window()
window.main_loop()
pygame.quit()
