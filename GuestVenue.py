import tkinter as tk
from tkinter import ttk, messagebox
from DataManager import DataManager
class Guest:
    """
    Class representing a guest
    """
    def __init__(self, guest_id, name, address, contact_details):
        """
        Initialize the Guest object with provided attributes
        Parameters:
        - ID for the guest
        - Name of the guest
        - address of the guest
        - contact  details of the guest
        """
        self.guest_id = guest_id
        self.name = name
        self.address = address
        self.contact_details = contact_details

class GuestGUI:
    """
    Class representing the (GUI) for managing guests
    """
    def __init__(self, root, data_manager):
        """
        Initialize the GuestGUI object
        - root window of the application
        - DataManager class for managing guest data.
        """
        self.root = root
        self.data_manager = data_manager

        # Define frames for organization
        entry_frame = tk.Frame(root)  #frame for guest details entry
        entry_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10) #grid placement for entry frame

        button_frame = tk.Frame(root) #frame for buttons
        button_frame.grid(row=1, column=0, sticky="ew", padx=10)  #grid placement for button frame

        display_frame = tk.Frame(root)  #frame for displaying guest data
        display_frame.grid(row=2, column=0, sticky="nsew", padx=10) #grid placement for display frame
        display_frame.grid_rowconfigure(0, weight=1) #configure row 0 to expand
        display_frame.grid_columnconfigure(0, weight=1) #configure column 0 to expand

        # Widgets for guest details entry
        self.guest_labels = ['Guest ID', 'Name', 'Address', 'Contact Details']
        self.guest_entries = {}
        for i, label in enumerate(self.guest_labels):
            tk.Label(entry_frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(entry_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.guest_entries[label] = entry

        #buttons for various operations
        self.add_guest_button = tk.Button(button_frame, text="Add Guest", command=self.add_guest)
        self.add_guest_button.grid(row=0, column=0, padx=5, pady=5)

        self.modify_guest_button = tk.Button(button_frame, text="Modify Guest", command=self.modify_guest)
        self.modify_guest_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_guest_button = tk.Button(button_frame, text="Delete Guest", command=self.delete_guest)
        self.delete_guest_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_guest_button = tk.Button(button_frame, text="Search by Guest ID", command=self.search_guest)
        self.search_guest_button.grid(row=0, column=3, padx=5, pady=5)

        # Treeview with scrollbars for displaying guest data
        self.guest_tree = ttk.Treeview(display_frame, columns=self.guest_labels, show='headings', height=5)
        vsb = ttk.Scrollbar(display_frame, orient="vertical", command=self.guest_tree.yview)
        hsb = ttk.Scrollbar(display_frame, orient="horizontal", command=self.guest_tree.xview)
        self.guest_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.guest_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Adjust column width as necessary and enable horizontal scrolling
        for label in self.guest_labels:
            self.guest_tree.heading(label, text=label)
            self.guest_tree.column(label, width=120, anchor='w')

        self.refresh_guest_list() # Refresh the list of guests

    def add_guest(self):
        """
        Add a new guest to the data and refresh the list
        """
        guest_data = {label: self.guest_entries[label].get() for label in self.guest_labels}
        guest_id = len(self.data_manager.guests) + 1
        guest = Guest(guest_id, guest_data['Name'], guest_data['Address'], guest_data['Contact Details'])
        self.data_manager.add_guest(guest)
        self.refresh_guest_list()
        self.clear_guest_form()
        messagebox.showinfo('Success', 'Added guest successfully')

    def modify_guest(self):
        """
        Modify the details of an existing guest
        """
        selected_item = self.guest_tree.selection()
        if selected_item:
            item_values = self.guest_tree.item(selected_item, 'values')
            for label, entry in self.guest_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, item_values[self.guest_labels.index(label)])

    def delete_guest(self):
        """
        Delete the selected guest from the data and refresh the list
        """
        selected_item = self.guest_tree.selection()
        if selected_item:
            item_values = self.guest_tree.item(selected_item, 'values')
            guest_id = item_values[0]  #assuming the guest ID is the first column in the Treeview
            self.data_manager.delete_guest(guest_id)
            self.guest_tree.delete(selected_item)  #remove the selected item from the tree
            messagebox.showinfo('Success', 'Deleted guest successfully')

    def search_guest(self):
        """
        Search for a guest by guest ID.
        """
        keyword = self.guest_entries['Guest ID'].get()
        results = self.data_manager.search_guests(keyword)
        self.refresh_guest_list(results)

    def refresh_guest_list(self, guests=None):
        """
        Refresh the displayed list of guests
        - List of guests to display
        """
        self.guest_tree.delete(*self.guest_tree.get_children())
        guests = guests or self.data_manager.guests
        for guest in guests:
            values = [guest.guest_id, guest.name, guest.address, guest.contact_details]  # Include email
            self.guest_tree.insert('', 'end', values=values)

    def clear_guest_form(self):
        """
        Clear the guest details entry form
        """
        for entry in self.guest_entries.values():
            entry.delete(0, tk.END)


class Venue:
    """
    Class representing a venue
    """
    def __init__(self, venue_id, name, address, contact, min_guests, max_guests):
        """
        Initialize the Venue object with provided attributes.
        - ID for the venue
        - name of the venue
        - address of the venue
        - contact details of the venue
        - minimum number of guests the venue can accommodate
        - maximum number of guests the venue can accommodate
        """
        self.venue_id = venue_id
        self.name = name
        self.address = address
        self.contact = contact
        self.min_guests = min_guests
        self.max_guests = max_guests

    def display_details(self):
        """
        Return a string representation of the venue details
        """
        return (f"Venue ID: {self.venue_id}\nName: {self.name}\nAddress: {self.address}\n"
                f"Contact: {self.contact}\nMin Guests: {self.min_guests}\nMax Guests: {self.max_guests}")
class VenueGUI:
    """
    Class representing the (GUI) for managing venues.
    """
    def __init__(self, root, data_manager):
        """
        initialize the VenueGUI object
        - root window of the application
        - DataManager class for managing venue data
        """
        self.root = root
        self.data_manager = data_manager

        # Define frames for organization
        entry_frame = tk.Frame(root) #frame for venue details entry
        entry_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10) #grid placement for entry frame

        button_frame = tk.Frame(root) #frame for buttons
        button_frame.grid(row=1, column=0, sticky="ew", padx=10)  #grid placement for button frame

        display_frame = tk.Frame(root)  #frame for displaying venue data
        display_frame.grid(row=2, column=0, sticky="nsew", padx=10) #grid placement for display frame
        display_frame.grid_rowconfigure(0, weight=1)  #configure row 0 to expand
        display_frame.grid_columnconfigure(0, weight=1)  #configure column 0 to expand

        # Widgets for venue details entry
        self.venue_labels = ['Venue ID', 'Name', 'Address', 'Contact', 'Min Guests', 'Max Guests']
        self.venue_entries = {}
        for i, label in enumerate(self.venue_labels):
            tk.Label(entry_frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(entry_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.venue_entries[label] = entry

        # Buttons for various operations
        self.add_venue_button = tk.Button(button_frame, text="Add Venue", command=self.add_venue)
        self.add_venue_button.grid(row=0, column=0, padx=5, pady=5)

        self.modify_venue_button = tk.Button(button_frame, text="Modify Venue", command=self.modify_venue)
        self.modify_venue_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_venue_button = tk.Button(button_frame, text="Delete Venue", command=self.delete_venue)
        self.delete_venue_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_venue_button = tk.Button(button_frame, text="Search by Venue ID", command=self.search_venue)
        self.search_venue_button.grid(row=0, column=3, padx=5, pady=5)

        # Treeview with scrollbars for displaying venue data
        self.venue_tree = ttk.Treeview(display_frame, columns=self.venue_labels, show='headings', height=5)
        vsb = ttk.Scrollbar(display_frame, orient="vertical", command=self.venue_tree.yview)
        hsb = ttk.Scrollbar(display_frame, orient="horizontal", command=self.venue_tree.xview)
        self.venue_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.venue_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Adjust column width as necessary and enable horizontal scrolling
        for label in self.venue_labels:
            self.venue_tree.heading(label, text=label)
            self.venue_tree.column(label, width=120, anchor='w')

        self.refresh_venue_list()

    def add_venue(self):
        """
        Add a new venue to the data and refresh the list
        """
        venue_data = {label: self.venue_entries[label].get() for label in self.venue_labels}
        venue_id = len(self.data_manager.venues) + 1
        venue = Venue(venue_id, venue_data['Name'], venue_data['Address'], venue_data['Contact'],
                      int(venue_data['Min Guests']), int(venue_data['Max Guests']))

        self.data_manager.add_venue(venue)
        self.refresh_venue_list()
        self.clear_venue_form()
        messagebox.showinfo('Success', 'Added venue successfully')

    def modify_venue(self):
        """
        Modify the details of an existing venue
        """
        selected_item = self.venue_tree.selection()
        if selected_item:
            item_values = self.venue_tree.item(selected_item, 'values')
            for label, entry in self.venue_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, item_values[self.venue_labels.index(label)])

    def delete_venue(self):
        """
        Delete the selected venue from the data and refresh the list
        """
        selected_item = self.venue_tree.selection()
        if selected_item:
            venue_id = self.venue_tree.item(selected_item, 'values')[0]
            self.data_manager.delete_venue(venue_id)
            self.venue_tree.delete(selected_item)  #remove the selected item from the tree
            messagebox.showinfo('Success', 'Deleted venue successfully')

    def search_venue(self):
        """
        Search for a venue by venue ID
        """
        keyword = self.venue_entries['Venue ID'].get()
        results = self.data_manager.search_venues(keyword)
        self.refresh_venue_list(results)

    def refresh_venue_list(self, venues=None):
        """
        refresh the displayed list of venues
        - list of venues to display.
        """
        self.venue_tree.delete(*self.venue_tree.get_children())
        venues = venues or self.data_manager.venues
        print("Refreshing list, current venues:", [v.venue_id for v in venues])  # Debug: print current venues
        for venue in venues:
            values = [venue.venue_id, venue.name, venue.address, venue.contact, venue.min_guests, venue.max_guests]
            self.venue_tree.insert('', 'end', values=values)
    def clear_venue_form(self):
        """
        Clear the venue details entry form.
        """
        for entry in self.venue_entries.values():
            entry.delete(0, tk.END)
