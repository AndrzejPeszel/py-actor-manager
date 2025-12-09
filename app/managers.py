import sqlite3
from typing import Optional, List, Tuple

try:
    from .models import Actor
except ImportError:
    from models import Actor


class ActorManager:
    def __init__(self, db_name: str = "cinema.db",
                 table_name: str = "actors"):
        self.db_name = db_name
        self.table_name = table_name
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            cursor.execute(f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    age INTEGER
                )
            """)
            conn.commit()

    # Dodano -> int (ANN201)
    def create(self, first_name: str, last_name: str, age: int = None) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {self.table_name} "
                f"(first_name, last_name, age) VALUES (?, ?, ?)",
                (first_name, last_name, age)
            )
            conn.commit()
            return cursor.lastrowid

    def _map_row_to_actor(self, row: Tuple) -> Actor:
        return Actor(
            id=row[0],
            first_name=row[1],
            last_name=row[2],
            age=row[3]
        )

    def all(self) -> List[Actor]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            return [self._map_row_to_actor(row) for row in rows]

    # Dodano -> None (ANN201)
    def update(self, pk: int, new_first_name: str, new_last_name: str,
               new_age: int = None) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE {self.table_name} SET "
                f"first_name=?, last_name=?, age=? WHERE id=?",
                (new_first_name, new_last_name, new_age, pk)
            )
            conn.commit()

    # Dodano -> None (ANN201)
    def delete(self, pk: int) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id=?", (pk,))
            conn.commit()
