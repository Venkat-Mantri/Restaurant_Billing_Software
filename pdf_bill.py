from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from datetime import datetime
import os
import pandas as pd

def create_pdf_bill(order_id, quantities, subtotal, gst, total, payment_method):
    pdf_file = "bill.pdf"
    
    # Load menu for pricing
    menu = pd.read_csv("menu.csv").set_index("item_name")
    
    # PDF Setup
    pdf = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # --------- HEADER WITH LOGO ---------
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=50*mm, height=20*mm)
        story.append(logo)
    
    story.append(Paragraph("<b><font size=18>RESTAURANT BILL</font></b>", styles['Title']))
    story.append(Spacer(1, 6))
    
    # Restaurant info
    restaurant_info = """
    <b>Restaurant Name:</b> Venkat’s Kitchen<br/>
    <b>Address:</b> Main Road, Hyderabad, Telangana<br/>
    <b>Phone:</b> +91 98765 43210<br/><br/>
    """
    story.append(Paragraph(restaurant_info, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # --------- BILL DETAILS ---------
