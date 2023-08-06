from .graphic import Graphic 
import math

class InputError(Exception):
    pass
class ShortSideInputError(InputError):
    pass
class LongSideInputError(InputError):
    pass

class Rectangle(Graphic):
    def __init__(self,short_len,long_len):
        self.short_len = short_len
        self.long_len = long_len
        self.perimeter = 2*(short_len+long_len)
        self.area = short_len*long_len
        
    def cal_perimeter(self):
        try:
            if self.long_len <= 0:
                raise LongSideInputError
            if self.short_len <= 0:
                raise ShortSideInputError
        except LongSideInputError:
            print("Long side length should be positive!")
            return None
        except ShortSideInputError:
            print("Short side length should be positive!")
            return None
        return 2*(self.short_len+self.long_len)
    
    def cal_area(self):
        return self.short_len*self.long_len
    
    def cal_area_circumcircle(self):
        gougu = self.short_len**2+self.long_len**2
        r2 = gougu/4
        return math.pi*r2
        
        
    