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

        login_hour = 9

        if scenario == INSIDER_ATTACK:
            login_hour = 2

        for event in scenario:

            events.append({
                "username": username,
                "event_type": event["event_type"],
                "description": event["description"],
                "severity": event["severity"],
                "downloads": event["downloads"],
                "files_opened": event["files_opened"],
                "login_hour": login_hour
            })

        return events