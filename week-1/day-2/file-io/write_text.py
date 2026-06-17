"""
Intern Daily Task Log Generator
Author: Maryam Fatima
"""

from datetime import datetime


class DailyTaskLog:

    def __init__(self, file_name):
        self.file_name = file_name

    def save_task(self, task, status, remarks):

        current_date = datetime.now().strftime("%Y-%m-%d")

        with open(self.file_name, "a") as file:

            file.write("\n====================\n")
            file.write(f"Date: {current_date}\n")
            file.write(f"Task: {task}\n")
            file.write(f"Status: {status}\n")
            file.write(f"Remarks: {remarks}\n")

        print("Task Saved Successfully")


log = DailyTaskLog("daily_log.txt")

log.save_task(
    "Completed OOP Practice",
    "Completed",
    "All programs executed successfully"
)