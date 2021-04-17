# Pygame шаблон - скелет для нового проекта Pygame
import pygame
from models.game import Game
import random

WIDTH = 480
HEIGHT = 360
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
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
game = Game(pygame)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    game.change_stage('ME')
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            print(event.data)

    # Обновление

    # Рендеринг
    screen.fill(BLUE)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()