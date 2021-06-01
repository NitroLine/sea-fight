from views.base_view import BaseView


class Timer(BaseView):
    def __init__(self, x, y, color, font):
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.start_ticks = 0
        self.time = 0
        self.on_end_func = None
        self.pygame = None
        self.is_ended = True
        self.pause_different = 0

    def setup(self, pygame, time_in_seconds, on_end_func):
        self.start_ticks = pygame.time.get_ticks()
        self.time = time_in_seconds
        self.on_end_func = on_end_func
        self.pygame = pygame

    def reset(self):
        if self.pygame is not None:
            self.start_ticks = self.pygame.time.get_ticks()
            self.is_ended = False

    def pause(self):
        self.is_ended = True
        self.pause_different = self.pygame.time.get_ticks()

    def resume(self):
        self.is_ended = False
        self.start_ticks += self.pygame.time.get_ticks() - self.pause_different

    def update(self, surface):
        if not self.is_ended:
            seconds = (self.pygame.time.get_ticks() - self.start_ticks) / 1000
            cur_time = max(self.time - seconds, 0)
            if cur_time == 0:
                self.on_end_func()
                self.is_ended = True
                self.reset()
        else:
            cur_time = 0
        cur_minutes = int(cur_time // 60)
        cur_seconds = round(cur_time % 60, 1)
        text = self.font.render(f'{cur_minutes}:{cur_seconds}', True,
                                self.color)
        surface.blit(text, (self.x, self.y))
