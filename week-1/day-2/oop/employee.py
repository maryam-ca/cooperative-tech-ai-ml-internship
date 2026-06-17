"""
Employee Salary Management System
"""

class Employee:
    """
    Handles employee salary calculations.
    """

    def __init__(self, emp_id, name, basic_salary):
        self.emp_id = emp_id
        self.name = name
        self.basic_salary = basic_salary

    def calculate_bonus(self):
        return self.basic_salary * 0.10

    def calculate_tax(self):
        return self.basic_salary * 0.05

    def calculate_net_salary(self):
        return (
            self.basic_salary
            + self.calculate_bonus()
            - self.calculate_tax()
        )

    def display_salary_slip(self):
        print("\n===== SALARY SLIP =====")
        print("Employee ID:", self.emp_id)
        print("Name:", self.name)
        print("Basic Salary:", self.basic_salary)
        print("Bonus:", self.calculate_bonus())
        print("Tax:", self.calculate_tax())
        print("Net Salary:", self.calculate_net_salary())


employee1 = Employee(1001, "Maryam Fatima", 50000)
employee1.display_salary_slip()