import pygame

from controls.AI import SimpleRandomAI
from views.base_view import BaseView


class Fight2PlayerControl(BaseView):
    def __init__(self):
        self.game = None
        self.first_field_view = None
        self.second_field_view = None

    def setup(self, game, first_field_view, second_field_view):
        self.game = game
        self.first_field_view = first_field_view
        self.second_field_view = second_field_view

        self.first_field_view.setup(game.first_player.field, True)
        self.second_field_view.setup(game.second_player.field, True)

    def click_on_point(self, pos, button):
        if button == 1:
            if self.game.current_player == self.game.first_player:
                point = self.second_field_view.global_pos_to_local_point(pos)
                if point is None:
                    return
                self.game.shoot_to(point)
            elif self.game.current_player == self.game.second_player:
                point = self.first_field_view.global_pos_to_local_point(pos)
                if point is None:
                    return
                self.game.shoot_to(point)

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.click_on_point(pos, event.button)


class FightAgainstAIControl(BaseView):
    def __init__(self):
        self.game = None
        self.player_field = None
        self.ai_field = None
        self.ai = SimpleRandomAI()
        self.ai_turns = []

    def setup(self, game, player_field, ai_field):
        self.game = game
        self.player_field = player_field
        self.ai_field = ai_field

        self.player_field.setup(game.first_player.field, False)
        self.ai_field.setup(game.second_player.field, True)

    def click_on_point(self, pos, button):
        if button == 1:
            if self.game.current_player == self.game.first_player:
                point = self.ai_field.global_pos_to_local_point(pos)
                if point is None:
                    return
                self.game.shoot_to(point)

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.click_on_point(pos, event.button)
        if event.type == pygame.USEREVENT:
            if event.data['name'] == 'ready_to_shoot':
                if self.game.stage == 'battle' and self.game.current_player == self.game.second_player:
                    self.ai.setup(self.game.first_player.field)
                    shot = self.ai.generate_shot(turns=self.ai_turns)
                    self.ai_turns.append(self.game.shoot_to(shot))
