import math
from shapely.geometry import Point

# get the angle of two vectors
def get_angle_of_two_vectors(v1, v2):
    root = Point(0, 0)
    return angleBetweenOriented(v1, root, v2)

def checkLeft(tail, tip1, tip2):
    return angleBetweenOriented(tail, tip1, tip2) < 0

def angleBetweenOriented(tip1, tail, tip2) :
    a1 = angle(tail, tip1)
    a2 = angle(tail, tip2)
    angDel = a2 - a1
    
    # normalize, maintaining orientation
    if angDel <= -math.pi:
        return angDel + 2 * math.pi
    if angDel > math.pi:
        return angDel - 2 * math.pi
    return angDel

def angle(v0, v1):
    dx = v1.x - v0.x
    dy = v1.y - v0.y
    return math.atan2(dy, dx)