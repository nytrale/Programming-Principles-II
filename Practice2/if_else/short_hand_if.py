# Короткие формы if и if...else

# 1) Однострочный if (когда одна команда)
a = 5
b = 2
if a > b: print("a is greater than b")

# 2) Однострочный if...else (тернарный оператор)
a = 2
b = 330
print("A") if a > b else print("B")

# 3) Несколько условий в одну строку (можно, но читаемость хуже)
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")
