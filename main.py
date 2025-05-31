from pdf_generator import create_invoice_pdf
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from invoice import Invoice  # Your existing Invoice class
from email_sender import send_email_with_attachment

# ... your existing imports and Builder.load_file ...
Builder.load_file("ui.kv")
class InvoiceLayout(BoxLayout):
    pass

class InvoiceApp(App):
    def build(self):
        self.title = "Quick Invoice"
        return InvoiceLayout()

    def clear_form(self):
        root = self.root
        root.ids.company_name.text = ''
        root.ids.customer_name.text = ''
        root.ids.customer_address.text = ''
        root.ids.email.text = ''
        root.ids.message.text = ''
        root.ids.total_price.text = "0.00"

        # Clear all item rows
        items_box = root.ids.items_box
        items_box.clear_widgets()
        self.add_item()  # Start with one empty item row

    def add_item(self):
        from kivy.factory import Factory
        items_box = self.root.ids.items_box
        item_row = Factory.ItemRow()
        items_box.add_widget(item_row)
        self.update_total()

    def remove_item(self):
        items_box = self.root.ids.items_box
        if items_box.children:
            items_box.remove_widget(items_box.children[-1])  # remove last added row (visually bottom)
            self.update_total()

    def update_total(self):
        total = 0.0
        items_box = self.root.ids.items_box
        for item_row in items_box.children:
            try:
                qty = int(item_row.ids.item_qty.text)
                price = float(item_row.ids.item_price.text)
                total += qty * price
            except (ValueError, AttributeError):
                continue
        self.root.ids.total_price.text = f"{total:.2f}"

    def generate_invoice(self):
        root = self.root
        items = []
        items_box = root.ids.items_box
        for item_row in reversed(items_box.children):
            desc = item_row.ids.item_desc.text.strip()
            qty_text = item_row.ids.item_qty.text.strip()
            price_text = item_row.ids.item_price.text.strip()
            if desc and qty_text and price_text:
                try:
                    qty = int(qty_text)
                    price = float(price_text)
                    items.append({"desc": desc, "qty": qty, "price": price})
                except ValueError:
                    pass

        if not items:
            print("No valid items to invoice.")
            return

        company_name = root.ids.company_name.text.strip()
        customer_name = root.ids.customer_name.text.strip()
        customer_address = root.ids.customer_address.text.strip()
        message = root.ids.message.text.strip()
        email = root.ids.email.text.strip()

        inv = Invoice(
            customer_name=customer_name,
            address=customer_address,
            company_name=company_name,
            message=message,
            items=items
        )

        pdf_filename = f"{inv.id}.pdf"
        print(f"Generating PDF for Invoice ID: {inv.id}")

        create_invoice_pdf(
            company_name=company_name,
            customer_name=customer_name,
            customer_address=customer_address,
            items=items,
            message=message,
            invoice_id=inv.id,
        )

        print(f"Invoice {inv.id} generated successfully!")
        self.clear_form()

        if email:
            try:
                send_email_with_attachment(
                    to_email=email,
                    subject=f"Invoice from Quick Invoice: {inv.id}",
                    body="Please find your invoice attached.",
                    attachment_path=pdf_filename,
                )
                print(f"Invoice emailed to {email} successfully.")
            except Exception as e:
                print(f"Failed to send email: {e}")
        else:
            print("No email provided, skipping email sending.")


if __name__ == "__main__":
    InvoiceApp().run()
