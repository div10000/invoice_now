from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

def create_invoice_pdf(company_name, customer_name, customer_address, items, message, invoice_id):
    c = canvas.Canvas(f"{invoice_id}.pdf", pagesize=A4)
    width, height = A4

    # Header Bar
    header_height = 60
    c.setFillColor(colors.HexColor('#2E86C1'))
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(inch, height - header_height + 20, company_name)
    # Logo placeholder (optional)
    # c.drawImage('logo.png', width - 2*inch, height - header_height + 10, width=50, height=40, mask='auto')

    y = height - header_height - 30

    # Invoice ID and Date
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    c.drawRightString(width - inch, y, f"Invoice ID: {invoice_id}")
    c.drawRightString(width - inch, y - 18, f"Date: {datetime.now().strftime('%d-%m-%Y')}")
    y -= 40

    # Customer Info Box
    c.setFillColor(colors.HexColor('#F2F3F4'))
    c.roundRect(inch - 5, y - 5, 250, 50, 8, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#2E4053'))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, y + 30, f"Billed To:")
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    c.drawString(inch, y + 15, customer_name)
    for i, line in enumerate(customer_address.split("\n")):
        c.drawString(inch, y + 2 - 12 * i, line)
    y -= 60

    # Table Column Positions
    col_desc_x = inch + 5
    col_qty_x = inch + 270
    col_price_x = inch + 350
    col_total_x = inch + 440
    table_width = width - 2 * inch
    row_height = 22

    # Table Header
    c.setFillColor(colors.HexColor('#2874A6'))
    c.roundRect(inch, y, table_width, row_height, 6, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(col_desc_x, y + 6, "Item Description")
    c.drawRightString(col_qty_x, y + 6, "Qty")
    c.drawRightString(col_price_x, y + 6, "Price")
    c.drawRightString(col_total_x, y + 6, "Total")
    y -= row_height

    # Table Rows with alternating colors and borders
    c.setFont("Helvetica", 10)
    total_price = 0
    for idx, item in enumerate(items):
        if y < 100:
            c.showPage()
            y = height - inch
        # Alternating row color
        if idx % 2 == 0:
            c.setFillColor(colors.HexColor('#EBF5FB'))
        else:
            c.setFillColor(colors.white)
        c.rect(inch, y, table_width, row_height, fill=1, stroke=0)
        c.setFillColor(colors.black)
        desc = item.get("desc", "")
        qty = item.get("qty", 0)
        price = item.get("price", 0.0)
        line_total = qty * price
        total_price += line_total
        c.drawString(col_desc_x, y + 6, desc)
        c.drawRightString(col_qty_x, y + 6, str(qty))
        c.drawRightString(col_price_x, y + 6, f"{price:.2f}")
        c.drawRightString(col_total_x, y + 6, f"{line_total:.2f}")
        # Row border
        c.setStrokeColor(colors.HexColor('#D5D8DC'))
        c.line(inch, y, inch + table_width, y)
        y -= row_height

    # Table border (bottom)
    c.setStrokeColor(colors.HexColor('#2874A6'))
    c.setLineWidth(1.2)
    c.line(inch, y + row_height, inch + table_width, y + row_height)
    c.line(inch, y, inch + table_width, y)
    c.setLineWidth(1)

    # Total amount summary box
    y -= 10
    c.setFillColor(colors.HexColor('#F9E79F'))
    c.roundRect(col_price_x - 30, y, 180, 30, 8, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#B9770E'))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(col_price_x - 20, y + 10, "Total:")
    c.setFillColor(colors.HexColor('#145A32'))
    c.drawRightString(col_total_x + 60, y + 10, f"₹{total_price:.2f}")
    y -= 40

    # Optional message
    if message:
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor('#2E4053'))
        c.drawString(inch, y, "Note:")
        y -= 15
        text = c.beginText(inch, y)
        text.setFont("Helvetica", 10)
        text.setFillColor(colors.black)
        for line in message.split("\n"):
            text.textLine(line)
        c.drawText(text)
        y = text.getY() - 20

    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.HexColor('#85929E'))
    c.drawCentredString(width / 2.0, 30, "Generated with Invoice Now")

    c.save()
