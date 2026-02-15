x = lambda a, b : a * b
print(x(18, 7))

y = lambda d, e, f : d + e + f
print(y(5, 10, 13))



def somefunc(n):
    return lambda a : a * n


doubler = somefunc(2)
tripler = somefunc(3)

print(doubler(13))
print(tripler(382))