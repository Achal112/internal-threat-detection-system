USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    department TEXT,
    role TEXT,
    normal_login_time TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    event_type TEXT,
    description TEXT,
    severity TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

ALERTS_TABLE = """
CREATE TABLE IF NOT EXISTS alerts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    risk_score INTEGER,
    alert_level TEXT,
    reason TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

RISK_TABLE = """
CREATE TABLE IF NOT EXISTS risk_scores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    score INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""