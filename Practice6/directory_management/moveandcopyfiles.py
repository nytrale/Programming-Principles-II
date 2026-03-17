import os
import shutil

# создаем папки
os.makedirs("source", exist_ok=True)
os.makedirs("destination", exist_ok=True)

# создаем файл в source
f = open("source/test.txt", "w")
f.write("Hello from source folder")
f.close()

# копируем файл
shutil.copy("source/test.txt", "destination/test_copy.txt")
print("File copied")

# перемещаем файл
shutil.move("source/test.txt", "destination/test.txt")
print("File moved")

# смотрим содержимое папок
print("\nSource folder:")
print(os.listdir("source"))

print("\nDestination folder:")
print(os.listdir("destination"))