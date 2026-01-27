# Valid variable names

myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"


# Naming styles

myVariableName = "John"   # camelCase
MyVariableName = "John"   # PascalCase
my_variable_name = "John" # snake_case


# Assign one value to multiple variables

x = y = z = "Orange"
print(x)
print(y)
print(z)


# Assign different values at once

x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)


# Unpacking a list into variables

fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)


# Printing multiple variables

x = "Python"
y = "is"
z = "awesome"
print(x, y, z)   # separated by spaces


# String concatenation

x = "Python "
y = "is "
z = "awesome"
print(x + y + z)


# Adding numbers

x = 5
y = 10
print(x + y)


# Mixing types in print

x = 5
y = "John"
print(x, y)


# Global variable example

x = "awesome"

def myfunc():
    print("Python is " + x)

myfunc()


# Local vs global variable

x = "awesome"

def myfunc():
    x = "fantastic"   # local variable
    print("Python is " + x)

myfunc()
print("Python is " + x)


# Modifying a global variable inside a function

x = "awesome"

def myfunc():
    global x          # allows modifying global variable
    x = "fantastic"

myfunc()
print("Python is " + x)
