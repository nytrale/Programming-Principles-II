import os

filename = "sample.txt"

if os.path.exists(filename):
    os.remove(filename)
    print("sample.txt deleted safely.")
else:
    print("File does not exist.")