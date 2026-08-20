import sqlite3
from pathlib import Path

from database.schema import (
    USERS_TABLE,
    EVENTS_TABLE,
    ALERTS_TABLE,
    RISK_TABLE,
    BASELINE_TABLE,
    AI_ANALYSIS_TABLE
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
        self.cursor.execute(AI_ANALYSIS_TABLE)

        self.connection.commit()

        self.insert_users()

    def insert_users(self):

        users = [
            ("Alice", "IT", "Developer", "09:00"),
            ("Bob", "Finance", "Analyst", "09:00"),
            ("Charlie", "HR", "Manager", "10:00"),
            ("David", "Security", "Security Analyst", "09:00")
        ]

        self.cursor.executemany(
            """
            INSERT OR IGNORE INTO users(
                username,
                department,
                role,
                normal_login_time
            )
            VALUES (?, ?, ?, ?)
            """,
            users
        )

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
            SELECT
                username,
                department,
                role,
                normal_login_time,
                created_at
            FROM users
            WHERE username = ?
            LIMIT 1
            """,
            (username,)
        )

        return self.cursor.fetchone()

    def get_user_baseline(self, username):

        self.cursor.execute(
            """
            SELECT
                username,
                login_start,
                login_end,
                usb_allowed,
                avg_downloads,
                avg_files_opened,
                department
            FROM user_baseline
            WHERE username = ?
            LIMIT 1
            """,
            (username,)
        )

        return self.cursor.fetchone()

    def get_all_users(self):

        self.cursor.execute(
            """
            SELECT
                username,
                MAX(department) AS department,
                MAX(role) AS role,
                MAX(normal_login_time) AS normal_login_time
            FROM users
            GROUP BY username
            ORDER BY username
            """
        )

        return self.cursor.fetchall()

    
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

    def insert_ai_analysis(
        self,
        username,
        login_hour,
        downloads,
        files_opened,
        usb_used,
        failed_logins,
        prediction
    ):

        self.cursor.execute(
            """
            INSERT INTO ai_analysis(
                username,
                login_hour,
                downloads,
                files_opened,
                usb_used,
                failed_logins,
                prediction
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                login_hour,
                downloads,
                files_opened,
                usb_used,
                failed_logins,
                prediction
            )
        )

        self.connection.commit()

    def get_ai_analysis(self):

        self.cursor.execute(
            """
            SELECT *
            FROM ai_analysis
            ORDER BY id DESC
            """
        )

        return self.cursor.fetchall()

    def get_user_ai_analysis(self, username):

        self.cursor.execute(
            """
            SELECT *
            FROM ai_analysis
            WHERE username = ?
            ORDER BY timestamp DESC
            """,
            (username,)
        )

        return self.cursor.fetchall()

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
            FROM users
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

    