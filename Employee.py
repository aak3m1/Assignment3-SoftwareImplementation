class Employee:
    def __init__(self, id, name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details):
        self.id = id
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