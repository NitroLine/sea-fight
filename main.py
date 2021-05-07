# Pygame шаблон - скелет для нового проекта Pygame
import pygame

from controls.fight_control import Fight2PlayerControl, FightAgainstAIControl
from controls.putting_ships_control import PuttingShipsControl, AIPuttingShipControl
from models.game import Game
from models.options import Options
from settings import *
from views.button import Button
from views.field import FieldView
from views.text import Text

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption("SEA FIGHT")

GAME_FONT = pygame.font.SysFont('Comic Sans MS', 30)

game_options = Options(10, 10)
game_options.set_fleet(10)


class Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = Game(pygame, settings=game_options)
        self.running = True
        self.is_two_player = True
        self.menu = [
            Text("SEA FIGHT", WIDTH / 2 - 90, HEIGHT / 2 - 200, BLACK, GAME_FONT),
            Button((WIDTH / 2 - 100, HEIGHT / 2 - 100, 200, 50), BLUE, self.start_one_player_game, text="1 Player",
                   **BUTTON_STYLE),
            Button((WIDTH / 2 - 100, HEIGHT / 2 - 40, 200, 50), BLUE, self.start_two_player_game, text="2 Players",
                   **BUTTON_STYLE),
            Button((WIDTH / 2 - 100, HEIGHT / 2 + 20, 200, 50), BLUE, self.exit_from_game, text="Exit", **BUTTON_STYLE)
        ]
        self.two_player_fight = [
            FieldView(WIDTH / 2 - 500, HEIGHT / 2 - 200, 400, 400),
            FieldView(WIDTH / 2 + 100, HEIGHT / 2 - 200, 400, 400),
            Fight2PlayerControl(),
            Text("First Player Field", WIDTH / 2 - 500, HEIGHT / 2 - 250, BLACK, GAME_FONT),
            Text("Second Player Field", WIDTH / 2 + 100, HEIGHT / 2 - 250, BLACK, GAME_FONT),
            Text("First Player Turn", WIDTH / 2 - 100, HEIGHT / 2 - 350, BLACK, GAME_FONT),
        ]
        self.putting_ships_first = [
            FieldView(WIDTH / 2 - 200, HEIGHT / 2 - 200, 400, 400),
            PuttingShipsControl(),
            Button((100, 100, 200, 50), BLUE, lambda x: x, text="Next", **BUTTON_STYLE, hidden=True),
            Text("First player arranges ships", WIDTH / 2 - 100, HEIGHT / 2 - 350, BLACK, GAME_FONT),
        ]
        self.putting_ships_second = [
            FieldView(WIDTH / 2 - 200, HEIGHT / 2 - 200, 400, 400),
            PuttingShipsControl(),
            Button((100, 100, 200, 50), BLUE, lambda x: x, text="Next", **BUTTON_STYLE, hidden=True),
            Text("Second player arranges ships", WIDTH / 2 - 100, HEIGHT / 2 - 350, BLACK, GAME_FONT),
        ]
        self.putting_ships_human = [
            FieldView(WIDTH / 2 - 200, HEIGHT / 2 - 200, 400, 400),
            AIPuttingShipControl(),
            Button((100, 100, 200, 50), BLUE, lambda x: x, text="Next", **BUTTON_STYLE, hidden=True),
            Text("Arrange your ships", WIDTH / 2 - 100, HEIGHT / 2 - 350, BLACK, GAME_FONT),
        ]
        self.against_ai_battle_scene = [
            FieldView(WIDTH / 2 - 500, HEIGHT / 2 - 200, 400, 400),
            FieldView(WIDTH / 2 + 100, HEIGHT / 2 - 200, 400, 400),
            FightAgainstAIControl(),
            Text("Human Field", WIDTH / 2 - 500, HEIGHT / 2 - 300, BLACK, GAME_FONT),
            Text("AI Field", WIDTH / 2 + 100, HEIGHT / 2 - 300, BLACK, GAME_FONT),
        ]
        self.end_screen = [
            Text("Wining", WIDTH / 2 - 90, HEIGHT / 2 - 200, BLACK, GAME_FONT),
            FieldView(WIDTH / 2 - 500, HEIGHT / 2 - 200, 400, 400),
            FieldView(WIDTH / 2 + 100, HEIGHT / 2 - 200, 400, 400),
            Button((WIDTH / 2 - 100, HEIGHT / 2 + 20, 200, 50), BLUE, self.restart_game, text="To main menu",
                   **BUTTON_STYLE)
        ]
        self.current_scene = self.menu

    def exit_from_game(self):
        self.running = False

    def start_two_player_game(self):
        self.game.start('First', 'Second')
        self.putting_ships_first[0].setup(self.game.first_player.field, False)
        self.putting_ships_first[1].setup(self.game, self.putting_ships_first[2], self.putting_ships_first[0])
        self.is_two_player = True
        self.current_scene = self.putting_ships_first

    def start_one_player_game(self):
        self.game.start('Human', 'AI')
        self.putting_ships_human[0].setup(self.game.first_player.field, False)
        self.is_two_player = False
        self.putting_ships_human[1].setup(self.game, self.putting_ships_human[2], self.putting_ships_human[0])
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
                    if event.data[
                        'name'] == 'player_changed' and self.game.stage == "putting_ships" and self.is_two_player:
                        self.putting_ships_second[0].setup(self.game.second_player.field, False)
                        self.putting_ships_second[1].setup(self.game, self.putting_ships_second[2],
                                                           self.putting_ships_second[0])
                        self.current_scene = self.putting_ships_second
                    if event.data['name'] == 'state_changed' and event.data['new_stage'] == 'battle':
                        if self.is_two_player:
                            self.two_player_fight[2].setup(self.game, self.two_player_fight[0],
                                                           self.two_player_fight[1])
                            self.current_scene = self.two_player_fight
                        else:
                            self.against_ai_battle_scene[2].setup(self.game, self.against_ai_battle_scene[0],
                                                                  self.against_ai_battle_scene[1])
                            self.current_scene = self.against_ai_battle_scene
                    if event.data['name'] == 'state_changed' and event.data['new_stage'] == 'finished':
                        self.end_screen[0].text = self.game.current_player.name + " WIN"
                        self.end_screen[1].setup(self.game.first_player.field, False)
                        self.end_screen[2].setup(self.game.second_player.field, False)
                        self.current_scene = self.end_screen
                    if event.data['name'] == 'player_changed' and self.game.stage == "battle" and self.is_two_player:
                        self.two_player_fight[5].text = event.data['player'].name + " Turn"
                for element in self.current_scene:
                    element.check_event(event)

            # Обновление
            self.screen.fill(WHITE)
            for element in self.current_scene:
                element.update(self.screen)
            pygame.display.update()


# Цикл игры
window = Window()
window.main_loop()
pygame.quit()
