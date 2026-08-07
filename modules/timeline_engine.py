class TimelineEngine:

    def build_timeline(self, events):

        timeline = []

        for event in events:

            severity = event["severity"].lower()

            if severity == "critical":
                icon = "🔴"

            elif severity == "high":
                icon = "🟠"

            elif severity == "medium":
                icon = "🟡"

            else:
                icon = "🟢"

            timeline.append({

                "time": event["timestamp"],
                "icon": icon,
                "event": event["event_type"],
                "severity": event["severity"],
                "description": event["description"],
                "user": event["username"]

            })

        return timeline