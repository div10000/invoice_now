import uuid

class Invoice:
    def __init__(self, customer_name, address, company_name=None, message=None, items=None):
        self.customer_name = customer_name
        self.address = address
        self.company_name = company_name
        self.message = message
        self.items = items or []  # list of dicts with keys: desc, qty, price
        
        # Generate a unique ID for the invoice
        self.id = str(uuid.uuid4())[:8]

    def total(self):
        # Sum total for all items
        return sum(item['qty'] * item['price'] for item in self.items)
