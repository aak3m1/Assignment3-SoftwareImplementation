import tkinter as tk
from tkinter import ttk, messagebox
from DataManager import DataManager
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



class EventGUI:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager

        # Define frames
        entry_frame = tk.Frame(root)
        entry_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        button_frame = tk.Frame(root)
        button_frame.grid(row=1, column=0, sticky="ew", padx=10)

        display_frame = tk.Frame(root)
        display_frame.grid(row=2, column=0, sticky="nsew", padx=10)
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

        # Widgets for event details entry
        self.event_labels = ['Event ID', 'Type', 'Theme', 'Date', 'Time', 'Duration', 'Venue', 'Client ID', 'Guest List', 'Suppliers', 'Invoice']
        self.event_entries = {}
        for i, label in enumerate(self.event_labels):
            tk.Label(entry_frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(entry_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.event_entries[label] = entry

        # Buttons
        self.add_event_button = tk.Button(button_frame, text="Add Event", command=self.add_event)
        self.add_event_button.grid(row=0, column=0, padx=5, pady=5)

        self.modify_event_button = tk.Button(button_frame, text="Modify Event", command=self.modify_event)
        self.modify_event_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_event_button = tk.Button(button_frame, text="Delete Event", command=self.delete_event)
        self.delete_event_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_event_button = tk.Button(button_frame, text="Search by Event ID", command=self.search_event)
        self.search_event_button.grid(row=0, column=3, padx=5, pady=5)

        # Treeview with scrollbars
        self.event_tree = ttk.Treeview(display_frame, columns=self.event_labels, show='headings', height=5)
        vsb = ttk.Scrollbar(display_frame, orient="vertical", command=self.event_tree.yview)
        hsb = ttk.Scrollbar(display_frame, orient="horizontal", command=self.event_tree.xview)
        self.event_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.event_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Adjust column width as necessary and enable horizontal scrolling
        for label in self.event_labels:
            self.event_tree.heading(label, text=label)
            self.event_tree.column(label, width=120, anchor='w')

        self.refresh_event_list()

    def add_event(self):
        event_data = {label: self.event_entries[label].get() for label in self.event_labels}
        event_id = len(self.data_manager.events) + 1
        suppliers_list = event_data['Suppliers'].split(',')
        suppliers_dict = {item.split('=')[0]: item.split('=')[1] for item in suppliers_list if
                          '=' in item and len(item.split('=')) == 2}
        event = Event(event_id, event_data['Type'], event_data['Theme'], event_data['Date'], event_data['Time'],
                      event_data['Duration'],
                      event_data['Venue'], event_data['Client ID'], event_data['Guest List'].split(','), suppliers_dict,
                      event_data['Invoice'])
        self.data_manager.add_event(event)
        self.refresh_event_list()
        self.clear_event_form()
        messagebox.showinfo('Success', 'Added event successfully')

    def modify_event(self):
        selected_item = self.event_tree.selection()
        if selected_item:
            item_values = self.event_tree.item(selected_item, 'values')
            for label, entry in self.event_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, item_values[self.event_labels.index(label)])

    def save_event_changes(self):
        selected_item = self.event_tree.selection()
        if selected_item:
            item_values = {label: self.event_entries[label].get() for label in self.event_labels}
            updated_event = Event(item_values['Event ID'], item_values['Type'], item_values['Theme'],
                                  item_values['Date'], item_values['Time'], item_values['Duration'], item_values['Venue'],
                                  item_values['Client ID'], item_values['Guest List'].split(','),
                                  dict(item.split('=') for item in item_values['Suppliers'].split(',')), item_values['Invoice'])
            self.data_manager.update_event(updated_event)
            self.refresh_event_list()
            messagebox.showinfo('Success', 'Event details updated successfully')

    def delete_event(self):
        selected_item = self.event_tree.selection()
        if selected_item:
            event_id = self.event_tree.item(selected_item, 'values')[0]  # assuming the first value is the event ID
            self.data_manager.delete_event(int(event_id))
            self.refresh_event_list()
            messagebox.showinfo('Success', 'Deleted event successfully')
    def search_event(self):
        keyword = self.event_entries['Event ID'].get()
        results = self.data_manager.search_events(keyword)
        self.refresh_event_list(results)

    def refresh_event_list(self, events=None):
        self.event_tree.delete(*self.event_tree.get_children())
        events = events or self.data_manager.events
        for event in events:
            values = []
            for label in self.event_labels:
                attr = label.lower().replace(" ", "_")
                if attr == 'type':  # Special handling for 'Type' which corresponds to 'event_type'
                    attr = 'event_type'
                values.append(getattr(event, attr, ""))  # Use getattr safely with a default
            self.event_tree.insert('', 'end', values=values)

    def clear_event_form(self):
        for entry in self.event_entries.values():
            entry.delete(0, tk.END)