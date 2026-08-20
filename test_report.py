from modules.report_generator import IncidentReportGenerator


generator = IncidentReportGenerator()

pdf = generator.generate(
    username="Alice",
    risk_score=85,
    threat_level="Critical",
    department="IT",
    events=[
        {
            "timestamp": "2026-08-10 14:30:00",
            "event_type": "USB",
            "severity": "Critical",
            "description": "Large data transfer detected"
        }
    ],
    mitre_results=[
        {
            "event": "USB",
            "name": "Exfiltration Over Physical Medium",
            "id": "T1052.001",
            "tactic": "Exfiltration"
        }
    ],
    explanation="User activity significantly deviates from the established behavioral baseline.",
    reasons=[
        "Unusual login time",
        "High file access volume",
        "USB activity detected"
    ]
)

with open("test_incident_report.pdf", "wb") as file:
    file.write(pdf.read())

print("Report generated successfully.")