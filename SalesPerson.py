from Employee import Employee

class Salesperson(Employee):
    def __init__(self, id, name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details, sales_target):
        super().__init__(id, name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details)
        self.sales_target = sales_target
    def record_sale(self):
        # Placeholder for recording sales
        return "Salesperson recording sale."