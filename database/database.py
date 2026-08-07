import sqlite3
from pathlib import Path

from database.schema import (
    USERS_TABLE,
    EVENTS_TABLE,
    ALERTS_TABLE,
    RISK_TABLE,
    BASELINE_TABLE
)

class DatabaseManager:
    def __init__(self):
        db_path = Path("database") / "sentinel.db"

        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute(USERS_TABLE)
        self.cursor.execute(EVENTS_TABLE)
        self.cursor.execute(ALERTS_TABLE)
        self.cursor.execute(RISK_TABLE)
        self.cursor.execute(BASELINE_TABLE)
        self.connection.commit()

    def insert_event(self, username, event_type, description, severity):
        self.cursor.execute(
            """
            INSERT INTO events(username, event_type, description, severity)
            VALUES (?, ?, ?, ?)
            """,
            (username, event_type, description, severity),
        )
        self.connection.commit()

    def get_events(self):
        self.cursor.execute("""
            SELECT *
            FROM events
            ORDER BY id DESC
        """)
        return self.cursor.fetchall()
    
    def insert_baseline(
        self,
        username,
        login_start,
        login_end,
        usb_allowed,
        avg_downloads,
        avg_files_opened,
        department
    ):
        self.cursor.execute(
        """
        INSERT OR REPLACE INTO user_baseline(
            username,
            login_start,
            login_end,
            usb_allowed,
            avg_downloads,
            avg_files_opened,
            department
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            login_start,
            login_end,
            usb_allowed,
            avg_downloads,
            avg_files_opened,
            department
        )
    )

        self.connection.commit()


    def get_baseline(self, username):

        self.cursor.execute(
            """
            SELECT *
            FROM user_baseline
            WHERE username=?
            """,
            (username,)
        )

        return self.cursor.fetchone()

    def get_user_profile(self, username):

        self.cursor.execute(
            """
            SELECT *
            FROM user_baseline
            WHERE username = ?
            """,
            (username,)
        )

        return self.cursor.fetchone()
    
    def insert_risk(self, username, score):

        self.cursor.execute(
        """
        INSERT INTO risk(
            username,
            risk_score
        )
        VALUES (?, ?)
        """,
        (username, score)
    )

        self.connection.commit()

    def insert_alert(
        self,
        username,
        risk_score,
        alert_level,
        reason
    ):

        self.cursor.execute(
        """
        INSERT INTO alerts(
            username,
            risk_score,
            alert_level,
            reason
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            risk_score,
            alert_level,
            reason
        )
    )

        self.connection.commit()


    def get_alerts(self):

        self.cursor.execute(
            """
            SELECT *
            FROM alerts
            ORDER BY id DESC
            """
        )

        return self.cursor.fetchall()

    def get_event_count(self):

        self.cursor.execute("""
            SELECT COUNT(*) AS total
            FROM events
        """)

        return self.cursor.fetchone()["total"]

    def get_alert_count(self):

        self.cursor.execute("""
            SELECT COUNT(*) AS total
            FROM alerts
        """)

        return self.cursor.fetchone()["total"]
    
    def get_user_count(self):

        self.cursor.execute("""
            SELECT COUNT(*) AS total
            FROM user_baseline
        """)

        return self.cursor.fetchone()["total"]
    
    def get_latest_risks(self):

        self.cursor.execute("""
            SELECT
                username,
                MAX(risk_score) AS risk_score
            FROM risk
            GROUP BY username
            ORDER BY risk_score DESC
        """)

        return [dict(row) for row in self.cursor.fetchall()]

    def get_user_risk_history(self, username):

        self.cursor.execute(
            """
            SELECT
                timestamp,
                risk_score
            FROM risk
            WHERE username = ?
            ORDER BY timestamp
            """,
            (username,)
        )

        return self.cursor.fetchall()

    def get_event_statistics(self):

        self.cursor.execute("""
            SELECT
                event_type,
                COUNT(*) AS total
            FROM events
            GROUP BY event_type
        """)

        return self.cursor.fetchall()

    def close(self):
        self.connection.close()