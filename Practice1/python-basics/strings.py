# Single (' ') and double (" ") quotes work the same

print("Hello")
print('Hello')


# Quotes inside strings

print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')


# Multiline string using triple quotes

a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)


# Strings are arrays (indexing starts from 0)

a = "Hello, World!"
print(a[1])   # prints 'e'


# Length of a string

print(len(a))


# Loop through characters

for x in "banana":
    print(x)


# Check if substring exists

txt = "The best things in life are free!"
print("free" in txt)


# Using if with 'in'

if "free" in txt:
    print("Yes, 'free' is present.")


# Using 'not in'

if "expensive" not in txt:
    print("No, 'expensive' is NOT present.")


# String slicing

b = "Hello, World!"
print(b[2:5])   # index 2 to 4


# Slice from start

print(b[:5])


# Slice to the end

print(b[2:])


# Negative indexing

print(b[-5:-2])


# Uppercase and lowercase

a = "Hello, World!"
print(a.upper())
print(a.lower())


# Remove spaces

a = " Hello, World! "
print(a.strip())


# Replace characters

a = "Hello, World!"
print(a.replace("H", "J"))


# Split string

a = "Hello, World!"
print(a.split(","))


# Concatenation

a = "Hello"
b = "World"
print(a + b)
print(a + " " + b)


# f-strings

age = 36
txt = f"My name is John, I am {age}"
print(txt)

price = 59
txt = f"The price is {price} dollars"
print(txt)

txt = f"The price is {price:.2f} dollars"
print(txt)

txt = f"The price is {20 * 59} dollars"
print(txt)


# Escape characters

txt = "We are the so-called \"Vikings\" from the north."
print(txt)
