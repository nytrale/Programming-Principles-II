class Student:
    def __init__(self, name, surname, major = "Automation and Control"):               # default value for major
        self.name = name
        self.surname = surname
        self.major = major

p1 = Student("Lorem", "Ipsum", "Management")
p2 = Student("Donald", "Trump")

print(p1.name, p1.major)

print(p2.name + " - " + p2.major)