from pdf_generator import create_invoice_pdf
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from invoice import Invoice  # Importing the Invoice class
from email_sender import send_email_with_attachment
from kivy.core.window import Window

# Set app icon (make sure 'icon.png' exists in the root folder)
Window.set_icon('icon.png')

Builder.load_file("ui.kv")  # Load the KV layout file


class MainWidget(BoxLayout):
    pass


class InvoiceLayout(BoxLayout):  # matches <InvoiceLayout> in KV
    pass


class InvoiceApp(App):
    def build(self):
        self.title = "Invoice Now"  # Set window title
        return InvoiceLayout()

    def clear_form(self):
        root = self.root
        root.ids.customer_name.text = ''
        root.ids.customer_address.text = ''
        root.ids.item_desc.text = ''
        root.ids.item_qty.text = ''
        root.ids.item_price.text = ''
        root.ids.email.text = ''

    def generate_invoice(self):
        root = self.root
        inv = Invoice(
            customer_name=root.ids.customer_name.text,
            address=root.ids.customer_address.text,
            item_desc=root.ids.item_desc.text,
            qty=root.ids.item_qty.text,
            price=root.ids.item_price.text,
        )
        email = root.ids.email.text
        pdf_filename = f"{inv.id}.pdf"

        print(f"Generating PDF for Invoice ID: {inv.id}")
        create_invoice_pdf(
            inv.customer_name,
            inv.address,
            inv.item_desc,
            inv.qty,
            inv.price,
            inv.id
        )
        print(f"Invoice {inv.id} generated successfully!")

        # Clear form fields
        self.clear_form()

        # Send email if provided
        if email:
            try:
                send_email_with_attachment(
                    to_email=email,
                    subject=f"Invoice from Quick Invoice: {inv.id}",
                    body="Please find your invoice attached.",
                    attachment_path=pdf_filename
                )
                print(f"Invoice emailed to {email} successfully.")
            except Exception as e:
                print(f"Failed to send email: {e}")
        else:
            print("No email provided, skipping email sending.")


if __name__ == "__main__":
    InvoiceApp().run()
