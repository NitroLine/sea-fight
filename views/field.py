from pygame import Rect, draw, USEREVENT
from .base_view import BaseView

class FieldView(BaseView):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.field = None
        self.rect = Rect(x, y, width, height)
        self.rects = None
        self.fog_of_war = False

    def setup(self, field, fog_of_war):
        self.fog_of_war = fog_of_war
        self.field = field
        self.rects = self.generate_point_to_rect(self.width, self.height)

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

    def update(self, surface):
        for rect in self.rects.values():
            draw.rect(surface, [255, 0, 0], rect, 2)

    def check_event(self,event):
        if event.type == USEREVENT:
            print(event.data)
