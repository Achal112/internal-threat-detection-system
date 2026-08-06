import random

from modules.scenarios import NORMAL_DAY, INSIDER_ATTACK

USERS = [
    "Alice",
    "Bob",
    "Charlie",
    "David"
]


class ActivitySimulator:

    def generate_scenario(self):

        username = random.choice(USERS)

        scenario = random.choice([
            NORMAL_DAY,
            INSIDER_ATTACK
        ])

        events = []

        if scenario == NORMAL_DAY:

                login_hour = random.randint(8, 10)
                usb_used = random.randint(0, 1)
                failed_logins = random.randint(0, 2)

        else:

                login_hour = random.randint(1, 3)
                usb_used = random.randint(1, 3)
                failed_logins = random.randint(3, 8)

        for event in scenario:

            events.append({
                "username": username,
                "event_type": event["event_type"],
                "description": event["description"],
                "severity": event["severity"],
                "downloads": event["downloads"],
                "files_opened": event["files_opened"],
                "login_hour": login_hour,
                "usb_used": usb_used,
                "failed_logins": failed_logins
            })

        return events