import tkinter as tk
from tkinter import ttk, messagebox
from DataManager import DataManager
class Client:
    def __init__(self, client_id, name, address, contact_details, budget):
        self.client_id = client_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.budget = budget

    def display_details(self):
        return f"Client ID: {self.client_id}\nName: {self.name}\nAddress: {self.address}\nContact Details: {self.contact_details}\nBudget: {self.budget}"

class ClientGUI:
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

        # Widgets for client details entry
        self.client_labels = ['Client ID', 'Name', 'Address', 'Contact Details', 'Budget']
        self.client_entries = {}
        for i, label in enumerate(self.client_labels):
            tk.Label(entry_frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(entry_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.client_entries[label] = entry

        # Buttons
        self.add_client_button = tk.Button(button_frame, text="Add Client", command=self.add_client)
        self.add_client_button.grid(row=0, column=0, padx=5, pady=5)

        self.modify_client_button = tk.Button(button_frame, text="Modify Client", command=self.modify_client)
        self.modify_client_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_client_button = tk.Button(button_frame, text="Delete Client", command=self.delete_client)
        self.delete_client_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_client_button = tk.Button(button_frame, text="Search by Client ID", command=self.search_client)
        self.search_client_button.grid(row=0, column=3, padx=5, pady=5)

        # Treeview with scrollbars
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

        self.refresh_client_list()

    def add_client(self):
        client_data = {label: self.client_entries[label].get() for label in self.client_labels}
        client_id = len(self.data_manager.clients) + 1
        client = Client(client_id, client_data['Name'], client_data['Address'], client_data['Contact Details'], client_data['Budget'])
        self.data_manager.add_client(client)
        self.refresh_client_list()
        self.clear_client_form()
        messagebox.showinfo('Success', 'Added client successfully')

    def modify_client(self):
        selected_item = self.client_tree.selection()
        if selected_item:
            item_values = self.client_tree.item(selected_item, 'values')
            for label, entry in self.client_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, item_values[self.client_labels.index(label)])

    def save_client_changes(self):
        selected_item = self.client_tree.selection()
        if selected_item:
            item_values = {label: self.client_entries[label].get() for label in self.client_labels}
            updated_client = Client(item_values['Client ID'], item_values['Name'], item_values['Address'], item_values['Contact Details'], item_values['Budget'])
            self.data_manager.update_client(updated_client)
            self.refresh_client_list()
            messagebox.showinfo('Success', 'Client details updated successfully')

    def delete_client(self):
        selected_item = self.client_tree.selection()
        if selected_item:
            client_id = self.client_tree.item(selected_item, 'values')[0]
            self.data_manager.delete_client(client_id)
            self.refresh_client_list()
            messagebox.showinfo('Success', 'Client deleted successfully')

    def search_client(self):
        keyword = self.client_entries['Client ID'].get()
        results = self.data_manager.search_clients(keyword)
        self.refresh_client_list(results)

    def refresh_client_list(self, clients=None):
        self.client_tree.delete(*self.client_tree.get_children())
        clients = clients or self.data_manager.clients
        for client in clients:
            values = [getattr(client, label.lower().replace(" ", "_"), "") for label in self.client_labels]
            self.client_tree.insert('', 'end', values=values)

    def clear_client_form(self):
        for entry in self.client_entries.values():
            entry.delete(0, tk.END)

