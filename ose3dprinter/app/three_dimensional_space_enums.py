"""A set of enumerations relating to three-dimensional space.
"""


class Axis:
    X = 'x'
    Y = 'y'
    Z = 'z'


class Side:
    FRONT = 'front'
    TOP = 'top'
    RIGHT = 'right'
    REAR = 'rear'
    BOTTOM = 'bottom'
    LEFT = 'left'


class Plane:
    XY = 'xy'
    YZ = 'yz'
    XZ = 'xz'