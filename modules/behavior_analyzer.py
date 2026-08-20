class BehaviorAnalyzer:

    def analyze(self, activity, baseline):

        deviations = []

        # -----------------------------------------
        # Login Time Deviation
        # -----------------------------------------

        login_hour = activity.get("login_hour")

        login_start = self._extract_hour(
            baseline["login_start"]
        )

        login_end = self._extract_hour(
            baseline["login_end"]
        )

        if login_hour is not None:

            if not (
                login_start <= login_hour <= login_end
            ):

                deviations.append({
                    "category": "Login Time",
                    "normal": (
                        f"{login_start:02d}:00 - "
                        f"{login_end:02d}:00"
                    ),
                    "observed": f"{login_hour:02d}:00",
                    "severity": "High",
                    "message": (
                        "Login occurred outside "
                        "the user's normal working window."
                    )
                })

        # -----------------------------------------
        # Download Deviation
        # -----------------------------------------

        downloads = activity.get(
            "downloads",
            0
        )

        avg_downloads = baseline[
            "avg_downloads"
        ]

        if downloads > avg_downloads * 2:

            deviations.append({
                "category": "Downloads",
                "normal": str(avg_downloads),
                "observed": str(downloads),
                "severity": "High",
                "message": (
                    "Download activity is significantly "
                    "higher than the user's baseline."
                )
            })

        # -----------------------------------------
        # File Access Deviation
        # -----------------------------------------

        files_opened = activity.get(
            "files_opened",
            0
        )

        avg_files = baseline[
            "avg_files_opened"
        ]

        if files_opened > avg_files * 2:

            deviations.append({
                "category": "File Access",
                "normal": str(avg_files),
                "observed": str(files_opened),
                "severity": "Medium",
                "message": (
                    "File access activity is significantly "
                    "higher than the user's baseline."
                )
            })

        # -----------------------------------------
        # USB Deviation
        # -----------------------------------------

        usb_used = activity.get(
            "usb_used",
            0
        )

        usb_allowed = baseline[
            "usb_allowed"
        ]

        if usb_used and not usb_allowed:

            deviations.append({
                "category": "USB Usage",
                "normal": "USB Not Allowed",
                "observed": "USB Used",
                "severity": "Critical",
                "message": (
                    "USB activity violates the user's "
                    "established security policy."
                )
            })

        return deviations

    # -----------------------------------------
    # Convert DB time → hour
    # -----------------------------------------

    def _extract_hour(self, value):

        if value is None:
            return 0

        value = str(value)

        # Handles "09:00"
        if ":" in value:

            return int(
                value.split(":")[0]
            )

        # Handles "9"
        return int(value)