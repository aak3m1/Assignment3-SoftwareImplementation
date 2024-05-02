import pickle
class DataManager:
    def __init__(self):
        self.employees = self.load_data('employees.pkl')
        self.events = self.load_data('events.pkl')
        self.clients = self.load_data('clients.pkl')
        self.suppliers = self.load_data('suppliers.pkl')
        self.guests = self.load_data('guests.pkl')
        self.venues = self.load_data('venues.pkl')
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

    def add_supplier(self, supplier):
        self.suppliers.append(supplier)
        self.save_data(self.suppliers, 'suppliers.pkl')

    def delete_supplier(self, supplier_id):
        self.suppliers = [supplier for supplier in self.suppliers if supplier.supplier_id != supplier_id]
        self.save_data(self.suppliers, 'suppliers.pkl')

    def search_suppliers(self, keyword):
        try:
            keyword = int(keyword)
            return [supplier for supplier in self.suppliers if supplier.supplier_id == keyword]
        except ValueError:
            return [supplier for supplier in self.suppliers if keyword.lower() in str(supplier.__dict__).lower()]

    def load_guests(self):
        try:
            with open('guests.pkl', 'rb') as f:
                guests = pickle.load(f)
        except (FileNotFoundError, EOFError):
            guests = []
        return guests

    def save_guests(self):
        with open('guests.pkl', 'wb') as f:
            pickle.dump(self.guests, f)

    def add_guest(self, guest):
        self.guests.append(guest)
        self.save_guests()

    def delete_guest(self, guest_id):
        self.guests = [guest for guest in self.guests if guest.guest_id != guest_id]
        self.save_guests()

    def search_guests(self, keyword):
        try:
            keyword = int(keyword)
            return [guest for guest in self.guests if guest.guest_id == keyword]
        except ValueError:
            return [guest for guest in self.guests if keyword.lower() in str(guest.__dict__).lower()]

    def load_venues(self):
        try:
            with open('venues.pkl', 'rb') as f:
                self.venues = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.venues = []
        return self.venues

    def save_venues(self):
        with open('venues.pkl', 'wb') as f:
            pickle.dump(self.venues, f)

    def add_venue(self, venue):
        self.venues.append(venue)
        self.save_venues()

    def delete_venue(self, venue_id):
        self.venues = [venue for venue in self.venues if venue.venue_id != venue_id]
        self.save_venues()

    def search_venues(self, keyword):
        try:
            keyword = int(keyword)
            return [venue for venue in self.venues if venue.venue_id == keyword]
        except ValueError:
            return [venue for venue in self.venues if keyword.lower() in str(venue.__dict__).lower()]