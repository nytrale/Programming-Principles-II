class Parent:
    def __init__(self, txt):
        self.message = txt

    def printmsg(self):
        print(self.message)

    def length_of_message(self):
        print(len(self.message))
        

class Child(Parent):
    def __init__(self, txt):
        super().__init__(txt)                          # Child class inherits all methods and properties from parent class by using super()
        self.response = "Bye!"

    def farewell(self):
        print("We had a great time together,", self.response)

x = Child("Welcome and goodbye")

x.printmsg()
x.length_of_message()

print(x.response)

x.farewell()