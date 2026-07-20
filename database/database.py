import sqlite3
from pathlib import Path

from database.schema import (
    USERS_TABLE,
    EVENTS_TABLE,
    ALERTS_TABLE,
    RISK_TABLE,
)


class DatabaseManager:
    def __init__(self):
        db_path = Path("database") / "sentinel.db"
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute(USERS_TABLE)
        self.cursor.execute(EVENTS_TABLE)
        self.cursor.execute(ALERTS_TABLE)
        self.cursor.execute(RISK_TABLE)

        self.connection.commit()

    def close(self):
        self.connection.close()