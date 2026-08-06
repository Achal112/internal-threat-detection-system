class ExplanationEngine:

    def explain(
        self,
        activity,
        baseline,
        risk,
        reasons
    ):

        explanation = []

        explanation.append(
            f"Final Risk Score : {risk}"
        )

        explanation.append("")

        explanation.append("Reasons")

        for reason in reasons:

            explanation.append(
                f"• {reason}"
            )

        explanation.append("")

        explanation.append("Behaviour Analysis")

        login_start = int(
            str(baseline["login_start"]).split(":")[0]
        )

        login_end = int(
            str(baseline["login_end"]).split(":")[0]
        )
        
        if activity["login_hour"] < login_start:

            explanation.append(
                "✓ Logged in before normal working hours."
            )

        if activity["downloads"] > baseline["avg_downloads"]:

            explanation.append(
                "✓ Download volume exceeded normal behaviour."
            )

        if activity["files_opened"] > baseline["avg_files_opened"]:

            explanation.append(
                "✓ Unusual number of files opened."
            )

        if activity["usb_used"]:

            explanation.append(
                "✓ USB activity detected."
            )

        if activity["failed_logins"] >= 3:

            explanation.append(
                "✓ Multiple failed login attempts."
            )

        return explanation