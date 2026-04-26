# connect.py — подключение к PostgreSQL и создание таблицы
 
import psycopg2
from config import DB_CONFIG
 
 
def get_connection():
    """Возвращает соединение с базой данных."""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn
 
 
def create_table():
    """Создаёт таблицу contacts, если она ещё не существует."""
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id      SERIAL PRIMARY KEY,
            name    VARCHAR(100) NOT NULL,
            phone   VARCHAR(20)  NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
 
    conn.commit()
    cur.close()
    conn.close()
    print("Таблица contacts готова.")
 
 
if __name__ == "__main__":
    create_table()