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
CREATE TABLE IF NOT EXISTS risk(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    risk_score INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

BASELINE_TABLE = """
CREATE TABLE IF NOT EXISTS user_baseline(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    login_start TEXT,

    login_end TEXT,

    usb_allowed INTEGER,

    avg_downloads INTEGER,

    avg_files_opened INTEGER,

    department TEXT
);
"""

AI_ANALYSIS_TABLE = """
CREATE TABLE IF NOT EXISTS ai_analysis(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL,

    login_hour INTEGER,

    downloads INTEGER,

    files_opened INTEGER,

    usb_used INTEGER,

    failed_logins INTEGER,

    prediction TEXT,

    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
"""