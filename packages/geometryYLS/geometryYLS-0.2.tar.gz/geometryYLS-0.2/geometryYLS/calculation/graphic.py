class Graphic():
    def __init__(self,perimeter,area,side_len):
        self.perimeter = perimeter
        self.area = area
        self.side_len = side_len
    def print_perimeter(self):
        print(f"The perimeter is: {self.perimeter}")
        return self.perimeter
    def print_area(self):
        print(f"The area is: {self.area}")
        return self.area
    def print_perimeter_and_area(self):
        print(f"The perimeter is: {self.perimeter}")
        print(f"The area is: {self.area}")
        return self.perimeter, self.area