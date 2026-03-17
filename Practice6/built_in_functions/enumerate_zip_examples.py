names = ["Ali", "Mira", "Dana"]
scores = [90, 85, 95]

# enumerate() индекс + значение
print("enumerate():")
for i, name in enumerate(names):
    print(i, name)

# zip() соединяет два списка
print("\nzip():")
for name, score in zip(names, scores):
    print(name, score)

# sorted() сортировка
numbers = [5, 2, 8, 1]
print("\nsorted():", sorted(numbers))

# type()тип переменной
x = 10
print("type():", type(x))