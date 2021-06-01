class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x} {self.y})'

    def get_round_points(self):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                yield Point(self.x + dx, self.y + dy)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x * 809 + self.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
