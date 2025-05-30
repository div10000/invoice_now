import uuid
class Invoice:
    def __init__(self, customer_name, address, item_desc, qty, price):
        self.customer_name = customer_name
        self.address = address
        self.item_desc = item_desc
        try:
            self.qty = int(qty)
        except ValueError:
            self.qty = 0
        try:
            self.price = float(price)
        except ValueError:
            self.price = 0.0
        
        # Generate a unique ID for the invoice
        self.id = str(uuid.uuid4())[:8]  # short 8-character unique string

    def total(self):
        return self.qty * self.price
