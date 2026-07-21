class RiskEngine:

    def calculate_risk(self, activity, baseline):

        risk = 0
        reasons = []

        # Rule 1
        if (
            activity["event_type"] == "USB Inserted"
            and baseline["usb_allowed"] == 0
        ):
            risk += 40
            reasons.append("Unauthorized USB usage")

        # Rule 2
        if activity["downloads"] > baseline["avg_downloads"]:
            risk += 20
            reasons.append("Download volume exceeded baseline")

        # Rule 3
        if activity["files_opened"] > baseline["avg_files_opened"]:
            risk += 15
            reasons.append("Opened unusually high number of files")

        # Rule 4
        if activity["login_hour"] < 6:
            risk += 25
            reasons.append("Login outside working hours")

        return risk, reasons

    def alert_level(self, risk):

        if risk >= 80:
            return "CRITICAL"

        elif risk >= 50:
            return "HIGH"

        elif risk >= 20:
            return "MEDIUM"

        return "LOW"