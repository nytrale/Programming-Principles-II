class Account:
    def __init__(self, money = 0, age = 16):
        self.money = money
        self.age = age

    def amount(self):
        print(f"You have ${self.money} on your account")

    def birthday(self):
        self.age += 1

        if self.age % 10 == 1:
            print(f"Happy {self.age}st birthday!")
        elif self.age % 10 == 2:
            print(f"Happy {self.age}nd birthday!")
        elif self.age % 10 == 3:
            print(f"Happy {self.age}rd birthday!")
        else:
            print(f"Happy {self.age}th birthday!")

test = Account(300, 18)

test.amount()

celebrate_bday = Account(100, 23)

celebrate_bday.birthday()

class Calculator:
    def substract(self, a, b):
        return a - b
    
    def divide(self, a, b):
        return a / b


calc = Calculator()

print(calc.substract(1934, 1238))

print(calc.divide(19824, 33))


class Subject:
    def __init__(self, name, ects):
        self.name = name
        self.ects = ects

    def __str__(self):
        return f"{self.name} does hold {self.ects} ECTS."         
        
# str makes this output and without __str__ output would be 
# <__main__.Subject object at 0x000001BB050C6CF0>


subj = Subject("Calculus", 5)

print(subj)