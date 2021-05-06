from views.base_view import BaseView
import pygame

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
            self.click_on_point(pos,event.button)