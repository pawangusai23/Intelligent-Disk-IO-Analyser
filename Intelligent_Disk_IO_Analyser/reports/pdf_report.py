
from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak,
    KeepTogether
)


# =====================================================
# COLOUR THEME
# =====================================================

NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#2563EB")
LIGHT_BLUE = colors.HexColor("#EFF6FF")
LIGHT_GREY = colors.HexColor("#F1F5F9")
DARK_GREY = colors.HexColor("#475569")
BORDER = colors.HexColor("#CBD5E1")


# =====================================================
# PDF PAGE HEADER AND FOOTER
# =====================================================

def add_page_footer(canvas, document):

    canvas.saveState()

    page_width, page_height = A4

    # Footer separator
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)

    canvas.line(
        20 * mm,
        16 * mm,
        page_width - 20 * mm,
        16 * mm
    )

    # Footer text
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(DARK_GREY)

    canvas.drawCentredString(
        page_width / 2,
        11 * mm,
        "Intelligent Disk I/O Scheduling Analyser | "
        "Advanced Operating Systems"
    )

    # Page number
    canvas.drawRightString(
        page_width - 20 * mm,
        11 * mm,
        f"Page {document.page}"
    )

    canvas.restoreState()


# =====================================================
# STYLE DEFINITIONS
# =====================================================

def create_styles():

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=DARK_GREY,
        alignment=TA_CENTER,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name="SectionHeadingCustom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=NAVY,
        spaceBefore=9,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name="NormalCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name="SmallCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=DARK_GREY
    ))

    styles.add(ParagraphStyle(
        name="AlgorithmHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=NAVY,
        spaceAfter=3
    ))

    return styles


# =====================================================
# TABLE STYLE
# =====================================================

def apply_table_style(table, header=True):

    commands = [
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        (
            "ROWBACKGROUNDS",
            (0, 1),
            (-1, -1),
            [colors.white, LIGHT_GREY]
        )
    ]

    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
        ])

    table.setStyle(TableStyle(commands))

    return table


# =====================================================
# MAIN PDF GENERATOR
# =====================================================

