class EventEmitter:
    def __init__(self, game=None):
        self.game = game

    def emit(self, event):
        if self.game is None:
            return
        ev = self.game.event.Event(self.game.USEREVENT, {'data': event})
        self.game.event.post(ev)
