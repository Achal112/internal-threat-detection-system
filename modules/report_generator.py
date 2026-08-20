from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


class IncidentReportGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.title_style = ParagraphStyle(
            "ReportTitle",
            parent=self.styles["Title"],
            alignment=TA_CENTER,
            fontSize=20,
            spaceAfter=10
        )

        self.heading_style = ParagraphStyle(
            "ReportHeading",
            parent=self.styles["Heading2"],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=8
        )

        self.body_style = ParagraphStyle(
            "ReportBody",
            parent=self.styles["BodyText"],
            fontSize=9,
            leading=13
        )

    def generate(
        self,
        username,
        risk_score,
        threat_level,
        events,
        mitre_results,
        explanation,
        reasons,
        department="Unknown",
        role="Unknown"
    ):

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm
        )

        story = []

        # -----------------------------------------
        # Title
        # -----------------------------------------

        story.append(
            Paragraph(
                "SentinelAI",
                self.title_style
            )
        )

        story.append(
            Paragraph(
                "Incident Investigation Report",
                self.heading_style
            )
        )

        story.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                self.body_style
            )
        )

        story.append(Spacer(1, 10))

        # -----------------------------------------
        # Employee Information
        # -----------------------------------------

        story.append(
            Paragraph(
                "1. Employee Information",
                self.heading_style
            )
        )

        employee_data = [
            ["Employee", username],
            ["Department", department],
            ["Role", role],
            ["Risk Score", str(risk_score)],
            ["Threat Level", threat_level]
        ]

        employee_table = Table(
            employee_data,
            colWidths=[45 * mm, 120 * mm]
        )

        employee_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6)
            ])
        )

        story.append(employee_table)

        # -----------------------------------------
        # Risk Assessment
        # -----------------------------------------

        story.append(
            Paragraph(
                "2. Risk Assessment",
                self.heading_style
            )
        )

        story.append(
            Paragraph(
                str(explanation),
                self.body_style
            )
        )

        story.append(Spacer(1, 6))

        if reasons:

            reason_rows = [
                ["Risk Indicators"]
            ]

            for reason in reasons:
                reason_rows.append([str(reason)])

            reason_table = Table(
                reason_rows,
                colWidths=[165 * mm]
            )

            reason_table.setStyle(
                TableStyle([
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("PADDING", (0, 0), (-1, -1), 6)
                ])
            )

            story.append(reason_table)

        # -----------------------------------------
        # MITRE ATT&CK
        # -----------------------------------------

        story.append(
            Paragraph(
                "3. MITRE ATT&CK Mapping",
                self.heading_style
            )
        )

        mitre_data = [
            [
                "Event",
                "Technique",
                "MITRE ID",
                "Tactic"
            ]
        ]

        for result in mitre_results:

            mitre_data.append([
                result.get("event", "Unknown"),
                result.get("name", "Unknown"),
                result.get("id", "N/A"),
                result.get("tactic", "Unknown")
            ])

        if len(mitre_data) > 1:

            mitre_table = Table(
                mitre_data,
                colWidths=[
                    35 * mm,
                    55 * mm,
                    30 * mm,
                    45 * mm
                ]
            )

            mitre_table.setStyle(
                TableStyle([
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 5)
                ])
            )

            story.append(mitre_table)

        else:

            story.append(
                Paragraph(
                    "No MITRE ATT&CK techniques identified.",
                    self.body_style
                )
            )

        # -----------------------------------------
        # Activity Timeline
        # -----------------------------------------

        story.append(
            Paragraph(
                "4. Activity Timeline",
                self.heading_style
            )
        )

        event_data = [
            [
                "Time",
                "Event",
                "Severity",
                "Description"
            ]
        ]

        for event in events:

            event_data.append([
                str(event["timestamp"]),
                str(event["event_type"]),
                str(event["severity"]),
                str(event["description"])
            ])

        if len(event_data) > 1:

            event_table = Table(
                event_data,
                colWidths=[
                    30 * mm,
                    35 * mm,
                    25 * mm,
                    75 * mm
                ]
            )

            event_table.setStyle(
                TableStyle([
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 4)
                ])
            )

            story.append(event_table)

        else:

            story.append(
                Paragraph(
                    "No activity events recorded.",
                    self.body_style
                )
            )

        # -----------------------------------------
        # Footer
        # -----------------------------------------

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "Generated by SentinelAI — AI-Based Insider Threat Detection & UEBA Platform",
                self.body_style
            )
        )

        document.build(story)

        buffer.seek(0)

        return buffer