def generate_pdf_report(
    disk_size,
    head,
    requests,
    direction,
    seek_time,
    metrics_list,
    recommendation,
    results
):
    """
    Generate a complete disk scheduling analysis PDF.

    Page 1:
        Report information
        Disk configuration
        Performance comparison
        Intelligent recommendation

    Page 2:
        Algorithm rankings
        Simulation details
        Warnings and limitations
    """

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------

    if not metrics_list:
        raise ValueError("Performance metrics are missing.")

    if not results:
        raise ValueError("Simulation results are missing.")

    if not recommendation:
        raise ValueError("Recommendation data is missing.")

    required_algorithms = {
        "FCFS", "SSTF", "SCAN",
        "C-SCAN", "LOOK", "C-LOOK"
    }

    if set(results.keys()) != required_algorithms:
        raise ValueError(
            "All six scheduling algorithm results are required."
        )

    if any(
        len(result["service_order"]) != len(requests)
        for result in results.values()
    ):
        raise ValueError(
            "One or more algorithms have incomplete service orders."
        )

    # -------------------------------------------------
    # CREATE PDF DOCUMENT
    # -------------------------------------------------

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=15 * mm,
        bottomMargin=23 * mm,
        title="Intelligent Disk I/O Scheduling Analysis",
        author="Advanced Operating Systems Mini Project"
    )

    styles = create_styles()

    story = []

    normal = styles["NormalCustom"]
    small = styles["SmallCustom"]
    heading = styles["SectionHeadingCustom"]

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------

    story.append(Paragraph(
        "INTELLIGENT DISK I/O SCHEDULING ANALYSER",
        styles["ReportTitleCustom"]
    ))

    story.append(Paragraph(
        "Performance Analysis and Simulation Report",
        styles["ReportSubtitle"]
    ))

    story.append(HRFlowable(
        width="100%",
        thickness=1,
        color=BLUE
    ))

    story.append(Spacer(1, 9))

    # -------------------------------------------------
    # SECTION 1: REPORT INFORMATION
    # -------------------------------------------------

    story.append(Paragraph(
        "1. Report Information",
        heading
    ))

    generated_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    story.append(Paragraph(
        f"<b>Generated on:</b> {generated_time}",
        normal
    ))

    story.append(Paragraph(
        "<b>Project:</b> Advanced Operating Systems Mini Project",
        normal
    ))

    # -------------------------------------------------
    # SECTION 2: DISK CONFIGURATION
    # -------------------------------------------------

    story.append(Paragraph(
        "2. Disk Configuration",
        heading
    ))

    configuration_data = [
        ["Parameter", "Value"],
        ["Disk Size", f"{disk_size} cylinders"],
        ["Initial Head Position", str(head)],
        ["Initial Direction", direction.title()],
        [
            "Request Queue",
            escape(", ".join(map(str, requests)))
        ],
        ["Number of Requests", str(len(requests))],
        [
            "Seek Time per Cylinder",
            f"{seek_time} ms"
        ]
    ]

    config_table = Table(
    configuration_data,
    colWidths=[75 * mm, 95 * mm],
    repeatRows=1
    )

    apply_table_style(config_table)

    story.append(config_table)

    # -------------------------------------------------
    # SECTION 3: PERFORMANCE COMPARISON
    # -------------------------------------------------

    story.append(Paragraph(
        "3. Algorithm Performance Comparison",
        heading
    ))

    performance_data = [[
        "Algorithm",
        "Head Movement",
        "Average",
        "Direction Changes",
        "Seek Time (ms)"
    ]]

    for item in metrics_list:

        performance_data.append([
            item["algorithm"],
            str(item["total_head_movement"]),
            str(item["average_head_movement"]),
            str(item["direction_changes"]),
            str(item["estimated_seek_time_ms"])
        ])

    performance_table = Table(
        performance_data,
        colWidths=[
            28 * mm,
            30 * mm,
            25 * mm,
            38 * mm,
            35 * mm
        ],
        repeatRows=1
    )

    apply_table_style(performance_table)

    performance_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("ALIGN", (1, 1), (-1, -1), "CENTER")
    ]))

    story.append(performance_table)

    # -------------------------------------------------
    # SECTION 4: INTELLIGENT RECOMMENDATION
    # -------------------------------------------------

    story.append(Paragraph(
        "4. Intelligent Recommendation",
        heading
    ))

    recommendation_name = escape(
        str(recommendation["recommended_algorithm"])
    )

    reason = escape(
        str(recommendation["reason"])
    )

    objective_name = escape(
        str(recommendation["objective"]).replace("_", " ").title()
    )

    score = recommendation["recommended_score"]

    recommendation_content = [
        Paragraph(
            f"<b>Recommended Algorithm:</b> {recommendation_name}",
            normal
        ),
        Paragraph(
            f"<b>Reason:</b> {reason}",
            normal
        ),
        Paragraph(
            f"<b>Recommendation Objective:</b> {objective_name}",
            normal
        ),
        Paragraph(
            f"<b>Performance Score:</b> {score}",
            normal
        )
    ]

    recommendation_table = Table(
        [[recommendation_content]],
        colWidths=[165 * mm]
    )

    recommendation_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
        ("BOX", (0, 0), (-1, -1), 0.8, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]))

    story.append(recommendation_table)

    # =================================================
    # PAGE BREAK
    # Keep all six rankings together on page 2.
    # =================================================

    story.append(PageBreak())

    # -------------------------------------------------
    # SECTION 5: ALGORITHM RANKINGS
    # -------------------------------------------------

    story.append(Paragraph(
        "5. Algorithm Rankings",
        heading
    ))

    ranking_data = [[
        "Rank",
        "Algorithm",
        "Head Movement",
        "Score"
    ]]

    for index, item in enumerate(
        recommendation["rankings"],
        start=1
    ):

        ranking_data.append([
            str(index),
            item["algorithm"],
            str(item["total_head_movement"]),
            str(item["score"])
        ])

    ranking_table = Table(
        ranking_data,
        colWidths=[
            25 * mm,
            45 * mm,
            55 * mm,
            35 * mm
        ],
        repeatRows=1
    )

    apply_table_style(ranking_table)

    ranking_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 8)
    ]))

    # Keep heading and complete ranking table together
    story.append(
        KeepTogether([
            ranking_table
        ])
    )

    # -------------------------------------------------
    # SECTION 6: SIMULATION DETAILS
    # -------------------------------------------------

    story.append(Paragraph(
        "6. Simulation Details",
        heading
    ))

    algorithm_order = [
        "FCFS",
        "SSTF",
        "SCAN",
        "C-SCAN",
        "LOOK",
        "C-LOOK"
    ]

    for name in algorithm_order:

        result = results[name]

        service_order = " -> ".join(
            map(str, result["service_order"])
        )

        movement_path = " -> ".join(
            map(str, result["movement_path"])
        )

        algorithm_block = [
            Paragraph(
                escape(name),
                styles["AlgorithmHeading"]
            ),
            Paragraph(
                f"<b>Service Order:</b> {escape(service_order)}",
                small
            ),
            Paragraph(
                f"<b>Movement Path:</b> {escape(movement_path)}",
                small
            )
        ]

        # Prevent one algorithm's details from splitting
        story.append(
            KeepTogether(algorithm_block)
        )

        story.append(Spacer(1, 7))

    # -------------------------------------------------
    # SECTION 7: WARNINGS AND LIMITATIONS
    # -------------------------------------------------

    story.append(Paragraph(
        "7. Warnings and Limitations",
        heading
    ))

    warnings = recommendation.get("warnings", [])

    if warnings:

        for warning in warnings:

            story.append(Paragraph(
                f"- {escape(str(warning))}",
                normal
            ))

    else:

        story.append(Paragraph(
            "No warnings generated.",
            normal
        ))

    story.append(Spacer(1, 6))

    limitation_text = (
        "<b>Technical Note:</b> Estimated seek time is calculated "
        "using the configured seek-time-per-cylinder value. "
        "It is a simulation estimate, not a measurement of actual "
        "disk hardware latency. This application simulates disk "
        "scheduling decisions and does not control physical disk hardware."
    )

    story.append(Paragraph(
        limitation_text,
        small
    ))

    # -------------------------------------------------
    # BUILD PDF
    # -------------------------------------------------

    document.build(
        story,
        onFirstPage=add_page_footer,
        onLaterPages=add_page_footer
    )

    buffer.seek(0)

    return buffer.getvalue()
