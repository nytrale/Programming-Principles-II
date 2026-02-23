# 1) Create a generator that generates the squares of numbers up to some number N.
def squares_up_to(N):
    # yield squares from 0^2 to N^2
    for x in range(0, N + 1):
        yield x * x

# Example:
# for v in squares_up_to(5):
#     print(v)


# 2) Print even numbers between 0 and n in comma separated form (using generator)
def evens_up_to(n):
    # yield even numbers from 0 to n
    for x in range(0, n + 1):
        if x % 2 == 0:
            yield x

n = int(input("n: "))
# turn generator into strings and join with commas
print(",".join(str(x) for x in evens_up_to(n)))


# 3) Generator: numbers divisible by 3 and 4 between 0 and n
def divisible_by_3_and_4(n):
    # divisible by 3 and 4 means divisible by 12
    for x in range(0, n + 1):
        if x % 3 == 0 and x % 4 == 0:
            yield x

# Example:
# for v in divisible_by_3_and_4(100):
#     print(v)


# 4) Generator called squares to yield squares of all numbers from a to b
def squares(a, b):
    # yield squares from a^2 to b^2
    for x in range(a, b + 1):
        yield x * x

# Test with a for loop:
# for v in squares(3, 7):
#     print(v)


# 5) Generator that returns all numbers from n down to 0
def countdown(n):
    # yield n, n-1, ..., 0
    for x in range(n, -1, -1):
        yield x

# Example:
# for v in countdown(5):
#     print(v)