from geometry.calculation.round_cal import Round
from geometry.calculation.rectangle_cal import Rectangle
import math

def round_to_square(a):
    sq = a.area
    side_len = sq**0.5
    square = Rectangle(side_len,side_len)
    return square

def square_to_round(a):
    sq = a.area
    r = (a.area/math.pi)**0.5
    roun = Round(r)
    return roun

def round_to_rect(a,long_side):
    sq = a.area
    short_side = sq/long_side
    rec = Rectangle(long_side,short_side)
    return rec
