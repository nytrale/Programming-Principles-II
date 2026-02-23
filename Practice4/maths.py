#1
import math

degree = float(input("Input degree: "))
radian = degree * math.pi / 180

print("Output radian:", round(radian, 6))



#2
h = float(input("Height: "))
b1 = float(input("Base, first value: "))
b2 = float(input("Base, second value: "))

area = (b1 + b2) / 2 * h
print("Expected Output:", area)




#3
import math

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

area = (n * s**2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", area)



#4
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height
print("Expected Output:", area)

