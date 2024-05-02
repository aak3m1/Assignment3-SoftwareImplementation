import pickle
class DataManager:
    """
    This class represents the Initialize of the DataManager object
    """
    #loading the data from pickle files
    def __init__(self):
        self.employees = self.load_data('employees.pkl') #employees data from file
        self.events = self.load_data('events.pkl') #events data from file
        self.clients = self.load_data('clients.pkl') #clients data from file
        self.suppliers = self.load_data('suppliers.pkl') #suppliers data from file
        self.guests = self.load_data('guests.pkl') #guests data from file
        self.venues = self.load_data('venues.pkl') #venues data from file


    def load_data(self, filename):
        """
        loading data from a pickle file , the name of the pickle file
        it will return a data loaded from the pickle file
        """
        try:
            with open(filename, 'rb') as f: #opening the file for reading in binary mode
                data = pickle.load(f) #loading data from the pickle file
        except (FileNotFoundError, EOFError):
            data = [] #if not found or EOF reached, initialize data as an empty list
        return data

    def save_data(self, data, filename):
        """
        Saving the data to a pickle file.
        - parameter the data
        - parameter the filename
        """
        with open(filename, 'wb') as f: #file for writing in binary mode
            pickle.dump(data, f) #write data to the pickle file

    # Methods for managing employees
    def load_employees(self):
        """
        Loading employees data from a pickle file
        """
        try:
            with open('employees.pkl', 'rb') as f: #open the file for reading in binary mode
                employees = pickle.load(f) #load employees data from the pickle file
        except (FileNotFoundError, EOFError):
            employees = [] #if the file not found or EOF reached, initialize employees as an empty list
        return employees
    def save_employees(self):
        """
        saving the employees data to a pickle file
        """
        with open('employees.pkl', 'wb') as f: #opening the file for writing in binary mode
            pickle.dump(self.employees, f) #employees data to the pickle file

    def add_employee(self, employee):
        """
        Add a new employee to the list of employees.

        """
        self.employees.append(employee) #append the new employee to the list
        self.save_employees() #saving the updated list of employees to the pickle file

    def get_employee_by_id(self, employee_id):
        """
        Get an employee by employee ID.
        """
        return next((emp for emp in self.employees if emp.employee_id == employee_id), None)  #return the employee with the given ID, if found

    def update_employee(self, updated_employee):
        """
        Update an existing employee with new information.
        """
        for emp in self.employees: #iterate through the list of employee
            if emp.employee_id == updated_employee.employee_id: # If employee ID matches
                emp.name = updated_employee.name
                emp.department = updated_employee.department
                emp.job_title = updated_employee.job_title
                emp.basic_salary = updated_employee.basic_salary
                emp.age = updated_employee.age
                emp.date_of_birth = updated_employee.date_of_birth
                emp.passport_details = updated_employee.passport_details
                self.save_employees() #save the updated list of employees to the pickle file
                break

    def delete_employee(self, employee_id):
        """
        Delete an employee from the list of employees
        """
        self.employees = [emp for emp in self.employees if emp.employee_id != employee_id] #removing the employee with the given ID from the list
        self.save_employees() #save the updated list of employees to the pickle file

    def search_employees(self, keyword):
        """
        Search for employees based on a keyword.
        """
        results = [emp for emp in self.employees if keyword.lower() in str(emp.__dict__).lower()]  #search for employees based on the keyword
        return results

    # Methods for managing events
    def add_event(self, event):
        """
        Add a new event to the list of events
        """
        self.events.append(event) #append the new event to the list
        self.save_data(self.events, 'events.pkl')  #save the updated list of events to the pickle file

    def delete_event(self, event_id):
        """
        Delete an event from the list of events.
        """
        self.events = [event for event in self.events if event.event_id != event_id] #remove the event with the given ID from the list
        self.save_data(self.events, 'events.pkl') #saving the updated list of events to the pickle file

    def search_events(self, keyword):
        """
        Searching for events based on a keyword
        """
        try:
            keyword = int(keyword)  #convert keyword to integer
            return [event for event in self.events if event.event_id == keyword]
        except ValueError:
            return [] #return an empty list if keyword cannot be converted to integer

    # Methods for managing clients
    def add_client(self, client):
        """
        Add a new client to the list of clients.
        """
        self.clients.append(client)  #append the new client to the list
        self.save_data(self.clients, 'clients.pkl') #saving the updated list of clients to the pickle file

    def delete_client(self, client_id):
        """
        Delete a client from the list of clients
        """
        self.clients = [client for client in self.clients if client.client_id != client_id] #removing the client with the given ID from the list
        self.save_data(self.clients, 'clients.pkl') #saving the updated list of clients to the pickle file

    def search_clients(self, keyword):
        """
        Search for clients based on a keyword
        """
        try:
            keyword = int(keyword) #convert keyword to integer
            return [client for client in self.clients if client.client_id == keyword]   #clients with matching client ID
        except ValueError:
            return [] #return an empty list if keyword cannot be converted to integer

    def update_client(self, updated_client):
        """
        Update an existing client with new information.
        """
        for client in self.clients: #iterate through the list of clients
            if client.client_id == updated_client.client_id: #if the client ID matches
                client.name = updated_client.name
                client.address = updated_client.address
                client.contact_details = updated_client.contact_details
                client.budget = updated_client.budget
                self.save_data(self.clients, 'clients.pkl')  #saving the updated list of clients to the pickle file
                break

    # Methods for managing suppliers
    def add_supplier(self, supplier):
        """
        Add a new supplier to the list of suppliers
        """
        self.suppliers.append(supplier) #append the new supplier to the list
        self.save_data(self.suppliers, 'suppliers.pkl') #saving the updated list of suppliers to the pickle file

    def delete_supplier(self, supplier_id):
        """
        Delete a supplier from the list of suppliers
        """
        #removing the supplier with the given ID from the list
        self.suppliers = [supplier for supplier in self.suppliers if supplier.supplier_id != supplier_id]
        #saving the updated list of suppliers to the pickle file
        self.save_data(self.suppliers, 'suppliers.pkl')

    def search_suppliers(self, keyword):
        """
        Search for suppliers based on a keyword.
        """
        try:
            keyword = int(keyword)  #converting keyword to integer
            #returning the suppliers with matching supplier ID
            return [supplier for supplier in self.suppliers if supplier.supplier_id == keyword]
        except ValueError:
            #returning suppliers with matching keyword in their attributes
            return [supplier for supplier in self.suppliers if keyword.lower() in str(supplier.__dict__).lower()]


    # Methods for managing guests
    def load_guests(self):
        """
        Load guests data from a pickle file
        """
        try:
            with open('guests.pkl', 'rb') as f:  #open the file for reading in binary mode
                guests = pickle.load(f) #loading guests data from the pickle file
        except (FileNotFoundError, EOFError):
            guests = []  #if the file not found or EOF reached, initialize guests as an empty list
        return guests

    def save_guests(self):
        """
        Save guests data to a pickle file
        """
        with open('guests.pkl', 'wb') as f: #open the file for writing in binary mode
            pickle.dump(self.guests, f)  #write guests data to the pickle file

    def add_guest(self, guest):
        """
        Add a new guest to the list of guests.
        """
        self.guests.append(guest) #append the new guest to the list
        self.save_guests() #save the updated list of guests to the pickle file

    def delete_guest(self, guest_id):
        """
        Delete a guest from the list of guests
        """
        #remove the guest with the given ID from the list
        self.guests = [guest for guest in self.guests if guest.guest_id != guest_id]
        #saving the updated list of guests to the pickle file
        self.save_guests()

    def search_guests(self, keyword):
        """
        Search for guests based on a keyword
        """
        try:
            keyword = int(keyword) #convert keyword to integer
            #return guests with matching guest ID
            return [guest for guest in self.guests if guest.guest_id == keyword]
        except ValueError:
            #return guests with matching keyword in their attributes
            return [guest for guest in self.guests if keyword.lower() in str(guest.__dict__).lower()]


    # Methods for managing venues
    def load_venues(self):
        """
        Load venues data from a pickle file
        """
        try:
            with open('venues.pkl', 'rb') as f:  #opening the file for reading in binary mode
                self.venues = pickle.load(f) #loading venues data from the pickle file
        except (FileNotFoundError, EOFError):
            self.venues = [] #if the file not found or EOF reached, initialize venues as an empty list
        return self.venues

    def save_venues(self):
        """
        Save venues data to a pickle file.
        """
        with open('venues.pkl', 'wb') as f:  #open the file for writing in binary mode
            pickle.dump(self.venues, f) #venues data to the pickle file

    def add_venue(self, venue):
        """
        Add a new venue to the list of venues
        """
        self.venues.append(venue) #append the new venue to the list
        self.save_venues() #save the updated list of venues to the pickle file

    def delete_venue(self, venue_id):
        """
        Delete a venue from the list of venues
        """
        #remove the venue with the given ID from the list
        self.venues = [venue for venue in self.venues if venue.venue_id != venue_id]
        self.save_venues() #saving the updated list of venues to the pickle file

    def search_venues(self, keyword):
        """
        Searching for venues based on a keyword
        """
        try:
            keyword = int(keyword)  #convert keyword to integer
            return [venue for venue in self.venues if venue.venue_id == keyword] #returining the venue with  matching venue ID
        except ValueError:
            #return venues with matching keyword in their attributes
            return [venue for venue in self.venues if keyword.lower() in str(venue.__dict__).lower()]