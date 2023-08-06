from geometry.calculation.rectangle_cal import Rectangle
from geometry.calculation.round_cal import Round

def is_same_shape(a,b):
    if type(a)==type(b):
        return True
    return False

def is_same(a,b):
    try:
        if type(a)!=Rectangle and type(a)!=Round:
            raise TypeError("Only Rectangle and Round type allowed")
    except TypeError as ex:
        print("Message:",ex)
        return None
    try:
        if type(b)!=Rectangle and type(b)!=Round:
            raise TypeError("Only Rectangle and Round type allowed")
    except TypeError as ex:
        print("Message:",ex) 
        return None  
        
    if is_same_shape(a,b):
        if type(a)==Rectangle:
            return a.short_len == b.short_len and a.long_len == b.long_len
        else:
            return a.radius == b.radius
    return False

def big_area(a,b):
    try:
        if type(a)!=Rectangle and type(a)!=Round:
            raise TypeError("Only Rectangle and Round type allowed")
    except TypeError as ex:
        print("Message:",ex)
        return None
    try:
        if type(b)!=Rectangle and type(b)!=Round:
            raise TypeError("Only Rectangle and Round type allowed")
    except TypeError as ex:
        print("Message:",ex)
        return None
    
    if a.area>b.area:

        return a
    elif a.area<b.area:

        return b
    print("a and b have the same area")
    return None

