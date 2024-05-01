import tkinter as tk
from tkinter import ttk, messagebox
from DataManager import DataManager
from Employee import Employee
from Event import Event

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Best Events Company Management System")

        self.tab_control = ttk.Notebook(root)

        self.employee_tab = ttk.Frame(self.tab_control)
        self.event_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.employee_tab, text='Employees')
        self.tab_control.add(self.event_tab, text='Events')

        self.data_manager = DataManager()
        self.employee_gui = EmployeeGUI(self.employee_tab, self.data_manager)
        self.event_gui = EventGUI(self.event_tab, self.data_manager)

        self.tab_control.pack(expand=1, fill="both")

class EmployeeGUI:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager

        entry_frame = tk.Frame(root)
        entry_frame.grid(row=0, column=0, sticky="ew")

        button_frame = tk.Frame(root)
        button_frame.grid(row=1, column=0, sticky="ew")

        display_frame = tk.Frame(root)
        display_frame.grid(row=2, column=0, sticky="nsew")

        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Widgets for employee details entry
        self.labels = ['Name', 'Employee ID', 'Department', 'Job Title', 'Basic Salary', 'Age', 'Date of Birth', 'Passport Details']
        self.entries = {}
        for i, label in enumerate(self.labels):
            tk.Label(entry_frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(entry_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.entries[label] = entry

        self.add_button = tk.Button(button_frame, text="Add Employee", command=self.add_employee)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.modify_button = tk.Button(button_frame, text="Modify Employee", command=self.modify_employee)
        self.modify_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(button_frame, text="Delete Employee", command=self.delete_employee)
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_button = tk.Button(button_frame, text="Search by ID", command=self.search_employee)
        self.search_button.grid(row=0, column=3, padx=5, pady=5)

        self.employee_tree = ttk.Treeview(display_frame, columns=self.labels, show='headings', height=5)
        vsb = ttk.Scrollbar(display_frame, orient="vertical", command=self.employee_tree.yview)
        hsb = ttk.Scrollbar(display_frame, orient="horizontal", command=self.employee_tree.xview)
        self.employee_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.employee_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        for label in self.labels:
            self.employee_tree.heading(label, text=label)
            self.employee_tree.column(label, width=100, anchor='w')
        self.refresh_employee_list()



    def add_employee(self):
        employee_data = {label: entry.get() for label, entry in self.entries.items()}
        id = len(self.data_manager.employees)
        print(employee_data)
        employee = Employee(id, employee_data['Name'], employee_data['Employee ID'], employee_data['Department'], employee_data['Job Title'], employee_data['Basic Salary'], employee_data['Age'], employee_data['Date of Birth'], employee_data['Passport Details'])
        self.data_manager.add_employee(employee)
        self.refresh_employee_list()
        self.clear_employee_form()
        messagebox.showinfo('Success', 'Added employee successfully')

    def clear_employee_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def modify_employee(self):
        selected_item = self.employee_tree.selection()
        if selected_item:
            item_values = self.employee_tree.item(selected_item, 'values')
            for label, entry in self.entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, item_values[self.labels.index(label)])

    def save_employee_changes(self):
        selected_item = self.employee_tree.selection()
        if selected_item:
            item_values = [entry.get() for entry in self.entries.values()]
            employee = Employee(*item_values)
            self.data_manager.update_employee(employee)
            self.refresh_employee_list()
            messagebox.showinfo('Success', 'Employee details updated successfully')

    def delete_employee(self):
        selected_item = self.employee_tree.selection()
        if selected_item:
            item_values = self.employee_tree.item(selected_item, 'values')
            employee_id = item_values[1]  # Adjust index based on your setup
            print(f"Attempting to delete employee ID: {employee_id}")

            # Call delete on DataManager with appropriate type handling
            self.data_manager.delete_employee(str(employee_id))  # or int(employee_id), depending on how IDs are stored
            self.refresh_employee_list()
            messagebox.showinfo('Success', 'Deleted employee successfully')
            print(f"Employee {employee_id} deleted. Refreshing list.")

    def search_employee(self):
        keyword = self.entries['Employee ID'].get()
        results = self.data_manager.search_employees(keyword)
        self.refresh_employee_list(results)

    def refresh_employee_list(self, employees=None):
        for i in self.employee_tree.get_children():
            self.employee_tree.delete(i)
        if employees is None:
            employees = self.data_manager.employees
        for employee in employees:
            values = [getattr(employee, self.convert_label_to_attribute(attr)) for attr in self.labels]
            self.employee_tree.insert('', 'end', values=values)

    def convert_label_to_attribute(self, label):
        return label.lower().replace(" ", "_")
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

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
