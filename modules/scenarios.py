NORMAL_DAY = [
    {
        "event_type": "Login",
        "description": "User logged into workstation",
        "severity": "Low",
        "downloads": 0,
        "files_opened": 0
    },
    {
        "event_type": "Open File",
        "description": "Opened department document",
        "severity": "Low",
        "downloads": 0,
        "files_opened": 8
    },
    {
        "event_type": "Send Email",
        "description": "Sent internal email",
        "severity": "Low",
        "downloads": 0,
        "files_opened": 8
    },
    {
        "event_type": "Logout",
        "description": "User logged out",
        "severity": "Low",
        "downloads": 0,
        "files_opened": 8
    }
]

INSIDER_ATTACK = [
    {
        "event_type": "Login",
        "description": "Late-night login",
        "severity": "Medium",
        "downloads": 0,
        "files_opened": 0
    },
    {
        "event_type": "USB Inserted",
        "description": "USB storage connected",
        "severity": "High",
        "downloads": 0,
        "files_opened": 0
    },
    {
        "event_type": "Access Database",
        "description": "Payroll database accessed",
        "severity": "High",
        "downloads": 100,
        "files_opened": 200
    },
    {
        "event_type": "Download File",
        "description": "Mass confidential file download",
        "severity": "Critical",
        "downloads": 500,
        "files_opened": 300
    }
]