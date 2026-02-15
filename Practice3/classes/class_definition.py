class SomeClass:
    x = 17
    y = 23

obj = SomeClass()

print(obj.x)

del obj

obj2 = SomeClass()

print(obj2.y)


class ImportantThing:
    pass