
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    if x == "banana":
        continue  # "banana" не печатаем
    print(x)

# range + continue
for i in range(9):
    if i == 3:
        continue
    print(i)
