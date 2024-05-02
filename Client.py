import tkinter as tk
from tkinter import ttk, messagebox
from DataManager import DataManager
class Client:
    """
    Class representing a client
    """
    def __init__(self, client_id, name, address, contact_details, budget):
        """
        initialize the Client object with provided attributes
        - ID for the client
        - name of the client
        - address of the client
        - contact details of the client
        - budget allocated for the client
        """
        self.client_id = client_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.budget = budget

    def display_details(self):
        """
         return a string representation of the client details
         """
        return f"Client ID: {self.client_id}\nName: {self.name}\nAddress: {self.address}\nContact Details: {self.contact_details}\nBudget: {self.budget}"

class ClientGUI:
    """
    Class representing the graphical user interface (GUI) for managing clients.
    """
    def __init__(self, root, data_manager):
        """
        Initialize the ClientGUI object
        - root window of the application
        - DataManager class for managing client data
        """
        self.root = root
        self.data_manager = data_manager

        # Define frames for organization
        entry_frame = tk.Frame(root) #frame for client details entry
        entry_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10) #grid placement for entry frame

        button_frame = tk.Frame(root) #frame for buttons
        button_frame.grid(row=1, column=0, sticky="ew", padx=10) #grid placement for button frame

        display_frame = tk.Frame(root) #frame for displaying client data
        display_frame.grid(row=2, column=0, sticky="nsew", padx=10)  #grid placement for display frame
        display_frame.grid_rowconfigure(0, weight=1) #configure row 0 to expand
        display_frame.grid_columnconfigure(0, weight=1) #configure column 0 to expand

        # Widgets for client details entry
        self.client_labels = ['Client ID', 'Name', 'Address', 'Contact Details', 'Budget']
        self.client_entries = {}
        for i, label in enumerate(self.client_labels):
            tk.Label(entry_frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(entry_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.client_entries[label] = entry

        # Buttons for various operations
        self.add_client_button = tk.Button(button_frame, text="Add Client", command=self.add_client)
        self.add_client_button.grid(row=0, column=0, padx=5, pady=5)

        self.modify_client_button = tk.Button(button_frame, text="Modify Client", command=self.modify_client)
        self.modify_client_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_client_button = tk.Button(button_frame, text="Delete Client", command=self.delete_client)
        self.delete_client_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_client_button = tk.Button(button_frame, text="Search by Client ID", command=self.search_client)
        self.search_client_button.grid(row=0, column=3, padx=5, pady=5)

        # Treeview with scrollbars for displaying client data
        self.client_tree = ttk.Treeview(display_frame, columns=self.client_labels, show='headings', height=5)
        vsb = ttk.Scrollbar(display_frame, orient="vertical", command=self.client_tree.yview)
        hsb = ttk.Scrollbar(display_frame, orient="horizontal", command=self.client_tree.xview)
        self.client_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.client_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Adjust column width as necessary and enable horizontal scrolling
        for label in self.client_labels:
            self.client_tree.heading(label, text=label)
            self.client_tree.column(label, width=120, anchor='w')

        self.refresh_client_list() #refresh the list of clients

    def add_client(self):
        """
        Add a new client to the data and refresh the list
        """
        client_data = {label: self.client_entries[label].get() for label in self.client_labels}
        client_id = len(self.data_manager.clients) + 1
        client = Client(client_id, client_data['Name'], client_data['Address'], client_data['Contact Details'], client_data['Budget'])
        self.data_manager.add_client(client)
        self.refresh_client_list()
        self.clear_client_form()
        messagebox.showinfo('Success', 'Added client successfully')

    def modify_client(self):
        """
        Modify the details of an existing client
        """
        selected_item = self.client_tree.selection()
        if selected_item:
            item_values = self.client_tree.item(selected_item, 'values')
            for label, entry in self.client_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, item_values[self.client_labels.index(label)])

    def save_client_changes(self):
        """
        Modify the details of an existing client
        """
        selected_item = self.client_tree.selection()
        if selected_item:
            item_values = {label: self.client_entries[label].get() for label in self.client_labels}
            updated_client = Client(item_values['Client ID'], item_values['Name'], item_values['Address'], item_values['Contact Details'], item_values['Budget'])
            self.data_manager.update_client(updated_client)
            self.refresh_client_list()
            messagebox.showinfo('Success', 'Client details updated successfully')

    def delete_client(self):
        """
        Delete the selected client from the data and refresh the list
        """
        selected_item = self.client_tree.selection()
        if selected_item:
            client_id = self.client_tree.item(selected_item, 'values')[0]
            self.data_manager.delete_client(client_id)
            self.refresh_client_list()
            messagebox.showinfo('Success', 'Client deleted successfully')

    def search_client(self):
        """
        Search for a client by client ID
        """
        keyword = self.client_entries['Client ID'].get()
        results = self.data_manager.search_clients(keyword)
        self.refresh_client_list(results)

    def refresh_client_list(self, clients=None):
        """
        refresh the displayed list of clients
        - list of clients to display
        """
        self.client_tree.delete(*self.client_tree.get_children())
        clients = clients or self.data_manager.clients
        for client in clients:
            values = [getattr(client, label.lower().replace(" ", "_"), "") for label in self.client_labels]
            self.client_tree.insert('', 'end', values=values)
    def clear_client_form(self):
        """
        clear the client details entry form
        """
        for entry in self.client_entries.values():
            entry.delete(0, tk.END)