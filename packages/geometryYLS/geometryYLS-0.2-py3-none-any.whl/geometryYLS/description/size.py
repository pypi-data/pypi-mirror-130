from __future__ import division
import math
from geometry.calculation.round_cal import Round
from geometry.calculation.rectangle_cal import Rectangle



def change_side_for_rec(rectangle,side_type,value):
    try:
        if type(rectangle)!=Rectangle:
            raise TypeError("Only Rectangle type allowed")
    except TypeError as ex:
        print("Message:",ex)
        return None
    
    if side_type == "long":
        val = rectangle.long_len+value
        try:
            math.sqrt(val)
        except ValueError as ve:
            print("The new side should be a positive number")
            return None
        rec = Rectangle(rectangle.short_len,rectangle.long_len+value)
        return rec
    elif side_type == "short":
        val = rectangle.short_len+value
        try:
            math.sqrt(val)
        except ValueError as ve:
            print("The new side should be a positive number")
            return None     
        rec = Rectangle(rectangle.short_len+value,rectangle.long_len)
        return rec
    
    print("The side type is wrong")
    return None

def change_radius_for_round(ori_round, value):
    try:
        if type(ori_round)!=Round:
            raise TypeError("Only Round type allowed")
    except TypeError as ex:
        print("Message:",ex)
        return None  
    try:
        val = ori_round.radius +value
        math.sqrt(val)
    except ValueError as ve:
        print("The new radius should be a positive number")
        return None
   
    res = Round(ori_round.radius+value)
    return res

def change_area(graphic,value):
    try:
        if type(graphic)!=Rectangle and type(graphic)!=Round:
            raise TypeError("Only Rectangle and Round type allowed")
    except TypeError as ex:
        print("Message:",ex)
        return None
    
    if type(graphic)==Rectangle:
        ori_area = graphic.area
        try:
            val = ori_area+value
            math.sqrt(val)
        except ValueError as ve:
            print("The new area should be a positive number")
            return None         
        new_area = ori_area+value
        new_short = new_area/graphic.long_len
        new_graphic = Rectangle(new_short,graphic.long_len)
        return new_graphic
    
    if type(graphic)==Round:
        ori_area = graphic.area
        try:
            val = ori_area+value
            math.sqrt(val)
        except ValueError as ve:
            print("The new area should be a positive number")
            return None 
        new_area = ori_area+value
        new_r = math.sqrt(new_area/math.pi)
        new_graphic = Round(new_r)
        return new_graphic
    
    return None
