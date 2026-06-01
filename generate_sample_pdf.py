from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

OUTPUT = "sample_contracts/globaltech_databridge_sow.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=LETTER,
    leftMargin=1 * inch,
    rightMargin=1 * inch,
    topMargin=1 * inch,
    bottomMargin=1 * inch,
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=16, alignment=TA_CENTER, spaceAfter=6)
subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=10, alignment=TA_CENTER, spaceAfter=20, textColor=colors.grey)
h1_style = ParagraphStyle("H1", parent=styles["Heading2"], fontSize=12, spaceBefore=16, spaceAfter=6, textColor=colors.HexColor("#1a1a2e"))
body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=15, alignment=TA_JUSTIFY, spaceAfter=8)
bold_style = ParagraphStyle("Bold", parent=body_style, fontName="Helvetica-Bold")

story = []

# Header
story.append(Spacer(1, 0.2 * inch))
story.append(Paragraph("STATEMENT OF WORK", title_style))
story.append(Paragraph("SOW-2024-0047 | Confidential", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1a1a2e")))
story.append(Spacer(1, 0.2 * inch))

# Parties table
party_data = [
    ["CLIENT", "SERVICE PROVIDER"],
    ["GlobalTech Solutions LLC", "DataBridge Analytics Inc."],
    ["1800 Tech Boulevard, Suite 400", "320 Innovation Drive, Floor 12"],
    ["Austin, TX 78701", "Boston, MA 02110"],
    ["EIN: 47-2938401", "EIN: 83-1047265"],
]
party_table = Table(party_data, colWidths=[3.2 * inch, 3.2 * inch])
party_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 10),
    ("FONTSIZE", (0, 1), (-1, -1), 9),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f9f9f9"), colors.white]),
]))
story.append(party_table)
story.append(Spacer(1, 0.2 * inch))

# Key dates table
dates_data = [
    ["Effective Date", "Expiration Date", "Total Value", "Currency"],
    ["September 1, 2024", "August 31, 2025", "$240,000.00", "USD"],
]
dates_table = Table(dates_data, colWidths=[1.6 * inch] * 4)
dates_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f0fe")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("PADDING", (0, 0), (-1, -1), 8),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
]))
story.append(dates_table)
story.append(Spacer(1, 0.2 * inch))

