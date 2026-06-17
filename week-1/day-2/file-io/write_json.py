"""
Employee Record Management System
"""

import json


employees = {
    "employees": [
        {
            "id": 1,
            "name": "Maryam",
            "salary": 80000
        },
        {
            "id": 2,
            "name": "Ali",
            "salary": 65000
        },
        {
            "id": 3,
            "name": "Sara",
            "salary": 72000
        }
    ]
}


with open("employees.json", "w") as file:

    json.dump(
        employees,
        file,
        indent=4
    )

print("JSON File Created Successfully")