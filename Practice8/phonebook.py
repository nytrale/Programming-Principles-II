from connect import get_connection


def call_function_search(pattern):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    if rows:
        print("\nSearch results:")
        for row in rows:
            print(row)
    else:
        print("\nNo matching records found.")

    cur.close()
    conn.close()


def call_function_paginate(limit, offset):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM paginate(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    if rows:
        print("\nPagination results:")
        for row in rows:
            print(row)
    else:
        print("\nNo records found.")

    cur.close()
    conn.close()


def call_procedure_insert_or_update(name, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()

    print("\nUser inserted or updated successfully.")

    cur.close()
    conn.close()


def call_procedure_insert_many(names, phones):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    conn.commit()

    print("\nBulk insert finished.")

    cur.close()
    conn.close()


def call_procedure_delete(name=None, phone=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_user(%s, %s)", (name, phone))
    conn.commit()

    print("\nDelete procedure finished.")

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PRACTICE 8 PHONEBOOK MENU ---")
        print("1 - Search by pattern")
        print("2 - Pagination")
        print("3 - Insert or update one user")
        print("4 - Insert many users")
        print("5 - Delete by name or phone")
        print("0 - Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            pattern = input("Enter pattern (part of name or phone): ")
            call_function_search(pattern)

        elif choice == "2":
            try:
                limit = int(input("Enter LIMIT: "))
                offset = int(input("Enter OFFSET: "))
                call_function_paginate(limit, offset)
            except ValueError:
                print("Limit and offset must be integers.")

        elif choice == "3":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            call_procedure_insert_or_update(name, phone)

        elif choice == "4":
            names_input = input("Enter names separated by commas: ")
            phones_input = input("Enter phones separated by commas: ")

            names = [name.strip() for name in names_input.split(",")]
            phones = [phone.strip() for phone in phones_input.split(",")]

            if len(names) != len(phones):
                print("The number of names and phones must be the same.")
            else:
                call_procedure_insert_many(names, phones)

        elif choice == "5":
            print("1 - Delete by name")
            print("2 - Delete by phone")
            delete_choice = input("Choose delete option: ")

            if delete_choice == "1":
                name = input("Enter name to delete: ")
                call_procedure_delete(name=name)

            elif delete_choice == "2":
                phone = input("Enter phone to delete: ")
                call_procedure_delete(phone=phone)

            else:
                print("Invalid delete option.")

        elif choice == "0":
            print("Program finished.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()