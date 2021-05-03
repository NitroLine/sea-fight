import pygame
from .base_view import BaseView

class Text(BaseView):
    def __init__(self,text,x,y,color,font):
        self.x = x
        self.y = y
        self.color = color
        self.text =text
        self.font = font

    def update(self, surface):
        text = self.font.render(self.text, True, self.color)
        surface.blit(text, (self.x, self.y))