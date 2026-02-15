# *args allows to enter any number of positional arguments

def students(*args):
    print("Type:", type(args))
    print("1.", args[0])
    print("2.", args[1])
    print("3.", args[2])
    print("total:", args)


students("Shugyla", "Bake", "Daulet")


def findsum(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(findsum(10, 12, 33, 22, 85))
print(findsum(3, -5, 39, 40))
print(findsum(123, 83, -46))


# *kwargs allows to enter any number of keyword arguments

def student_info(**var):
  print("Type:", type(var))
  print("Name:", var["name"])
  print("Year:", var["year"])
  print("Full information:", var)

student_info(name = "Yeraly", year = 3, major = "Petroleum Engineering")




# Combining *args and **kwargs


def somefunc(title, *args, **kwargs):
    print("title: " + title)
    print("positional args", args)
    print("keyword args", kwargs)

somefunc("Club members", "Artyom", "Karlygash", hobby = "Football", interest = "Pets")