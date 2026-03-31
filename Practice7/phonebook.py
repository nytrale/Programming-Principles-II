from connect import get_connection
import csv
import os


#table
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully.")


# insert CSV
def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()

    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "contacts.csv")

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row["name"], row["phone"])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Contacts imported from CSV.")


#from user
def insert_user():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added.")


# all contacts
def show_all():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


# query 
def query_contacts():
    print("1 - Search by name")
    print("2 - Search by phone prefix")
    choice = input("Choose filter: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE name ILIKE %s",
            (f"%{name}%",)
        )

    elif choice == "2":
        prefix = input("Enter phone prefix: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (f"{prefix}%",)
        )

    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


# update phone
def update_phone():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s",
        (new_phone, name)
    )

    conn.commit()
    print("Contact updated.")

    cur.close()
    conn.close()


# delete
def delete_contact():
    print("1 - Delete by name")
    print("2 - Delete by phone")
    choice = input("Choose delete option: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name to delete: ")
        cur.execute(
            "DELETE FROM phonebook WHERE name = %s",
            (name,)
        )

    elif choice == "2":
        phone = input("Enter phone to delete: ")
        cur.execute(
            "DELETE FROM phonebook WHERE phone = %s",
            (phone,)
        )

    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return

    conn.commit()
    print("Contact deleted.")

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1 - Create table")
        print("2 - Insert contacts from CSV")
        print("3 - Insert new contact")
        print("4 - Show all contacts")
        print("5 - Query contacts")
        print("6 - Update phone")
        print("7 - Delete contact")
        print("0 - Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            insert_user()
        elif choice == "4":
            show_all()
        elif choice == "5":
            query_contacts()
        elif choice == "6":
            update_phone()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            print("Program finished.")
            break
        else:
            print("Invalid choice. Try again.")


menu()