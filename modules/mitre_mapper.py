class MitreMapper:

    MITRE_MAPPING = {

        "login": {
            "name": "Valid Accounts",
            "id": "T1078",
            "tactic": "Initial Access"
        },

        "failed_login": {
            "name": "Brute Force",
            "id": "T1110",
            "tactic": "Credential Access"
        },

        "file_access": {
            "name": "Data from Local System",
            "id": "T1005",
            "tactic": "Collection"
        },

        "mass_download": {
            "name": "Data from Local System",
            "id": "T1005",
            "tactic": "Collection"
        },

        "usb": {
            "name": "Exfiltration Over Physical Medium",
            "id": "T1052.001",
            "tactic": "Exfiltration"
        },

        "usb_transfer": {
            "name": "Exfiltration Over Physical Medium",
            "id": "T1052.001",
            "tactic": "Exfiltration"
        }
    }

    def map_event(self, event_type):

        event_type = event_type.lower().strip()

        return self.MITRE_MAPPING.get(
            event_type,
            {
                "name": "Unknown",
                "id": "N/A",
                "tactic": "Unknown"
            }
        )

    def map_events(self, events):

        mappings = []

        for event in events:

            technique = self.map_event(
                event["event_type"]
            )

            mappings.append({
                "event": event["event_type"],
                "name": technique["name"],
                "id": technique["id"],
                "tactic": technique["tactic"]
            })

        return mappings