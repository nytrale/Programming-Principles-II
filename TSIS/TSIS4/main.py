# main.py — точка входа

from db import db_connect, db_init
from game import SnakeGame


def main():
    conn = db_connect()
    db_init(conn)
    SnakeGame(conn).run()


if __name__ == "__main__":
    main()