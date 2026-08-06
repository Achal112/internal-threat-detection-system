from modules.explanation_engine import ExplanationEngine

engine = ExplanationEngine()

activity = {
    "login_hour":2,
    "downloads":250,
    "files_opened":120,
    "usb_used":1,
    "failed_logins":5
}

baseline = {
    "login_start":"9",
    "avg_downloads":15,
    "avg_files_opened":20
}

reasons = [
    "Login outside working hours",
    "USB detected",
    "Large download"
]

result = engine.explain(
    activity,
    baseline,
    90,
    reasons
)

for line in result:
    print(line)