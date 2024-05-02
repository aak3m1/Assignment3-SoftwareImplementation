import tkinter as tk
from tkinter import ttk, messagebox
from DataManager import DataManager
class Suppliers:
    def __init__(self, supplier_id, name, address, contact_details, service_type):
        self.supplier_id = supplier_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.service_type = service_type  # e.g., 'Catering', 'Cleaning', 'Furniture', 'Decorations'

    def display_details(self):
        return (f"Supplier ID: {self.supplier_id}\n"
                f"Name: {self.name}\n"
                f"Address: {self.address}\n"
                f"Contact Details: {self.contact_details}\n"
                f"Service Type: {self.service_type}\n")

class SupplierGUI:
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

        # Widgets for supplier details entry
        self.supplier_labels = ['Supplier ID', 'Name', 'Address', 'Contact Details', 'Service Type']
        self.supplier_entries = {}
        for i, label in enumerate(self.supplier_labels):
            tk.Label(entry_frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(entry_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.supplier_entries[label] = entry

        # Buttons
        self.add_supplier_button = tk.Button(button_frame, text="Add Supplier", command=self.add_supplier)
        self.add_supplier_button.grid(row=0, column=0, padx=5, pady=5)

        self.modify_supplier_button = tk.Button(button_frame, text="Modify Supplier", command=self.modify_supplier)
        self.modify_supplier_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_supplier_button = tk.Button(button_frame, text="Delete Supplier", command=self.delete_supplier)
        self.delete_supplier_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_supplier_button = tk.Button(button_frame, text="Search by Supplier ID", command=self.search_supplier)
        self.search_supplier_button.grid(row=0, column=3, padx=5, pady=5)

        # Treeview with scrollbars
        self.supplier_tree = ttk.Treeview(display_frame, columns=self.supplier_labels, show='headings', height=5)
        vsb = ttk.Scrollbar(display_frame, orient="vertical", command=self.supplier_tree.yview)
        hsb = ttk.Scrollbar(display_frame, orient="horizontal", command=self.supplier_tree.xview)
        self.supplier_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.supplier_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Adjust column width as necessary and enable horizontal scrolling
        for label in self.supplier_labels:
            self.supplier_tree.heading(label, text=label)
            self.supplier_tree.column(label, width=120, anchor='w')

        self.refresh_supplier_list()

    def add_supplier(self):
        supplier_data = {label: self.supplier_entries[label].get() for label in self.supplier_labels}
        supplier_id = len(self.data_manager.suppliers) + 1
        supplier = Suppliers(supplier_id, supplier_data['Name'], supplier_data['Address'],
                             supplier_data['Contact Details'], supplier_data['Service Type'])

        self.data_manager.add_supplier(supplier)
        self.refresh_supplier_list()
        self.clear_supplier_form()
        messagebox.showinfo('Success', 'Added supplier successfully')

    def modify_supplier(self):
        selected_item = self.supplier_tree.selection()
        if selected_item:
            item_values = self.supplier_tree.item(selected_item, 'values')
            for label, entry in self.supplier_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, item_values[self.supplier_labels.index(label)])

    def delete_supplier(self):
        selected_item = self.supplier_tree.selection()
        if selected_item:
            supplier_id = self.supplier_tree.item(selected_item, 'values')[0]
            self.data_manager.delete_supplier(supplier_id)
            self.supplier_tree.delete(selected_item)  # Remove the selected item from the tree
            messagebox.showinfo('Success', 'Deleted supplier successfully')

    def search_supplier(self):
        keyword = self.supplier_entries['Supplier ID'].get()
        results = self.data_manager.search_suppliers(keyword)
        self.refresh_supplier_list(results)

    def refresh_supplier_list(self, suppliers=None):
        self.supplier_tree.delete(*self.supplier_tree.get_children())
        suppliers = suppliers or self.data_manager.suppliers
        for supplier in suppliers:
            values = [supplier.supplier_id, supplier.name, supplier.address, supplier.contact_details, supplier.service_type]
            self.supplier_tree.insert('', 'end', values=values)

    def clear_supplier_form(self):
        for entry in self.supplier_entries.values():
            entry.delete(0, tk.END)
