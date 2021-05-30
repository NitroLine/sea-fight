from .point import Point

directions = {
    'vertical' : [Point(0,0),Point(0,1),Point(0,2),Point(0,3),Point(0,4)],
    'horizontal' : [Point(0,0),Point(1,0),Point(2,0),Point(3,0),Point(4,0)],
    'cube-1' : [Point(0,0),Point(1,0),Point(0,1),Point(1,1),Point(2,1)],
    'cube-2' : [Point(0,0),Point(0,1),Point(1,0),Point(1,1),Point(1,2)],
    'cube-3' : [Point(0,0),Point(1,0),Point(1,1),Point(0,1),Point(1,2)],
    'cube-4' : [Point(0,0),Point(0,1),Point(1,1),Point(1,0),Point(2,1)],
    'line-1' : [Point(0,0),Point(1,0),Point(2,0),Point(2,1),Point(2,2)],
    'line-2' : [Point(0,0),Point(0,1),Point(0,2),Point(1,2),Point(2,2)],
    'line-3' : [Point(0,0),Point(0,1),Point(0,2),Point(1,0),Point(2,0)],
    'line-4' : [Point(0,0),Point(1,0),Point(1,1),Point(1,2),Point(2,2)],
    'line-5' : [Point(0,0),Point(0,1),Point(1,1),Point(2,1),Point(2,2)],
}

directions_for_size = {
    1: ['horizontal'],
    2: ['horizontal', 'vertical'],
    3: ['horizontal', 'vertical', 'cube-1', 'cube-3', 'cube-4'],
    4: ['horizontal', 'vertical', 'cube-1', 'line-1','line-2','line-3','line-4','line-5'],
    5: ['horizontal', 'vertical', 'cube-1','cube-2', 'cube-3', 'cube-4', 'line-1','line-2','line-3','line-4','line-5'],
}

class Ship:
    def __init__(self, size):
        self.size = size
        self._direction = 'horizontal'
        self.dx = size - 1
        self.dy = 0
        self.position = None

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        points = directions[value]
        self._direction = value
        dx = 0
        dy = 0
        for i in range(self.size):
            dx = max(dx, points[i].x)
            dy = max(dy, points[i].y)
        self.dx = dx
        self.dy = dy

    def get_position_points(self):
        ans = []
        if self.position:
            for i in range(self.size):
                ans.append(self.position + directions[self.direction][i])
        return ans
