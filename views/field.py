from pygame import Rect, draw
import pygame
from .base_view import BaseView
from settings import *

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
        self.rects = self.generate_point_to_rect(self.rect.width, self.rect.height)

    def change_size(self,width,height):
        self.rect.width = width
        self.rect.height = height
        self.rects = self.generate_point_to_rect(width,height)

    def generate_point_to_rect(self, width, height):
        res = dict()
        for x in range(self.field.width):
            for y in range(self.field.height):
                left = (width - 2) * x // self.field.width + 1
                right = (width - 2) * (x + 1) // self.field.width + 1
                top = (height - 2) * y // self.field.height + 1
                bottom = (height - 2) * (y + 1) // self.field.height + 1
                rectangle = Rect(self.x+left, self.y+top, right - left, bottom - top)
                res[(self.x+x, self.y+y)] = rectangle
        return res


    def draw_ship(self, surface,ship,conflicted_points,shots,use_light):
        for point in ship.get_position_points():
            if not self.fog_of_war or point in shots:
                Drawer.draw_ship_cell(surface,self.rects[point],
                                      use_light=use_light,
                                      in_conflict= point in conflicted_points,
                                      is_shot= point in shots)


    def update(self, surface):
        for rect in self.rects.values():
            Drawer.draw_cell(surface,rect)
        conflicted_points = self.field.get_conflicted_points()
        shots = self.field.get_shoots()
        for shot in shots:
            Drawer.draw_shot_cell(surface,self.rects[shot])
        for ship in filter(lambda x: x != self.now_selected_ship, self.field.get_ships()):
            self.draw_ship(surface,ship,conflicted_points,shots,False)
        if self.now_selected_ship is not None:
            self.draw_ship(surface,self.now_selected_ship,conflicted_points,shots,True)



    def check_event(self,event):
        if event.type == pygame.USEREVENT:
            print(event.data)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for point in self.rects:
                if self.rects[point].collidepoint(pos):
                    print(pos, self.rects[point])



class Drawer:
    @staticmethod
    def draw_shot_cell(surface, rect):
        draw.ellipse(surface,LIGHT_BLUE,rect)

    @staticmethod
    def draw_ship_cell(surface,rect,is_shot,in_conflict,use_light):
        border_color = YELLOW if use_light else LIGHT_BLUE
        color = LIGHT_RED if in_conflict else BLUE
        draw.rect(surface, rect, color)
        draw.rect(surface, rect, border_color, 2)
        if is_shot:
            draw.line(surface, GRAY, rect.topleft, rect.bottomright)
            draw.line(surface, GRAY, rect.topright, rect.bottomleft)

    @staticmethod
    def draw_cell(surface, rect):
        draw.rect(surface, GRAY, rect)
        draw.rect(surface, LIGHT_BLUE, rect, 2)


