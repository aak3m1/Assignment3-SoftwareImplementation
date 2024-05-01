import pickle
class DataManager:
    def __init__(self):
        self.employees = self.load_employees()

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