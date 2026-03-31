from connect import get_connection

def call_function_search(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def call_function_paginate(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM paginate(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def call_procedure_insert_or_update(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def call_procedure_insert_many(names, phones):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    conn.commit()
    cur.close()
    conn.close()

def call_procedure_delete(name=None, phone=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()



if __name__ == "__main__":

    # insert/update
    call_procedure_insert_or_update("Nurbolat", "123456789")

    # Multiple insert
    call_procedure_insert_many(
        ["Bob", "Charlie"], 
        ["987654321", "invalid_phone"]
    )

    # Search pattern
    call_function_search("bo")

    # Pagination
    call_function_paginate(2, 0)

    # Delete
    call_procedure_delete(name="Nurbolat")