# Pygame шаблон - скелет для нового проекта Pygame
import pygame
from models.game import Game
from views.button import Button
from views.field import FieldView
from views.text import Text
from settings import *
from controls.putting_ships_control import PuttingShipsControl
import random

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption("SEA FIGHT")

GAME_FONT = pygame.font.SysFont('Comic Sans MS', 30)

class Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = Game(pygame)
        self.running = True
        self.menu = [
            Text("SEA FIGHT", WIDTH/2 - 90, HEIGHT/2-200,BLACK,GAME_FONT),
            Button((WIDTH/2-100,HEIGHT/2-100,200,50),BLUE, self.start_one_player_game, text="1 Player", **BUTTON_STYLE),
            Button((WIDTH/2-100,HEIGHT/2-40,200,50),BLUE, self.start_one_player_game, text="2 Player", **BUTTON_STYLE),
            Button((WIDTH/2-100,HEIGHT/2+20,200,50),BLUE, self.exit_from_game, text="Exit", **BUTTON_STYLE)
        ]
        self.two_fields = [
            FieldView(WIDTH / 2 - 300, HEIGHT / 2 - 100, 200, 200),
            FieldView(WIDTH / 2 + 100, HEIGHT / 2 - 100, 200, 200)
        ]
        self.putting_ships = [
            FieldView(WIDTH / 2 - 200, HEIGHT / 2 - 200, 400, 400),
            PuttingShipsControl(),
            Button((100,100,200,50), BLUE, lambda x: x, text="Battle", **BUTTON_STYLE, hidden = True),

        ]
        self.current_scene = self.menu

    def exit_from_game(self):
        self.running = False

    def start_one_player_game(self):
        self.game.start('HUMAN', "AI")
        self.putting_ships[0].setup(self.game.first_player.field, False)
        self.putting_ships[1].setup(self.game, self.putting_ships[2], self.putting_ships[0])
        self.current_scene = self.putting_ships

    def main_loop(self):
        while self.running:
            # Держим цикл на правильной скорости
            self.clock.tick(FPS)
            # Ввод процесса (события)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.exit_from_game()
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
