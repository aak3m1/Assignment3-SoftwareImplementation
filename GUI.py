import tkinter as tk
from tkinter import ttk, messagebox
from DataManager import DataManager
from Employee import Employee

class EmployeeGUI:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        self.root.title("Employee Management System")

        # Widgets for employee details entry
        self.labels = ['Name', 'Employee ID', 'Department', 'Job Title', 'Basic Salary', 'Age', 'Date of Birth', 'Passport Details']
        self.entries = {}
        for i, label in enumerate(self.labels):
            tk.Label(root, text=label + ":").grid(row=i, column=0)
            entry = tk.Entry(root)
            entry.grid(row=i, column=1)
            self.entries[label] = entry

        # Buttons
        self.add_button = tk.Button(root, text="Add Employee", command=self.add_employee)
        self.add_button.grid(row=len(self.labels), columnspan=2)

        self.modify_button = tk.Button(root, text="Modify Employee", command=self.modify_employee)
        self.modify_button.grid(row=len(self.labels)+1, column=0)

        self.delete_button = tk.Button(root, text="Delete Employee", command=self.delete_employee)
        self.delete_button.grid(row=len(self.labels)+1, column=1)

        self.search_button = tk.Button(root, text="Search by ID", command=self.search_employee)
        self.search_button.grid(row=len(self.labels), column=0)

        # Treeview to display employees
        self.employee_tree = ttk.Treeview(root, columns=self.labels, show='headings')
        for label in self.labels:
            self.employee_tree.heading(label, text=label)
        self.employee_tree.grid(row=len(self.labels)+2, columnspan=2)

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
            employee_id = item_values[self.labels.index('Employee ID')]
            self.data_manager.delete_employee(employee_id)
            self.refresh_employee_list()
            messagebox.showinfo('Success', 'Deleted employee successfully')

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
	    return label.lower().replace(" ", "_")  # This converts 'Employee ID' to 'employee_id'
if __name__ == "__main__":
    root =tk.Tk()
    data_manager = DataManager()
    app = EmployeeGUI(root, data_manager)
    root.mainloop()
