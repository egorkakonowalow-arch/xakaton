"""
Module: export.py
Layer: Utils
Description:
    Builds report exports in PDF and CSV formats.
Interacts with:
    - reportlab
    - app.models.report
Called by:
    - app.service.report_service
"""

import csv
from io import BytesIO, StringIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.models.report import Report


def build_report_pdf_bytes(report: Report) -> bytes:
    buf = BytesIO()
    pdf = canvas.Canvas(buf, pagesize=A4)
    pdf.drawString(50, 800, f"Report ID: {report.id}")
    pdf.drawString(50, 780, f"Template: {report.template_id}")
    pdf.drawString(50, 760, f"District: {report.district_id}")
    pdf.drawString(50, 740, f"Status: {report.status.value}")
    pdf.showPage()
    pdf.save()
    return buf.getvalue()


def build_report_csv_bytes(report: Report) -> bytes:
    stream = StringIO()
    writer = csv.writer(stream)
    writer.writerow(["report_id", "template_id", "district_id", "submitted_by", "status"])
    writer.writerow([report.id, report.template_id, report.district_id, report.submitted_by, report.status.value])
    return stream.getvalue().encode("utf-8")
