import pickle
class DataManager:
    def __init__(self):
        self.employees = self.load_data('employees.pkl')
        self.events = self.load_data('events.pkl')
        self.clients = self.load_data('clients.pkl')

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

    def load_employees(self):
        try:
            with open('employees.pkl', 'rb') as f:
                employees = pickle.load(f)
        except (FileNotFoundError, EOFError):
            employees = []
        return employees

    def save_employees(self):
        with open('employees.pkl', 'wb') as f:
            pickle.dump(self.employees, f)

    def add_employee(self, employee):
        self.employees.append(employee)
        self.save_employees()

    def get_employee_by_id(self, employee_id):
        return next((emp for emp in self.employees if emp.employee_id == employee_id), None)

    def update_employee(self, updated_employee):
        for emp in self.employees:
            if emp.employee_id == updated_employee.employee_id:
                emp.name = updated_employee.name
                emp.department = updated_employee.department
                emp.job_title = updated_employee.job_title
                emp.basic_salary = updated_employee.basic_salary
                emp.age = updated_employee.age
                emp.date_of_birth = updated_employee.date_of_birth
                emp.passport_details = updated_employee.passport_details
                self.save_employees()
                break

    def delete_employee(self, employee_id):
        self.employees = [emp for emp in self.employees if emp.employee_id != employee_id]
        self.save_employees()

    def search_employees(self, keyword):
        results = [emp for emp in self.employees if keyword.lower() in str(emp.__dict__).lower()]
        return results

    def add_event(self, event):
        self.events.append(event)
        self.save_data(self.events, 'events.pkl')

    def delete_event(self, event_id):
        self.events = [event for event in self.events if event.event_id != event_id]
        self.save_data(self.events, 'events.pkl')

    def search_events(self, keyword):
        try:
            keyword = int(keyword)
            return [event for event in self.events if event.event_id == keyword]
        except ValueError:
            return []


    def add_client(self, client):
        self.clients.append(client)
        self.save_data(self.clients, 'clients.pkl')

    def delete_client(self, client_id):
        self.clients = [client for client in self.clients if client.client_id != client_id]
        self.save_data(self.clients, 'clients.pkl')

    def search_clients(self, keyword):
        try:
            keyword = int(keyword)
            return [client for client in self.clients if client.client_id == keyword]
        except ValueError:
            return []

    def update_client(self, updated_client):
        for client in self.clients:
            if client.client_id == updated_client.client_id:
                client.name = updated_client.name
                client.address = updated_client.address
                client.contact_details = updated_client.contact_details
                client.budget = updated_client.budget
                self.save_data(self.clients, 'clients.pkl')
                break