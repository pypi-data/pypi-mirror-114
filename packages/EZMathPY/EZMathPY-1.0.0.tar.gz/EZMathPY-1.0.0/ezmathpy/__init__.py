import statistics
import math

#region STATISTICS
def get_average(numbers):
    split = numbers.split(",")
    length = len(split)
    x = 0
    for i in split:
        e = int(i)
        x = x + e
    return x / length

def get_median(numbers):
    split = numbers.split(",")
    x = []
    for i in split:
        x.append(int(i))
    return statistics.median(x)
#endregion
#region SUM
def sum(numbers):
    split = numbers.split(",")
    x = 0
    for i in split:
        x = x + int(i)
    return(x)
#endregion
#region AREAS

def area_square(length_of_side):
    return int(length_of_side)**2

def area_rectangle(width, height):
    return int(width) * int(height)

def area_triangle(base, height):
    return int(base) * int(height) / 2

def area_rhombus(large_diagonal, diagonal):
    return int(large_diagonal) * int(diagonal) / 2

def area_trapezoid(large_side, small_side, height):
    return (int(large_side) + int(small_side) / 2) * int(height)

def area_circle(radius):
    return (pi() * int(radius)) ** 2

def area_cone(radius, slant_height):
    return (pi() * int(radius)) * int(slant_height)

def area_sphere(radius):
    return ((4 * pi()) * int(radius)) ** 2

#endregion
#region VOLUMES

def volume_cube(side):
    return (int(side) ** 3) # volume = side ^ 3

def volume_parallelepiped(length, width, height):
    return (int(length) * int(width) * int(height))

def volume_prism(base, height):
    return (int(base) * int(height))

def volume_cylinder(radius, height):
    return ((pi() * int(radius)) ** 2) * int(height)

def volume_cone(base, height):
    return ((1/3) * int(base)) * int(height)

def volume_pyramid(base, height):
    return ((1/3) * int(base)) * int(height)

def volume_sphere(radius):
    return (((4/3)*pi()) * int(radius)) ** 3

#endregion
#region PERIMETER

def perimeter_square(length_of_side):
    return 4 * area_square(int(length_of_side))

def perimeter_rectangle(length, width):
    return 2 * (length + width)

#endregion

def pi():
    return math.pi