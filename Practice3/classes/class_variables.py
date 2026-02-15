class LivingBeing:
    species = ["Human", "Animal", "Fish", "Insect", "Bird"]      # Class variable (class property)

    def __init__(self, name):
        self.name = name                         # Instance variable  (instance property)


n = LivingBeing("Bobik")

n.poroda = "Dobberman"               # adds new property only for this object

print(n.name)
print(n.species[1])

print(n.poroda)



class Person:
    lastname = ""

    def __init__(self, name):
        self.name = name


p1 = Person("Alisher")
p2 = Person("Ilyas")

Person.lastname = "Serik"       # affects all objects of the class

print(p1.lastname)
print(p2.lastname)