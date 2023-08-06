from .graphic import Graphic 
import math

class InputError(Exception):
    pass

class Round(Graphic):
    def __init__(self,radius):
        self.radius = radius
        self.perimeter = 2*radius*math.pi
        self.area = radius**2*math.pi
        
    def cal_perimeter(self):
        try:
            if self.radius <= 0:
                raise InputError
        except InputError:
            print("Radius should be positive!")
            return None
        return 2*self.radius*math.pi
    
    def cal_area(self):
        return self.radius**2*math.pi
    
    def cal_area_ins_square(self):
        return 2*(self.radius**2)
        
 