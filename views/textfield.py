import pygame as pg
from settings import COLOR_INACTIVE, COLOR_ACTIVE
from views.base_view import BaseView
class InputBox(BaseView):
    def __init__(self, x, y, w, h, font,on_enter_func,is_numerable=False, text='',):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.font = font
        self.active = False
        self.is_numerable = is_numerable
        self.on_enter_func = on_enter_func

    def check_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.on_enter_func()
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if not self.is_numerable or event.unicode.isdigit():
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update_size(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def update(self, screen):
        # Blit the text.
        self.update_size()
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

