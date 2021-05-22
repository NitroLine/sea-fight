import pygame

from controls.AI import SimpleRandomAI, AutomaticPutShip
from views.base_view import BaseView


class PuttingShipsControl(BaseView):
    def __init__(self):
        self.game = None
        self.end_button = None
        self.field_view = None
        self.auto_put = None

    def setup(self, game, end_button, field_view):
        self.game = game
        self.end_button = end_button
        self.field_view = field_view
        auto_put = AutomaticPutShip()
        auto_put.setup(field_view.field)
        auto_put.put_ship_automatic()
        end_button.function = self.end_putting_ships

    def end_putting_ships(self):
        self.game.end_putting_current_player_ships()

    def click_on_point(self, pos, mouse_button):
        point = self.field_view.global_pos_to_local_point(pos)
        if mouse_button == 3:
            self.field_view.now_selected_ship = None
        elif mouse_button == 1:
            if point is None:
                return
            selected_ship = self.field_view.now_selected_ship
            if selected_ship is not None:
                if point in selected_ship.get_position_points():
                    self.game.current_player.field.change_ship_direction(selected_ship)
                else:
                    self.game.current_player.field.put_ship(selected_ship, point)
                self.field_view.now_selected_ship = None
                return
            ship_on_point = next(self.game.current_player.field.get_ships_at(point), None)
            if ship_on_point is not None:
                self.field_view.now_selected_ship = ship_on_point
                return

            ship_to_put = self.game.current_player.field.get_first_to_put_ship()
            if ship_to_put is not None:
                self.game.current_player.field.put_ship(ship_to_put, point)
                return

    def check_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.data['name'] == 'updated':
                self.end_button.hidden = not self.game.is_current_can_end_putting()

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.click_on_point(pos, event.button)


class AIPuttingShipControl(PuttingShipsControl):
    def __init__(self):
        super().__init__()
        self.ai = SimpleRandomAI()

    def end_putting_ships(self):
        if self.game.current_player == self.game.first_player:
            self.game.end_putting_current_player_ships()
        if self.game.current_player == self.game.second_player:
            self.ai.setup(self.game.current_player.field)
            if self.ai.put_ship_automatic():
                self.game.end_putting_current_player_ships()
            else:
                raise RuntimeError("AI can't put all ships to field")
