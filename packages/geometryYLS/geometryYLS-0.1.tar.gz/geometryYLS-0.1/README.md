# Geometry-project

Yilin Sun and Song Zhang 

The geometry project has two sub packages. 

## calculation sub package

The calculation sub packages has 3 modules: graphic.py, rectangle_cal.py and round_cal.py.

__________________________

In the graphic.py, we have 1 parent class with 3 functions to define the Graphic class. 

The print_perimeter function is used to print the perimeter parameter of the object in class Graphic. It returns the value of self.perimeter.

The print_area function is used to print the area parameter of the object in class Graphic. It returns the value of self.area.

The print_perimeter_and_area function is used to print the perimeter and area parameters of the object in class Graphic. It returns the values of self.perimeter and self.area.

__________________________

In the rectangle_cal.py, we have 1 child class with 3 functions to calculate the perimeter, area, and the circumcircle area of rectangle.

The cal_perimeter function is used to calculate the perimeter of rectangle in the child class Rectangle. It calculates the rectangle perimeter by summing the length of its short and long sides, and then doubles the sum. It returns the value of the rectangle perimeter calculation result.

The cal_area function is used to calculate the area of rectangle in the child class Rectangle. It calculates the rectangle area by multiplying  the length of its short and long sides. It returns the value of the rectangle area calculation result.

The cal_area_circumcircle function is used to calculate the area of the circumcircle of rectangle in the child class Rectangle. As the diameter of the circumcircle is the diagonal of rectangle, we calculate the square of the length of the diameter by calculating the square of the length of the diagonal. Then, we calculate the area of the circumcircle according to the circle area formula with respect to the diameter, S=pi*d^2/4. This function returns the value of the area of the circumcircle of rectangle.

__________________________

In the round_cal.py, we have 1 child class with 3 functions to calculate the perimeter, area, and the inscribed square area of round.

The cal_perimeter function is used to calculate the perimeter of round in the child class Round. It calculates the round perimeter according to the circle perimeter formula with respect to the radius, C=2\*r\*pi. It returns the value of the round perimeter calculation result.

The cal_area function is used to calculate the area of round in the child class Round. It calculates the round area according to the circle area formula with respect to the radius, S=pi\*r^2. It returns the value of the round area calculation result.

The cal_area_ins_square function used to calculate the area of the inscribed square of round in the child class Round. As the diagonal of the inscribed square is the the diameter of the round, we firstly calculate the area of the inscribed square by calculating each of the four small right-angled triangles in the inscribed square, using the right-angled triangle area formula s=(1/2)\*radius^2. Then, we calculate the area of the inscribed square by 4\*s, and that is 2\*radius^2. This function returns the value of the area of the inscribed square of round.



## description sub package

The description sub package has 3 modules: compare.py, shape.py and size.py.

__________________________

In the compare.py, we have 3 functions to compare the graphic. 

The is_same_shape function has two parameters that in type Round or Rectangle,  and if the two parameters are in the same shape type, it return true, otherwise return false.

The is_same function has two parameters that  in type Round or Rectangle, and if the two parameters are in the same shape type and also has the same size, it return true, otherwise return false.

The big_area function has two parameters that in type Round or Rectangle,  and it will return the graphic that has a larger area. If the area are same, it will print the info and return None.

__________________________

In the shape.py, we have 3 functions to change the shape between rectangle and round.

The round_to_square function have a round object as parameter and return a square in rectangle object with the same area.

The square_to_round function have a rectangle object as parameter and return a round with the same area.

The round_to_rect function have a round object and the long_side requirement as parameter and return a rectangle with the same area.

__________________________

In the size.py, we have 3 functions to change the size of the graphic.

The change_side_for_rec function has a rectangle object, side_type(long or short) that need to change and the change value (negative number to subtract, positive number to add) as the parameter. It will return the new rectangle object or print error message if the new value is negative or zero.

The change_redius_for_round function has a round object and the change value for radius (negative number to subtract, positive number to add) as the parameter. It will return the new round object or print error message if the new value is negative or zero.

The change_area function has a round or rectangle object and the change value for the area (negative number to subtract, positive number to add) as the parameter. It will return the new round or rectangle object or print error message if the new value is negative or zero. For the rectangle object, the long length is fixed and all the change will on the short length).

