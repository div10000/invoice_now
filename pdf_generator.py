from fpdf import FPDF

def create_invoice_pdf(name, address, desc, qty, price, invoice_id):
    try:
        qty = int(qty)
    except ValueError:
        qty = 0
    try:
        price = float(price)
    except ValueError:
        price = 0.0

    total = qty * price

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Invoice", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(100, 10, txt=f"Customer Name: {name}", ln=True)
    pdf.cell(100, 10, txt=f"Address: {address}", ln=True)
    pdf.ln(10)

    pdf.cell(100, 10, txt=f"Item Description: {desc}", ln=True)
    pdf.cell(100, 10, txt=f"Quantity: {qty}", ln=True)
    pdf.cell(100, 10, txt=f"Price per Unit: Rs. {price}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, txt=f"Total: Rs. {total}", ln=True)

    output_file = f"{invoice_id}.pdf"
    pdf.output(output_file)
