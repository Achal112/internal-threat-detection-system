class BehaviorEngine:

    def compare(self, activity, baseline):

        comparison = []

        # Login
        if activity["login_hour"] < int(baseline["login_start"][:2]):

            comparison.append({
                "Feature": "Login Time",
                "Status": "Abnormal",
                "Value": activity["login_hour"]
            })

        else:

            comparison.append({
                "Feature": "Login Time",
                "Status": "Normal",
                "Value": activity["login_hour"]
            })

        # Downloads
        if activity["downloads"] > baseline["avg_downloads"]:

            comparison.append({
                "Feature": "Downloads",
                "Status": "Abnormal",
                "Value": activity["downloads"]
            })

        else:

            comparison.append({
                "Feature": "Downloads",
                "Status": "Normal",
                "Value": activity["downloads"]
            })

        # Files Opened
        if activity["files_opened"] > baseline["avg_files_opened"]:

            comparison.append({
                "Feature": "Files Opened",
                "Status": "Abnormal",
                "Value": activity["files_opened"]
            })

        else:

            comparison.append({
                "Feature": "Files Opened",
                "Status": "Normal",
                "Value": activity["files_opened"]
            })

        return comparison