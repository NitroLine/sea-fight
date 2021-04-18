from pygame import Rect, draw


class FieldView:
    def __init__(self, x, y, width, height, field):
        self.x = x
        self.y = y
        self.field = field
        self.rects = self.generate_point_to_rect(width, height)
        self.rect = Rect(x, y, width, height)

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

    def draw(self, screen):
        for rect in self.rects.values():
            draw.rect(screen, [255, 0, 0], rect, 2)
