import bottle
import history

class UnderspecifiedShapeError(Exception):
    pass

class Drawable:
    def i_am_a(self):
        return str(self.__class__).rsplit('.').pop().lower()
    def draw(self):
        """ Returns the json needed to draw itself. """
        raise NotImplementedError

def draw(items):
    """ Return a list which will be converted to json for the draw.js drawing system. """
    if not (isinstance(items, list) 
            or isinstance(items, tuple)):
        items = [items]

    # Check whether all items are drawable
    assert(reduce(lambda x,y: x and y, map(lambda x: isinstance(x, Drawable), items)))

    # Track what we're drawing
    history.history.extend(items)

    return [item.draw() for item in items]

def identity(x):
    return x

def loc(x,y):
    return (x,y)

def pixel(p):
    return p

class Radius:
    def __init__(self, l):
        self.radius = int(l)

    def val(self):
        return self.radius

class Diameter(Radius):
    def __init__(self, l):
        self.radius = int(l)//2

def and_(x, y):
    return (x,y)

class Circle(Drawable):
    """ A round plane figure whose boundary (the circumference)
    consists of points equidistant from a fixed center.
    """
    def __init__(self, at=None, radius=None):
        assert isinstance(radius, Radius), "I do not know what the radius is."
        self.at = at
        self.radius = radius

    def draw(self):
        """ Returns the json needed to draw itself. """
        if not self.at or not self.radius:
            raise UnderspecifiedShapeError, "I am missing a radius or location." 
        return self.at + (self.radius.val(), 'circle')

class Line(Drawable):
    """A long, narrow mark or band.
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self):
        return self.start + self.end + ('line',)

class Rectangle(Drawable):
    """ A plane figure with four straight sides and four right angles, esp. one with unequal adjacent sides, in contrast to a square.
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self):
        return self.start + self.end + ('rectangle',)

class Question:
    def answer(self):
        raise NotImplementedError        

functions = \
    {
    'rectangle': Rectangle,
    'line': Line,
    'circle': Circle,
    'radius': Radius,
    'diameter': Diameter,
    'pixel': pixel,
    'loc': loc,
    'identity': identity,
    'and_': and_,
    'draw': draw,
}
