class Game:
    def __init__(self):
        self.stage = "not_started"
        self.first_player = Player()
        self.second_player = Player()
        self.turn = 1


class Field:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self._shots = []
        self._ships = []




class Player:
    def __init__(self,name,field):
        self.name = name
        self.field = field


class Ship:
    def __init__(self,size):
        self.size = size
        self.direction = None
        self.position = None

    def get_position_points(self):
        ans = []
        if self.position:
            for i in range(self.size):
                if self.position == 'horizontal':
                    ans.append(Point(self.position.x + i,self.position.y))
                else:
                    ans.append(Point(self.position.x, self.position.y + i))
        return ans

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x} {self.y})'