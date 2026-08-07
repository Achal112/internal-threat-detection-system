from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime


class ReportGenerator:

    def generate(
        self,
        filename,
        profile,
        risk,
        reasons,
        mitre,
        explanation
    ):

        styles = getSampleStyleSheet()

        pdf = SimpleDocTemplate(filename)

        story = []

        story.append(
            Paragraph(
                "<b>SentinelAI Incident Report</b>",
                styles["Title"]
            )
        )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                f"<b>Employee:</b> {profile['username']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Department:</b> {profile['department']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Risk Score:</b> {risk}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Date:</b> {datetime.now()}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                "<b>Reasons</b>",
                styles["Heading2"]
            )
        )

        for reason in reasons:

            story.append(
                Paragraph(
                    f"• {reason}",
                    styles["BodyText"]
                )
            )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                "<b>MITRE ATT&CK</b>",
                styles["Heading2"]
            )
        )

        for attack in mitre:

            story.append(
                Paragraph(
                    attack,
                    styles["BodyText"]
                )
            )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                "<b>AI Explanation</b>",
                styles["Heading2"]
            )
        )

        for line in explanation:

            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

        pdf.build(story)