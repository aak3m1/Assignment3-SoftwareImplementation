class Event:
    def __init__(self, event_id, event_type, theme, date, time, duration, venue, client_id, guest_list, suppliers, invoice):
        self.event_id = event_id
        self.event_type = event_type
        self.theme = theme
        self.date = date
        self.time = time
        self.duration = duration
        self.venue = venue
        self.client_id = client_id
        self.guest_list = guest_list
        self.suppliers = suppliers
        self.invoice = invoice

    def display_details(self):
        details = f"Event ID: {self.event_id}\nType: {self.event_type}\nTheme: {self.theme}\nDate: {self.date}\nTime: {self.time}\n"
        details += f"Duration: {self.duration} hours\nVenue: {self.venue}\nClient ID: {self.client_id}\nGuests: {len(self.guest_list)}\n"
        details += "Suppliers:\n"
        for key, value in self.suppliers.items():
            details += f"{key}: {value}\n"
        details += f"Invoice Total: {self.invoice}"
        return details
