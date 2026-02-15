numbers = [3, 4, 6, 7, 2, 10]

squares  = list(map(lambda i : i ** 2, numbers))

print(squares)


sounds = ["bark", "meow", "chvik"]

n = int(input("How many pollution noises do you want to hear?: "))
noise_pollution = list(map(lambda j : j * n, sounds))

for i in noise_pollution:
    print(i, end=" ")