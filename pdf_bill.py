import os
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)

def create_pdf_bill(order_id, quantities, subtotal, gst, total, payment_method):
    BASE_DIR = os.path.dirname(__file__)
    pdf_file = os.path.join(BASE_DIR, "bill.pdf")   # FIXED: absolute path

    # Load menu
    menu = pd.read_csv(os.path.join(BASE_DIR, "menu.csv")).set_index("item_name")

    styles = getSampleStyleSheet()
    story = []

    # PDF Document
    pdf = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    # Title
    story.append(Paragraph("<b><font size=18>RESTAURANT BILL</font></b>", styles['Title']))
    story.append(Spacer(1, 12))

    # Order info
    info = f"""
    <b>Order ID:</b> {order_id}<br/>
    <b>Date:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br/>
    <b>Payment Method:</b> {payment_method}<br/>
    """
    story.append(Paragraph(info, styles['Normal']))
    story.append(Spacer(1, 12))

    # Items table
    table_data = [["Item", "Qty", "Price", "GST%", "Total"]]

    for item, qty in quantities.items():
        price = menu.loc[item, "price"]
        gst_percent = menu.loc[item, "GST"]
        item_total = price * qty + (price * qty * gst_percent / 100)
        table_data.append([item, qty, f"₹{price}", f"{gst_percent}%", f"₹{item_total:.2f}"])

    table = Table(table_data, colWidths=[50*mm, 20*mm, 25*mm, 20*mm, 35*mm])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    # Total section
    summary = f"""
    <b>Subtotal:</b> ₹{subtotal:.2f}<br/>
    <b>GST:</b> ₹{gst:.2f}<br/>
    <b><font size=14>Total Amount:</font></b> ₹{total:.2f}
    """
    story.append(Paragraph(summary, styles['Normal']))

    pdf.build(story)
