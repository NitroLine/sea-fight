from pygame import Rect, draw

from models.point import Point
from settings import *
from .base_view import BaseView


class FieldView(BaseView):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.field = None
        self.rect = Rect(x, y, width, height)
        self.rects = None
        self.fog_of_war = False
        self.now_selected_ship = None

    def setup(self, field, fog_of_war):
        self.fog_of_war = fog_of_war
        self.field = field
        self.rects = self.generate_point_to_rect(self.rect.width,
                                                 self.rect.height)

    def change_size(self, width, height):
        self.rect.width = width
        self.rect.height = height
        self.rects = self.generate_point_to_rect(width, height)

    def generate_point_to_rect(self, width, height):
        res = dict()
        for x in range(self.field.width):
            for y in range(self.field.height):
                left = (width - 2) * x // self.field.width + 1
                right = (width - 2) * (x + 1) // self.field.width + 1
                top = (height - 2) * y // self.field.height + 1
                bottom = (height - 2) * (y + 1) // self.field.height + 1
                rectangle = Rect(self.x + left, self.y + top, right - left,
                                 bottom - top)
                res[Point(x, y)] = rectangle
        return res

    def draw_ship(self, surface, ship, conflicted_points, shots, use_light):
        for point in ship.get_position_points():
            if not self.fog_of_war or point in shots:
                Drawer.draw_ship_cell(surface, self.rects[point],
                                      use_light=use_light,
                                      in_conflict=point in conflicted_points,
                                      is_shot=point in shots)

    def update(self, surface):
        for rect in self.rects.values():
            Drawer.draw_cell(surface, rect)
        conflicted_points = self.field.get_conflicted_points()
        shots = self.field.get_shoots()
        for shot in shots:
            Drawer.draw_shot_cell(surface, self.rects[shot])
        for ship in filter(lambda x: x != self.now_selected_ship,
                           self.field.get_ships()):
            self.draw_ship(surface, ship, conflicted_points, shots, False)
        if self.now_selected_ship is not None:
            self.draw_ship(surface, self.now_selected_ship, conflicted_points,
                           shots, True)

    def global_pos_to_local_point(self, pos):
        for point in self.rects:
            if self.rects[point].collidepoint(pos):
                return point


class Drawer:
    @staticmethod
    def draw_shot_cell(surface, rect):
        draw.ellipse(surface, SHOT_CELL_COLOR, rect)

    @staticmethod
    def draw_ship_cell(surface, rect, is_shot, in_conflict, use_light):
        border_color = SELECTED_BORDER_SHIP_COLOR if use_light\
            else BORDER_SHIP_COLOR
        color = CONFLICTED_SHIP_COLOR if in_conflict else SHIP_COLOR
        draw.rect(surface, color, rect)
        draw.rect(surface, border_color, rect, 4)
        if is_shot:
            draw.line(surface, DESTROY_SHIP_COLOR, rect.topleft,
                      rect.bottomright)
            draw.line(surface, DESTROY_SHIP_COLOR, rect.topright,
                      rect.bottomleft)

    @staticmethod
    def draw_cell(surface, rect):
        draw.rect(surface, CELL_COLOR, rect)
        draw.rect(surface, BORDER_CELL_COLOR, rect, 2)
