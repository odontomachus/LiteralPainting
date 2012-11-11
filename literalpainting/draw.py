functions = \
    {
    'rectangle': lambda start, end: start + end + ('rectangle',),
    'line': lambda start, end: start + end + ('line',),

    'draw': lambda x: x,

    'circle': lambda at, rad: at + rad + ('circle',),

    'radius': lambda rad: (rad,),

    'diameter': lambda rad: (int(rad)//2,),

    'pixel': lambda p: p,

    'loc': lambda x,y: (x,y),

    'identity': lambda x: x,

}
