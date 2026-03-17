# map_filter_reduce.py

from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map() - применяет функцию к каждому элементу
squares = list(map(lambda x: x * x, numbers))
print("map():", squares)

# filter() - оставляет элементы по условию
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("filter():", evens)

# reduce() - делает одно значение из списка
total = reduce(lambda x, y: x + y, numbers)
print("reduce():", total)

# другие built-in функции
print("len():", len(numbers))
print("sum():", sum(numbers))
print("min():", min(numbers))
print("max():", max(numbers))

# преобразование типов
a = "123"
print("int():", int(a))
print("float():", float(a))
print("str():", str(456))