# Multiple inheritance  (child class inherits more than one parent class)

class Person:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print(f"My name is {self.name}")


class Student:
    def __init__(self, university):
        self.university = university

    def study(self):
        print(f"I study at {self.university}")


class WorkingStudent(Person, Student):
    def __init__(self, name, university, job):
        Person.__init__(self, name)
        Student.__init__(self, university)
        self.job = job

    def work(self):
        print(f"I work as a {self.job}")


ws = WorkingStudent("Ratmir", "KBTU", "Software Developer")

ws.introduce()   # from Person
ws.study()       # from Student
ws.work()        # from WorkingStudent