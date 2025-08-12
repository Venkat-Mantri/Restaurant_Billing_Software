from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def create_pdf_bill(order_id, items, total, gst, payment_method, path="data/bill.pdf"):
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica", 14)
    c.drawString(200, 750, "Restaurant Bill")

    c.setFont("Helvetica", 10)
    y = 700
    c.drawString(50, y, f"Order ID: {order_id}")
    c.drawString(300, y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30

    c.drawString(50, y, "Items:")
    y -= 20

    for item, qty in items.items():
        c.drawString(60, y, f"{item} x {qty}")
        y -= 20

    y -= 10
    c.drawString(50, y, f"GST: ₹{gst:.2f}")
    y -= 20
    c.drawString(50, y, f"Total: ₹{total:.2f}")
    y -= 20
    c.drawString(50, y, f"Payment Method: {payment_method}")

    c.save()