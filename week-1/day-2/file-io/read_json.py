"""
Employee JSON Dashboard
"""

import json


def employee_dashboard():

    with open("employees.json", "r") as file:

        data = json.load(file)

    employees = data["employees"]

    salaries = []

    for employee in employees:
        salaries.append(employee["salary"])

    highest_salary = max(salaries)
    lowest_salary = min(salaries)
    average_salary = sum(salaries) / len(salaries)

    print("\n===== EMPLOYEE DASHBOARD =====")

    print("Total Employees:", len(employees))
    print("Highest Salary:", highest_salary)
    print("Lowest Salary:", lowest_salary)
    print("Average Salary:", round(average_salary, 2))

    print("\nEmployee Records")

    for employee in employees:

        print(
            employee["id"],
            employee["name"],
            employee["salary"]
        )


employee_dashboard()