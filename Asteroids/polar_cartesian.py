from math import sqrt,sin,cos,atan2

def length(v):
    return sqrt(sum([coord ** 2 for coord in v]))

def distance(obj1,obj2):
    return sqrt((obj1.x-obj2.x)**2+(obj1.y-obj2.y)**2)

def distance_pts(x1,y1,x2,y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def to_cartesian(polar_vector):
    radius, angle = polar_vector[0], polar_vector[1]
    return [radius*cos(angle), radius*sin(angle)]

def to_polar(vector):
    x, y = vector[0], vector[1]
    angle = atan2(y,x)
    return [length(vector), angle]