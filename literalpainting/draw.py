import bottle

history = None

def init(hist):
    history = hist

stack = None

class UnderspecifiedShapeError(Exception):
    pass

class Drawable:
    def i_am_a(self):
        return str(self.__class__).rsplit('.').pop().lower()
    def do(self):
        """ Returns the json needed to draw itself. """
        raise NotImplementedError

def identity(x):
    return x

def loc(x,y):
    return (x,y)

def pixel(p):
    return p

def diameter(rad):
    return (int(rad)//2,)

def radius(rad):
    return (rad,)

class Circle(Drawable):
    def __init__(self, at=None, rad=None):
        self.at = at
        self.rad = rad

    def do(self):
        """ Returns the json needed to draw itself. """
        if not self.at or not self.rad:
            raise UnderspecifiedShapeError, "I am missing a radius or location." 
        return self.at + self.rad + ('circle',)

class Line(Drawable):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def do(self):
        return start + end + ('line',)

class Rectangle(Drawable):
    def __init__(self, start, end):
        return start + end + ('rectangle',)

functions = \
    {
    'rectangle': Rectangle,
    'line': Line,
    'circle': Circle,
    'radius': radius,
    'diameter': diameter,
    'pixel': pixel,
    'loc': loc,
    'identity': identity,
}
