class Student:
    def __init__(self, fname, lname, major, year):
        self.fname = fname
        self.lname = lname
        self.major = major
        self.year = year

    def printinfo(self):
        print(self.fname, self.lname)
        print("Major:", self.major)
        print("Year:", self.year)

    
class FirstYear(Student):
    def __init__(self, fname, lname, major, year):
        super().__init__(fname, lname, major, year)

    def printinfo(self):
        print(self.fname, self.lname)
        print("Your major isssss", self.major)
        print("And you are first year")

# FirstYear inherited all methods and properties from Student
# But the method printinfo() in FirstYear overrides method printinfo() in Student

x = Student("LeBron", "James", "Robotics", 2)

y = FirstYear("Pedro", "Gonzalez", "Pedagogics", 3)

x.printinfo()

print("\n")

y.printinfo()