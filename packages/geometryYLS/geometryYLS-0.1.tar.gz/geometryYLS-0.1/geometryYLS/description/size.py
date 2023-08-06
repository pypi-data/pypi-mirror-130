from __future__ import division
from geometry.calculation.round_cal import Round
from geometry.calculation.rectangle_cal import Rectangle
import math


def change_side_for_rec(rectangle,side_type,value):
    if side_type == "long":
        if rectangle.long_len+value<=0:
            print("Error. The value is negative or zero")
            return
        else:
            rec = Rectangle(rectangle.short_len,rectangle.long_len+value)
            return rec
    elif side_type == "short":
        if rectangle.short_len+value<=0:
            print("Error. The value is negative or zero")
            return
        else:
            rec = Rectangle(rectangle.short_len+value,rectangle.long_len)
            return rec

    print("The side type is wrong")
    return None

def change_radius_for_round(ori_round, value):
    if ori_round.radius +value<=0:
        print("Error. The value is negative or zero")
        return
    else:
        res = Round(ori_round.radius+value)
        return res

def change_area(graphic,value):
    if type(graphic)==Rectangle:
        ori_area = graphic.area
        if ori_area+value <= 0:
            print("Error. The value is negative or zero")
            return
        new_area = ori_area+value
        new_short = new_area/graphic.long_len
        new_graphic = Rectangle(new_short,graphic.long_len)
        return new_graphic
    if type(graphic)==Round:
        ori_area = graphic.area
        if ori_area+value<=0:
            print("Error. The value is negative or zero")
            return
        new_area = ori_area+value
        new_r = math.sqrt(new_area/math.pi)
        new_graphic = Round(new_r)
        return new_graphic
    print("The graphic is not rectangle or round")
    return None
