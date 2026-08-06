class MitreMapper:

    def __init__(self):

        self.techniques = {

            "Login": {
                "id": "T1078",
                "name": "Valid Accounts"
            },

            "USB Inserted": {
                "id": "T1091",
                "name": "Replication Through Removable Media"
            },

            "Download File": {
                "id": "T1048",
                "name": "Exfiltration Over Alternative Protocol"
            },

            "Access Database": {
                "id": "T1213",
                "name": "Data from Information Repositories"
            },

            "Open File": {
                "id": "T1005",
                "name": "Data from Local System"
            },

            "Send Email": {
                "id": "T1567",
                "name": "Exfiltration Over Web Service"
            },

            "Logout": {
                "id": "-",
                "name": "Normal Activity"
            }

        }

    def map_event(self, event_type):

        return self.techniques.get(

            event_type,

            {
                "id": "Unknown",
                "name": "Unknown Technique"
            }

        )