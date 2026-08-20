from modules.behavior_analyzer import BehaviorAnalyzer


analyzer = BehaviorAnalyzer()


activity = {
    "login_hour": 2,
    "downloads": 50,
    "files_opened": 100,
    "usb_used": 1
}


baseline = {
    "login_start": "09:00",
    "login_end": "18:00",
    "avg_downloads": 5,
    "avg_files_opened": 20,
    "usb_allowed": 0
}


deviations = analyzer.analyze(
    activity,
    baseline
)


for deviation in deviations:

    print(
        f"{deviation['category']}: "
        f"{deviation['message']}"
    )