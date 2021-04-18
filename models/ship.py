from .point import Point


class Ship:
    def __init__(self, size):
        self.size = size
        self.direction = None
        self.position = None

    def get_position_points(self):
        ans = []
        if self.position:
            for i in range(self.size):
                if self.position == 'horizontal':
                    ans.append(Point(self.position.x + i, self.position.y))
                else:
                    ans.append(Point(self.position.x, self.position.y + i))
        return ans
