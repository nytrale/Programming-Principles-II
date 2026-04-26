# phonebook.py — PhoneBook TSIS 1 (Practice 7 + 8 + extended)

import csv
import json
import psycopg2
from connect import get_connection, create_table


# ─────────────────────────────────────────────
# CREATE — добавление контактов
# ─────────────────────────────────────────────

def insert_contact(name: str, phone: str, email: str = None, birthday: str = None, group_name: str = None):
    """Добавляет один контакт в БД."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Находим group_id если указана группа
        group_id = None
        if group_name:
            cur.execute("SELECT id FROM groups WHERE name ILIKE %s;", (group_name,))
            row = cur.fetchone()
            if row:
                group_id = row[0]

        cur.execute(
            "INSERT INTO contacts (name, phone, email, birthday, group_id) VALUES (%s, %s, %s, %s, %s);",
            (name, phone, email, birthday, group_id)
        )
        conn.commit()
        print(f"Добавлен контакт: {name} — {phone}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при добавлении: {e}")
    finally:
        cur.close()
        conn.close()


def import_from_csv(filepath: str):
    """Импортирует контакты из CSV-файла (поддерживает новые поля)."""
    conn = get_connection()
    cur = conn.cursor()
    added = 0
    try:
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name     = row.get("name", "").strip()
                phone    = row.get("phone", "").strip()
                email    = row.get("email", "").strip() or None
                birthday = row.get("birthday", "").strip() or None
                group_name = row.get("group", "").strip() or None
                phone_type = row.get("phone_type", "mobile").strip() or "mobile"

                # Находим group_id
                group_id = None
                if group_name:
                    cur.execute("SELECT id FROM groups WHERE name ILIKE %s;", (group_name,))
                    g = cur.fetchone()
                    if g:
                        group_id = g[0]

                # Вставляем контакт
                cur.execute(
                    "INSERT INTO contacts (name, phone, email, birthday, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                    (name, phone, email, birthday, group_id)
                )
                contact_id = cur.fetchone()[0]

                # Добавляем телефон в таблицу phones
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                    (contact_id, phone, phone_type)
                )
                added += 1

        conn.commit()
        print(f"Импортировано {added} контактов из {filepath}")
    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка БД при импорте: {e}")
    finally:
        cur.close()
        conn.close()


# ─────────────────────────────────────────────
# READ — чтение / поиск / фильтрация
# ─────────────────────────────────────────────

def get_all_contacts(sort_by: str = "name"):
    """Возвращает все контакты с сортировкой."""
    allowed = {"name": "c.name", "birthday": "c.birthday", "date": "c.created_at"}
    order = allowed.get(sort_by, "c.name")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name as group_name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY {order};
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def filter_by_group(group_name: str):
    """Фильтрует контакты по группе."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        WHERE g.name ILIKE %s
        ORDER BY c.name;
    """, (group_name,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def search_by_email(query: str):
    """Поиск контактов по части email."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        WHERE c.email ILIKE %s
        ORDER BY c.name;
    """, (f"%{query}%",))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def search_by_pattern(query: str):
    """Расширенный поиск через функцию БД (имя, email, все телефоны)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s);", (query,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_paginated(page: int, page_size: int = 3):
    """Возвращает контакты постранично."""
    conn = get_connection()
    cur = conn.cursor()
    offset = (page - 1) * page_size
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (page_size, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ─────────────────────────────────────────────
# UPDATE — обновление контакта
# ─────────────────────────────────────────────

def update_contact(contact_id: int, new_name: str = None, new_phone: str = None):
    """Обновляет имя или телефон контакта по его id."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        if new_name:
            cur.execute("UPDATE contacts SET name = %s WHERE id = %s;", (new_name, contact_id))
        if new_phone:
            cur.execute("UPDATE contacts SET phone = %s WHERE id = %s;", (new_phone, contact_id))
        conn.commit()
        print(f"Контакт #{contact_id} обновлён.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при обновлении: {e}")
    finally:
        cur.close()
        conn.close()


def upsert_contact(name: str, phone: str):
    """Добавляет или обновляет контакт через процедуру БД."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
        conn.commit()
        print(f"Upsert выполнен для: {name}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при upsert: {e}")
    finally:
        cur.close()
        conn.close()


def bulk_insert(names: list, phones: list):
    """Массовая вставка с валидацией через процедуру БД."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL bulk_insert_contacts(%s, %s);", (names, phones))
        cur.execute("SELECT name, phone, reason FROM invalid_contacts;")
        invalid = cur.fetchall()
        conn.commit()
        if invalid:
            print("\nНекорректные данные:")
            for row in invalid:
                print(f"  {row[0]} | {row[1]} | {row[2]}")
        else:
            print("Все контакты успешно добавлены!")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при массовой вставке: {e}")
    finally:
        cur.close()
        conn.close()


def add_phone_to_contact(contact_name: str, phone: str, phone_type: str):
    """Добавляет новый телефон к контакту через процедуру БД."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s);", (contact_name, phone, phone_type))
        conn.commit()
        print(f"Телефон добавлен контакту {contact_name}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()


def move_contact_to_group(contact_name: str, group_name: str):
    """Перемещает контакт в группу через процедуру БД."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s);", (contact_name, group_name))
        conn.commit()
        print(f"{contact_name} перемещён в группу {group_name}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()


# ─────────────────────────────────────────────
# DELETE — удаление контакта
# ─────────────────────────────────────────────

def delete_contact(name: str = None, phone: str = None):
    """Удаляет контакт по имени или телефону через процедуру БД."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_contact(%s, %s);", (name or '', phone or ''))
        conn.commit()
        print("Контакт удалён.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при удалении: {e}")
    finally:
        cur.close()
        conn.close()


