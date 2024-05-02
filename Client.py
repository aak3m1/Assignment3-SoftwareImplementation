class Client:
    def __init__(self, client_id, name, address, contact_details, budget):
        self.client_id = client_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.budget = budget

    def display_details(self):
        return f"Client ID: {self.client_id}\nName: {self.name}\nAddress: {self.address}\nContact Details: {self.contact_details}\nBudget: {self.budget}"
