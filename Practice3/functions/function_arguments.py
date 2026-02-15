
# Function arguments and parameters

print("If your name starts with an A, then you are in team #1 else team #2")
name = str(input(("Enter your name: ")))

def teams(st):                        # st is parameter
    if name[0].lower() == "a":
        print("TEAM #1")
    else:
        print("TEAM #2")

teams(name)         # name is argument

print("\n")

def fullName(fname, lname):                        # two parameters
    print("Greetings,", fname, lname + ".")

fullName("Napoleone", "Bonaparte")




def greetingSynonyms(default = "Hello"):                 # default value of parameter
    print(default, "is a way to greet someone.")

greet = str(input("What word can describe a greeting?: "))

greetingSynonyms(greet)
greetingSynonyms()                # outputs default value

def func(persons):
  print("Name:", person["name"])
  print("Age:", person["age"])

person = {"name": "Alisher", "age": 18}

func(person)