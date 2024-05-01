import pickle
class DataManager:
    def __init__(self):
        self.employees = self.load_data('employees.pkl')
        self.events = self.load_data('events.pkl')

    def load_data(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
        except (FileNotFoundError, EOFError):
            data = []
        return data

    def save_data(self, data, filename):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def add_employee(self, employee):
        self.employees.append(employee)
        self.save_data(self.employees, 'employees.pkl')

    def add_event(self, event):
        self.events.append(event)
        self.save_data(self.events, 'events.pkl')

    def delete_employee(self, employee_id):
        employee_id = int(employee_id)
        self.employees = [emp for emp in self.employees if str(emp.employee_id) != str(employee_id)]
        self.save_data(self.employees, 'employees.pkl')
        print(f"Employees after deletion: {[emp.employee_id for emp in self.employees]}")

    def delete_event(self, event_id):
        self.events = [event for event in self.events if event.event_id != event_id]
        self.save_data(self.events, 'events.pkl')

    def search_events(self, keyword):
        try:
            keyword = int(keyword)
            return [event for event in self.events if event.event_id == keyword]
        except ValueError:
            return []

    def refresh_employee_list(self):
        self.employee_tree.delete(*self.employee_tree.get_children())
        for employee in self.data_manager.employees:
            values = [getattr(employee, attr) for attr in self.labels]
            self.employee_tree.insert('', 'end', values=values)