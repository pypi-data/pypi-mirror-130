from geometry.calculation.round_cal import Round
from geometry.calculation.rectangle_cal import Rectangle
import math

def round_to_square(a):
    try:
        if type(a)!=Round:
            raise TypeError("Only Round type allowed")
    except TypeError as ex:
        print("Message:",ex)
        return None
    sq = a.area
    side_len = sq**0.5
    square = Rectangle(side_len,side_len)
    return square

def square_to_round(a):
    try:
        if type(a)!=Rectangle:
            raise TypeError("Only Rectangle type allowed")
    except TypeError as ex:
        print("Message:",ex)
        return None
    
    sq = a.area
    r = (a.area/math.pi)**0.5
    roun = Round(r)
    return roun

def round_to_rect(a,long_side):
    try:
        if type(a)!=Round:
            raise TypeError("Only Round type allowed")
    except TypeError as ex:
        print("Message:",ex)
        return None    
    sq = a.area
    try:
        short_side = sq/long_side
        math.sqrt(short_side)
    except ValueError as ve:
        print("The side should be a positive number")
        return None   
    except ZeroDivisionError as de:
        print("The long_side should not be zero")
        return None  
    
    rec = Rectangle(long_side,short_side)
    return rec
