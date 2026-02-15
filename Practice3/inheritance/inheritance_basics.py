
class Human:                                         # Parent class
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
    
    def printname(self):
        print(self.fname, self.lname)

    def greeting(self):
        print(f"Hello, {self.fname}.")


class Coach(Human):                           # Child class 
    pass

x = Coach("Pep", "Guardiola")
x.printname()                          # Child class inherited the methods from parent class
x.greeting()