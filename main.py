# Pygame шаблон - скелет для нового проекта Pygame
import pygame
from models.game import Game
from views.view import FieldView
import random

WIDTH = 1080
HEIGHT = 720
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SEA FIGHT")
clock = pygame.time.Clock()
game = Game(pygame)
game.start('HUMAN', "AI")
player_field = FieldView(50, 50, 200, 200, game.first_player.field)
enemy_field = FieldView(350, 50, 200, 200, game.second_player.field)
screen.fill(WHITE)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            print(event.data)

    # Обновление
    player_field.draw(screen)
    enemy_field.draw(screen)
    pygame.display.update()
    # Рендеринг

    # После отрисовки всего, переворачиваем экран


pygame.quit()