# Sections
sections = [
    ("1. PURPOSE AND SCOPE", [
        "This Statement of Work (SOW) is entered into as of September 1, 2024 (the <b>Effective Date</b>) "
        "between <b>GlobalTech Solutions LLC</b> (Client) and <b>DataBridge Analytics Inc.</b> (Service Provider), "
        "and is incorporated into the Master Services Agreement dated January 15, 2024 (the MSA).",
        "Service Provider shall design, develop, and deploy a cloud-native data integration platform "
        "enabling real-time data ingestion from Client's legacy ERP systems into a modern lakehouse "
        "architecture hosted on AWS. The platform shall support a minimum of 50 concurrent data streams "
        "and process no fewer than 10 million records per day.",
    ]),
    ("2. TERM AND RENEWAL", [
        "This SOW shall commence on the Effective Date and expire on <b>August 31, 2025</b>, unless earlier "
        "terminated in accordance with the MSA. This SOW shall <b>not automatically renew</b>; any extension "
        "must be agreed in writing by both parties no later than 30 days prior to expiration.",
    ]),
    ("3. FEES AND PAYMENT TERMS", [
        "Client shall pay Service Provider a fixed fee of <b>USD 240,000</b> for the services described herein, "
        "payable in quarterly installments of USD 60,000 each. Invoices shall be issued on the first business "
        "day of each calendar quarter. Client shall remit payment within <b>Net 45 days</b> of invoice receipt.",
        "All amounts are exclusive of applicable taxes. Client shall be responsible for all sales, use, "
        "VAT, or similar taxes imposed on the services.",
    ]),
    ("4. SERVICE LEVELS AND PERFORMANCE", [
        "Service Provider guarantees the following service levels for the production platform:",
        "• <b>Platform Availability:</b> 99.5% uptime measured monthly, excluding scheduled maintenance windows.",
        "• <b>Data Latency:</b> End-to-end processing latency not to exceed 15 minutes for 95% of records.",
        "• <b>Incident Response:</b> P1 incidents acknowledged within 30 minutes; resolved within 4 hours.",
        "• <b>P2 Incidents:</b> Acknowledged within 2 hours; resolved within 1 business day.",
        "• <b>Monthly Reporting:</b> Service Provider shall deliver a monthly SLA compliance report by the 5th business day of the following month.",
        "In the event of SLA breach, Client shall be entitled to service credits equal to 5% of the monthly fee for each 0.5% of availability below the guaranteed threshold, up to a maximum of 20% of the monthly fee.",
    ]),
    ("5. KEY OBLIGATIONS", [
        "<b>Service Provider shall:</b> (a) assign a dedicated Project Manager and Technical Lead to the engagement; "
        "(b) conduct bi-weekly progress reviews with Client stakeholders; (c) deliver all source code to Client "
        "upon completion under an irrevocable license; (d) maintain SOC 2 Type II certification throughout the term; "
        "(e) ensure all data processing occurs within AWS us-east-1 region unless otherwise approved in writing.",
        "<b>Client shall:</b> (a) provide Service Provider with read access to all relevant source systems within "
        "10 business days of the Effective Date; (b) designate a named technical point of contact; "
        "(c) review and approve deliverables within 15 business days of submission; "
        "(d) pay all undisputed invoices on time.",
    ]),
    ("6. GOVERNING LAW AND DISPUTE RESOLUTION", [
        "This SOW and any disputes arising hereunder shall be governed by the laws of the "
        "<b>Commonwealth of Massachusetts</b>, without regard to its conflict of laws provisions. "
        "Any dispute not resolved through good-faith negotiation within 30 days shall be submitted "
        "to binding arbitration under the AAA Commercial Arbitration Rules in Boston, Massachusetts.",
    ]),
    ("7. LIABILITY", [
        "Each party's total aggregate liability under this SOW shall not exceed <b>USD 480,000</b>, "
        "representing two times the total fees payable hereunder. Neither party shall be liable for "
        "indirect, incidental, consequential, or punitive damages, regardless of the theory of liability.",
    ]),
    ("8. TERMINATION FOR CONVENIENCE", [
        "Either party may terminate this SOW for convenience upon <b>60 days' prior written notice</b> "
        "to the other party. In the event of such termination, Client shall pay Service Provider for "
        "all work completed and non-cancellable commitments incurred prior to the termination effective date.",
    ]),
]

for heading, paragraphs in sections:
    story.append(Paragraph(heading, h1_style))
    for para in paragraphs:
        story.append(Paragraph(para, body_style))
    story.append(Spacer(1, 0.05 * inch))

# Signature block
story.append(Spacer(1, 0.3 * inch))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
story.append(Spacer(1, 0.15 * inch))
story.append(Paragraph("AGREED AND ACCEPTED", bold_style))
story.append(Spacer(1, 0.1 * inch))

sig_data = [
    ["GlobalTech Solutions LLC", "DataBridge Analytics Inc."],
    ["Signature: ___________________", "Signature: ___________________"],
    ["Name: Sarah K. Millward", "Name: James T. Okafor"],
    ["Title: VP, Technology Partnerships", "Title: Chief Revenue Officer"],
    ["Date: ____________________", "Date: ____________________"],
]
sig_table = Table(sig_data, colWidths=[3.2 * inch, 3.2 * inch])
sig_table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("PADDING", (0, 0), (-1, -1), 4),
    ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#cccccc")),
]))
story.append(sig_table)

doc.build(story)
print(f"PDF generated: {OUTPUT}")