# ─────────────────────────────────────────────
# EXPORT / IMPORT JSON
# ─────────────────────────────────────────────

def export_to_json(filepath: str = "contacts.json"):
    """Экспортирует все контакты в JSON файл."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.id, c.name, c.phone, c.email,
                   c.birthday::TEXT, g.name as group_name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY c.name;
        """)
        contacts = cur.fetchall()

        result = []
        for row in contacts:
            contact_id, name, phone, email, birthday, group_name = row

            # Получаем все телефоны контакта
            cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s;", (contact_id,))
            phones = [{"phone": p[0], "type": p[1]} for p in cur.fetchall()]

            result.append({
                "name": name,
                "phone": phone,
                "email": email,
                "birthday": birthday,
                "group": group_name,
                "phones": phones
            })

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Экспортировано {len(result)} контактов в {filepath}")
    except psycopg2.Error as e:
        print(f"Ошибка при экспорте: {e}")
    finally:
        cur.close()
        conn.close()


def import_from_json(filepath: str = "contacts.json"):
    """Импортирует контакты из JSON файла с обработкой дубликатов."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(filepath, encoding="utf-8") as f:
            contacts = json.load(f)

        for contact in contacts:
            name     = contact.get("name")
            phone    = contact.get("phone")
            email    = contact.get("email")
            birthday = contact.get("birthday")
            group_name = contact.get("group")
            phones   = contact.get("phones", [])

            # Проверяем дубликат
            cur.execute("SELECT id FROM contacts WHERE name ILIKE %s;", (name,))
            existing = cur.fetchone()

            if existing:
                choice = input(f'Контакт "{name}" уже существует. Перезаписать? (y/n): ').strip().lower()
                if choice == "y":
                    cur.execute("DELETE FROM contacts WHERE id = %s;", (existing[0],))
                    conn.commit()
                else:
                    print(f'Пропущен: {name}')
                    continue

            # Находим group_id
            group_id = None
            if group_name:
                cur.execute("SELECT id FROM groups WHERE name ILIKE %s;", (group_name,))
                g = cur.fetchone()
                if g:
                    group_id = g[0]

            # Вставляем контакт
            cur.execute(
                "INSERT INTO contacts (name, phone, email, birthday, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                (name, phone, email, birthday, group_id)
            )
            contact_id = cur.fetchone()[0]

            # Вставляем телефоны
            for p in phones:
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                    (contact_id, p.get("phone"), p.get("type"))
                )

            conn.commit()
            print(f"Импортирован: {name}")

    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка БД: {e}")
    finally:
        cur.close()
        conn.close()


# ─────────────────────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────

def print_contacts(rows):
    """Красиво выводит список контактов."""
    if not rows:
        print("Контакты не найдены.")
        return
    print(f"\n{'ID':<5} {'Имя':<20} {'Телефон':<18} {'Email':<25} {'День рождения':<15} {'Группа':<10}")
    print("-" * 93)
    for row in rows:
        print(f"{str(row[0]):<5} {str(row[1]):<20} {str(row[2]):<18} {str(row[3] or ''):<25} {str(row[4] or ''):<15} {str(row[5] or ''):<10}")
    print()


def print_search_results(rows):
    """Выводит результаты расширенного поиска."""
    if not rows:
        print("Контакты не найдены.")
        return
    print(f"\n{'ID':<5} {'Имя':<20} {'Email':<25} {'День рождения':<15} {'Группа':<10} {'Телефон':<18} {'Тип':<10}")
    print("-" * 103)
    for row in rows:
        print(f"{str(row[0]):<5} {str(row[1]):<20} {str(row[2] or ''):<25} {str(row[3] or ''):<15} {str(row[4] or ''):<10} {str(row[5] or ''):<18} {str(row[6] or ''):<10}")
    print()


def paginated_navigation():
    """Консольная навигация по страницам."""
    page = 1
    page_size = 3
    while True:
        rows = get_paginated(page, page_size)
        print(f"\n--- Страница {page} ---")
        if not rows:
            print("Больше контактов нет.")
            page = max(1, page - 1)
        else:
            for row in rows:
                print(f"  {row[0]}. {row[1]} — {row[2]}")

        cmd = input("\nnext / prev / quit: ").strip().lower()
        if cmd == "next":
            page += 1
        elif cmd == "prev":
            page = max(1, page - 1)
        elif cmd == "quit":
            break
        else:
            print("Неверная команда.")


# ─────────────────────────────────────────────
# КОНСОЛЬНОЕ МЕНЮ
# ─────────────────────────────────────────────

def menu():
    create_table()

    while True:
        print("=" * 45)
        print("         ТЕЛЕФОННАЯ КНИГА — TSIS 1")
        print("=" * 45)
        print("1.  Показать все контакты")
        print("2.  Добавить контакт")
        print("3.  Расширенный поиск (имя/email/телефон)")
        print("4.  Фильтр по группе")
        print("5.  Поиск по email")
        print("6.  Обновить контакт (по ID)")
        print("7.  Удалить по имени")
        print("8.  Удалить по телефону")
        print("9.  Импорт из CSV")
        print("10. Upsert контакт")
        print("11. Массовая вставка")
        print("12. Листать постранично")
        print("13. Добавить телефон контакту")
        print("14. Переместить в группу")
        print("15. Экспорт в JSON")
        print("16. Импорт из JSON")
        print("0.  Выход")
        print("-" * 45)

        choice = input("Выбери действие: ").strip()

        if choice == "1":
            print("Сортировка: name / birthday / date (Enter = name)")
            sort = input("Сортировать по: ").strip() or "name"
            rows = get_all_contacts(sort)
            print_contacts(rows)

        elif choice == "2":
            name     = input("Имя: ").strip()
            phone    = input("Телефон: ").strip()
            email    = input("Email (Enter пропустить): ").strip() or None
            birthday = input("День рождения (YYYY-MM-DD, Enter пропустить): ").strip() or None
            print("Группы: Family / Work / Friend / Other")
            group    = input("Группа (Enter пропустить): ").strip() or None
            insert_contact(name, phone, email, birthday, group)

        elif choice == "3":
            query = input("Поисковый запрос: ").strip()
            rows = search_by_pattern(query)
            print_search_results(rows)

        elif choice == "4":
            print("Группы: Family / Work / Friend / Other")
            group = input("Введи название группы: ").strip()
            rows = filter_by_group(group)
            print_contacts(rows)

        elif choice == "5":
            query = input("Введи часть email: ").strip()
            rows = search_by_email(query)
            print_contacts(rows)

        elif choice == "6":
            try:
                contact_id = int(input("ID контакта: ").strip())
            except ValueError:
                print("Неверный ID.")
                continue
            print("Оставь пустым чтобы не менять")
            new_name  = input("Новое имя: ").strip() or None
            new_phone = input("Новый телефон: ").strip() or None
            update_contact(contact_id, new_name, new_phone)

        elif choice == "7":
            name = input("Имя для удаления: ").strip()
            delete_contact(name=name)

        elif choice == "8":
            phone = input("Телефон для удаления: ").strip()
            delete_contact(phone=phone)

        elif choice == "9":
            filepath = input("Путь к CSV (Enter = contacts.csv): ").strip() or "contacts.csv"
            import_from_csv(filepath)

        elif choice == "10":
            name  = input("Имя: ").strip()
            phone = input("Телефон: ").strip()
            upsert_contact(name, phone)

        elif choice == "11":
            print("Вводи контакты: Имя:Телефон (пустая строка — конец)")
            names, phones = [], []
            while True:
                line = input("  > ").strip()
                if not line:
                    break
                parts = line.split(":")
                if len(parts) == 2:
                    names.append(parts[0].strip())
                    phones.append(parts[1].strip())
                else:
                    print("  Формат: Имя:Телефон")
            if names:
                bulk_insert(names, phones)

        elif choice == "12":
            paginated_navigation()

        elif choice == "13":
            name  = input("Имя контакта: ").strip()
            phone = input("Новый телефон: ").strip()
            print("Тип: home / work / mobile")
            ptype = input("Тип телефона: ").strip()
            add_phone_to_contact(name, phone, ptype)

        elif choice == "14":
            name  = input("Имя контакта: ").strip()
            print("Группы: Family / Work / Friend / Other")
            group = input("Название группы: ").strip()
            move_contact_to_group(name, group)

        elif choice == "15":
            filepath = input("Имя файла (Enter = contacts.json): ").strip() or "contacts.json"
            export_to_json(filepath)

        elif choice == "16":
            filepath = input("Имя файла (Enter = contacts.json): ").strip() or "contacts.json"
            import_from_json(filepath)

        elif choice == "0":
            print("Выход.")
            break

        else:
            print("Неверный выбор, попробуй снова.")


if __name__ == "__main__":
    menu()