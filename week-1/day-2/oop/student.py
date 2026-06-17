"""
Student Performance Management System
Author: Maryam Fatima
"""

class Student:
    """
    Represents a student and manages academic performance.
    """

    def __init__(self, name, roll_no, marks):
        self.name = name
        self.roll_no = roll_no
        self.marks = marks

    def calculate_average(self):
        """Calculate average marks."""
        return sum(self.marks) / len(self.marks)

    def calculate_grade(self):
        """Calculate grade based on average."""
        avg = self.calculate_average()

        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        else:
            return "F"

    def display_report(self):
        """Display complete student report."""
        print("\n===== STUDENT REPORT =====")
        print("Name:", self.name)
        print("Roll Number:", self.roll_no)
        print("Marks:", self.marks)
        print("Average:", round(self.calculate_average(), 2))
        print("Grade:", self.calculate_grade())


student1 = Student("Maryam", 101, [85, 90, 88, 92, 95])
student1.display_report()