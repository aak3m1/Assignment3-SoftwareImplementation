import tkinter as tk
from tkinter import ttk, messagebox
from DataManager import DataManager

class Employee:
    def __init__(self, name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details):
        self.name = name
        self.employee_id = employee_id
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.age = age
        self.date_of_birth = date_of_birth
        self.passport_details = passport_details

    def display_details(self):
        return f"ID: {self.id}\nName: {self.name}\nEmployee ID: {self.employee_id}\nDepartment: {self.department}\nJob Title: {self.job_title}\nBasic Salary: {self.basic_salary}\nAge: {self.age}\nDate of Birth: {self.date_of_birth}\nPassport Details: {self.passport_details}"


class SalesManager(Employee):
    def __init__(self, id, name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details):
        super().__init__(id, name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details)
    def manage_clients(self):
        # Placeholder for managing clients
        return "Sales Manager managing clients."
    def manage_events(self):
        # Placeholder for managing events
        return "Sales Manager managing events."


class Salesperson(Employee):
    def __init__(self, id, name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details, sales_target):
        super().__init__(id, name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details)
        self.sales_target = sales_target
    def record_sale(self):
        # Placeholder for recording sales
        return "Salesperson recording sale."


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
        print(employee_data)  # Print employee_data for debugging
        employee = Employee(*employee_data.values())
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
        return label.lower().replace(" ", "_")

