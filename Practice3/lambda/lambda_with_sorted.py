

names = ["Aliaskar", "Dinmuhammed", "Alexey", "Vladislav", "Aiaru", "Zhansezim"]

for i in names:
    print(i, end=" ")

print("\n")

print("Let's list this by the length of the names:")
sorted_names = sorted(names, key = lambda x : len(x))
print(sorted_names)