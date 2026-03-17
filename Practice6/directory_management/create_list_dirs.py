import os

# создать одну папку
if not os.path.exists("my_folder"):
    os.mkdir("my_folder")
    print("my_folder created")

# создать вложенные папки
os.makedirs("parent/child/grandchild", exist_ok=True)
print("Nested folders created")

# показать текущую папку
print("Current directory:", os.getcwd())

# показать список файлов и папок
print("\nList of files and folders:")
print(os.listdir())

# найти .txt файлы
print("\nTXT files:")
for item in os.listdir():
    if item.endswith(".txt"):
        print(item)

# удалить пустую папку
if os.path.exists("empty_folder"):
    os.rmdir("empty_folder")
else:
    os.mkdir("empty_folder")
    os.rmdir("empty_folder")
    print("empty_folder created and removed")